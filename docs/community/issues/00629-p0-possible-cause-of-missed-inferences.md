---
title: "#629 — [P0] Possible cause of missed inferences"
source: https://github.com/gonka-ai/gonka/issues/629
issue_number: 629
synced_at: 2026-08-05T12:21:29Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    [P0] Possible cause of missed inferences
    <span class="issues-number">#629</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-01-23 19:47 UTC</span>
    <span class="issues-meta-item">4 comments</span>
    <span class="issues-meta-item">Updated 2026-04-28 18:28 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
We're distributing inference requests on the chain based on the total weight of the participant, not the weight of the participant's mlnode for a specific `model_id`. Seems like it's easy can be the cause of missed inferences (e.g. I have 100 nodes for `model_id1` and 3 nodes for `model_id2`, but I get the amount of requests based on the weight of 103 nodes for `model_id2`)
</div>

---

## 💬 Comments (4)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/x0152">@x0152</a></span>
    <span class="issues-meta-item">commented 2026-01-26 08:06 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <h1>642</h1>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-03-20 23:41 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@tamazgadaev @IgnatovFedor @0xgonka do we want the same for preserved ML Nodes during PoC phase?</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-03-24 23:12 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>This issue is a subset of multi-model support (https://github.com/gonka-ai/gonka/issues/728)
We'll figure out when to review and merge this issue during work on multimodels https://github.com/gonka-ai/gonka/issues/728
@x0152 @0xgonka </p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/x0152">@x0152</a></span>
    <span class="issues-meta-item">commented 2026-04-28 18:28 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Closing as resolved by the multi-PoC updates</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #629](https://github.com/gonka-ai/gonka/issues/629) every hour.
