---
title: "#464 — Difficulty with PoC, defined by `RTarget`"
source: https://github.com/gonka-ai/gonka/issues/464
issue_number: 464
synced_at: 2026-07-27T18:54:13Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Difficulty with PoC, defined by `RTarget`
    <span class="issues-number">#464</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2025-12-03 21:23 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-01-15 22:20 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
There is a difficulty with PoC, defined by `RTarget` in the repo. It essentially defines the percentage of "correct" nonces from all nonces => how many nonces participants has to check to find the correct one. 

Let's say we:
- increase complexity 
- add coefficient which transforn new weight to ~old weight (just to maintain same numbers in dashboard)

Please figure out how we're doing that. The open question - how we check which nodes were preserved, which are not, and which we preserved for > 1 epochs
=> to understand which weight to transform and which not 

There is some simple and elegant solution for that, e.g., use this coefficient at transforming len(nonces) -> weight
=> already transformed weight will be recorded in further preserved nodes

</div>

---

> 🔄 **Auto-synced** from [Issue #464](https://github.com/gonka-ai/gonka/issues/464) every hour.
