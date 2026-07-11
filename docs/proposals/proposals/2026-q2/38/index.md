---
title: "#38 – CryptoCommons: Community Support & Token Promotion Plan"
description: "If you agree say YES — Solution 1: Produce a short review video with 1-2 active community members. Solution 2: Introduce the project to BD managers of major CIS exchanges for listings. Solution 3 (Reg"
template: proposals-proposals-main.html
---

# #38 – CryptoCommons: Community Support & Token Promotion Plan

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-rejected">Rejected</span>

**Proposal ID:** `38`

**Type:** Batch Transfer With Vesting, Community Pool Spend

**Submit:** 2026-04-08 19:24 UTC

**Voting:** 2026-04-08 19:24 UTC → 2026-04-09 19:24 UTC

**Proposer:** [`gonka1kk4a0kuc6uh5yrlfqe2ehuq6a4v7vcxx8fvxxr`](https://gonka.gg/address/gonka1kk4a0kuc6uh5yrlfqe2ehuq6a4v7vcxx8fvxxr){:target="_blank"}

**Metadata:** [https://discord.com/channels/1336477374442770503/1425189436748206171/1481942972055552041](https://discord.com/channels/1336477374442770503/1425189436748206171/1481942972055552041)

**Failed reason:** proposal did not get enough votes to pass

<div class="prop-funding-line prop-funding-line-rejected">20,000 GNK · Community Pool · 25,000 GNK · Gov Module</div>


[View on gonka.gg](https://gonka.gg/network/proposals/38){:target="_blank"}

</div>

If you agree say YES — Solution 1: Produce a short review video with 1-2 active community members. Solution 2: Introduce the project to BD managers of major CIS exchanges for listings. Solution 3 (Regulatory safety): To avoid future regulatory risks, we will run regular token drops

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:0.0%"></div>
    <div class="prop-tally-no" style="width:2.3%"></div>
    <div class="prop-tally-veto" style="width:97.7%"></div>
    <div class="prop-tally-abstain" style="width:0.0%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes 0 (0.0%)</span>
    <span class="prop-tally-no-text">No 183 (2.3%)</span>
    <span class="prop-tally-veto-text">Veto 7,893 (97.7%)</span>
    <span class="prop-tally-abstain-text">Abstain 0 (0.0%)</span>
    <span class="prop-tally-total-text">Total 8,076 votes</span>
  </div>
</div>

<div class="prop-quorum">
  <span class="prop-quorum-label">Turnout</span>
  <span class="prop-quorum-value">8,076 / 741,825 (1.1%)</span>
  <span class="prop-quorum-label">Quorum</span>
  <span class="prop-quorum-value">25% (185,456 votes)</span>
  <span class="prop-quorum-status prop-quorum-not-met">✗ NOT MET</span>
</div>


---

## Messages

| # | Type |
| :- | :--- |
| 1 | `/inference.streamvesting.MsgBatchTransferWithVesting` |
| 2 | `/cosmos.distribution.v1beta1.MsgCommunityPoolSpend` |

<details class="prop-contracts" markdown="1">
<summary markdown="1">Contract Details</summary>

```json
[
  {
    "@type": "/inference.streamvesting.MsgBatchTransferWithVesting",
    "sender": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "outputs": [
      {
        "recipient": "gonka1lqjjgnme3ayk2q0w8thxnhx69l639dtz9j3r2l",
        "amount": [
          {
            "denom": "ngonka",
            "amount": "25000000000000"
          }
        ]
      }
    ],
    "vesting_epochs": "180"
  },
  {
    "@type": "/cosmos.distribution.v1beta1.MsgCommunityPoolSpend",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "recipient": "gonka1lqjjgnme3ayk2q0w8thxnhx69l639dtz9j3r2l",
    "amount": [
      {
        "denom": "ngonka",
        "amount": "20000000000000"
      }
    ]
  }
]
```

</details>

---