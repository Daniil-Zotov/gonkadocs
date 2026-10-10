---
title: "#1906 — Preserve settlement decision across restart for pending escrows"
source: https://github.com/gonka-ai/gonka/issues/1906
issue_number: 1906
synced_at: 2026-10-10T18:41:59Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Preserve settlement decision across restart for pending escrows
    <span class="issues-number">#1906</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/qdanik">@qdanik</a> opened 2026-10-02 18:44 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-10-02 20:09 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Problem

The current settlement flow works as expected while the process stays alive, but there is a fault-tolerance gap around restarts.

When an escrow is marked for settlement, only `SettlementPending` is persisted. We do not persist:

- why the settlement mark was created;
- whether settlement was enabled for that model at that moment;
- whether the settlement was triggered automatically or manually.

After a restart, reconciliation loads the current configuration and decides again whether the escrow should be settled.

This means the behavior before and after a restart can differ.

| Situation | Process stays up | After restart |
|---|---|---|
| Settlement is already marked, then model `M` is disabled | Drain still settles it because the flag is not checked again. | Reconcile reads the new flag, skips settlement, and keeps the pending mark. |
| Model `M` was disabled when the escrow was retired | Nothing is queued and no pending mark is created. | There is nothing to resume. Enabling `M` later does not settle that escrow. |
| A pending mark exists, then `M.settlement_enabled` is omitted or `M` is removed from `models` | An already queued settlement still runs. | Reconcile no longer sees the model override. If the global flag is enabled, it settles. |
| Manual `POST .../settle` returned `409` because requests were still in flight | Drain eventually settles it. | Reconcile treats it as an ordinary pending mark. If `M` is disabled, the manually requested settlement is never completed. |

## Expected behavior

Once a settlement decision has been made and persisted, restarting the process should not change that decision based on newer configuration.

Reconciliation should be able to distinguish between:

- an escrow that was explicitly marked for settlement;
- an escrow that should only be settled if the current configuration allows it.

Manual settlement requests should also survive a restart and eventually complete once the escrow becomes drainable.

## Possible approach

Persist enough context together with `SettlementPending` so reconciliation can resume the original settlement intent instead of recalculating it from the current model settings.

For example, the persisted state could include the settlement source/reason or the effective settlement decision at the time the mark was created.

Original posted by @a-kuprin https://github.com/gonka-ai/gonka/issues/1866#issuecomment-5921201295
</div>

---

> 🔄 **Auto-synced** from [Issue #1906](https://github.com/gonka-ai/gonka/issues/1906) every hour.
