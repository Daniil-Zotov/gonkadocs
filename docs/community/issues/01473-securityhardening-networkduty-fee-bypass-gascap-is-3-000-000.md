---
title: "#1473 — Security/hardening: NetworkDuty fee bypass GasCap is 3_000_000_000 — free block-space DoS risk"
source: https://github.com/gonka-ai/gonka/issues/1473
issue_number: 1473
synced_at: 2026-08-09T15:51:27Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Security/hardening: NetworkDuty fee bypass GasCap is 3_000_000_000 — free block-space DoS risk
    <span class="issues-number">#1473</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/Aphelios01-sdk">@Aphelios01-sdk</a> opened 2026-07-18 03:05 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-07-18 03:08 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

`NetworkDutyFeeBypassDecorator` allows zero-fee transactions when all messages are “network duty” types, with `GasCap: 3_000_000_000`. That is far above documented ~100M batch sizes and enables large free block-space consumption.

Exempt types include PoC validation V2, Start/Finish inference, MsgValidation, invalidate/revalidate, and several BLS DKG messages (`inference-chain/app/ante_fee.go`).

## Paths

- `inference-chain/app/ante.go` — `GasCap: 3_000_000_000`
- `inference-chain/app/ante_fee.go` — `isExemptMessageType`

## Impact

Medium: mempool/block spam without paying min gas price by accounts that can sign duty messages (hosts / warm authz keys).

## Suggested remediation

1. Lower GasCap to a tight multiple of real DAPI batch limits
2. Per-account rate limits on fee-exempt txs
3. Revisit which messages truly need zero fees
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Aphelios01-sdk">@Aphelios01-sdk</a></span>
    <span class="issues-meta-item">commented 2026-07-18 03:08 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Closing to focus disclosure on the highest-priority finding: https://github.com/gonka-ai/gonka/issues/1470 (SSRF via InferenceUrl). Other items can be re-opened or filed via HackerOne if needed.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1473](https://github.com/gonka-ai/gonka/issues/1473) every hour.
