---
title: "#1067 — bug: ClaimRewards error handling — payout path silently continues on failure"
source: https://github.com/gonka-ai/gonka/issues/1067
issue_number: 1067
synced_at: 2026-07-26T00:17:28Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    bug: ClaimRewards error handling — payout path silently continues on failure
    <span class="issues-number">#1067</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/Mayveskii">@Mayveskii</a> opened 2026-04-15 19:40 UTC</span>
    <span class="issues-meta-item">5 comments</span>
    <span class="issues-meta-item">Updated 2026-04-28 20:55 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #a2eeef; color: #24292f; border-color: #a2eeef;">enhancement</span></div>
</div>

<div class="issues-content" markdown="1">
## Summary
In `msg_server_claim_rewards.go`, when `PayParticipantFromEscrow` or `PayParticipantFromModule` returns an error, the function logs the error and continues processing instead of returning the error. This can result in partial payouts or silent fund loss when the payment path fails.
## Motivation
This was identified during audit of payout error handling in the inference escrow claims path. The current behavior allows settlement records to be finalized even when underlying payments have failed, making the loss non-recoverable. PR #948 (v0.2.12 upgrade) introduces `CacheContext` to make payouts atomic, confirming the maintainers are aware of this class of issue.
## Impact
- Affected components: `x/inference/keeper/msg_server_claim_rewards.go`
- Who is impacted: Validators and delegators who claim rewards from inference escrow
- Which metric is expected to improve: payout success rate — errors that should halt the transaction are logged and swallowed, resulting in settlements marked complete without actual payment
## Detailed description
- `ClaimRewards` calls `PayParticipantFromEscrow` and `PayParticipantFromModule` to distribute work and reward coins. When either returns an error:
  1. Work payment failure: `k.LogError("Error paying participant from escrow", ...)` is logged, but `finishSettle` is still called, marking the settlement complete even though the participant was never paid.
  2. Reward payment failure: `k.LogError("Error paying participant for rewards", ...)` is logged, but the function continues, potentially completing a partial settlement.
- In both cases, the settlement is finalized regardless of payment success. There is no mechanism to retry failed payments.
- Evidence: PR #948 (CacheContext atomic payouts) addresses this pattern. PR #1013 (escrow fund loss prevention) addresses a related class. PR #1016 (this fix) was previously opened but closed without merge. Сheck it out - https://github.com/gonka-ai/gonka/commit/ec5e453e03b0970ce6c4db1ca4243d0843f57989
## Expected outcome
- `ClaimRewards` should use `CacheContext` to wrap all payout mutations atomically
- If any payment fails, the entire transaction should be rolled back
- The settlement record should persist for retry, not be finalized as complete
- Backward compatible: settlement records that were partially paid remain claimable
## Proposed approach
- Use `CacheContext` for atomic payouts (aligned with PR #948 approach):
  1. Wrap all payment operations in `cacheCtx`
  2. Call `writeFn()` only after all payments succeed
  3. On failure, settlement persists with pending status for retry
- Alternatives considered:
  - Return error immediately on first payment failure (simpler but doesn't allow partial recovery)
  - Add a retry queue for failed payments (over-engineered for this scope)
## External feedback
- Discord thread link: https://discord.com/channels/1336477374442770503/1425189436748206171/1492754655170662431
- Community reviewer(s): Mayveskii
</div>

---

## 💬 Comments (5)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Doog-bot534">@Doog-bot534</a></span>
    <span class="issues-meta-item">commented 2026-04-16 03:08 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>This issue aligns with the finding in our security audit (#1053, finding #3) and the fix submitted in PR #1051.</p>
<p>Our PR #1051 takes the simpler approach (return error without calling <code>finishSettle</code>), while the <code>CacheContext</code> approach described here is more comprehensive and aligned with the pattern in PR #948. Happy to update #1051 to use <code>CacheContext</code> if the maintainers prefer that approach.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Mayveskii">@Mayveskii</a></span>
    <span class="issues-meta-item">commented 2026-04-16 03:37 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <blockquote>
<p>This issue aligns with the finding in our security audit (<a href="https://github.com/gonka-ai/gonka/issues/1053">#1053</a>, finding <a href="https://github.com/gonka-ai/gonka/pull/3">#3</a>) and the fix submitted in PR <a href="https://github.com/gonka-ai/gonka/pull/1051">#1051</a>.</p>
<p>Our PR <a href="https://github.com/gonka-ai/gonka/pull/1051">#1051</a> takes the simpler approach (return error without calling <code>finishSettle</code>), while the <code>CacheContext</code> approach described here is more comprehensive and aligned with the pattern in PR <a href="https://github.com/gonka-ai/gonka/pull/948">#948</a>. Happy to update <a href="https://github.com/gonka-ai/gonka/pull/1051">#1051</a> to use <code>CacheContext</code> if the maintainers prefer that approach.</p>
</blockquote>
<p>Thanks for the context and the alignment with #1053 finding #3.
For the maintainers' visibility: the fix proposed in this issue and the approach in PR #1051 were already proposed and implemented in commit ec5e453 (https://github.com/gonka-ai/gonka/commit/ec5e453) and PR #1016 (https://github.com/gonka-ai/gonka/pull/1016) (opened Apr 5, closed without merge). It is closed cause of terms of visibily bugs finding that the team set in contrib proccess. That commit predates PR #1051 by 10 days and includes both the error propagation fix and a unit test (TestClaimRewards_PayoutRewardFailure_RollsBackState).
The approach in ec5e453 goes further than just removing finishSettle:
1. ClaimRewards: return payoutResponse, nil → return nil, payoutErr — the critical line that enables full TX rollback
2. payoutClaim reward failure: finishSettle removed, response changed to Amount: 0, Result: "Claim payout failed, no funds moved." — no partial success signal
3. handleUnderfundedWork: finishSettle removed — Cosmos SDK rollback preserves SettleAmount for retry
4. Unit test: verifies error propagation and that SettleAmount remains in store after failure
Happy to re-submit as a new PR from Mayveskii/gonka if the maintainers prefer the full approach.
Regarding the label — this is a bug (fund loss on payment failure), not an enhancement. Could a maintainer update the label from enhancement to bug?</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Doog-bot534">@Doog-bot534</a></span>
    <span class="issues-meta-item">commented 2026-04-16 12:09 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Good catch on the timeline — I wasn't aware of PR #1016 and commit ec5e453 when I filed #1051. My fix came independently from the audit in #1053 (finding #3), but yours clearly predates it and covers more ground (full TX rollback + unit test). Happy to defer to whichever approach the maintainers prefer. Agreed this should be labeled as bug, not enhancement.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Mayveskii">@Mayveskii</a></span>
    <span class="issues-meta-item">commented 2026-04-28 19:09 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@x0152 watch out this one , please </p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/x0152">@x0152</a></span>
    <span class="issues-meta-item">commented 2026-04-28 20:55 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>There were additional non-atomic paths, and they were fully addressed in #789</p>
<p>Closing as resolved</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1067](https://github.com/gonka-ai/gonka/issues/1067) every hour.
