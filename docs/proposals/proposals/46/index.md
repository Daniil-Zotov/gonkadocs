---
title: "#46 – Epochs 132-247 compensation payout from gov module (batch vesting)"
description: "Two prior upgrades changed the lifecycle of unpaid miner rewards. v0.2.9 (proposal #26, 2026-02-01): when a participant is penalized during cPoC validation, the unaccounted portion of their epoch rewa"
template: proposals-proposals-main.html
---

# #46 – Epochs 132-247 compensation payout from gov module (batch vesting)

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-passed">Passed</span>

**Proposal ID:** `46`

**Type:** Batch Transfer With Vesting, Multi Send

**Submit:** 2026-05-02 03:52 UTC

**Voting:** 2026-05-02 03:52 UTC → 2026-05-04 03:52 UTC

**Proposer:** `gonka1gmuxdcxlsxn5z72elx77w9zym7yrgfxqgzg6ry`

**Metadata:** [https://github.com/gonkavip/taxreturn/blob/main/README.md](https://github.com/gonkavip/taxreturn/blob/main/README.md)

</div>

Two prior upgrades changed the lifecycle of unpaid miner rewards. v0.2.9 (proposal #26, 2026-02-01): when a participant is penalized during cPoC validation, the unaccounted portion of their epoch reward is no longer redistributed among the remaining participants in the epoch — it is sent to the gov module account. v0.2.11 (proposal #31, 2026-03-20, PR #775): slashed collateral was likewise routed to the gov account instead of being burned. As a result the gov account (gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33) has accumulated roughly 3 053 801 GNK of withheld miner rewards over epochs 132–247. These coins were originally minted as miner reward, not as community subsidy. The community pool (gonka1jv65s3grqf6v6jl3dp4t6c9t9rk99cd8h2rzwa, separate account) already holds ~103M GNK + 10K IBC USDT for community initiatives.

What this proposal does. Returns the historical inflow of epochs 132–247 to the miners who actually performed in those epochs, proportional to each miner's rewarded_coins. Distribution is computed deterministically from on-chain data via a single Python script: see https://github.com/gonkavip/taxreturn for the full algorithm, reproducible code, and the exact payout CSV. Total to be distributed: 3 053 800.853 GNK across 1 623 recipients.

Execution. Recipients with share ≥ 10 GNK (1 204 miners, 3 052 968.210 GNK) are paid via MsgBatchTransferWithVesting with 180-epoch vesting (same instrument used by proposals #32 and #33), split into 3 batches of ≤500 outputs as required by the streamvesting module. Recipients with share < 10 GNK (419 miners, 832.643 GNK) are paid via a single MsgMultiSend from the gov account, instant (no vesting). This is required because the streamvesting module enforces MinTransferNgonka = 10_000_000_000 (10 GNK) on every output of MsgBatchTransferWithVesting; including a sub-10 GNK recipient in a vesting batch would cause the entire transaction to fail with ErrInvalidCoins. Sending the dust portion via plain bank transfer is the only way to keep these miners whole without artificially inflating their share.

Notes. The proposer takes no fee — every ngonka returns to the miners. Hamilton (largest-remainder) integer apportionment guarantees the sum of all per-recipient amounts equals the total inflow exactly, with no rounding loss. Past compensations from proposals #32 and #33 (~55 000 GNK) are not subtracted from individual recipients; the resulting double-payment for those addresses is on the order of 1.7% of the total wallet balance and below typical per-epoch noise. After execution roughly 200 160 GNK will remain in the gov account (inflows from epochs > 247 plus minor pre-132 entries) and is not addressed by this proposal.

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:36.0%"></div>
    <div class="prop-tally-no" style="width:0.0%"></div>
    <div class="prop-tally-veto" style="width:0.0%"></div>
    <div class="prop-tally-abstain" style="width:64.0%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes 97,030 (36.0%)</span>
    <span class="prop-tally-no-text">No 0 (0.0%)</span>
    <span class="prop-tally-veto-text">Veto 0 (0.0%)</span>
    <span class="prop-tally-abstain-text">Abstain 172,837 (64.0%)</span>
  </div>
</div>


---

## Messages

| # | Type |
| :- | :--- |
| 1 | `/inference.streamvesting.MsgBatchTransferWithVesting` |
| 2 | `/inference.streamvesting.MsgBatchTransferWithVesting` |
| 3 | `/inference.streamvesting.MsgBatchTransferWithVesting` |
| 4 | `/cosmos.bank.v1beta1.MsgMultiSend` |

---

<div class="prop-footer" markdown="1">

[View on gonka.gg](https://gonka.gg/network/proposals/46){:target="_blank"}

</div>
