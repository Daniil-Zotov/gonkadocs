---
title: "#908 — bls: BlsManager stores context.Background() — DKG gRPC calls have no cancellation or timeout"
source: https://github.com/gonka-ai/gonka/issues/908
issue_number: 908
synced_at: 2026-08-07T09:19:48Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    bls: BlsManager stores context.Background() — DKG gRPC calls have no cancellation or timeout
    <span class="issues-number">#908</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/Mayveskii">@Mayveskii</a> opened 2026-03-17 23:21 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-04-28 18:11 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
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
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/x0152">@x0152</a></span>
    <span class="issues-meta-item">commented 2026-04-28 18:11 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>for the same reason as #909</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #908](https://github.com/gonka-ai/gonka/issues/908) every hour.
