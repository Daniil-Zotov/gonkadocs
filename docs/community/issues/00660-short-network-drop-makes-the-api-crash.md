---
title: "#660 — Short network drop makes the api crash"
source: https://github.com/gonka-ai/gonka/issues/660
issue_number: 660
synced_at: 2026-07-06T09:52:57Z
template: issues-main.html
---

> 🔄 **Auto-synced:** from [Issue #660](https://github.com/gonka-ai/gonka/issues/660) every 6 hours. 

# 🔴 Short network drop makes the api crash

**Author:** [@x0152](https://github.com/x0152) · **State:** Closed · **Created:** 2026-01-28 16:31 UTC · **Updated:** 2026-02-06 23:46 UTC

**Веха:** v0.2.10

---

## 📝 Описание

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
