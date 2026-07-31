---
title: "#891 — [P0] Proxy server for `devshards`: timeout handling"
source: https://github.com/gonka-ai/gonka/issues/891
issue_number: 891
synced_at: 2026-07-31T10:01:53Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    [P0] Proxy server for `devshards`: timeout handling
    <span class="issues-number">#891</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/dcastro">@dcastro</a> opened 2026-03-16 13:45 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-04-01 03:20 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #aaaaaa; color: #24292f; border-color: #aaaaaa;">devshards</span></div>
</div>

<div class="issues-content" markdown="1">
At the moment, the proxy server in `/subnet/cmd/subnetctl` handles 3 types of actions: chat completions (with diff propagation), finalizing `devshards`, and querying the `devshards` status.

It should also handle timeout-related mechanisms.
</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/dcastro">@dcastro</a></span>
    <span class="issues-meta-item">commented 2026-03-20 08:35 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Closed in favor of #911</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-03-20 22:41 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@gmorgachev, you wanted to include this issue in the upgrade v0.2.12. Does https://github.com/gonka-ai/gonka/pull/911 cover everything you expected here?</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #891](https://github.com/gonka-ai/gonka/issues/891) every hour.
