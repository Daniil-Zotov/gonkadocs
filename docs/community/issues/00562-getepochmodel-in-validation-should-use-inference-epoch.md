---
title: "#562 — GetEpochModel in validation should use inference epoch"
source: https://github.com/gonka-ai/gonka/issues/562
issue_number: 562
synced_at: 2026-07-17T23:13:03Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    GetEpochModel in validation should use inference epoch
    <span class="issues-number">#562</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/x0152">@x0152</a> opened 2026-01-15 10:00 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-02-06 00:58 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Follow-up to #553. Line 68 uses GetEpochModel (current epoch) instead of GetEpochModelForEpoch(ctx, inference.EpochId, inference.Model)
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/DimaOrekhovPS">@DimaOrekhovPS</a></span>
    <span class="issues-meta-item">commented 2026-02-06 00:58 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Resolved with #545 </p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #562](https://github.com/gonka-ai/gonka/issues/562) every hour.
