---
title: "#429 — Cleaning nats"
source: https://github.com/gonka-ai/gonka/issues/429
issue_number: 429
synced_at: 2026-08-03T15:23:58Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Cleaning nats
    <span class="issues-number">#429</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2025-11-12 19:08 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-01-15 22:19 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Problem with .nats queue being quite big
```
root@CL-Gonka1-NetNode:~/gonka/deploy/join# du -d1 -h .dapi/.nats
3.6G .dapi/.nats/jetstream
3.6G .dapi/.nats
```

Add some cleaning, maybe find a way to clean manually
</div>

---

> 🔄 **Auto-synced** from [Issue #429](https://github.com/gonka-ai/gonka/issues/429) every hour.
