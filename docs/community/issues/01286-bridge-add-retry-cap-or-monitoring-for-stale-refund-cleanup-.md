---
title: "#1286 — Bridge: add retry cap or monitoring for stale refund cleanup retries"
source: https://github.com/gonka-ai/gonka/issues/1286
issue_number: 1286
synced_at: 2026-07-06T09:51:40Z
---

> 🔄 **Авто-синхронизация:** из [Issue #1286](https://github.com/gonka-ai/gonka/issues/1286) каждые 6 часов. 

# 🟢 Bridge: add retry cap or monitoring for stale refund cleanup retries

**Автор:** [@Ryanchen911](https://github.com/Ryanchen911) · **Состояние:** Open · **Создано:** 2026-06-01 02:34 UTC · **Обновлено:** 2026-07-01 21:37 UTC

**Веха:** v0.2.15

---

## 📝 Описание

## Summary

When a threshold signing request reaches COMPLETED, the inference BLS hook calls `CleanupBridgePendingRefundByBlsRequestID` to remove pending bridge refund state.

If this cleanup persistently fails, the request is re-queued under `CompletedPostProcessRetryPrefix`, but `ProcessCompletedPostProcessRetries` currently has no maximum retry cap.

## Impact

This does not appear to create a direct safety issue:

- `cancelThresholdSigningRequest` rejects cancellation once the BLS request is COMPLETED.
- Therefore a stale pending refund entry should not allow double-spend.

However, persistent cleanup failures can cause:

- stale refund entries remaining in state indefinitely
- retry queue growth
- noisy monitoring / operational confusion

## Suggested fix

Either:

1. add a maximum retry count for completed post-process retries, or
2. add monitoring / alerting for retry queue depth and old retry entries.

## Relevant code

- `inference-chain/x/inference/module/bls_hooks.go`
  - `AfterThresholdSigningCompleted`
- `inference-chain/x/inference/keeper/bridge_pending_refund.go`
  - `CleanupBridgePendingRefundByBlsRequestID`
- `inference-chain/x/bls/keeper/threshold_signing.go`
  - `ProcessCompletedPostProcessRetries`

## Acceptance criteria

- Persistent cleanup failures cannot retry forever without visibility.
- Either a max retry cap exists, or an alert/metric exists for stale completed post-process retries.
- Existing double-spend protection remains unchanged.

---

## 💬 Комментарии (4)

### Комментарий 1 — [@tcharchian](https://github.com/tcharchian)

*2026-06-02 00:50 UTC*

@Ryanchen911, are you ready to write a fix?

### Комментарий 2 — [@Ryanchen911](https://github.com/Ryanchen911)

*2026-06-02 07:15 UTC*

sure, we will take it @bonujel

### Комментарий 3 — [@bonujel](https://github.com/bonujel)

*2026-06-02 08:27 UTC*

Picking this up — I'll add a maximum retry cap for completed post-process retries (with metrics/logging for stale entries) so persistent cleanup failures can't retry forever, while keeping the existing double-spend protection unchanged. PR to follow on the v0.2.14 line.

### Комментарий 4 — [@tcharchian](https://github.com/tcharchian)

*2026-06-02 17:46 UTC*

@GLiberman fyi
