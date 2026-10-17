---
title: "#2014 — [BUG] fully_reserved_by_training abort is unreachable on a short segment"
source: https://github.com/gonka-ai/gonka/issues/2014
issue_number: 2014
synced_at: 2026-10-17T04:39:07Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    [BUG] fully_reserved_by_training abort is unreachable on a short segment
    <span class="issues-number">#2014</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/maria-mitina">@maria-mitina</a> opened 2026-10-15 09:49 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-10-15 21:50 UTC</span>
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

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/x0152">@x0152</a></span>
    <span class="issues-meta-item">commented 2026-10-15 21:23 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>https://github.com/gonka-ai/gonka/commit/0853195ca2da7bb7553805ba26be9d0fb03ffaf1</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2014](https://github.com/gonka-ai/gonka/issues/2014) every hour.
