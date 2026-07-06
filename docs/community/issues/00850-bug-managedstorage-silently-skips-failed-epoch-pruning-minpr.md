---
title: "#850 — Bug: ManagedStorage silently skips failed epoch pruning — minPruned advanced before goroutines complete"
source: https://github.com/gonka-ai/gonka/issues/850
issue_number: 850
synced_at: 2026-07-06T09:52:46Z
template: issues-main.html
---

> 🔄 **Авто-синхронизация:** из [Issue #850](https://github.com/gonka-ai/gonka/issues/850) каждые 6 часов. 

# 🟢 Bug: ManagedStorage silently skips failed epoch pruning — minPruned advanced before goroutines complete

**Автор:** [@Mayveskii](https://github.com/Mayveskii) · **Состояние:** Open · **Создано:** 2026-03-03 12:04 UTC · **Обновлено:** 2026-03-03 12:04 UTC

---

## 📝 Описание

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

