---
title: "#463 — Nodes always available"
source: https://github.com/gonka-ai/gonka/issues/463
issue_number: 463
synced_at: 2026-07-16T00:15:55Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Nodes always available
    <span class="issues-number">#463</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item">[@tcharchian](https://github.com/tcharchian) opened 2025-12-03 21:19 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-01-21 19:58 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
The defunal "INFERENCE" state for MLNode de-facto didn't work. 
it deployed model, but model was not in epoch state
=> validation would not go to this node => recovery is not possible 

take a look at this commit and test it https://github.com/gonka-ai/gonka/commit/21cb61ee61bace322de67265bcb971016e609cb3

goal: if MLNode is availabe and not in poc => it must be used for inference
</div>

---

> 🔄 **Auto-synced** from [Issue #463](https://github.com/gonka-ai/gonka/issues/463) every hour.
