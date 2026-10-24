---
title: "#2014 — [BUG] fully_reserved_by_training abort is unreachable on a short segment"
source: https://github.com/gonka-ai/gonka/issues/2014
issue_number: 2014
synced_at: 2026-10-24T00:47:40Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    [BUG] fully_reserved_by_training abort is unreachable on a short segment
    <span class="issues-number">#2014</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/maria-mitina">@maria-mitina</a> opened 2026-10-15 09:49 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-10-21 09:37 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span></div>
</div>

<div class="issues-content" markdown="1">
# Title
fully_reserved_by_training abort is unreachable on a short segment

## Summary
The intended guard for a target whose nodes are all training-reserved lives inside the punishable-segment evaluation:

reserved := am.keeper.CollectEpochReservedNodeWeightsBetween(ctx, ch.EpochIndex, ch.StartHeight, finish-1, keeper.ReservationScopeShield)
// ...
if shielded[ch.Target] > 0 && expected <= 0 {
	if !rotate && am.keeper.BuildEpochReservationView(ctx, ch.EpochIndex).FullyReservedAt(ch.Target, finish-1) {
		return am.keeper.MarkChallengeAborted(ctx, ch.Target, "fully_reserved_by_training")
	}

Because [Bug with min punishable window](https://github.com/gonka-ai/gonka/issues/2013) returns before this code, a fully reserved target is never aborted; it is paid instead. The reservation check should run before the duration check (or at create time, see [Bug 3](https://github.com/gonka-ai/gonka/issues/2012)).


</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/x0152">@x0152</a></span>
    <span class="issues-meta-item">commented 2026-10-15 21:23 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>https://github.com/gonka-ai/gonka/commit/0853195ca2da7bb7553805ba26be9d0fb03ffaf1</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/maria-mitina">@maria-mitina</a></span>
    <span class="issues-meta-item">commented 2026-10-21 09:37 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>solved thank you</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2014](https://github.com/gonka-ai/gonka/issues/2014) every hour.
