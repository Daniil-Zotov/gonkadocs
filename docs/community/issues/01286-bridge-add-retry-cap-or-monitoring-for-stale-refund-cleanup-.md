---
title: "#1286 — Bridge: add retry cap or monitoring for stale refund cleanup retries"
source: https://github.com/gonka-ai/gonka/issues/1286
issue_number: 1286
synced_at: 2026-07-15T15:03:43Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Bridge: add retry cap or monitoring for stale refund cleanup retries
    <span class="issues-number">#1286</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item">[@Ryanchen911](https://github.com/Ryanchen911) opened 2026-06-01 02:34 UTC</span>
    <span class="issues-meta-item">4 comments</span>
    <span class="issues-meta-item">Updated 2026-07-01 21:37 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
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
</div>

---

## 💬 Comments (4)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@tcharchian](https://github.com/tcharchian)</span>
    <span class="issues-meta-item">commented 2026-06-02 00:50 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@Ryanchen911, are you ready to write a fix?</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@Ryanchen911](https://github.com/Ryanchen911)</span>
    <span class="issues-meta-item">commented 2026-06-02 07:15 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>sure, we will take it @bonujel</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@bonujel](https://github.com/bonujel)</span>
    <span class="issues-meta-item">commented 2026-06-02 08:27 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Picking this up — I'll add a maximum retry cap for completed post-process retries (with metrics/logging for stale entries) so persistent cleanup failures can't retry forever, while keeping the existing double-spend protection unchanged. PR to follow on the v0.2.14 line.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@tcharchian](https://github.com/tcharchian)</span>
    <span class="issues-meta-item">commented 2026-06-02 17:46 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@GLiberman fyi</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1286](https://github.com/gonka-ai/gonka/issues/1286) every hour.
