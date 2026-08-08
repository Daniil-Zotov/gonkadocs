---
title: "#440 — All the old keys from the cluster entered the new epoch, even though that cluster was deleted"
source: https://github.com/gonka-ai/gonka/issues/440
issue_number: 440
synced_at: 2026-08-08T09:06:33Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    All the old keys from the cluster entered the new epoch, even though that cluster was deleted
    <span class="issues-number">#440</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2025-11-17 20:12 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-01-29 05:48 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
All the old keys from the cluster entered the new epoch, even though that cluster was deleted about six hours ago. For some reason, they passed the PoC with a small weight, but it still looks like they shouldn’t have appeared there at all.

The cluster was shut down and the warm keys were deleted.
fs was completely deleted

![Image](https://github.com/user-attachments/assets/de21696d-5fdd-4020-b212-50f44f282e93)
</div>

---

> 🔄 **Auto-synced** from [Issue #440](https://github.com/gonka-ai/gonka/issues/440) every hour.
