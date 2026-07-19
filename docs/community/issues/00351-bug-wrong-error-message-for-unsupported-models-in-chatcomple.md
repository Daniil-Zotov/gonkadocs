---
title: "#351 — BUG: Wrong error message for unsupported models in /chat/completions"
source: https://github.com/gonka-ai/gonka/issues/351
issue_number: 351
synced_at: 2026-07-19T15:27:24Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    BUG: Wrong error message for unsupported models in /chat/completions
    <span class="issues-number">#351</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/gmorgachev">@gmorgachev</a> opened 2025-09-10 23:19 UTC</span>
    <span class="issues-meta-item">5 comments</span>
    <span class="issues-meta-item">Updated 2026-04-28 18:50 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
When inference for unsupported message requested, system returns:

"HTTP/1.1 402 Payment Required"
</div>

---

## 💬 Comments (5)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-01-28 22:23 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Needs to be rechecked</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/AlexeySamosadov">@AlexeySamosadov</a></span>
    <span class="issues-meta-item">commented 2026-02-08 14:14 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>PR created: https://github.com/gonka-ai/gonka/pull/679</p>
<p>Fixes wrong error message for unsupported models in /chat/completions.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/AlexeySamosadov">@AlexeySamosadov</a></span>
    <span class="issues-meta-item">commented 2026-02-12 15:26 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>I already have a PR for this: #679 — fixes the wrong error message for unsupported models. Would appreciate a review when you get a chance.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/unameisfine">@unameisfine</a></span>
    <span class="issues-meta-item">commented 2026-03-19 22:42 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Starting work on this. Previous PR was closed as stale — will investigate the current error handling path and submit a fix. ETA: 2-3 days.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/x0152">@x0152</a></span>
    <span class="issues-meta-item">commented 2026-04-28 17:15 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Already fixed in #614. Closing</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #351](https://github.com/gonka-ai/gonka/issues/351) every hour.
