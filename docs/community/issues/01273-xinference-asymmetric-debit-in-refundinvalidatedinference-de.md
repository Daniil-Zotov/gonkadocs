---
title: "#1273 — x/inference: asymmetric debit in refundInvalidatedInference — design clarification"
source: https://github.com/gonka-ai/gonka/issues/1273
issue_number: 1273
synced_at: 2026-08-05T10:01:29Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    x/inference: asymmetric debit in refundInvalidatedInference — design clarification
    <span class="issues-number">#1273</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/vitaly-andr">@vitaly-andr</a> opened 2026-05-28 19:14 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-05-29 05:26 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Question

`refundInvalidatedInference` ([`x/inference/keeper/msg_server_invalidate_inference.go:64-79`](https://github.com/gonka-ai/gonka/blob/main/inference-chain/x/inference/keeper/msg_server_invalidate_inference.go#L64-L79)) issues a full-`ActualCost` escrow refund to `RequestedBy` (the client) while debiting the **same** full `ActualCost` from `executor.CoinBalance` **only** (`:74`).

Earlier in the inference lifecycle, `shareWorkWithValidators` ([`msg_server_validation.go:473-504`](https://github.com/gonka-ai/gonka/blob/main/inference-chain/x/inference/keeper/msg_server_validation.go#L473-L504)) splits the same `ActualCost` across executor **and** validators (each validation moves a slice of the executor's credit to the validating worker via `calculations.ShareWork`).

So the credit side is **distributed** (executor + validators), but the invalidation debit is **concentrated** (executor only). The validators' positive `CoinBalance` claims from the now-invalidated inference are never reversed.

**Is this asymmetry intentional**, with the resulting drift covered by the debt-recovery / collateral / slash mechanisms? Or is it an oversight in the refund path?

## Mechanism

`CoinBalance` is a per-epoch virtual "owed" ledger. It is reset to `0` and converted to real coins at settlement (`accountsettle.go:233`). `refundInvalidatedInference` only runs while `inferenceIsBeforeClaimsSet` is true (`msg_server_validation.go:450`) — i.e. *before* that settlement.

By that point `shareWorkWithValidators` may already have credited the validators their share. The refund then:

1. Pays the client back the full `ActualCost` directly from module escrow (`IssueRefund` → `PayParticipantFromEscrow`), reducing the module balance immediately.
2. Subtracts the full `ActualCost` from the executor's `CoinBalance` only.

At the next settlement the validators' still-positive `CoinBalance` is paid out as real coins from the module — but the escrow that backed it was already refunded to the client. Net module drift = sum of the validators' shares for that inference.

## Constructive reproducer

`inference-chain/x/inference/keeper/refund_invalidation_bug_test.go` (local; can attach as PR/gist on request). Single PASS, deterministic:

- Pre-state: executor `+400`, validator `+100`, module account `500`. Invariant holds (`positiveSum = 500 == moduleBalance = 500`).
- After a single legitimate refund of `ActualCost = 500`: executor `-100`, validator `+100`, module `0`. Now `positiveSum = 100 > moduleBalance = 0` — drift equals exactly the validator's never-reversed share.

## Sim evidence

After applying local fixes for the two sibling manifestations (#1265 timeout-cleanup, #1269 revalidation-vote), `make sim-full-test` (seed=99) runs to completion (~500 blocks, 10 epochs, 12 430 inferences) and a post-run accounting invariant fires:

```
inference: bank-backs-positive-balance invariant
module account ... has 7684000 ngonka but participants are owed 8041500
```

Gap = 357 500 ngonka accumulated across the run, consistent with multiple `Invalid Inference subtracted from Executor CoinBalance` events leaving validators' shares un-reversed.

## What the code already says about negative balances

The codebase clearly tolerates negative `CoinBalance` by design:

- `bitcoin_rewards.go:742-754` treats `CoinBalance < 0` as recoverable **debt**, repaid from future `RewardCoins` before distribution.
- `types/errors.go:23` registers `ErrNegativeCoinBalance` (1114) as a signal emitted on partial debt recovery — not a guard.
- `GracePeriodEndEpoch` default `180` (`params.go:290`): during grace, collateral is not required; after grace, slash on `Status=INVALID` recovers via collateral (`collateral.go`).

So the apparent design intent: short-term drift is acceptable; long-term it is backstopped by (a) reward-redirected debt repayment for participants who stay `ACTIVE`, and (b) collateral + slash after the grace period.

## What is still unclear (edge cases)

1. **Executor exits / goes INVALID during grace**, when `GetRequiredCollateralForSlash` returns `0`: neither debt-recovery (no future rewards) nor slash (no collateral) backstops the validators' share. The deficit looks permanent. Intended bootstrap-only cost?
2. **Post-grace, undercollateralized executor**: if collateral is smaller than the accumulated `ActualCost − own contribution` across that executor's invalidations, the residual deficit persists. Is the slash sized to always cover the *full* `ActualCost` (including validators' shares), or is this an accepted risk?
3. **Long-standing pattern, not a regression**: the executor-only debit has been present since the function's introduction (`v0.2.5`, #404) and survived every refactor of this function since — `v0.2.10` (#695) and `v0.2.12` (#948) only reordered refund-before-debit and simplified the payer lookup; the asymmetry itself was never touched. This stability is what makes us ask "intended?" rather than assume a bug.

## Suggested next step

Maintainer clarification before any code change:

- **If intentional** — close with a docstring on `refundInvalidatedInference` capturing the design and its dependence on the collateral / grace / debt-recovery mechanisms (so the next reader doesn't re-file this).
- **If an oversight** — a symmetric refund (reverse the `shareWorkWithValidators` adjustments for validators too) or participant-state-aware accounting would close the gap.

## References

- Handler: `x/inference/keeper/msg_server_invalidate_inference.go:64-79` (debit `:74`)
- Credit path: `x/inference/keeper/msg_server_validation.go:473-504`; guard `inferenceIsBeforeClaimsSet` `:450`
- Settlement reset: `x/inference/keeper/accountsettle.go:233`
- Refund: `x/inference/keeper/payment_handler.go:113` (`IssueRefund` → `PayParticipantFromEscrow`)
- Debt model: `x/inference/keeper/bitcoin_rewards.go:742-754`; `x/inference/types/errors.go:23`
- Grace/collateral: `x/inference/types/params.go:290`; `x/inference/keeper/collateral.go`
- Sibling manifestations of the same invalidate/revalidate cluster: #1265, #1269

</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/vitaly-andr">@vitaly-andr</a></span>
    <span class="issues-meta-item">commented 2026-05-29 05:26 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p><strong>Update — the asymmetry is pervasive, not a grace-period edge case.</strong></p>
<p>While building the simulation/fuzz harness for #982 (Phase 3 — improving simulation quality with custom invariants + multi-seed runs), this asymmetry surfaces on the large majority of seeds, not just the constructed reproducer above.</p>
<p><strong>Multi-seed evidence.</strong> A <code>bank-backs-positive-balance</code> invariant — <code>module account balance ≥ Σ positive participant CoinBalances</code> — was added and checked post-run across the framework's default seed list (37 seeds, <code>-NumBlocks=100 -BlockSize=100</code>, <code>-GenesisTime</code> pinned for reproducibility):</p>
<ul>
<li><strong>30 of 33 completing seeds break module solvency</strong> (the other 3 pass; 5 seeds skipped early on an unrelated sim-substrate limitation — empty validator set — and never reached the check).</li>
<li>Gaps range from ~1k to ~3.6M ngonka, e.g. <code>module account … has 27284434 ngonka spendable (27284434 total) but participants are owed 28400962</code> (gap 1,116,528 on seed=99).</li>
</ul>
<p><strong>Root cause confirmed (seed=99, verbose trace).</strong> 16 invalidations occurred, each emitting the asymmetric debit:</p>
<pre><code>Invalid Inference subtracted from Executor CoinBalance  actualCost=479000 coinBalance=-479000 executor=gonka194weg3...
</code></pre>
<p>The executor is debited the <strong>full</strong> <code>ActualCost</code> (going into negative/debt), while the validators' work-shares for the same inference — credited earlier via <code>shareWorkWithValidators</code> — are <strong>not</strong> reversed. The module account, having refunded the client the full <code>ActualCost</code>, is left under-funded by approximately the sum of those un-reversed validator shares. The ~1.12M ngonka gap on seed=99 matches the validator-share total across the 16 invalidated inferences.</p>
<p><code>spendable == total</code> on the module account rules out a locked/vesting artifact — this is genuine under-backing.</p>
<p><strong>Takeaway:</strong> the asymmetric debit doesn't merely create a recoverable executor debt in rare grace-period conditions — it breaks the module-solvency invariant on ~91% of completing simulation seeds whenever invalidations occur. This strengthens the case that the refund path should reverse the validators' shares (or otherwise reconcile against the escrow actually held), rather than charging the executor alone.</p>
<p>(Surfaced by the #982 simulation work; the invariant and multi-seed harness are part of that effort.)</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1273](https://github.com/gonka-ai/gonka/issues/1273) every hour.
