---
title: "#1539 — Hardening: network-duty fee-bypass admits zero-fee txs from non-participants (no signer authorization at the ante layer)"
source: https://github.com/gonka-ai/gonka/issues/1539
issue_number: 1539
synced_at: 2026-08-09T14:56:00Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Hardening: network-duty fee-bypass admits zero-fee txs from non-participants (no signer authorization at the ante layer)
    <span class="issues-number">#1539</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/kAIPraxisBot">@kAIPraxisBot</a> opened 2026-08-03 19:33 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-08-03 19:33 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

`NetworkDutyFeeBypassDecorator` waives fees + clears min-gas-price for ~12 "network duty" message types, and the exemption is decided **purely by Go message type** (`isExemptMessageType` in `inference-chain/app/ante_fee.go`) — there is no check at the ante/`CheckTx` layer that the signer is an active participant / authorized host. So **any funded account can submit structurally-valid, zero-fee duty-typed transactions.** They pass `CheckTx`, enter the mempool, occupy block space, incur secp256k1 signature verification on every validator, and are rejected only later in `DeliverTx` (e.g. `participant is not active`).

The real authorization for these types (allowlist / participant / dedup / deadline) lives in the message handlers, which run in `DeliverTx` — i.e. **after** mempool admission and block inclusion. `CheckTx` runs the ante only, so unauthorized duty-typed txs are admitted regardless.

## Where

- `inference-chain/app/ante_fee.go` — `NetworkDutyFeeBypassDecorator` / `isExemptMessageType` / `GonkaFeeChecker`. On `main`, the exempt set is 12 types: `MsgSubmitPocBatch`, `MsgSubmitPocValidationsV2`, `MsgMLNodeWeightDistribution`, `MsgSubmitSeed`, `MsgSubmitHardwareDiff`, `MsgClaimRewards`, `MsgSettleDevshardEscrow`, and the 5 BLS DKG types.
- `inference-chain/app/ante_poc_period.go` — `PocPeriodValidationDecorator` gates only **timing** (`checkPocMessageTooLate`) and only for the 4 PoC types; it does not check the signer. The other 8 exempt types have no ante-layer gate at all.

## Impact (bounded — hardening, not a critical exploit)

An attacker imposes **free, unauthenticated load**: zero-fee inclusion consuming validator sig-verify + gossip + mempool + block bytes, with no economic cost (balance never drains; one-time dust to fund accounts).

Honest severity limits, verified against live mainnet consensus params (`max_gas = -1`, `max_bytes = 22 MB`):
- **Not** a practical throughput DoS: with unlimited block gas, saturating a block is bounded only by the ~22 MB byte limit, which (given `CheckTx` enforces the account sequence → one pending tx per account) would require on the order of tens of thousands of concurrently-funded accounts.
- The `Priority: 10_000_000` boost is **inert** for block ordering: the app uses the default `NoOpMempool`, so `PrepareProposal` builds blocks in CometBFT FIFO order and never consults the priority. No priority-based censorship of paid traffic.

So this is a resource-abuse / free-spam hardening gap, not a network-halting exploit.

## Reproduction

A zero-fee `MsgClaimRewards` signed by a non-participant account: `CheckTx` returns code 0 (admitted), the tx is included in a block, and only then fails in `DeliverTx` with `participant is not active` — having consumed block gas at zero fee.

## Suggested fix

Add an ante-layer signer-authorization check for the exempt types (reject duty-typed txs from non-participants / non-allowlisted signers at `CheckTx`), and/or withhold the fee-bypass + priority until the signer is authorized. This mirrors the participant check that already protects `MsgValidation`, and closes the gap where the only authorization runs in `DeliverTx` after admission.

</div>

---

> 🔄 **Auto-synced** from [Issue #1539](https://github.com/gonka-ai/gonka/issues/1539) every hour.
