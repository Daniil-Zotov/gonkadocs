---
title: "#1909 — Devshard work-coin payouts bypass WorkVestingPeriod on late-settle and unsettled-prune paths (diverges from tokenomics.md)"
source: https://github.com/gonka-ai/gonka/issues/1909
issue_number: 1909
synced_at: 2026-10-07T08:49:38Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Devshard work-coin payouts bypass WorkVestingPeriod on late-settle and unsettled-prune paths (diverges from tokenomics.md)
    <span class="issues-number">#1909</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/kaileido">@kaileido</a> opened 2026-10-03 00:14 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-10-06 22:05 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

`docs/tokenomics.md` states that all newly distributed rewards — including Work Coins (fees from user requests) — are routed through the vesting system. For devshard host income this holds only on the on-time settlement path. The late-settlement and unsettled-prune payout paths send the coins as a liquid bank transfer, bypassing `WorkVestingPeriod`.

## Documented policy

`docs/tokenomics.md` (Vesting Mechanism): "All newly distributed rewards are routed through a dedicated vesting system" — "Work Coins: Fees from user requests, subject to configurable vesting periods".

## Code (origin/main)

Vesting is applied only when a positive period is passed to `PayParticipantFromModule` (`inference-chain/x/inference/keeper/payment_handler.go:65` → `AddVestedRewards`); a bare `SendCoinsFromModuleToAccount` is liquid (`payment_handler.go:91`).

- **Vested — on-time settle:** a current-epoch devshard settlement credits `CoinBalance` (`msg_server_settle_devshard_escrow.go:161`), later claimed via `ClaimRewards` → `PayParticipantFromEscrow(..., workVestingPeriod)` (`msg_server_claim_rewards.go:90`). Vests over `WorkVestingPeriod`.
- **Liquid — late settle:** a previous-epoch settlement takes the `else` branch → `payCoinsDirectly` (`msg_server_settle_devshard_escrow.go:170`) → `SendCoinsFromModuleToAccount` (`msg_server_settle_devshard_escrow.go:266`). No vesting period is passed.
- **Liquid — unsettled prune:** `distributeUnsettledEscrow` on prune (`pruning.go:262` → `devshard_pruning.go:50`) → `SendCoinsFromModuleToAccount`. No vesting.

`WorkVestingPeriod` is 180 epochs on the live network. No principal is lost; the effect is that devshard work income escapes the lockup on these two paths, and settlement timing is chosen by the escrow creator (a late settlement, one epoch after the work, hits the liquid path on every settle).

## Suggested resolution

Either route `payCoinsDirectly` and `distributeUnsettledEscrow` through `PayParticipantFromModule(..., &params.TokenomicsParams.WorkVestingPeriod)` so all devshard work income vests consistently, or update `docs/tokenomics.md` to state that late/unsettled devshard payouts are intentionally liquid.

</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/danielhubersstorm">@danielhubersstorm</a></span>
    <span class="issues-meta-item">commented 2026-10-06 22:05 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Starting work, ETA 3 to 5 days.</p>
<p>I will route the late-settle and unsettled-prune devshard payouts through PayParticipantFromModule with WorkVestingPeriod, so they match the on-time path and docs/tokenomics.md. I will not change the documented policy to "intentionally liquid" unless a maintainer says that is the intended behavior.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1909](https://github.com/gonka-ai/gonka/issues/1909) every hour.
