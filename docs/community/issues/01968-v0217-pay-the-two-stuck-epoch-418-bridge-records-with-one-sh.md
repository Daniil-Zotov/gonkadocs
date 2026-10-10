---
title: "#1968 — v0.2.17: Pay the two stuck epoch-418 bridge records, with one shared active-weight check"
source: https://github.com/gonka-ai/gonka/issues/1968
issue_number: 1968
synced_at: 2026-10-10T07:15:31Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    v0.2.17: Pay the two stuck epoch-418 bridge records, with one shared active-weight check
    <span class="issues-number">#1968</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-10-10 00:05 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-10-10 00:07 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Two inbound bridge records from epoch 418 are `BRIDGE_PENDING` and can no longer reach a majority.

Seven participants were excluded with `failed_confirmation_poc` at heights 6451720 and 6457153. Group 1661 was left with 419,861 of x/group weight. Completion still required `GroupData.TotalWeight / 2 + 1` = 420,664 (`epoch_group_data/418` `total_weight` 841,326). The records are ETH `26149258:181` (4,000 GNK) and `26149505:257` (1,000 GNK). Both already hold 357,479. The four members that have not voted can only bring them to 419,861. Inbound records have no expiry and no refund.

#1958 by @cyberdelamain is the protocol fix for 0.2.17. `ValidateBridgeExchange` counts a majority of the x/group members still in the group, capped at `GroupData.TotalWeight`. A vote from a member removed after voting no longer counts. Required power never drops below `GroupData.TotalWeight / 3 + 1`. On epoch 418 that floor is 280,443, and both records are already above it.

These two records are the only stuck ones on chain. #1958 does not complete them: dapi does not return to Ethereum blocks it has already processed, so no further vote will arrive. Complete and pay them in the v0.2.17 upgrade handler by re-checking pending inbound records against the new rule.

Additional protection uses that same check and the same recount of weight still active, in every place that takes a threshold from epoch weight. One mechanism, the one in #1958. Align the call sites with @cyberdelamain before adding another.

Since v0.2.16, BLS is measured in trusted weight (`CapWeight`, previous-epoch confirmed weight). Slot assignment and any BLS threshold in this protection stay on trusted weight.
</div>

---

> 🔄 **Auto-synced** from [Issue #1968](https://github.com/gonka-ai/gonka/issues/1968) every hour.
