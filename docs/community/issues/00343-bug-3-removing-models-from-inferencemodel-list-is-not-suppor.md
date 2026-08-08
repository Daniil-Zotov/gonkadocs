---
title: "#343 — BUG-3: Removing models from inference/model_list is not supported"
source: https://github.com/gonka-ai/gonka/issues/343
issue_number: 343
synced_at: 2026-08-08T10:00:09Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    BUG-3: Removing models from inference/model_list is not supported
    <span class="issues-number">#343</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/gmorgachev">@gmorgachev</a> opened 2025-09-05 07:31 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-01-28 22:26 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Fix the bug in network inference API where sending a request with an unsupported model name incorrectly returns the error 402 Insufficient balance.
</div>

---

> 🔄 **Auto-synced** from [Issue #343](https://github.com/gonka-ai/gonka/issues/343) every hour.
