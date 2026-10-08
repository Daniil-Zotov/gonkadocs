---
title: "#1943 — v0.2.17: Mark `/admin/v1/setup/report` failed when this node cannot pay one epoch of fees"
source: https://github.com/gonka-ai/gonka/issues/1943
issue_number: 1943
synced_at: 2026-10-08T22:11:09Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    v0.2.17: Mark `/admin/v1/setup/report` failed when this node cannot pay one epoch of fees
    <span class="issues-number">#1943</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-10-07 21:55 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-10-07 22:18 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #4cbc0f; color: #24292f; border-color: #4cbc0f;">up-for-grabs</span></div>
</div>

<div class="issues-content" markdown="1">
`checkFeegrant` passes when the cold-to-warm feegrant exists and is not expired. It does not read the cold spendable balance.
The HTTP handler stays 200. Failure is the `feegrant_allowance` check status `FAIL`, which sets `overall_status` to `FAIL`. A query error stays `UNAVAILABLE`, as it does today.

Usable amount comes from `FeePayerSpendable`: cold spendable `ngonka`, capped by the remaining allowance when the warm key is a different account. An empty `spend_limit` is unlimited, so use cold spendable alone. Vesting and the warm-key balance do not count. A valid allowance with 0 cold spendable must fail.

Use `epochFeeBudgetNgonka` and `epochBudgetKnown` for the one-epoch budget. Fees are on when `epochPrice` is above 0. That is the epoch group price, not `min_gas_price_ngonka`.

Fail when fees are on and usable is 0, or when the budget is known and usable is below it. If the warm key is a different account, a missing or expired feegrant still fails. If the signer is the cold account, do not require a feegrant; `FeePayerSpendable` uses the cold spendable balance alone.

Resolve the StoreCommit count the same way as `GET /admin/v1/epoch-fee-budget`. If that count is unknown, pass it as unknown. A count of 0 with a positive per-count rate makes the budget look known and too small. If the budget is unknown and usable is above 0, do not fail: `spendable_covers_budget` is false in that case even when the cold account has funds.
</div>

---

> 🔄 **Auto-synced** from [Issue #1943](https://github.com/gonka-ai/gonka/issues/1943) every hour.
