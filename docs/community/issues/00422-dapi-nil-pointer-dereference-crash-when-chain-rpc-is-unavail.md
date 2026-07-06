---
title: "#422 — DAPI  nil pointer dereference crash when chain RPC is unavailable"
source: https://github.com/gonka-ai/gonka/issues/422
issue_number: 422
synced_at: 2026-07-06T09:52:53Z
template: issues-main.html
---

> 🔄 **Авто-синхронизация:** из [Issue #422](https://github.com/gonka-ai/gonka/issues/422) каждые 6 часов. 

# 🔴 DAPI  nil pointer dereference crash when chain RPC is unavailable

**Автор:** [@mfursov](https://github.com/mfursov) · **Состояние:** Closed · **Создано:** 2025-11-10 02:37 UTC · **Обновлено:** 2026-02-10 03:59 UTC

**Веха:** v0.2.10

---

## 📝 Описание

**Problem:** DAPI crashes when chain node RPC becomes temporarily unavailable (I/O errors, restarts, network issues)

**Root Cause:** Missing `return` statement after error in `tryClaimingTaskToAssign()` function

** Timeline:  **
```
00:06:26 - Chain node I/O error (trigger)
         CONSENSUS FAILURE: error writing batch to DB
         "sync /workspace/gonka-data/chain/data/blockstore.db/002855.log:
          input/output error"

         Chain RPC temporarily stops responding to connections

00:06:26 - DAPI attempts to query chain status
         ERROR: [training-task-assigner] Failed to query chain status
         err="post failed: Post \"http://localhost:26657\": EOF"

         Function logs error but CONTINUES EXECUTION (BUG!)

00:06:26 - Nil pointer dereference
         panic: runtime error: invalid memory address or nil pointer dereference
         [signal SIGSEGV: segmentation violation code=0x1 addr=0x0 pc=0x3edaae2]
```

Fix:
```go
func (a *Assigner) tryClaimingTaskToAssign() {
	chainStatus, err := a.tendermintClient.Status()
	if err != nil {
		slog.Error(logTag+"Failed to query chain status", "err", err)
		return  // <===============================  This is the fix =============================== 
	}
```

---

## 💬 Комментарии (2)

### Комментарий 1 — [@AlexeySamosadov](https://github.com/AlexeySamosadov)

*2026-01-24 21:05 UTC*

Fixed in PR #639 - added missing return statement after error to prevent nil pointer dereference.

### Комментарий 2 — [@mtvnastya](https://github.com/mtvnastya)

*2026-02-10 03:59 UTC*

hi @mfursov, I'd like to propose a bounty for reporting this issue and proposing a fix.
reached out to you via email
