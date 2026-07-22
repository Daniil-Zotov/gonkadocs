---
title: "#1097 — Improve API response for non-existent wallet"
source: https://github.com/gonka-ai/gonka/issues/1097
issue_number: 1097
synced_at: 2026-07-22T03:52:26Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Improve API response for non-existent wallet
    <span class="issues-number">#1097</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-04-21 19:47 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-04-22 22:21 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
When querying a non-existent wallet via `GET https://node3.gonka.ai/v1/participants/{address}` the API currently returns a 500 Internal Server Error.

Expected Behavior
If the wallet is not found, the API should return `404 Not Found` instead of 500

Rationale
A missing wallet is a valid client-side case, not a server error. Returning 404 improves API correctness and makes error handling more predictable for clients.
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-04-22 22:21 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>https://github.com/gonka-ai/gonka/pull/750</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1097](https://github.com/gonka-ai/gonka/issues/1097) every hour.
