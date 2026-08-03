---
title: "#928 — [P1] Open Questions: Block Gas Limits, Fees, Cost per Participant, and System TX Prioritization"
source: https://github.com/gonka-ai/gonka/issues/928
issue_number: 928
synced_at: 2026-08-03T20:40:32Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    [P1] Open Questions: Block Gas Limits, Fees, Cost per Participant, and System TX Prioritization
    <span class="issues-number">#928</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-03-20 23:46 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-07-07 23:31 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #12a6e8; color: #24292f; border-color: #12a6e8;">Priority: Medium</span></div>
</div>

<div class="issues-content" markdown="1">
## Summary

- Introduces a governance-controlled minimum gas price (`FeeParams.min_gas_price`) enforced at consensus level via a custom `TxFeeChecker`, replacing the current `nil` fee checker that allows zero-fee transactions
- Adds a `NetworkDutyFeeBypassDecorator` that exempts protocol-obligation messages (PoC, validations, BLS, weight distributions) from fees, following the existing `LiquidityPoolFeeBypassDecorator` pattern
- Proposes initial gas price of `10ngonka` (~$0.00046/tx at current GNK price), making sustained spam attacks cost real money while keeping individual transactions under a cent

## Key design decisions

- **Consensus-level enforcement** via `TxFeeChecker` (runs in both `CheckTx` and `DeliverTx`), not per-validator `app.toml` which is `CheckTx`-only and can be bypassed by block proposers
- **Recursive `MsgExec` unpacking** to prevent wrapping fee-required messages inside authz executions
- **Governance-adjustable** parameter — no chain upgrade needed to tune the gas price
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/unameisfine">@unameisfine</a></span>
    <span class="issues-meta-item">commented 2026-05-07 22:46 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <h2>Implementation-level review from the current codebase</h2>
<p>The two-track approach — consensus-level <code>TxFeeChecker</code> + <code>NetworkDutyFeeBypassDecorator</code> modeled on the existing <code>LiquidityPoolFeeBypassDecorator</code> — is the right shape. A few concrete gaps from the current code worth resolving before implementation:</p>
<h3>1. The "network duty" message set needs to be exhaustive, not exemplary</h3>
<p>The summary lists "PoC, validations, BLS, weight distributions" — this is the right category but not the complete msg list. Inference defines ~45 msg types (<a href="https://github.com/gonka-ai/gonka/blob/main/inference-chain/x/inference/types/tx.pb.go"><code>tx.pb.go</code></a>). Concrete classification needed before merge:</p>
<p><strong>Clearly network duty (must bypass):</strong>
- PoC: <code>MsgSubmitPocBatch</code>, <code>MsgSubmitPocValidation</code>, <code>MsgSubmitPocValidationsV2</code>, <code>MsgPoCV2StoreCommit</code>, <code>MsgSubmitSeed</code>
- Validation: <code>MsgValidation</code>, <code>MsgInvalidateInference</code>, <code>MsgRevalidateInference</code>
- Weight distribution: <code>MsgMLNodeWeightDistribution</code>
- BLS: <code>MsgSubmitDealerPart</code>, <code>MsgSubmitVerificationVector</code>, <code>MsgSubmitGroupKeyValidationSignature</code>, <code>MsgSubmitPartialSignature</code>, <code>MsgRespondDealerComplaints</code> (added in v0.2.13 — see <a href="https://github.com/gonka-ai/gonka/blob/main/inference-chain/app/upgrades/v0_2_13/upgrades.go#L148"><code>upgrades/v0_2_13/upgrades.go:148</code></a>)
- Hardware diff: <code>MsgSubmitHardwareDiff</code></p>
<p><strong>Ambiguous (proposal must decide explicitly):</strong>
- <code>MsgStartInference</code> / <code>MsgFinishInference</code> — emitted by Transfer Agents per inference. At ~83K inferences/day × 2 chain txs × <code>10ngonka × 200K gas</code> ≈ $80/day TA overhead. Bypass them and TA spam is a free attack surface; charge them and TAs need a per-tx gas reserve change.
- <code>MsgClaimRewards</code> — 1 per participant per epoch × 43 epochs/day × N participants. Charging is fine economically (~$0.0005 per claim), but the proposal mentions "Cost per Participant" in the title and this is the dominant per-participant cost.
- <code>MsgRequestThresholdSignature</code> — who triggers it? If user-driven (request-to-sign), it's user-paid; if protocol (rotation/recovery), it's network duty.
- <code>MsgSettleSubnetEscrow</code> — periodic settlement vs user-triggered settle.</p>
<p>A flat enumeration in the proposal (or a typed registry interface alongside <code>LiquidityPoolFeeBypassDecorator</code>) is the only way to make this auditable.</p>
<h3>2. Recursive <code>MsgExec</code> unpacking — needs depth limit and authz grant interaction</h3>
<p>The summary correctly flags recursive unpacking. Two follow-ons:</p>
<ul>
<li><strong>Depth limit</strong>: nested <code>authz.MsgExec</code> chains are syntactically unbounded. Without a max recursion depth, a malicious tx with <code>MsgExec(MsgExec(MsgExec(...MsgValidation...)))</code> either DoS the fee checker or silently fails to enforce. SDK convention is depth ≤ 5.</li>
<li><strong>Authz grant migration</strong>: cold→warm grants today don't account for fees on the granter. After upgrade, <code>authz.MsgExec</code> from grantee will deduct fees from <strong>granter</strong>, but operators have historically funded only the warm (grantee) account. The v0.2.13 backfill in <a href="https://github.com/gonka-ai/gonka/blob/main/inference-chain/app/upgrades/v0_2_13/upgrades.go#L148"><code>upgrades.go:148</code></a> sets up new <code>MsgRespondDealerComplaints</code> grants but doesn't address this funding shift. If MsgExec'd network-duty messages bypass entirely, this is moot. If a fee-required user message gets MsgExec'd through cold→warm authz, the granter is silently debited — worth being explicit about.</li>
</ul>
<h3>3. Mempool priority interaction with existing <code>LiquidityPoolFeeBypassDecorator</code></h3>
<p><a href="https://github.com/gonka-ai/gonka/blob/main/inference-chain/app/ante.go#L165"><code>ante.go:165</code></a> sets <code>Priority: 1_000_000</code> for liquidity pool bypassed txs. If <code>NetworkDutyFeeBypassDecorator</code> doesn't apply at least the same priority, in a peak-load mempool spam-but-fee-paying user txs will displace network-duty txs, which is the opposite of intent.</p>
<p>The proposal should specify priority levels:
- Network duty (PoC/validation/BLS): highest (e.g., <code>10_000_000</code>)
- Liquidity pool: existing <code>1_000_000</code>
- Fee-paying user: priority proportional to gas-price (default SDK behavior)
- Zero-fee non-bypass: rejected by <code>TxFeeChecker</code></p>
<h3>4. <code>TxFeeChecker</code> parity between <code>CheckTx</code> and <code>DeliverTx</code> proposer manipulation</h3>
<p>The summary correctly notes that <code>app.toml</code> is <code>CheckTx</code>-only. One subtlety to call out:</p>
<p><a href="https://github.com/gonka-ai/gonka/blob/main/inference-chain/cmd/inferenced/cmd/config.go#L61-L67"><code>config.go:61-67</code></a> currently relies on per-validator <code>MinGasPrices</code>. ABCI++ allows a block proposer to include any tx in their proposal — <code>DeliverTx</code> then runs the chain's fee logic. A custom <code>TxFeeChecker</code> that reads <code>FeeParams.min_gas_price</code> from chain state correctly closes this. Two implementation notes:</p>
<ul>
<li>The <code>TxFeeChecker</code> MUST read from current block context (<code>ctx.BlockHeight()</code>), not from a cached value, so a governance change to <code>min_gas_price</code> takes effect at the next block, not the next epoch.</li>
<li>For determinism: <code>TxFeeChecker</code> must never return different fee/priority for the same tx between <code>CheckTx</code> and <code>DeliverTx</code> (other than the SDK's standard <code>Priority</code> handling).</li>
</ul>
<h3>5. Bypass + gas metering: block-gas DoS still possible</h3>
<p>Today's <code>LiquidityPoolFeeBypassDecorator</code> (<a href="https://github.com/gonka-ai/gonka/blob/main/inference-chain/app/ante.go#L163"><code>ante.go:163</code></a>) waives min-gas-prices but keeps metering — gas is still consumed against the block limit. <code>NetworkDutyFeeBypassDecorator</code> should do the same, <strong>and</strong> the proposal should size the block gas limit to absorb worst-case PoC submission volume:</p>
<ul>
<li>~200 participants × 20 PoC msgs/epoch × 50K gas ≈ 200M gas/epoch</li>
<li>33-min epoch ÷ 5s blocks ≈ 396 blocks → ~500K gas/block for PoC alone</li>
</ul>
<p>SDK default <code>MaxGas</code> is 10M (or <code>-1</code> for unlimited). At ~500 participants the per-block PoC budget approaches 1.25M gas — still fine, but worth a sentence in the proposal to confirm the budget and to commit governance to revisiting it as participant count grows.</p>
<p>A <code>GasCap</code> per bypassed-tx (analogous to the existing <code>GasCap: 500000</code> on liquidity pool, <a href="https://github.com/gonka-ai/gonka/blob/main/inference-chain/app/ante.go#L215"><code>ante.go:215</code></a>) is also worth specifying for network-duty messages, so an oversized PoC submission can't single-handedly dominate a block.</p>
<h3>6. Initial price <code>10 ngonka</code> — sanity check + governance escape hatch</h3>
<p>Math reproduces the proposal's $0.00046/tx claim:
- 1 GNK = 10⁹ ngonka, current price ≈ $0.23/GNK
- Default tx: 200K gas × 10 ngonka = 2M ngonka = 0.002 GNK = $0.00046 ✓</p>
<p>One gap: for spam to <strong>cost real money</strong>, the attacker has to be paying actual GNK. New participants today get <code>genesis_guardian_addresses</code> (<a href="https://github.com/gonka-ai/gonka/blob/main/inference-chain/proto/inference/inference/params.proto"><code>params.proto</code></a>) and <code>BlackListAccounts</code> exclusions, but a fresh adversary-funded account can still pay. With 200K gas × 10 ngonka, a determined attacker spending $46 can burn 100K block-gas budget. The proposal should:</p>
<ul>
<li>State the threat model explicitly (what's the spam cost-floor we're targeting?).</li>
<li>Provide a governance fast-path to raise <code>min_gas_price</code> mid-attack — <code>x/group</code> operational voting, given v0.2.12's split between <code>x/gov</code> and <code>x/group</code> (per <a href="https://github.com/gonka-ai/gonka/blob/main/docs/voting.md"><code>docs/voting.md</code></a>).</li>
</ul>
<hr />
<p>Outline LGTM, but the network-duty msg enumeration (#1) and the authz grant migration (#2) are blockers for safe deployment. Worth landing a follow-on PR with the typed registry of network-duty msg types before the upgrade.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #928](https://github.com/gonka-ai/gonka/issues/928) every hour.
