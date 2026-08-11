---
title: "#1539 — Hardening: network-duty fee-bypass admits zero-fee txs from non-participants (no signer authorization at the ante layer)"
source: https://github.com/gonka-ai/gonka/issues/1539
issue_number: 1539
synced_at: 2026-08-11T12:01:16Z
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
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-08-11 01:51 UTC</span>
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

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Ryanchen911">@Ryanchen911</a></span>
    <span class="issues-meta-item">commented 2026-08-11 01:51 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>I verified this end-to-end against <code>upgrade-v0.2.16</code> (<code>6e92e9089</code>) and can confirm the report. I'd like to take it.</p>
<h2>Confirmed</h2>
<p><strong>Ante ordering.</strong> In <code>NewAnteHandler</code> (<code>inference-chain/app/ante.go:195</code>) <code>NetworkDutyFeeBypassDecorator</code> sits at index 11 and <code>ante.NewSigVerificationDecorator</code> at index 19 — the fee-waiver decision is made <em>before</em> the signature is verified, so the exemption is granted on unauthenticated input.</p>
<p><strong>No signer gate.</strong> <code>isExemptMessageType</code> (<code>ante_fee.go:116-160</code>) switches on the Go type only. <code>isNetworkDuty</code> unwraps one <code>authz.MsgExec</code> level but likewise never looks at who signed.</p>
<p><strong>Authorization really does live only in <code>DeliverTx</code>.</strong> Per <code>MessagePermissions</code> (<code>x/inference/keeper/permissions.go:84</code>) and the handlers:</p>
<table>
<thead>
<tr>
<th>exempt type</th>
<th>handler permission</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>MsgClaimRewards</code></td>
<td><code>ActiveParticipant</code> OR <code>PreviousActiveParticipant</code> (<code>msg_server_claim_rewards.go:23</code>)</td>
</tr>
<tr>
<td><code>MsgSubmitPocBatch</code>, <code>MsgSubmitSeed</code>, <code>MsgSubmitHardwareDiff</code></td>
<td><code>ParticipantPermission</code></td>
</tr>
<tr>
<td><code>MsgSettleDevshardEscrow</code></td>
<td><code>EscrowAllowListPermission</code></td>
</tr>
<tr>
<td><code>MsgSubmitPocValidationsV2</code>, <code>MsgMLNodeWeightDistribution</code></td>
<td><code>NoPermission</code> — only a blocklist check on <code>msg.Creator</code></td>
</tr>
<tr>
<td>5 BLS DKG types</td>
<td>in-handler scan of <code>epochBLSData.Participants</code></td>
</tr>
</tbody>
</table>
<p><strong>Inert priority confirmed.</strong> There is no <code>SetMempool</code> call anywhere in <code>app/</code>, so the default <code>NoOpMempool</code> is in effect and <code>Priority: 10_000_000</code> never influences block ordering — matching your severity analysis.</p>
<h2>One constraint the report doesn't mention, and it decides the fix</h2>
<p>A naive "check the tx signer is a participant" would <strong>break production</strong>. In warm-key mode the DAPI wraps duty messages in <code>authztypes.NewMsgExec(granteeAddress, msgs)</code> (<code>tx_manager.go:833</code>) while setting <code>transaction.Creator = icc.Address</code>, the <em>cold</em> account (<code>cosmosclient.go:409</code>). The tx signer is the grantee; the protocol actor is the <code>Creator</code>/<code>Settler</code> field. The ante check must read the message field, not the signer.</p>
<p>Two more invariants I checked, which decide <em>which</em> predicate is safe:</p>
<ul>
<li><code>ActiveParticipantsSet</code> only retains ~2 epochs — <code>module.go:862-868</code> clears <code>epoch-2</code>. So gating on <em>active</em> would reject legitimate <code>MsgClaimRewards</code> from a previous-epoch participant and BLS DKG traffic for the epoch being rotated.</li>
<li><code>Participants</code> is effectively append-only: <code>RemoveParticipant</code> has no production caller, and every <code>ActiveParticipant</code> is constructed from a registered one (<code>chainvalidation.go:220</code>). Registration is therefore a strict superset of every handler's requirement — it cannot reject traffic <code>DeliverTx</code> would accept.</li>
</ul>
<h2>Proposed fix</h2>
<p>Take the report's second option — <strong>withhold the fee bypass and the priority boost when the actor is not authorized</strong>, rather than rejecting the tx outright:</p>
<ul>
<li>authorized actor → unchanged behaviour, still zero-fee;</li>
<li>unauthorized actor → no waiver, so <code>GonkaFeeChecker</code> applies <code>MinGasPriceNgonka</code> and an unfunded zero-fee spam tx fails <code>CheckTx</code> on <code>ErrInsufficientFee</code> and never reaches the mempool.</li>
</ul>
<p>This closes the free-load gap while keeping a false positive on my side from ever halting consensus-critical PoC/BLS traffic — an outright <code>reject</code> would make a mistaken predicate a liveness bug. Predicate: <code>Participants.Has(Creator)</code> for the participant-gated and BLS types, <code>IsAllowedEscrowCreator(Settler)</code> for <code>MsgSettleDevshardEscrow</code>, fail-closed on a nil keeper or unparseable address, applied inside the <code>MsgExec</code> unwrap as well.</p>
<p>Tests: end-to-end <code>CheckTx</code> via <code>BaseApp</code> (registered vs. unregistered actor, direct and <code>MsgExec</code>-wrapped, following the <code>ante_bridge_checktx_test.go</code> harness) plus unit coverage for the actor extraction and the escrow allowlist branch.</p>
<p>Will open a PR against <code>upgrade-v0.2.16</code>.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1539](https://github.com/gonka-ai/gonka/issues/1539) every hour.
