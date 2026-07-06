---
title: "#885 — Non-deterministic queries, unhandled settlement errors, epoch stats underflow"
source: https://github.com/gonka-ai/gonka/issues/885
issue_number: 885
synced_at: 2026-07-06T09:52:12Z
template: issues-main.html
---

> 🔄 **Auto-synced:** from [Issue #885](https://github.com/gonka-ai/gonka/issues/885) every 6 hours. 

# 🔴 Non-deterministic queries, unhandled settlement errors, epoch stats underflow

**Author:** [@unameisfine](https://github.com/unameisfine) · **State:** Closed · **Created:** 2026-03-13 19:29 UTC · **Updated:** 2026-04-27 22:46 UTC

---

## 📝 Описание

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

---

## 💬 Comments (1)

### Комментарий 1 — [@unameisfine](https://github.com/unameisfine)

*2026-04-27 22:46 UTC*

Closing — PR #886 was closed as part of refocusing on larger scoped contributions.
