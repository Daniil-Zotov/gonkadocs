---
title: "#337 — [P1] Config update process"
source: https://github.com/gonka-ai/gonka/issues/337
issue_number: 337
synced_at: 2026-07-14T15:06:37Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    [P1] Config update process
    <span class="issues-number">#337</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item">[@tcharchian](https://github.com/tcharchian) opened 2025-09-03 23:19 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-01-15 23:10 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
- [x] The `node-config.json`, which contains the initial configuration, should not be applied automatically at the start — it should only be applied after an explicit command (otherwise, it creates a mess).
- [x] We need an `UPDATE nodes/:id` endpoint to modify node parameters, and some way to understand what exactly is being changed — so that a node’s status updates after the next PoC. Right now, when you delete and re-add a node, it results in chaos.
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@tcharchian](https://github.com/tcharchian)</span>
    <span class="issues-meta-item">commented 2026-01-15 23:10 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <h1>390 #281 #240</h1>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #337](https://github.com/gonka-ai/gonka/issues/337) every hour.
