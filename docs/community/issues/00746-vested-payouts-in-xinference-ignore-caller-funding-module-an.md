---
title: "#746 — Vested payouts in x/inference ignore caller funding module and always debit inference account"
source: https://github.com/gonka-ai/gonka/issues/746
issue_number: 746
synced_at: 2026-07-06T09:51:54Z
template: issues-main.html
---

> 🔄 **Авто-синхронизация:** из [Issue #746](https://github.com/gonka-ai/gonka/issues/746) каждые 6 часов. 

# 🔴 Vested payouts in x/inference ignore caller funding module and always debit inference account

**Автор:** [@Schwartz10](https://github.com/Schwartz10) · **Состояние:** Closed · **Создано:** 2026-02-13 06:15 UTC · **Обновлено:** 2026-06-04 21:44 UTC

---

## 📝 Описание

## Summary
`PayParticipantFromModule` in `x/inference` hardcodes `types.ModuleName` (`inference`) when calling `streamvesting.AddVestedRewards`, instead of forwarding the caller-provided `moduleName`.

## Affected code
- `inference-chain/x/inference/keeper/payment_handler.go`

## Expected behavior
When vesting is enabled, payouts should debit the same funding module passed to `PayParticipantFromModule`.

## Actual behavior
The vested path always debits `inference`.

## Impact
- Top miner vested payouts (`top_reward`) can debit the wrong module account.
- Can cause false insufficient-funds errors in `inference`.
- Can skew module-account accounting.

## Repro
Call:
`PayParticipantFromModule(..., moduleName=types.TopRewardPoolAccName, vestingPeriods>0)`
and assert `AddVestedRewards(..., types.TopRewardPoolAccName, ...)`.
Before fix it receives `types.ModuleName` instead.

## Fix
In vested path:
`AddVestedRewards(..., moduleName, ...)`
instead of:
`AddVestedRewards(..., types.ModuleName, ...)`.

---

## 💬 Комментарии (2)

### Комментарий 1 — [@AlexeySamosadov](https://github.com/AlexeySamosadov)

*2026-02-17 21:52 UTC*

PR with fix: #770 — forwards the caller-provided module name in vested payouts instead of hardcoding "inference".

### Комментарий 2 — [@tcharchian](https://github.com/tcharchian)

*2026-02-19 00:32 UTC*

@Schwartz10, have you noticed that the top reward module is not used?
