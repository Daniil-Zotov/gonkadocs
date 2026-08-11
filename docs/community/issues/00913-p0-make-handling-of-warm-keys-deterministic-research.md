---
title: "#913 — [P0] Make handling of warm keys deterministic (research)"
source: https://github.com/gonka-ai/gonka/issues/913
issue_number: 913
synced_at: 2026-08-11T06:08:20Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    [P0] Make handling of warm keys deterministic (research)
    <span class="issues-number">#913</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/dcastro">@dcastro</a> opened 2026-03-18 10:28 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-07-01 06:17 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #f86c7a; color: #24292f; border-color: #f86c7a;">Priority: High</span> <span class="issues-label" style="background-color: #aaaaaa; color: #24292f; border-color: #aaaaaa;">devshards</span></div>
</div>

<div class="issues-content" markdown="1">
At the moment, `devshards` handle hosts' warm keys in a non deterministic way.

Different hosts can check whether a warm key is authorized at different points in time, using the mainnet bridge, and therefore get different results.
One example could be a host `H` shutting down for 20 mins, and then becoming available again. They'll need to process diffs from 20 mins ago. If some other host has rotated their warm key in the meantime, `H` will not deem the warm key used to sign the original diff as authorized (even though it was at the time it was signed)

We need to think of a solution to make this deterministic, and implement it.
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/KKizilov">@KKizilov</a></span>
    <span class="issues-meta-item">commented 2026-03-26 15:20 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Will be finished by March 27th. </p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #913](https://github.com/gonka-ai/gonka/issues/913) every hour.
