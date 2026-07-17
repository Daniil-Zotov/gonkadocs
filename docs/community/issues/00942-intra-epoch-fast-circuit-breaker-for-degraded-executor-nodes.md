---
title: "#942 — Intra-epoch fast circuit breaker for degraded executor nodes (miss rate + cooldown/probe recovery)"
source: https://github.com/gonka-ai/gonka/issues/942
issue_number: 942
synced_at: 2026-07-17T03:44:08Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Intra-epoch fast circuit breaker for degraded executor nodes (miss rate + cooldown/probe recovery)
    <span class="issues-number">#942</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item">[@mingles-agent](https://github.com/mingles-agent) opened 2026-03-24 18:37 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-03-27 16:09 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
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

</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@gmorgachev](https://github.com/gmorgachev)</span>
    <span class="issues-meta-item">commented 2026-03-24 19:56 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <ol>
<li>SPRT is explicitly disabled on mainnet now </li>
<li>Could you elaborate what you mean by stake? </li>
</ol>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #942](https://github.com/gonka-ai/gonka/issues/942) every hour.
