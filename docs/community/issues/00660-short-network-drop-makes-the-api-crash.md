---
title: "#660 — Short network drop makes the api crash"
source: https://github.com/gonka-ai/gonka/issues/660
issue_number: 660
synced_at: 2026-07-30T03:37:24Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Short network drop makes the api crash
    <span class="issues-number">#660</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/x0152">@x0152</a> opened 2026-01-28 16:31 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-02-06 23:46 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
If chain node is unreachable even for short period, the API can crash:

```
2026/01/28 14:01:30 ERROR [training-task-assigner] Failed to query chain status err="post failed: Post \"http://genesis-node:26657\": dial tcp: lookup genesis-node on 127.0.0.11:53: no such host"
panic: runtime error: invalid memory address or nil pointer dereference
[signal SIGSEGV: segmentation violation code=0x1 addr=0x140 pc=0x42d18e2]

goroutine 10 [running]:
decentralized-api/training.(*Assigner).tryClaimingTaskToAssign(0xc0017a8090)
  /app/decentralized-api/training/assigner.go:74 +0xc2
decentralized-api/training.(*Assigner).claimTasksForAssignment(0xc0017a8090)
  /app/decentralized-api/training/assigner.go:55 +0x10c
created by decentralized-api/training.NewAssigner in goroutine 1
  /app/decentralized-api/training/assigner.go:41 +0xd8
```
</div>

---

> 🔄 **Auto-synced** from [Issue #660](https://github.com/gonka-ai/gonka/issues/660) every hour.
