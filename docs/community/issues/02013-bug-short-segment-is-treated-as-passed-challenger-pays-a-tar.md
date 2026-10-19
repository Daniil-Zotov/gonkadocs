---
title: "#2013 — [BUG] Short segment is treated as PASSED (challenger pays a target that did nothing)"
source: https://github.com/gonka-ai/gonka/issues/2013
issue_number: 2013
synced_at: 2026-10-19T13:35:33Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    [BUG] Short segment is treated as PASSED (challenger pays a target that did nothing)
    <span class="issues-number">#2013</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/maria-mitina">@maria-mitina</a> opened 2026-10-15 09:44 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-10-15 21:50 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span></div>
</div>

<div class="issues-content" markdown="1">
## Summary
decideCurrentChallengeSegment skips evaluation whenever the segment is shorter than min_punishable_segment_blocks and returns nil; the caller treats nil as "passed":

if finish <= ch.StartHeight {
	return nil
}
duration := finish - ch.StartHeight
// ...
if duration < types.EffectiveMinPunishableSegmentBlocks(params.PocChallengeParams) {
	return am.advanceAfterDecision(ctx, ch, rotate)
}

if !rotate {
	if err := am.keeper.MarkChallengePassed(cacheCtx, ch.Target); err != nil {

Both segments in my test were below the threshold (18744−18648 = 96 at cPoC rotation, 18870−18788 = 82 at the final decision), so the challenge was never evaluated at all and defaulted to PASSED → lock paid to target. "Not enough data to punish" must not equal "target passed". Expected: ABORTED (refund the challenger, payLockedChallengePayment already handles ABORTED → poc_challenge_refund), or carry the segment over / require at least one punishable segment before PASSED is possible.


</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/x0152">@x0152</a></span>
    <span class="issues-meta-item">commented 2026-10-15 21:22 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>https://github.com/gonka-ai/gonka/commit/24a4204de78cefbe14d3e1dda2784ab4fbebc65d</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2013](https://github.com/gonka-ai/gonka/issues/2013) every hour.
