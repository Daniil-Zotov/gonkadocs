---
title: "#2013 — [BUG] Short segment is treated as PASSED (challenger pays a target that did nothing)"
source: https://github.com/gonka-ai/gonka/issues/2013
issue_number: 2013
synced_at: 2026-10-24T18:14:16Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    [BUG] Short segment is treated as PASSED (challenger pays a target that did nothing)
    <span class="issues-number">#2013</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/maria-mitina">@maria-mitina</a> opened 2026-10-15 09:44 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-10-21 09:38 UTC</span>
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

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/x0152">@x0152</a></span>
    <span class="issues-meta-item">commented 2026-10-15 21:22 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>https://github.com/gonka-ai/gonka/commit/24a4204de78cefbe14d3e1dda2784ab4fbebc65d</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/maria-mitina">@maria-mitina</a></span>
    <span class="issues-meta-item">commented 2026-10-21 09:37 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>solved, thanks</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2013](https://github.com/gonka-ai/gonka/issues/2013) every hour.
