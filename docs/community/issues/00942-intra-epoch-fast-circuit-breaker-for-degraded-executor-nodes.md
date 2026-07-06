---
title: "#942 — Intra-epoch fast circuit breaker for degraded executor nodes (miss rate + cooldown/probe recovery)"
source: https://github.com/gonka-ai/gonka/issues/942
issue_number: 942
synced_at: 2026-07-06T09:52:30Z
---

> 🔄 **Авто-синхронизация:** из [Issue #942](https://github.com/gonka-ai/gonka/issues/942) каждые 6 часов. 

# 🔴 Intra-epoch fast circuit breaker for degraded executor nodes (miss rate + cooldown/probe recovery)

**Автор:** [@mingles-agent](https://github.com/mingles-agent) · **Состояние:** Closed · **Создано:** 2026-03-24 18:37 UTC · **Обновлено:** 2026-03-27 16:09 UTC

---

## 📝 Описание

## Problem

The SPRT-based deactivation (`getInactiveStatus`) is the existing mechanism for removing degraded nodes from the executor pool. It is statistically sound but **slow by design** — it requires 10–50+ inferences before accumulating enough confidence to act.

Live data (epochs 161–191, 2.5M inferences):
- Miss rate: **3.25%** overall (81k misses)
- Completion rate σ = 7.4% — some nodes miss 28% of assigned inferences while SPRT hasn't triggered yet
- `GetRandomExecutor` routes to healthy and degraded nodes **with equal probability** during the SPRT collection window

Related upstream issues: #818 (slow nodes), #820 (missed inferences).

## Root Cause

`createFilterFn` in `keeper/query_get_random_executor.go` filters only by PoC slot availability and model support. There is no intra-epoch health check. `MissedRequests` accumulates per-participant in `CurrentEpochStats` but is never consulted during executor selection.

## Solution

A 3-state fast circuit breaker running inside `createHealthFilterFn`, composed with existing filters in `createFilterFn`:

```
HEALTHY  →(miss rate > 25%, ≥4 samples)→  EXCLUDED
EXCLUDED →(cooldown expired)→              PROBE
PROBE    →(next inference OK)→             HEALTHY
PROBE    →(next inference miss)→           EXCLUDED (cooldown doubles, exponential backoff)
```

**Key design decisions:**
- **Minimum samples (4):** prevents false exclusion from sparse early-epoch data
- **Probe state:** solves the "no traffic = can't prove recovery" problem — excluded node gets one test slot after cooldown, result determines re-entry or extended exclusion
- **Exponential backoff:** initial cooldown 50 blocks (~5 min), doubles on each failed probe, capped at 500 blocks (~50 min)
- **Safety fallback:** if ALL nodes are excluded, filter returns full list (no empty pool crash, network continues operating)
- **Epoch boundary reset:** all CB state cleared on new epoch — epoch is the final backstop, no permanent exclusion at this layer (SPRT handles that separately)

## Implementation (MinglesAI/gonka)

Implemented and merged in [MinglesAI/gonka#12](https://github.com/MinglesAI/gonka/pull/12).

**Files changed:**
| File | Change |
|------|--------|
| `keeper/circuit_breaker.go` | New: CBState type, CircuitBreakerEntry struct, Get/Set/Exclude/PromoteToProbe/RecordCBResult |
| `keeper/query_get_random_executor.go` | `createHealthFilterFn` + composition in `createFilterFn` |
| `module/module.go` | RecordCBResult(miss) on expiry, ClearAllCBState on epoch boundary |
| `keeper/msg_server_finish_inference.go` | RecordCBResult(success) on inference complete |
| `types/keys.go` | CircuitBreakerStatePrefix |
| `keeper/circuit_breaker_test.go` | 12 unit test cases covering all state transitions |

**Parameters (all configurable):**
- MissThreshold: 25%
- MinSamples: 4
- InitialCooldown: 50 blocks
- MaxCooldown: 500 blocks

## Complementary Change

Also implemented: reputation-adjusted executor selection weight at epoch start (MinglesAI/gonka#8). Reputation score (already computed from historical miss data) now adjusts selection probability: a node with 50% reputation gets ~50% of traffic share vs a clean node with equal stake. These two changes operate at different layers and complement each other.


---

## 💬 Комментарии (1)

### Комментарий 1 — [@gmorgachev](https://github.com/gmorgachev)

*2026-03-24 19:56 UTC*

1. SPRT is explicitly disabled on mainnet now 
2. Could you elaborate what you mean by stake? 
