---
title: "#850 — Bug: ManagedStorage silently skips failed epoch pruning — minPruned advanced before goroutines complete"
source: https://github.com/gonka-ai/gonka/issues/850
issue_number: 850
synced_at: 2026-08-07T17:11:56Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Bug: ManagedStorage silently skips failed epoch pruning — minPruned advanced before goroutines complete
    <span class="issues-number">#850</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/Mayveskii">@Mayveskii</a> opened 2026-03-03 12:04 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-07-28 20:35 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Location

`decentralized-api/payloadstorage/managed_storage.go` — lines 129–138

## Description

In `ManagedStorage.cleanup()`, `m.minPruned` is advanced to `threshold` **before** the pruning goroutines complete:

```go
for epoch := m.minPruned; epoch < threshold; epoch++ {
    go func(e uint64) {
        if err := m.storage.PruneEpoch(context.Background(), e); err != nil {
            logging.Warn("Auto-prune failed", types.PayloadStorage, "epochId", e, "error", err)
            // error only logged — epoch is silently skipped
        }
    }(epoch)
}
m.minPruned = threshold  // ← advanced immediately, goroutines still running
```

### What goes wrong

If any `PruneEpoch` goroutine fails (DB connection lost, file I/O error, PostgreSQL timeout), that epoch is **permanently skipped**:

- `m.minPruned` is already past it
- The `maxPruneLookback = 10` guard does not help — it only prevents jumping too far forward on first run, not recovering already-skipped epochs
- Next `cleanup()` tick starts from the new `m.minPruned` — the failed epoch is never retried

### Secondary issue

`cleanup()` holds `m.mu.Lock()` while spawning goroutines, but the goroutines themselves run **without the lock**. If goroutines from a previous 30-second tick are still running when the next tick fires, multiple goroutines can call `PruneEpoch` for the same epoch concurrently.

## Impact

**High** — off-chain payload data for failed epochs accumulates on disk indefinitely. Under sustained prune failures (e.g. intermittent DB connectivity), this leads to unbounded disk growth and eventual disk exhaustion on API nodes.

## Fix Direction

Only advance `m.minPruned` after confirming successful pruning. Simplest correct approach — run pruning synchronously within the lock:

```go
for epoch := m.minPruned; epoch < threshold; epoch++ {
    if err := m.storage.PruneEpoch(context.Background(), epoch); err != nil {
        logging.Warn("Auto-prune failed", types.PayloadStorage, "epochId", epoch, "error", err)
        break // stop advancing minPruned past the failed epoch
    }
    m.minPruned = epoch + 1
    logging.Info("Auto-pruned epoch", types.PayloadStorage, "epochId", epoch)
}
```

Alternatively, if async pruning is required for performance, track per-epoch completion via a channel or atomic and only advance `m.minPruned` for contiguously completed epochs.

</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/redstartechno">@redstartechno</a></span>
    <span class="issues-meta-item">commented 2026-07-28 20:35 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>A fix for this is pending in PR #1336 (it references this issue): failed epoch prunes are retried on subsequent cleanup ticks instead of being skipped, with a per-epoch single-flight guard so stuck prunes don't accumulate goroutines. Reviewed by @x0152 (approved pre-guard, re-review requested after addressing his blocker), rebased onto current main, CI green. Linking here so the issue reflects the pending fix.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #850](https://github.com/gonka-ai/gonka/issues/850) every hour.
