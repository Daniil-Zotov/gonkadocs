---
title: "#784 — [P2] Possible underfunded issues"
source: https://github.com/gonka-ai/gonka/issues/784
issue_number: 784
synced_at: 2026-07-08T03:51:26Z
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

<div class="issues-content" markdown="1">
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
    <p>Working on it!</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@0xMayoor](https://github.com/0xMayoor)</span>
    <span class="issues-meta-item">commented 2026-02-21 14:20 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <h2>Task 1 — analysis (updated with IDs)</h2>
<p><em>Same findings as before, now with IDs so the Task 2 PRs can reference them.</em></p>
<p>Went through every runtime path where coins move out of a module account — <code>inference</code>, <code>bridge_escrow</code>, <code>top_reward</code>, <code>collateral</code>, <code>streamvesting</code>. Checked what happens if the sending account is underfunded at that moment.</p>
<p>Found ~25 distinct payout/refund paths. 12 handle it fine (error returned, state rolls back). 13 have issues, plus 2 more found while working on the fixes. Listed below.</p>
<hr />
<h3>settlement</h3>
<ul>
<li><strong>[F-01]</strong> <code>GetBitcoinSettleAmounts</code> error logged not returned. On failure the amounts slice is nil, <code>amounts[i]</code> panics in the settlement loop. EndBlock panic = permanent node crash.</li>
<li><strong>[F-02]</strong> <code>SettleAccounts</code> does mint, balance resets, perf summaries, and settle writes as independent KV operations. Failure mid-way means earlier writes are already committed. Participants can end up with zeroed balances but no settle record.</li>
<li><strong>[F-03]</strong> <code>SetSettleAmountWithGovernanceTransfer</code> return value ignored. If the governance transfer of an old settle fails, function returns before writing the new settle. Participant loses current epoch earnings silently.</li>
<li><strong>[F-04]</strong> <code>TransferOldSettleAmountsToGovernance</code> error logged not returned. Old settles stuck but records persist for retry. Low severity on its own, but was inside the atomic section so a failure here rolls back current-epoch settlement too.</li>
<li><strong>[F-05]</strong> <code>SettleAccounts</code> error swallowed by the orchestrator in <code>module.go</code>. Even when the function correctly returns an error, it gets thrown away.</li>
</ul>
<h3>claim rewards</h3>
<ul>
<li><strong>[F-06]</strong> <code>finishSettle</code> deletes the settle record and marks <code>Claimed = true</code> before the payout is confirmed. If the payout fails, participant's claim is gone permanently. No retry path. Probably the worst one.</li>
</ul>
<h3>inference lifecycle</h3>
<ul>
<li><strong>[F-07]</strong> expired inference refund fails → logged → inference marked EXPIRED anyway → timeout record removed. Requester's escrow stuck. This is the normal timeout path, happens routinely.</li>
<li><strong>[F-08]</strong> refund error swallowed in <code>processInferencePayments</code>. When FinishInference reprices lower and the refund fails, error logged, execution continues. Inference marked finished without developer getting their refund.</li>
<li><strong>[F-09]</strong> FinishInference mutation section runs on the raw context with no CacheContext. If any step fails after earlier writes, partial state persists. <code>FinishedProcessed()</code> blocks retry, making it permanent. Found this one while fixing F-08.</li>
</ul>
<h3>cross-module</h3>
<ul>
<li><strong>[F-10]</strong> collateral and streamvesting <code>AdvanceEpoch</code> errors swallowed by the inference orchestrator. If collateral fails its epoch counter doesn't increment, leading to desync.</li>
<li><strong>[F-11]</strong> collateral unbonding loop aborts on first <code>SendCoins</code> failure. Remaining entries skipped until next epoch.</li>
<li><strong>[F-12]</strong> streamvesting: coins sent to participant, then <code>SetVestingSchedule</code> fails. Schedule still has the entry, same amount sent again next epoch. Double payment.</li>
</ul>
<h3>misc</h3>
<ul>
<li><strong>[F-13]</strong> <code>addTimeout</code> is a void function. If the timeout write fails, inference never expires, escrow locked forever.</li>
<li><strong>[F-14]</strong> int64→int32 casts in keeper code with no bounds check. Worst case is the weight casts in validation sampling — silent truncation corrupts probability. Governance misconfiguration in top miner params could cause div-by-zero.</li>
<li><strong>[F-15]</strong> <code>TransferOldSettleAmountsToGovernance</code> returns error to EndBlock, halting the chain on what should be a non-fatal cleanup. The existing code comment already says this shouldn't block settlement. Found this while working on the EndBlock audit.</li>
</ul>
<hr />
<h3>what's fine</h3>
<p>Direct payments, vested payments, burns, refund wrapper, governance transfers, invalidation refunds, bridge release/rollback, slash/burn, minting — all return errors correctly.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@0xMayoor](https://github.com/0xMayoor)</span>
    <span class="issues-meta-item">commented 2026-02-22 18:38 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <h2>Task 2 — fixes</h2>
<p>Two PRs.</p>
<p><strong>PR 1</strong> (#787) — settlement bugs in <code>accountsettle.go</code>. Panic fix, CacheContext wrap, error checking, cleanup separation. Covers F-01 through F-05.</p>
<p><strong>PR 2</strong> (#789) — applies the same CacheContext approach to ClaimRewards, inference expiry, streamvesting, and FinishInference. Also did a full integer narrowing audit and EndBlock error path audit. Covers F-06, F-07, F-08, F-09, F-12, F-14, F-15. Each atomicity fix has a rollback test that would fail without CacheContext (proving the bug) and passes with it (proving the fix).</p>
<hr />
<p>Three findings still open — they all need a design decision before fix:</p>
<ul>
<li><strong>[F-10]</strong> cross-module <code>AdvanceEpoch</code> errors are swallowed. What's the desired recovery when collateral or streamvesting fails their epoch advance? Added <code>epoch_error</code> events for visibility in PR 2, but the actual recovery mechanism is the open question.</li>
<li><strong>[F-11]</strong> collateral unbonding aborts on first failure. Should the loop keep going and leave the failed entry for next epoch, or should the whole batch fail?</li>
<li><strong>[F-13]</strong> <code>addTimeout</code> is void. If the timeout write fails, inference sits in STARTED forever. Should StartInference roll back the whole inference, or continue without expiry tracking?</li>
</ul>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@0xMayoor](https://github.com/0xMayoor)</span>
    <span class="issues-meta-item">commented 2026-02-23 14:50 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <h2>Task 3 — standardized handling for underfunded events</h2>
<p>Principles based off Task 1 analysis and Task 2 fixes. Every fund-movement path should conform to these. Exceptions listed at the bottom.</p>
<hr />
<h3>Principles</h3>
<p><strong>1. Atomicity via CacheContext</strong></p>
<p>Any path that moves funds and writes related state (status changes, schedule updates, settle records) must wrap both in a single <code>CacheContext</code>. Either everything commits or nothing does. This prevents partial state where funds moved but the tracking record didn't update, or vice versa.</p>
<p>Applies to: msg server handlers, EndBlock expiry, settlement, vesting payments.</p>
<hr />
<p><strong>2. Nil-error response encoding for selected handlers</strong></p>
<p>Some handlers return <code>(response, nil)</code> to the SDK and encode failures in <code>response.ErrorMessage</code> instead of returning a real error. This is intentional — in Cosmos SDK, a non-nil error from any message handler rolls back the entire multi-message transaction, including unrelated messages that succeeded. Handlers that are expected to appear alongside other messages in a single tx use this pattern to allow per-message failure without aborting the batch.</p>
<p>Currently applies to: StartInference, FinishInference, ClaimRewards. Other handlers (validation submission, PoC validation, etc.) follow standard SDK error returns and rely on tx-level rollback. Since SDK rollback never triggers for the nil-error handlers, CacheContext is the only atomicity mechanism available to them.</p>
<hr />
<p><strong>3. Settle records survive payout failure</strong></p>
<p>If a payout fails during ClaimRewards, the settle record and perf summary must not be deleted or marked claimed. The participant can retry on a subsequent block. <code>finishSettle</code> only runs inside the CacheContext after all payments succeed.</p>
<hr />
<p><strong>4. EndBlock error classification</strong></p>
<ul>
<li><strong>Unrecoverable</strong> (return error, halt chain): missing params, failed epoch state writes (SetEpoch, SetEffectiveEpochIndex), failed DKG group creation. These mean the chain can't advance and would process stale data if it continued.</li>
<li><strong>Recoverable</strong> (log + skip): individual inference expiry failures, pruning errors, compute result errors. The chain can safely continue. Failed items keep their state for retry on the next pass.</li>
<li><strong>Cross-module</strong> (log + continue): collateral AdvanceEpoch, streamvesting AdvanceEpoch, BLS key gen. Failures in other modules should not block the inference module's epoch transition. <code>epoch_error</code> events emitted at collateral advance, settlement, and weight adjustment stages for indexer visibility. Not yet added at streamvesting advance or BLS keygen — those should be added for consistency.</li>
</ul>
<hr />
<p><strong>5. Expiry retry safety</strong></p>
<p>When an inference timeout fires and the refund fails, the inference stays in STARTED status and the timeout record is preserved. EndBlock only removes timeouts for successfully expired inferences. Executor penalty only applied after refund commits.</p>
<hr />
<p><strong>6. Errors must not be silently ignored</strong></p>
<p>In tx/msg code paths, functions that can fail should return errors so the caller can decide whether to roll back or continue. Void functions that perform state writes (like <code>addTimeout</code>) hide failures from the caller.</p>
<p>In EndBlock and cross-module paths, returning an error isn't always viable (you may not want to halt the chain for a collateral issue). In those cases, "not ignoring" means structured surfacing — emit a typed event, log at error level, and have an explicit policy on whether the failure is retried, skipped, or escalated. The key is that someone (operator, indexer, governance) can observe and act on the failure, even if the chain continues.</p>
<hr />
<p><strong>7. Integer narrowing at trust boundaries</strong></p>
<p>Any cast from a wider type to a narrower type (int64 to int32, uint64 to uint8, etc.) must be bounds-checked. Consensus paths return an error on overflow. Query-only paths clamp with a log warning. Silent truncation is never acceptable — it corrupts downstream calculations.</p>
<hr />
<h3>What conforms (after Task 2)</h3>
<ul>
<li>Settlement loop in <code>SettleAccounts</code> — CacheContext, error checked, old cleanup separated (PR #787)</li>
<li>ClaimRewards payout — CacheContext, settle record preserved on failure (PR #789)</li>
<li>FinishInference mutations — CacheContext, refund error propagated (PR #789)</li>
<li>Inference expiry — CacheContext per inference, retry-safe timeout removal (PR #789)</li>
<li>Streamvesting payments (AddVestedRewards) — CacheContext for transfer + schedule (PR #789)</li>
<li>All 11 narrowing casts audited and guarded (PR #789)</li>
<li>EndBlock error paths documented with rationale (PR #789)</li>
</ul>
<hr />
<h3>What doesn't conform yet</h3>
<p><strong>[F-10]</strong> Collateral and streamvesting <code>AdvanceEpoch</code> errors lack consistent observability. <code>epoch_error</code> events exist at some stages (collateral advance, settlement, weight adjustment) but not at streamvesting advance or BLS keygen. Retry semantics are also unclear — if collateral unbonding fails mid-epoch, is the expectation that the next epoch retries it, or is it silently dropped? Needs team input on classification and whether these paths need explicit retry or just consistent event coverage.</p>
<p><strong>[F-11]</strong> Collateral unbonding loop aborts on first <code>SendCoins</code> failure. The actual risk is worse than just "remaining entries skipped" — emtries already paid before the failure don't get removed from state because removal happens after the loop. On retry next epoch, those entries pay out again. This is a double-payout risk. 
Fix options: 
(a) per-entry atomic send+remove via CacheContext 
(b) whole-batch atomic commit
(c) mark entries as processed before sending with rollback on failure. 
Needs team input.</p>
<p><strong>[F-13]</strong> <code>addTimeout</code> is void — it drops errors from <code>SetInferenceTimeout</code> silently. In practice KV writes rarely fail during block execution, so the likelihood is low, but it still violates principle 6 by hiding the failure from the caller. If it ever did fail, the inference would have no expiry and escrow would be stuck until manual intervention. Low priority, but worth cleaning up for consistency.
Fix options:
(a) return error and roll back StartInference
(b) continue without expiry but add a fallback sweep.
Needs teaam input.</p>
<hr />
<h3>How to verify</h3>
<p>TASK 4</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #784](https://github.com/gonka-ai/gonka/issues/784) every hour.
