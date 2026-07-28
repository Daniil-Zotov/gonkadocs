---
title: "#1205 — chain-halt: `markValidatorForDeletion` jailed branch races CometBFT validator-update lag → slashing fails with ErrNoValidatorFound"
source: https://github.com/gonka-ai/gonka/issues/1205
issue_number: 1205
synced_at: 2026-07-28T16:55:06Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    chain-halt: `markValidatorForDeletion` jailed branch races CometBFT validator-update lag → slashing fails with ErrNoValidatorFound
    <span class="issues-number">#1205</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/vitaly-andr">@vitaly-andr</a> opened 2026-05-20 02:36 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-05-20 02:36 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

In the [`gonka-ai/cosmos-sdk`](https://github.com/gonka-ai/cosmos-sdk) fork, the jailed branch of `markValidatorForDeletion` (`x/staking/keeper/compute.go:559-563`) immediately deletes the validator record **and** the `ValidatorByConsAddr` index via `deleteValidatorInternal` (`x/staking/keeper/val_state_change.go:78-126`). When `SetComputeValidators` runs with a set that excludes a still-jailed validator, this branch fires. CometBFT, however, continues to include the deleted validator in `LastCommit` for `ValidatorUpdateDelay` blocks (≈ 2 effective blocks: `header.Height + 1 + 1` per cometbft `state/execution.go`'s "next next height" rule). On the next block, `slashing.BeginBlocker` (`x/slashing/abci.go:24-29`) walks `LastCommit` votes and calls `HandleValidatorSignature → GetValidatorByConsAddr` (`x/slashing/keeper/infractions.go:26-30`). The lookup returns a bare `stakingtypes.ErrNoValidatorFound` → `BeginBlocker` returns an error → consensus halts.

## Reproduction (chain halt)

Deterministic halt under the `inference-chain` simulation harness with seed 99 and `IS_TEST_NET=true` (selects the post-`ValidatorIndexFixHeight=658087` production path of `SetComputeValidators` — the same code mainnet runs):

```
block finalization failed: validator does not exist
```

Both top-level sim tests reproduce this halt deterministically on the current upstream code:
- `TestFullSimulation_x_Inference_Integrated`
- `TestFullAppSimulation`

## Root cause

`x/staking/keeper/compute.go:559-563`:
```go
// Jailed validators can't be added to power index, so delete them immediately
if validator.Jailed {
    logger.Info("deleting jailed validator immediately", "operator", validator.OperatorAddress)
    return k.deleteValidatorInternal(ctx, validator, valAddr)
}
```

`deleteValidatorInternal` wipes the validator record, the `ValidatorByConsAddr` index, the power index, `LastValidatorPower` (suppressed via `_ =`), and self-delegation — all in one `EndBlock`, with no `ValidatorUpdate` signalled to CometBFT. The non-jailed branch (`compute.go:565-598`) does not have this problem: it sets power to zero and re-adds to the power index, so the next `ApplyAndReturnValidatorSetUpdates` emits a power-0 `ValidatorUpdate` while the record stays reachable.

This jailed branch was added in commit `cefc31d3a8e` («Delete jailed immediately», 2025-10-02) to bypass an unrelated error at `val_state_change.go:176-184` («should never retrieve a jailed validator from the power store») that would fire if the safe path re-added a jailed validator to the power index. The local symptom was fixed; the CometBFT-side race was not considered.

## Why `RestoreValidatorIndex` does not cover this

`slashing.BeginBlocker` calls `k.RestoreValidatorIndex(ctx)` on every block before iterating votes (`x/slashing/abci.go:24`). That heal iterates `GetAllValidators()` and restores a missing `ValidatorByConsAddr` entry **when the underlying validator record still exists** (`x/staking/keeper/validator.go:647-669`). Here the record itself is gone, so the deleted validator is not in `GetAllValidators()` and the heal has nothing to restore.

## Self-contained reproducer (unit test)

Drop-in for `x/staking/keeper/mark_validator_for_deletion_test.go` (uses the existing `KeeperTestSuite` scaffolding): **https://gist.github.com/vitaly-andr/83816dc3704211a6720edbf63b45761c**

Fails on current code with `validator does not exist`. Passes once the jailed branch is changed to leave the record reachable for the CometBFT lag window.

## Naive fix attempts that don't work

I empirically verified two:

1. **Replace `deleteValidatorInternal` with `return nil` in the jailed branch.** Prevents the halt (sim runs past the trigger point). But the validator lingers as `Bonded` with `Jailed=true` and **non-zero tokens** — `DeleteZeroPowerValidators` (`x/staking/keeper/val_state_change.go:40-74`) won't pick it up. `UnbondAllMatureValidators` exists but is **not called from `EndBlocker`** in this fork (`x/staking/keeper/abci.go:18-21` only calls `BlockValidatorUpdates`), so `unbonding_time=0` doesn't auto-cleanup. Net: no halt but no cleanup either.

2. **Mirror the non-jailed path's full state reset** (zero `Tokens`, zero `DelegatorShares`, persist). Triggers a runtime `division by zero` panic when `slashing.Unjail` (`x/slashing/keeper/unjail.go:33`) is later called on this validator and reaches `Validator.TokensFromShares` (`x/staking/types/validator.go:308`) — the formula is `shares × Tokens / DelegatorShares`, and zero denominator panics.

## Working candidate fix

`compute.go:559-563`:
```go
if validator.Jailed {
    // Zero out Tokens (the power proxy in PoC) but KEEP DelegatorShares.
    // TokensFromShares = shares × Tokens / DelegatorShares — with Tokens=0
    // and DelegatorShares unchanged, the formula returns 0 cleanly and
    // slashing.Unjail no longer panics on stale-jailed validators.
    //
    // jailValidator (val_state_change.go:335) already removed this validator
    // from the power index, so ApplyAndReturnValidatorSetUpdates' main loop
    // won't iterate it. The tail loop over `last` (LastValidatorPower) will
    // emit the power-0 ValidatorUpdate and start bondedToUnbonding.
    // DeleteZeroPowerValidators physically removes the record on the next
    // block, after LastValidatorPower is cleared and CometBFT has been told
    // to drop the validator from its active set.
    validator.Tokens = math.ZeroInt()
    validator.UnbondingIds = []uint64{}
    return k.SetValidator(ctx, validator)
}
```

## Empirical verification

1. **Unit test PASS** with this fix, FAIL without (test at https://gist.github.com/vitaly-andr/83816dc3704211a6720edbf63b45761c).

2. **Full `x/staking/keeper` test suite**: 30 PASS, 21 FAIL — the 21 are pre-existing `NoOpBankKeeper`-related failures, unchanged from baseline (no regressions introduced by this fix).

3. **`inference-chain` simulation, seed=99, IS_TEST_NET=true, full 500 blocks × 200 ops**: the same two sim tests that deterministically halt on the current upstream code (`TestFullSimulation_x_Inference_Integrated` and `TestFullAppSimulation`) **BOTH pass to completion** when this fix is combined with the in-flight GON-191 fix (Sam Johnson, `origin/sj/gon-191-stale-consensus-key-conflicts`, commit `5473018e72`, not yet merged in main):

   ```
   --- PASS: TestFullSimulation_x_Inference_Integrated (54.45s)
       height=501  opsCount=25767  inference_completed=8721
       AppHash=2b3f3ae9c02614795179d4b8d377a07e78fecebade1aeade5e041a16114475b3
   --- PASS: TestFullAppSimulation                      (52.04s)
       height=501  opsCount=25767  inference_completed=8721
       AppHash=2b3f3ae9c02614795179d4b8d377a07e78fecebade1aeade5e041a16114475b3
   ```

   Same deterministic AppHash across both tests; no halt, no panic, no SKIP. 282 `MsgUnjail` attempts processed gracefully in the run (some returning «validator with invalid exchange rate» — clean rejection where the naive fix #2 above would panic).

   With this fix **alone** (no GON-191) the halt is cleared but the sim later SKIPs «empty validator set» because the cleaned-up validators cannot re-register their cons-keys — that's the path GON-191 closes. With GON-191 **alone** (no this fix) the chain still halts at the same point.

   **The two fixes are symbiotic.** They touch different functions (`markValidatorForDeletion`'s jailed branch vs `filterBasedOnExisting` + `deleteValidatorInternal`'s defensive cons-addr guard) with no semantic overlap, and compose cleanly. Recommended to land coordinated.

## Related: secondary divide-by-zero in non-jailed branch

The non-jailed branch (`compute.go:573`) zeros `DelegatorShares` as well — the same precondition that caused the divide-by-zero in fix attempt #2 above. On mainnet this is currently masked by `DeleteZeroPowerValidators` cleaning the validator up on the very next block, but a window where a concurrent `MsgUnjail` could land and panic does exist. Worth a defensive fix in the non-jailed branch too (or in `TokensFromShares` directly).

## Severity

**Mainnet vulnerable.** The jailed branch of `markValidatorForDeletion` is on the active mainnet code path. The trigger pattern — jail a validator, then drop them from the next epoch's PoC compute set — is the standard rotation for any validator that goes offline.

## Context

Found while implementing simulation tests for [#982](https://github.com/gonka-ai/gonka/issues/982).

</div>

---

> 🔄 **Auto-synced** from [Issue #1205](https://github.com/gonka-ai/gonka/issues/1205) every hour.
