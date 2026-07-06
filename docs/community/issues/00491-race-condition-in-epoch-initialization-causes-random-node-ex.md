---
title: "#491 — Race Condition in Epoch Initialization Causes Random Node Exclusion"
source: https://github.com/gonka-ai/gonka/issues/491
issue_number: 491
synced_at: 2026-07-06T09:53:34Z
template: issues-main.html
---

> 🔄 **Auto-synced:** from [Issue #491](https://github.com/gonka-ai/gonka/issues/491) every 6 hours. 

# 🔴 Race Condition in Epoch Initialization Causes Random Node Exclusion

**Author:** [@baychak](https://github.com/baychak) · **State:** Closed · **Created:** 2025-12-13 17:25 UTC · **Updated:** 2025-12-15 01:18 UTC

---

## 📝 Описание

# Bug Report: Race Condition in Epoch Initialization

**Date:** December 13, 2025  
**Severity:** High - Causes node exclusion from epoch  
**Affected Version:** v0.2.5  
**Node:** gonka1yq4vwn7fc9x7lykjhc0x3e7r2atee32czy34mt

## Problem

API queries `EpochGroupData` before blockchain finishes processing member additions, receives empty `SubGroupModels` array, triggers early return in `broker.go:1323`, node excluded from epoch.

## Evidence

**Timeline with millisecond precision:**

```
11:37:39.000 UTC - Block 1,704,365: Epoch 110 starts
11:37:39.256 UTC - API queries GetEpochGroupData(110, "")
11:37:39.256 UTC - Response: SubGroupModels = [] (empty)
11:37:39.256 UTC - Log: "WARN broker/broker.go:1323 Parent epoch group SubGroupModels are empty"
11:37:39.256 UTC - Early return - node excluded
~11:37:39.XXX UTC - Blockchain finishes AddMember() processing
16:30:00.000 UTC - Manual query executed (5 hours later)
16:30:00.XXX UTC - Response: SubGroupModels = ["Qwen/Qwen3-32B-FP8", ...] (5 models)
```

**Proof of race condition:**
- **Empty query:** 11:37:39.256Z shows `SubGroupModels = []`
- **Populated query:** 16:30:00Z shows `SubGroupModels` with 5 models including user's
- **Conclusion:** Data written correctly but API queried before blockchain completion

**Log evidence:**
```
2025-12-13T11:37:39.256Z WARN broker/broker.go:1323 Parent epoch group SubGroupModels are empty
```

**Why it repeated 4 times:**

`UpdateNodeWithEpochData()` вызывается на каждой фазе эпохи:
1. **11:37:39** - PoCGenerate (race condition - запрос слишком рано)
2. **11:38:32** - PoCValidate (нода уже исключена, снова empty)
3. **11:39:25** - PoCAggregate (нода уже исключена, снова empty)
4. **11:40:18** - PoCReward (нода уже исключена, снова empty)

## Root Cause

**File:** `decentralized-api/broker/broker.go` lines 1323-1325

```go
if len(epochGroupData.SubGroupModels) == 0 {
    log.Warn().Msg("Parent epoch group SubGroupModels are empty")
    return nil  // ← No retry, immediate exit
}
```

**Issue:** No retry mechanism when blockchain hasn't finished writing data yet.

## Impact

- Node excluded from epoch despite correct configuration
- Non-deterministic - depends on timing/load
- May affect multiple nodes across different epochs

---

**Node:** gonka1yq4vwn7fc9x7lykjhc0x3e7r2atee32czy34mt  
**Version:** v0.2.5  

