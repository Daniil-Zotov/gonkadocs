---
title: "#885 — Non-deterministic queries, unhandled settlement errors, epoch stats underflow"
source: https://github.com/gonka-ai/gonka/issues/885
issue_number: 885
synced_at: 2026-08-08T14:54:05Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Non-deterministic queries, unhandled settlement errors, epoch stats underflow
    <span class="issues-number">#885</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/unameisfine">@unameisfine</a> opened 2026-03-13 19:29 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-04-27 22:46 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

Found several bugs during code review of `x/inference/keeper/`:

### 1. Non-deterministic gRPC query responses (consensus risk)

Three query handlers iterate Go maps and return results directly without sorting:

- `GetParticipantsFullStats` — `maps.Values(participants)` returns unstable order
- `InferencesAndTokensStatsByModels` — iterates `map[string]StatsSummary`
- `DebugStatsDeveloperStats` — iterates `statByTime` and `statByEpoch` maps

Go map iteration order is randomized per-process. This means different nodes return the same data in different order, which can cause issues with deterministic replay and client-side caching.

### 2. uint64 underflow in `GetSummaryLastNEpochs` / `GetSummaryLastNEpochsByDeveloper`

```go
epochIdFrom := effectiveEpochIndex - uint64(n)
```

When `n > effectiveEpochIndex` (e.g. early chain with epoch=1, requesting last 5 epochs), this wraps to `MaxUint64`, creating an enormous iterator range. This is reproducible on any chain in its first few epochs.

### 3. Ignored errors in `SettleAccounts`

Four error return values are silently discarded in the settlement path:

- `GetBitcoinSettleAmounts` error logged but settlement continues with potentially uninitialized data
- `AddTokenomicsData` return value completely ignored
- `SetSettleAmountWithGovernanceTransfer` return value completely ignored
- `TransferOldSettleAmountsToGovernance` error logged but `nil` returned to caller

### 4. Missing error in log call

`shareWorkWithValidators` logs `"Unable to update participant"` but omits the actual error value, making debugging impossible.

## Files

- `x/inference/keeper/accountsettle.go`
- `x/inference/keeper/developer_stats_aggregation.go`
- `x/inference/keeper/msg_server_validation.go`
- `x/inference/keeper/query_developer_stats_aggregation.go`
- `x/inference/keeper/query_get_participant_current_stats.go`
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/unameisfine">@unameisfine</a></span>
    <span class="issues-meta-item">commented 2026-04-27 22:46 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Closing — PR #886 was closed as part of refocusing on larger scoped contributions.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #885](https://github.com/gonka-ai/gonka/issues/885) every hour.
