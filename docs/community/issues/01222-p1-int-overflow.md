---
title: "#1222 — [P1] Int overflow"
source: https://github.com/gonka-ai/gonka/issues/1222
issue_number: 1222
synced_at: 2026-07-07T04:28:01Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    [P1] Int overflow
    <span class="issues-number">#1222</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item">[@tcharchian](https://github.com/tcharchian) opened 2026-05-21 22:30 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-06-30 13:00 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #12a6e8; color: #24292f; border-color: #12a6e8;">Priority: Medium</span></div>
</div>

<div class="issues-content">
The goal of this is to have in place after this a standard way of handling possible overflows, have it implemented consistently across the entire codebase and to have a check (preferably a static check, an AI persona if necessary as a backup) that flags anything that doesn't use the established pattern
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@olegsuhoparov](https://github.com/olegsuhoparov)</span>
    <span class="issues-meta-item">commented 2026-06-30 13:00 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    Opened a surgical first PR against main: #1379.

It ports the already-accepted #1100/#1101 overflow fixes to main and adds two small guards for payout uint64->int64 conversion and validation totalWeight accumulation.

I intentionally left broad static analysis and #1017 supply-cap semantics out of scope so this remains reviewable.
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1222](https://github.com/gonka-ai/gonka/issues/1222) every hour.
