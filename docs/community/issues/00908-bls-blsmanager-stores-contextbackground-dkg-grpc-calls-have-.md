---
title: "#908 — bls: BlsManager stores context.Background() — DKG gRPC calls have no cancellation or timeout"
source: https://github.com/gonka-ai/gonka/issues/908
issue_number: 908
synced_at: 2026-07-06T09:52:11Z
---

> 🔄 **Авто-синхронизация:** из [Issue #908](https://github.com/gonka-ai/gonka/issues/908) каждые 6 часов. 

# 🔴 bls: BlsManager stores context.Background() — DKG gRPC calls have no cancellation or timeout

**Автор:** [@Mayveskii](https://github.com/Mayveskii) · **Состояние:** Closed · **Создано:** 2026-03-17 23:21 UTC · **Обновлено:** 2026-04-28 18:11 UTC

---

## 📝 Описание

## Summary

`NewBlsManager` stores `context.Background()` as a struct field `bm.ctx`. This means two gRPC calls in the DKG dealer path run without any timeout and cannot be cancelled on node shutdown.

## Affected Code

**`decentralized-api/internal/bls/manager.go:133`**
```go
func NewBlsManager(recorder cosmosclient.InferenceCosmosClient) *BlsManager {
    return &BlsManager{
        ctx: context.Background(), // Use background context for chain queries
        ...
    }
}
```

**`decentralized-api/internal/bls/dealer.go:392,404`** — no timeout wrapper:
```go
// No WithTimeout — hangs indefinitely if chain RPC is slow/unavailable
grantees, err := queryClient.GranteesByMessageType(bm.ctx, ...)
participant, err := queryClient.InferenceParticipant(bm.ctx, ...)
```

Contrast with `manager.go:165` which correctly adds a 60s timeout:
```go
ctx, cancel := context.WithTimeout(bm.ctx, 60*time.Second)
defer cancel()
```

## Impact

1. **DKG epoch block**: If the chain RPC node is slow or unreachable during `EventKeyGenerationInitiated`, the worker goroutine inside `event_listener` blocks indefinitely on `GranteesByMessageType` or `InferenceParticipant`. This causes the node to miss the entire DKG window and drop out of consensus for that epoch.

2. **No graceful shutdown**: On SIGINT, `main.go` cancels the root `ctx` via `defer cancel()`, which propagates to `listener.Start(ctx)`. However `bm.ctx = context.Background()` is independent — in-flight BLS gRPC calls are never interrupted, delaying process exit.

3. **No Stop/Close on BlsManager**: There is no shutdown method to cancel pending operations.

## Root Cause

The context is stored at construction time as `Background()` instead of being passed from the caller. `main.go` already has a properly-scoped `ctx` with cancel:

```go
// main.go:145
ctx, cancel := context.WithCancel(context.Background())
defer cancel()
// ...
blsManager := bls.NewBlsManager(*recorder)  // ctx NOT passed
listener := event_listener.NewEventListener(..., cancel, blsManager)
```

## Fix

```go
// manager.go
func NewBlsManager(ctx context.Context, recorder cosmosclient.InferenceCosmosClient) *BlsManager {
    return &BlsManager{
        ctx: ctx,  // propagate caller context
        ...
    }
}

// main.go
blsManager := bls.NewBlsManager(ctx, *recorder)
```

This ensures:
- `GranteesByMessageType` and `InferenceParticipant` respect the node lifecycle context
- On SIGINT, pending BLS queries are cancelled immediately
- Future callers can add per-call timeouts via `context.WithTimeout(bm.ctx, ...)`

## Verified

Statically verified via AST analysis of commit history (904 commits). No existing fix found in HEAD. The `dealer.go` calls at lines 392 and 404 have no timeout wrapper, unlike the correctly-handled call in `manager.go:165`.

**Severity**: Medium-High — affects node availability during DKG under degraded RPC conditions.

---

## 💬 Комментарии (1)

### Комментарий 1 — [@x0152](https://github.com/x0152)

*2026-04-28 18:11 UTC*

for the same reason as #909
