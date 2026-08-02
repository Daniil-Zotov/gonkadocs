---
title: "#746 — Vested payouts in x/inference ignore caller funding module and always debit inference account"
source: https://github.com/gonka-ai/gonka/issues/746
issue_number: 746
synced_at: 2026-08-02T10:55:43Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Vested payouts in x/inference ignore caller funding module and always debit inference account
    <span class="issues-number">#746</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/Schwartz10">@Schwartz10</a> opened 2026-02-13 06:15 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-06-04 21:44 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
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
</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/AlexeySamosadov">@AlexeySamosadov</a></span>
    <span class="issues-meta-item">commented 2026-02-17 21:52 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>PR with fix: #770 — forwards the caller-provided module name in vested payouts instead of hardcoding "inference".</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-02-19 00:32 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@Schwartz10, have you noticed that the top reward module is not used?</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #746](https://github.com/gonka-ai/gonka/issues/746) every hour.
