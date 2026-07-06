---
title: "#928 — [P1] Open Questions: Block Gas Limits, Fees, Cost per Participant, and System TX Prioritization"
source: https://github.com/gonka-ai/gonka/issues/928
issue_number: 928
synced_at: 2026-07-06T09:52:05Z
template: issues-main.html
---

> 🔄 **Авто-синхронизация:** из [Issue #928](https://github.com/gonka-ai/gonka/issues/928) каждые 6 часов. 

# 🟢 [P1] Open Questions: Block Gas Limits, Fees, Cost per Participant, and System TX Prioritization

**Автор:** [@tcharchian](https://github.com/tcharchian) · **Состояние:** Open · **Создано:** 2026-03-20 23:46 UTC · **Обновлено:** 2026-05-07 22:46 UTC

**Метки:** `Priority: Medium`

**Веха:** v0.2.14

---

## 📝 Описание

## Summary

- Introduces a governance-controlled minimum gas price (`FeeParams.min_gas_price`) enforced at consensus level via a custom `TxFeeChecker`, replacing the current `nil` fee checker that allows zero-fee transactions
- Adds a `NetworkDutyFeeBypassDecorator` that exempts protocol-obligation messages (PoC, validations, BLS, weight distributions) from fees, following the existing `LiquidityPoolFeeBypassDecorator` pattern
- Proposes initial gas price of `10ngonka` (~$0.00046/tx at current GNK price), making sustained spam attacks cost real money while keeping individual transactions under a cent

## Key design decisions

- **Consensus-level enforcement** via `TxFeeChecker` (runs in both `CheckTx` and `DeliverTx`), not per-validator `app.toml` which is `CheckTx`-only and can be bypassed by block proposers
- **Recursive `MsgExec` unpacking** to prevent wrapping fee-required messages inside authz executions
- **Governance-adjustable** parameter — no chain upgrade needed to tune the gas price

---

## 💬 Комментарии (1)

### Комментарий 1 — [@unameisfine](https://github.com/unameisfine)

*2026-05-07 22:46 UTC*

## Implementation-level review from the current codebase

The two-track approach — consensus-level `TxFeeChecker` + `NetworkDutyFeeBypassDecorator` modeled on the existing `LiquidityPoolFeeBypassDecorator` — is the right shape. A few concrete gaps from the current code worth resolving before implementation:

### 1. The "network duty" message set needs to be exhaustive, not exemplary

The summary lists "PoC, validations, BLS, weight distributions" — this is the right category but not the complete msg list. Inference defines ~45 msg types ([`tx.pb.go`](https://github.com/gonka-ai/gonka/blob/main/inference-chain/x/inference/types/tx.pb.go)). Concrete classification needed before merge:

**Clearly network duty (must bypass):**
- PoC: `MsgSubmitPocBatch`, `MsgSubmitPocValidation`, `MsgSubmitPocValidationsV2`, `MsgPoCV2StoreCommit`, `MsgSubmitSeed`
- Validation: `MsgValidation`, `MsgInvalidateInference`, `MsgRevalidateInference`
- Weight distribution: `MsgMLNodeWeightDistribution`
- BLS: `MsgSubmitDealerPart`, `MsgSubmitVerificationVector`, `MsgSubmitGroupKeyValidationSignature`, `MsgSubmitPartialSignature`, `MsgRespondDealerComplaints` (added in v0.2.13 — see [`upgrades/v0_2_13/upgrades.go:148`](https://github.com/gonka-ai/gonka/blob/main/inference-chain/app/upgrades/v0_2_13/upgrades.go#L148))
- Hardware diff: `MsgSubmitHardwareDiff`

**Ambiguous (proposal must decide explicitly):**
- `MsgStartInference` / `MsgFinishInference` — emitted by Transfer Agents per inference. At ~83K inferences/day × 2 chain txs × `10ngonka × 200K gas` ≈ $80/day TA overhead. Bypass them and TA spam is a free attack surface; charge them and TAs need a per-tx gas reserve change.
- `MsgClaimRewards` — 1 per participant per epoch × 43 epochs/day × N participants. Charging is fine economically (~$0.0005 per claim), but the proposal mentions "Cost per Participant" in the title and this is the dominant per-participant cost.
- `MsgRequestThresholdSignature` — who triggers it? If user-driven (request-to-sign), it's user-paid; if protocol (rotation/recovery), it's network duty.
- `MsgSettleSubnetEscrow` — periodic settlement vs user-triggered settle.

A flat enumeration in the proposal (or a typed registry interface alongside `LiquidityPoolFeeBypassDecorator`) is the only way to make this auditable.

### 2. Recursive `MsgExec` unpacking — needs depth limit and authz grant interaction

The summary correctly flags recursive unpacking. Two follow-ons:

- **Depth limit**: nested `authz.MsgExec` chains are syntactically unbounded. Without a max recursion depth, a malicious tx with `MsgExec(MsgExec(MsgExec(...MsgValidation...)))` either DoS the fee checker or silently fails to enforce. SDK convention is depth ≤ 5.
- **Authz grant migration**: cold→warm grants today don't account for fees on the granter. After upgrade, `authz.MsgExec` from grantee will deduct fees from **granter**, but operators have historically funded only the warm (grantee) account. The v0.2.13 backfill in [`upgrades.go:148`](https://github.com/gonka-ai/gonka/blob/main/inference-chain/app/upgrades/v0_2_13/upgrades.go#L148) sets up new `MsgRespondDealerComplaints` grants but doesn't address this funding shift. If MsgExec'd network-duty messages bypass entirely, this is moot. If a fee-required user message gets MsgExec'd through cold→warm authz, the granter is silently debited — worth being explicit about.

### 3. Mempool priority interaction with existing `LiquidityPoolFeeBypassDecorator`

[`ante.go:165`](https://github.com/gonka-ai/gonka/blob/main/inference-chain/app/ante.go#L165) sets `Priority: 1_000_000` for liquidity pool bypassed txs. If `NetworkDutyFeeBypassDecorator` doesn't apply at least the same priority, in a peak-load mempool spam-but-fee-paying user txs will displace network-duty txs, which is the opposite of intent.

The proposal should specify priority levels:
- Network duty (PoC/validation/BLS): highest (e.g., `10_000_000`)
- Liquidity pool: existing `1_000_000`
- Fee-paying user: priority proportional to gas-price (default SDK behavior)
- Zero-fee non-bypass: rejected by `TxFeeChecker`

### 4. `TxFeeChecker` parity between `CheckTx` and `DeliverTx` proposer manipulation

The summary correctly notes that `app.toml` is `CheckTx`-only. One subtlety to call out:

[`config.go:61-67`](https://github.com/gonka-ai/gonka/blob/main/inference-chain/cmd/inferenced/cmd/config.go#L61-L67) currently relies on per-validator `MinGasPrices`. ABCI++ allows a block proposer to include any tx in their proposal — `DeliverTx` then runs the chain's fee logic. A custom `TxFeeChecker` that reads `FeeParams.min_gas_price` from chain state correctly closes this. Two implementation notes:

- The `TxFeeChecker` MUST read from current block context (`ctx.BlockHeight()`), not from a cached value, so a governance change to `min_gas_price` takes effect at the next block, not the next epoch.
- For determinism: `TxFeeChecker` must never return different fee/priority for the same tx between `CheckTx` and `DeliverTx` (other than the SDK's standard `Priority` handling).

### 5. Bypass + gas metering: block-gas DoS still possible

Today's `LiquidityPoolFeeBypassDecorator` ([`ante.go:163`](https://github.com/gonka-ai/gonka/blob/main/inference-chain/app/ante.go#L163)) waives min-gas-prices but keeps metering — gas is still consumed against the block limit. `NetworkDutyFeeBypassDecorator` should do the same, **and** the proposal should size the block gas limit to absorb worst-case PoC submission volume:

- ~200 participants × 20 PoC msgs/epoch × 50K gas ≈ 200M gas/epoch
- 33-min epoch ÷ 5s blocks ≈ 396 blocks → ~500K gas/block for PoC alone

SDK default `MaxGas` is 10M (or `-1` for unlimited). At ~500 participants the per-block PoC budget approaches 1.25M gas — still fine, but worth a sentence in the proposal to confirm the budget and to commit governance to revisiting it as participant count grows.

A `GasCap` per bypassed-tx (analogous to the existing `GasCap: 500000` on liquidity pool, [`ante.go:215`](https://github.com/gonka-ai/gonka/blob/main/inference-chain/app/ante.go#L215)) is also worth specifying for network-duty messages, so an oversized PoC submission can't single-handedly dominate a block.

### 6. Initial price `10 ngonka` — sanity check + governance escape hatch

Math reproduces the proposal's $0.00046/tx claim:
- 1 GNK = 10⁹ ngonka, current price ≈ $0.23/GNK
- Default tx: 200K gas × 10 ngonka = 2M ngonka = 0.002 GNK = $0.00046 ✓

One gap: for spam to **cost real money**, the attacker has to be paying actual GNK. New participants today get `genesis_guardian_addresses` ([`params.proto`](https://github.com/gonka-ai/gonka/blob/main/inference-chain/proto/inference/inference/params.proto)) and `BlackListAccounts` exclusions, but a fresh adversary-funded account can still pay. With 200K gas × 10 ngonka, a determined attacker spending $46 can burn 100K block-gas budget. The proposal should:

- State the threat model explicitly (what's the spam cost-floor we're targeting?).
- Provide a governance fast-path to raise `min_gas_price` mid-attack — `x/group` operational voting, given v0.2.12's split between `x/gov` and `x/group` (per [`docs/voting.md`](https://github.com/gonka-ai/gonka/blob/main/docs/voting.md)).

---

Outline LGTM, but the network-duty msg enumeration (#1) and the authz grant migration (#2) are blockers for safe deployment. Worth landing a follow-on PR with the typed registry of network-duty msg types before the upgrade.

