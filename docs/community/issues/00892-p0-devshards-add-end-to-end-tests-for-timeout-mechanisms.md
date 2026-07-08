---
title: "#892 — [P0] `devshards`: add end-to-end tests for timeout mechanisms"
source: https://github.com/gonka-ai/gonka/issues/892
issue_number: 892
synced_at: 2026-07-08T06:41:52Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    [P0] `devshards`: add end-to-end tests for timeout mechanisms
    <span class="issues-number">#892</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item">[@dcastro](https://github.com/dcastro) opened 2026-03-16 13:48 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-05-25 18:37 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #f86c7a; color: #24292f; border-color: #f86c7a;">Priority: High</span> <span class="issues-label" style="background-color: #aaaaaa; color: #24292f; border-color: #aaaaaa;">devshards</span></div>
</div>

<div class="issues-content" markdown="1">
In #891 we're making the proxy server handle timeout-related mechanisms.

We should write end-to-end testermint tests for these mechanisms.

The proxy server should allow configuring the deadline limits so that the tests can choose a shorter deadline.
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@KKizilov](https://github.com/KKizilov)</span>
    <span class="issues-meta-item">commented 2026-03-26 15:07 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Will be done by April 5th.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #892](https://github.com/gonka-ai/gonka/issues/892) every hour.
