---
title: "#883 — Minor safety issues: non-deterministic query, unhandled error continuation, uint64 overflow"
source: https://github.com/gonka-ai/gonka/issues/883
issue_number: 883
synced_at: 2026-07-06T09:52:12Z
---

> 🔄 **Авто-синхронизация:** из [Issue #883](https://github.com/gonka-ai/gonka/issues/883) каждые 6 часов. 

# 🔴 Minor safety issues: non-deterministic query, unhandled error continuation, uint64 overflow

**Автор:** [@unameisfine](https://github.com/unameisfine) · **Состояние:** Closed · **Создано:** 2026-03-13 17:49 UTC · **Обновлено:** 2026-04-27 22:46 UTC

---

## 📝 Описание

## Description

Found three minor safety issues during code review:

### 1. Non-deterministic `GetAllModelPerTokenPrices` response

**File:** `inference-chain/x/inference/keeper/query_dynamic_pricing.go:52-58`

`GetAllModelPerTokenPrices()` iterates over `map[string]uint64` and appends to a slice. Since Go map iteration order is non-deterministic, different nodes return models in different order for the same gRPC query.

While this doesn't affect consensus (query-only), deterministic API responses are generally expected in blockchain systems and make debugging/testing easier.

### 2. `SubmitPocValidation` continues after `GetActiveConfirmationPoCEvent` error

**File:** `inference-chain/x/inference/keeper/msg_server_poc_validation_v1.go:41-45`

When `GetActiveConfirmationPoCEvent()` returns an error, it's logged but execution continues without resetting `activeEvent` and `isActive`. Per Go convention, return values are not guaranteed to be meaningful when `err != nil`. If the function returns partially initialized values on error, the subsequent routing logic could behave unexpectedly.

### 3. Silent uint64 overflow in `GetTotalCoins`

**File:** `inference-chain/x/inference/types/settle_amount.go:5-11`

`GetTotalCoins()` adds `RewardCoins + WorkCoins` (both `uint64`) without checking for addition overflow. If the sum wraps around, it produces a small value that passes the `sum > math.MaxInt64` check, returning an incorrect (silently corrupted) result.

While overflow is unlikely with the current token supply, the silent corruption makes this a correctness issue worth fixing.

## Proposed Fix

See PR linked below with fixes for all three issues.

---

## 💬 Комментарии (1)

### Комментарий 1 — [@unameisfine](https://github.com/unameisfine)

*2026-04-27 22:46 UTC*

Closing — PR #884 was closed as part of refocusing on larger scoped contributions.
