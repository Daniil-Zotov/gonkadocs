---
title: "#979 — `devshards` escrow: fund loss on unsettled pruning + missing overflow guards in host stats aggregation"
source: https://github.com/gonka-ai/gonka/issues/979
issue_number: 979
synced_at: 2026-07-16T18:36:07Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    `devshards` escrow: fund loss on unsettled pruning + missing overflow guards in host stats aggregation
    <span class="issues-number">#979</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item">[@unameisfine](https://github.com/unameisfine) opened 2026-03-30 17:05 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-04-29 21:27 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

Three related bugs in subnet escrow settlement and pruning code (v0.2.11):

### 1. Fund loss in unsettled escrow pruning (Medium)

`distributeUnsettledEscrow` (subnet_pruning.go) silently logs `SendCoinsFromModuleToAccount` failures but returns nil. The subnet Remover in `pruning.go` then deletes the escrow from state. Validators whose payments failed permanently lose their share — the funds remain locked in the inference module account with no way to recover.

**Remover also swallows errors**: Even if escrow or index deletion fails, the Remover returns nil (line 149), potentially leaving orphaned state entries while advancing the pruning cursor past them.

**Root cause**: Error-handling pattern treats pruning cleanup as "best-effort" but deletes the source-of-truth (escrow) regardless of outcome.

**Impact**: Permanent fund loss for validators in any unsettled escrow where at least one `SendCoins` call fails during pruning.

### 2. Inconsistent overflow protection in `AggregateSubnetHostStats` (Low-Medium)

`subnet_host_stats.go` — `Cost` (uint64) has an overflow check before addition, but `Missed`, `Invalid`, `RequiredValidations`, and `CompletedValidations` (all uint32) do not. The developer clearly intended overflow protection (present for Cost) but missed the other four fields.

### 3. Missing overflow check in `SettleSubnetEscrow` validator cost aggregation (Low)

`msg_server_settle_subnet_escrow.go:37` — `validatorCosts[addr] += hs.Cost` accumulates costs for validators with multiple slots without overflow protection. Same pattern that `AggregateSubnetHostStats` correctly guards for Cost.

## Affected files

- `inference-chain/x/inference/keeper/subnet_pruning.go` (distributeUnsettledEscrow)
- `inference-chain/x/inference/keeper/pruning.go` (GetSubnetPruner Remover)
- `inference-chain/x/inference/keeper/subnet_host_stats.go` (AggregateSubnetHostStats)
- `inference-chain/x/inference/keeper/msg_server_settle_subnet_escrow.go` (SettleSubnetEscrow)
</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@unameisfine](https://github.com/unameisfine)</span>
    <span class="issues-meta-item">commented 2026-04-27 22:46 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Closing — covered by PRs #1013, #1014, #1015.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@tcharchian](https://github.com/tcharchian)</span>
    <span class="issues-meta-item">commented 2026-04-29 21:27 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@akup please take a look</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #979](https://github.com/gonka-ai/gonka/issues/979) every hour.
