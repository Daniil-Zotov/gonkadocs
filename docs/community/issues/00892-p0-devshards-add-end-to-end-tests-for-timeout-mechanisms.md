---
title: "#892 — [P0] `devshards`: add end-to-end tests for timeout mechanisms"
source: https://github.com/gonka-ai/gonka/issues/892
issue_number: 892
synced_at: 2026-08-10T02:38:28Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    [P0] `devshards`: add end-to-end tests for timeout mechanisms
    <span class="issues-number">#892</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/dcastro">@dcastro</a> opened 2026-03-16 13:48 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-07-20 05:03 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #f86c7a; color: #24292f; border-color: #f86c7a;">Priority: High</span> <span class="issues-label" style="background-color: #aaaaaa; color: #24292f; border-color: #aaaaaa;">devshards</span></div>
</div>

<div class="issues-content" markdown="1">
In #891 we're making the proxy server handle timeout-related mechanisms.

We should write end-to-end testermint tests for these mechanisms.

The proxy server should allow configuring the deadline limits so that the tests can choose a shorter deadline.
</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/KKizilov">@KKizilov</a></span>
    <span class="issues-meta-item">commented 2026-03-26 15:07 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Will be done by April 5th.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/a-kuprin">@a-kuprin</a></span>
    <span class="issues-meta-item">commented 2026-07-20 05:03 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Closed by https://github.com/gonka-ai/gonka/pull/1332 and https://github.com/gonka-ai/gonka/pull/1482</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #892](https://github.com/gonka-ai/gonka/issues/892) every hour.
