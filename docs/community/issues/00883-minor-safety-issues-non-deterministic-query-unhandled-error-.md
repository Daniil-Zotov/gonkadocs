---
title: "#883 — Minor safety issues: non-deterministic query, unhandled error continuation, uint64 overflow"
source: https://github.com/gonka-ai/gonka/issues/883
issue_number: 883
synced_at: 2026-07-17T22:09:31Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Minor safety issues: non-deterministic query, unhandled error continuation, uint64 overflow
    <span class="issues-number">#883</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/unameisfine">@unameisfine</a> opened 2026-03-13 17:49 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-04-27 22:46 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
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
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/unameisfine">@unameisfine</a></span>
    <span class="issues-meta-item">commented 2026-04-27 22:46 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Closing — PR #884 was closed as part of refocusing on larger scoped contributions.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #883](https://github.com/gonka-ai/gonka/issues/883) every hour.
