---
title: "#422 — DAPI  nil pointer dereference crash when chain RPC is unavailable"
source: https://github.com/gonka-ai/gonka/issues/422
issue_number: 422
synced_at: 2026-07-09T08:55:23Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    DAPI  nil pointer dereference crash when chain RPC is unavailable
    <span class="issues-number">#422</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item">[@mfursov](https://github.com/mfursov) opened 2025-11-10 02:37 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-02-10 03:59 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
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
</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@AlexeySamosadov](https://github.com/AlexeySamosadov)</span>
    <span class="issues-meta-item">commented 2026-01-24 21:05 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Fixed in PR #639 - added missing return statement after error to prevent nil pointer dereference.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@mtvnastya](https://github.com/mtvnastya)</span>
    <span class="issues-meta-item">commented 2026-02-10 03:59 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>hi @mfursov, I'd like to propose a bounty for reporting this issue and proposing a fix.
reached out to you via email</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #422](https://github.com/gonka-ai/gonka/issues/422) every hour.
