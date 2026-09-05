---
title: "#1708 — chain-halt: ValidatorByConsAddr propagates ErrNoValidatorFound, so the evidence/slashing BeginBlock nil-guards never run"
source: https://github.com/gonka-ai/gonka/issues/1708
issue_number: 1708
synced_at: 2026-09-05T05:51:17Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    chain-halt: ValidatorByConsAddr propagates ErrNoValidatorFound, so the evidence/slashing BeginBlock nil-guards never run
    <span class="issues-number">#1708</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/vitaly-andr">@vitaly-andr</a> opened 2026-09-02 17:03 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-09-02 17:31 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

`ValidatorByConsAddr` (`x/staking/keeper/alias_functions.go` in the
[`gonka-ai/cosmos-sdk`](https://github.com/gonka-ai/cosmos-sdk) fork) returns
`ErrNoValidatorFound` when the consensus address does not resolve. Its only non-test consumers are
`x/evidence` `handleEquivocationEvidence` and `x/slashing` `HandleValidatorSignature`, both running
inside `BeginBlock`. Both check the error before checking for a nil validator, so the graceful
branches written for exactly this situation are unreachable. The error propagates out of
`BeginBlocker` into `FinalizeBlock` and consensus stops on every node at once:

```
block finalization failed at height N: validator does not exist
```

Same failure class as #1205, different mechanism: #1205 is about a deletion path that removes a
record still in use, this one is about the lookup contract that turns any such absence into a halt,
whatever removed the validator.

## How the state arises

Stock cosmos removes a validator only after the full unbonding period, long after it has left every
commit. The compute-validator model deletes zero-power and stale validators immediately, with no
unbonding, on epoch transitions. CometBFT keeps a validator in the active set for
`ValidatorUpdateDelay` blocks after its power update, so it signs one more block and appears in that
block's `LastCommitInfo`. The next block's `BeginBlock` looks it up and finds nothing.

Two independent routes, both on every node:

1. **Evidence** — `handleEquivocationEvidence` resolves the reported validator. CometBFT submits
   equivocation evidence within the evidence age window, which on this chain can outlive the
   validator record by many blocks.
2. **Slashing** — `HandleValidatorSignature` resolves a validator that crossed the downtime
   threshold. Removal at epoch rotation is routine, and missed blocks accumulate on their own.

## Root cause

```go
// x/staking/keeper/alias_functions.go
func (k Keeper) ValidatorByConsAddr(ctx context.Context, addr sdk.ConsAddress) (types.ValidatorI, error) {
	return k.GetValidatorByConsAddr(ctx, addr)   // returns ErrNoValidatorFound
}
```

Consumer side, evidence:

```go
validator, err := k.stakingKeeper.ValidatorByConsAddr(ctx, consAddr)
if err != nil {
	return err                       // <- exits here, error reaches FinalizeBlock
}
if validator == nil || validator.IsUnbonded() {
	// Defensive: Simulation doesn't take unbonding periods into account, and
	// CometBFT might break this assumption at some point.
	return nil                       // <- never reached
}
```

Slashing has the same shape with `if validator != nil`.

## Fix

Report a missing validator as `(nil, nil)` so both consumers take the branches they already have.
Submitted as gonka-ai/cosmos-sdk#19, with two regression tests; the staking and slashing suites show
the same pre-existing failures before and after.

## Verification

Multi-seed sweep of the simulation suite from #982, 500 blocks x 200 ops, `release/v0.53.x` + gonka-ai/cosmos-sdk#14 and
gonka-ai/cosmos-sdk#16: **27 of 37 seeds halt** at heights 54-367 without the fix, **0 of 37** with it.

Re-verified 2026-09-02 against `upgrade-v0.2.16` (SDK `v0.53.3-ps19-observability` +
gonka-ai/cosmos-sdk#14 and #16): seed 99 at 500x200 halts at height 74 without the fix and completes in 12 seconds with it.

## Severity

Full chain halt: the error surfaces from `BeginBlocker` on every validator simultaneously, so the
network stops and needs manual intervention to recover.

## Context

First reported 2026-06-06 as a comment on gonka-ai/cosmos-sdk#14, with the root cause, the stack
trace and the same fix:
https://github.com/gonka-ai/cosmos-sdk/pull/14#issuecomment-4637525807 — filing it here so it has a
tracking issue of its own.

</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/vitaly-andr">@vitaly-andr</a></span>
    <span class="issues-meta-item">commented 2026-09-02 17:31 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Submitted to the HackerOne program.</p>
<ul>
<li><strong>Report ID: #3990765</strong></li>
<li>HackerOne handle: <code>plitochnik_ru</code> — my GitHub handle <code>vitaly-andr</code> is listed on that profile</li>
</ul>
<p>The submission covers this issue together with the fix in gonka-ai/cosmos-sdk#19. The lookup contract is unchanged on <code>release/v0.53.x</code> and on <code>v0.53.3-ps19-observability</code> as of today.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1708](https://github.com/gonka-ai/gonka/issues/1708) every hour.
