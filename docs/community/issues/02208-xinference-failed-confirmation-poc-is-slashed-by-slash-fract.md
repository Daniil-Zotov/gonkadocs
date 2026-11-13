---
title: "#2208 — x/inference: failed confirmation PoC is slashed by slash_fraction_downtime; confirmation_poc_params.slash_fraction is never read"
source: https://github.com/gonka-ai/gonka/issues/2208
issue_number: 2208
synced_at: 2026-11-13T08:08:27Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    x/inference: failed confirmation PoC is slashed by slash_fraction_downtime; confirmation_poc_params.slash_fraction is never read
    <span class="issues-number">#2208</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/kaileido">@kaileido</a> opened 2026-11-03 14:03 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-11-03 14:03 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Problem

A participant that fails confirmation PoC is slashed by `collateral_params.slash_fraction_downtime`, not by `confirmation_poc_params.slash_fraction`. The confirmation PoC field has no reader in the chain code.

- `ComputeStatus` returns `INACTIVE` with reason `FailedConfirmationPoC` ([calculations/status.go:80-82](https://github.com/gonka-ai/gonka/blob/c5b9b9d373d536ead44e72b330818936b6db31ba/inference-chain/x/inference/calculations/status.go#L80-L82)).
- Every move into `INACTIVE` goes to `deactiveParticipant`, which calls `SlashForDowntime` whatever the reason ([keeper/participant_status.go:69-79](https://github.com/gonka-ai/gonka/blob/c5b9b9d373d536ead44e72b330818936b6db31ba/inference-chain/x/inference/keeper/participant_status.go#L69-L79)), and logs "deactivated for downtime".
- `SlashForDowntime` uses `CollateralParams.SlashFractionDowntime` ([keeper/collateral.go:197-210](https://github.com/gonka-ai/gonka/blob/c5b9b9d373d536ead44e72b330818936b6db31ba/inference-chain/x/inference/keeper/collateral.go#L197-L210)).
- `ConfirmationPocParams.SlashFraction` is set to 0 in the v0.2.5 upgrade ([app/upgrades/v0_2_5/upgrades.go:76](https://github.com/gonka-ai/gonka/blob/c5b9b9d373d536ead44e72b330818936b6db31ba/inference-chain/app/upgrades/v0_2_5/upgrades.go#L76)) and otherwise only appears in param validation.

Current mainnet params: `confirmation_poc_params.slash_fraction = 0`, `collateral_params.slash_fraction_downtime = 0.1`, `alpha_threshold = 0.5`. So a host whose confirmation PoC ratio drops below 0.5 loses 10% of its required collateral, although the confirmation PoC slash is configured as 0. Governance cannot change the confirmation PoC penalty without also changing the downtime penalty. A PoC challenge writes the same ratio ([module/poc_challenge.go:208-210](https://github.com/gonka-ai/gonka/blob/c5b9b9d373d536ead44e72b330818936b6db31ba/inference-chain/x/inference/module/poc_challenge.go#L208-L210)), so a failed challenge ends in the same slash.

## Expected

`proposals/random-poc/README.md` describes `slash_fraction` as the collateral slashed for a failed confirmation PoC. With the field at 0, a failed confirmation PoC should move the participant to `INACTIVE` without a collateral slash.

## Suggested fix

In `deactiveParticipant`, when the reason is `FailedConfirmationPoC`, slash with `ConfirmationPocParams.SlashFraction` (skip when it is nil or zero) instead of `SlashForDowntime`, and log the actual reason. This changes state transitions, so it ships with a chain upgrade. If the downtime fraction is the intended penalty, the confirmation PoC field should be removed instead, so the parameter set does not suggest a separate knob.

#2205 updates the proto comments to describe the current behaviour; they need another edit once this is decided.

</div>

---

> 🔄 **Auto-synced** from [Issue #2208](https://github.com/gonka-ai/gonka/issues/2208) every hour.
