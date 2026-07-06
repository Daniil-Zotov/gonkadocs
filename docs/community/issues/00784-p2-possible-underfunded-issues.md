---
title: "#784 — [P2] Possible underfunded issues"
source: https://github.com/gonka-ai/gonka/issues/784
issue_number: 784
synced_at: 2026-07-06T15:05:47Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    [P2] Possible underfunded issues
    <span class="issues-number">#784</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item">[@tcharchian](https://github.com/tcharchian) opened 2026-02-20 23:24 UTC</span>
    <span class="issues-meta-item">4 comments</span>
    <span class="issues-meta-item">Updated 2026-04-10 04:50 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #95b500; color: #24292f; border-color: #95b500;">Priority: Low</span></div>
</div>

<div class="issues-content">
# Problem
Much of the Gonka system depends on funds being moved in and out of "escrow", which is stored in the types.ModuleName ("inference") account (the "module account"). Payments for inferences are moved here as well as money for rewards. There are also (possibly) movement from or to other module accounts (such as collateral, governance and streamvesting).

There are unlikely but possible scenarios that _might_ result in these account having insufficient funds.

We would like to solve this problem comprehensively rather than piecemeal.

Tasks need to be done in order.

## Task 1: Analysis
This means going through and finding every place where payouts _might_ result in insufficient funds, and defining and understanding current behavior when this happens.

## Task 2: Important fixes
This means making sure that in each instance of these possible failures that no **critical** errors will occur. This means (in order of priority):
1. No possible exploit to gain un-earned funds
2. No consensus failures (panics during EndBlock, for instance)
3. No panics during a message transaction (rather, they should return an error for deterministic rollback)

## Task 3: Standardize handling
This is fairly open ended, but the end goal is to have the behavior for an unfunded event to be consistent and logical across scenarios and accounts. Principles should be clearly outlined and exceptions that need to conform with the policy should be fixed.

## Task 4: Prevent future failures
This is also open ended, but some mechanism should clearly make it so no new behavior will violate the outcome of Task 3. Methods available:
1. Unit test failures (that may include searching files or using the AST)
2. Static checks (similar to the current use of `forbidigo` to prevent calls to `panic` or `Must`)
3. AI guidelines - explicit, reliable AI guidelines that can be added to the ai-review tool `gonka-ai/ai-review`

Any other method, as long as it serves the purpose, would work.
</div>

---

## 💬 Comments (4)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@0xMayoor](https://github.com/0xMayoor)</span>
    <span class="issues-meta-item">commented 2026-02-21 08:10 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    Working on it!
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@0xMayoor](https://github.com/0xMayoor)</span>
    <span class="issues-meta-item">commented 2026-02-21 14:20 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    ## Task 1 — analysis (updated with IDs)

_Same findings as before, now with IDs so the Task 2 PRs can reference them._

Went through every runtime path where coins move out of a module account — `inference`, `bridge_escrow`, `top_reward`, `collateral`, `streamvesting`. Checked what happens if the sending account is underfunded at that moment.

Found ~25 distinct payout/refund paths. 12 handle it fine (error returned, state rolls back). 13 have issues, plus 2 more found while working on the fixes. Listed below.

---

### settlement

- **[F-01]** `GetBitcoinSettleAmounts` error logged not returned. On failure the amounts slice is nil, `amounts[i]` panics in the settlement loop. EndBlock panic = permanent node crash.
- **[F-02]** `SettleAccounts` does mint, balance resets, perf summaries, and settle writes as independent KV operations. Failure mid-way means earlier writes are already committed. Participants can end up with zeroed balances but no settle record.
- **[F-03]** `SetSettleAmountWithGovernanceTransfer` return value ignored. If the governance transfer of an old settle fails, function returns before writing the new settle. Participant loses current epoch earnings silently.
- **[F-04]** `TransferOldSettleAmountsToGovernance` error logged not returned. Old settles stuck but records persist for retry. Low severity on its own, but was inside the atomic section so a failure here rolls back current-epoch settlement too.
- **[F-05]** `SettleAccounts` error swallowed by the orchestrator in `module.go`. Even when the function correctly returns an error, it gets thrown away.

### claim rewards

- **[F-06]** `finishSettle` deletes the settle record and marks `Claimed = true` before the payout is confirmed. If the payout fails, participant's claim is gone permanently. No retry path. Probably the worst one.

### inference lifecycle

- **[F-07]** expired inference refund fails → logged → inference marked EXPIRED anyway → timeout record removed. Requester's escrow stuck. This is the normal timeout path, happens routinely.
- **[F-08]** refund error swallowed in `processInferencePayments`. When FinishInference reprices lower and the refund fails, error logged, execution continues. Inference marked finished without developer getting their refund.
- **[F-09]** FinishInference mutation section runs on the raw context with no CacheContext. If any step fails after earlier writes, partial state persists. `FinishedProcessed()` blocks retry, making it permanent. Found this one while fixing F-08.

### cross-module

- **[F-10]** collateral and streamvesting `AdvanceEpoch` errors swallowed by the inference orchestrator. If collateral fails its epoch counter doesn't increment, leading to desync.
- **[F-11]** collateral unbonding loop aborts on first `SendCoins` failure. Remaining entries skipped until next epoch.
- **[F-12]** streamvesting: coins sent to participant, then `SetVestingSchedule` fails. Schedule still has the entry, same amount sent again next epoch. Double payment.

### misc

- **[F-13]** `addTimeout` is a void function. If the timeout write fails, inference never expires, escrow locked forever.
- **[F-14]** int64→int32 casts in keeper code with no bounds check. Worst case is the weight casts in validation sampling — silent truncation corrupts probability. Governance misconfiguration in top miner params could cause div-by-zero.
- **[F-15]** `TransferOldSettleAmountsToGovernance` returns error to EndBlock, halting the chain on what should be a non-fatal cleanup. The existing code comment already says this shouldn't block settlement. Found this while working on the EndBlock audit.

---

### what's fine

Direct payments, vested payments, burns, refund wrapper, governance transfers, invalidation refunds, bridge release/rollback, slash/burn, minting — all return errors correctly.

  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@0xMayoor](https://github.com/0xMayoor)</span>
    <span class="issues-meta-item">commented 2026-02-22 18:38 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    ## Task 2 — fixes

Two PRs.

**PR 1** (#787) — settlement bugs in `accountsettle.go`. Panic fix, CacheContext wrap, error checking, cleanup separation. Covers F-01 through F-05.

**PR 2** (#789) — applies the same CacheContext approach to ClaimRewards, inference expiry, streamvesting, and FinishInference. Also did a full integer narrowing audit and EndBlock error path audit. Covers F-06, F-07, F-08, F-09, F-12, F-14, F-15. Each atomicity fix has a rollback test that would fail without CacheContext (proving the bug) and passes with it (proving the fix).

---

Three findings still open — they all need a design decision before fix:

- **[F-10]** cross-module `AdvanceEpoch` errors are swallowed. What's the desired recovery when collateral or streamvesting fails their epoch advance? Added `epoch_error` events for visibility in PR 2, but the actual recovery mechanism is the open question.
- **[F-11]** collateral unbonding aborts on first failure. Should the loop keep going and leave the failed entry for next epoch, or should the whole batch fail?
- **[F-13]** `addTimeout` is void. If the timeout write fails, inference sits in STARTED forever. Should StartInference roll back the whole inference, or continue without expiry tracking?

  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@0xMayoor](https://github.com/0xMayoor)</span>
    <span class="issues-meta-item">commented 2026-02-23 14:50 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    ## Task 3 — standardized handling for underfunded events

Principles based off Task 1 analysis and Task 2 fixes. Every fund-movement path should conform to these. Exceptions listed at the bottom.

---

### Principles

**1. Atomicity via CacheContext**

Any path that moves funds and writes related state (status changes, schedule updates, settle records) must wrap both in a single `CacheContext`. Either everything commits or nothing does. This prevents partial state where funds moved but the tracking record didn't update, or vice versa.

Applies to: msg server handlers, EndBlock expiry, settlement, vesting payments.

---

**2. Nil-error response encoding for selected handlers**

Some handlers return `(response, nil)` to the SDK and encode failures in `response.ErrorMessage` instead of returning a real error. This is intentional — in Cosmos SDK, a non-nil error from any message handler rolls back the entire multi-message transaction, including unrelated messages that succeeded. Handlers that are expected to appear alongside other messages in a single tx use this pattern to allow per-message failure without aborting the batch.

Currently applies to: StartInference, FinishInference, ClaimRewards. Other handlers (validation submission, PoC validation, etc.) follow standard SDK error returns and rely on tx-level rollback. Since SDK rollback never triggers for the nil-error handlers, CacheContext is the only atomicity mechanism available to them.

---

**3. Settle records survive payout failure**

If a payout fails during ClaimRewards, the settle record and perf summary must not be deleted or marked claimed. The participant can retry on a subsequent block. `finishSettle` only runs inside the CacheContext after all payments succeed.

---

**4. EndBlock error classification**

- **Unrecoverable** (return error, halt chain): missing params, failed epoch state writes (SetEpoch, SetEffectiveEpochIndex), failed DKG group creation. These mean the chain can't advance and would process stale data if it continued.
- **Recoverable** (log + skip): individual inference expiry failures, pruning errors, compute result errors. The chain can safely continue. Failed items keep their state for retry on the next pass.
- **Cross-module** (log + continue): collateral AdvanceEpoch, streamvesting AdvanceEpoch, BLS key gen. Failures in other modules should not block the inference module's epoch transition. `epoch_error` events emitted at collateral advance, settlement, and weight adjustment stages for indexer visibility. Not yet added at streamvesting advance or BLS keygen — those should be added for consistency.

---

**5. Expiry retry safety**

When an inference timeout fires and the refund fails, the inference stays in STARTED status and the timeout record is preserved. EndBlock only removes timeouts for successfully expired inferences. Executor penalty only applied after refund commits.

---

**6. Errors must not be silently ignored**

In tx/msg code paths, functions that can fail should return errors so the caller can decide whether to roll back or continue. Void functions that perform state writes (like `addTimeout`) hide failures from the caller.

In EndBlock and cross-module paths, returning an error isn't always viable (you may not want to halt the chain for a collateral issue). In those cases, "not ignoring" means structured surfacing — emit a typed event, log at error level, and have an explicit policy on whether the failure is retried, skipped, or escalated. The key is that someone (operator, indexer, governance) can observe and act on the failure, even if the chain continues.

---

**7. Integer narrowing at trust boundaries**

Any cast from a wider type to a narrower type (int64 to int32, uint64 to uint8, etc.) must be bounds-checked. Consensus paths return an error on overflow. Query-only paths clamp with a log warning. Silent truncation is never acceptable — it corrupts downstream calculations.

---

### What conforms (after Task 2)

- Settlement loop in `SettleAccounts` — CacheContext, error checked, old cleanup separated (PR #787)
- ClaimRewards payout — CacheContext, settle record preserved on failure (PR #789)
- FinishInference mutations — CacheContext, refund error propagated (PR #789)
- Inference expiry — CacheContext per inference, retry-safe timeout removal (PR #789)
- Streamvesting payments (AddVestedRewards) — CacheContext for transfer + schedule (PR #789)
- All 11 narrowing casts audited and guarded (PR #789)
- EndBlock error paths documented with rationale (PR #789)

---

### What doesn't conform yet

**[F-10]** Collateral and streamvesting `AdvanceEpoch` errors lack consistent observability. `epoch_error` events exist at some stages (collateral advance, settlement, weight adjustment) but not at streamvesting advance or BLS keygen. Retry semantics are also unclear — if collateral unbonding fails mid-epoch, is the expectation that the next epoch retries it, or is it silently dropped? Needs team input on classification and whether these paths need explicit retry or just consistent event coverage.

**[F-11]** Collateral unbonding loop aborts on first `SendCoins` failure. The actual risk is worse than just "remaining entries skipped" — emtries already paid before the failure don't get removed from state because removal happens after the loop. On retry next epoch, those entries pay out again. This is a double-payout risk. 
Fix options: 
(a) per-entry atomic send+remove via CacheContext 
(b) whole-batch atomic commit
(c) mark entries as processed before sending with rollback on failure. 
Needs team input.

**[F-13]** `addTimeout` is void — it drops errors from `SetInferenceTimeout` silently. In practice KV writes rarely fail during block execution, so the likelihood is low, but it still violates principle 6 by hiding the failure from the caller. If it ever did fail, the inference would have no expiry and escrow would be stuck until manual intervention. Low priority, but worth cleaning up for consistency.
Fix options:
(a) return error and roll back StartInference
(b) continue without expiry but add a fallback sweep.
Needs teaam input.

---

### How to verify

TASK 4

  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #784](https://github.com/gonka-ai/gonka/issues/784) every 6 hours.
