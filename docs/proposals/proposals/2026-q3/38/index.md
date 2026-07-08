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

**Submit:** 2026-01-01 00:00 UTC

**Voting:**  → 2026-01-02 00:00 UTC

<div class="prop-funding-line">20,000 GNK · Community Pool · 25,000 GNK · Gov Module</div>


[View on gonka.gg](https://gonka.gg/network/proposals/38){:target="_blank"}

</div>

If you agree say YES — Solution 1: Produce a short review video with 1-2 active community members. Solution 2: Introduce the project to BD managers of major CIS exchanges for listings. Solution 3 (Reg

---

## Messages

| # | Type |
| :- | :--- |
| 1 | `/inference.streamvesting.MsgBatchTransferWithVesting` |
| 2 | `/cosmos.distribution.v1beta1.MsgCommunityPoolSpend` |

<details class="prop-contracts">
<summary>Contract Details</summary>

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