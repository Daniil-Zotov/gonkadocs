---
title: "#979 — `devshards` escrow: fund loss on unsettled pruning + missing overflow guards in host stats aggregation"
source: https://github.com/gonka-ai/gonka/issues/979
issue_number: 979
synced_at: 2026-07-06T09:52:07Z
---

> 🔄 **Авто-синхронизация:** из [Issue #979](https://github.com/gonka-ai/gonka/issues/979) каждые 6 часов. 

# 🔴 `devshards` escrow: fund loss on unsettled pruning + missing overflow guards in host stats aggregation

**Автор:** [@unameisfine](https://github.com/unameisfine) · **Состояние:** Closed · **Создано:** 2026-03-30 17:05 UTC · **Обновлено:** 2026-04-29 21:27 UTC

---

## 📝 Описание

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

---

## 💬 Комментарии (2)

### Комментарий 1 — [@unameisfine](https://github.com/unameisfine)

*2026-04-27 22:46 UTC*

Closing — covered by PRs #1013, #1014, #1015.

### Комментарий 2 — [@tcharchian](https://github.com/tcharchian)

*2026-04-29 21:27 UTC*

@akup please take a look
