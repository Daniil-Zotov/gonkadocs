---
title: "#74 – Gonka Labs: Maintaining Infrastructure, Improving Products, and Launching New Ones"
description: "Proposal #74"
template: proposals-proposals-main.html
---

# #74 – Gonka Labs: Maintaining Infrastructure, Improving Products, and Launching New Ones

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-passed">Passed</span>

**Proposal ID:** `74`

**Type:** Execute Contract, Transfer With Vesting

**Submit:** 2026-01-01 00:00 UTC

**Voting:**  → 2026-01-02 00:00 UTC

<div class="prop-funding-line">$70,000 · Community Pool · 330,000 GNK · Gov Module</div>


[View on gonka.gg](https://gonka.gg/network/proposals/74){:target="_blank"}

</div>

## Messages

| # | Type |
| :- | :--- |
| 1 | `/cosmwasm.wasm.v1.MsgExecuteContract` |
| 2 | `/inference.streamvesting.MsgTransferWithVesting` |

<details class="prop-contracts">
<summary>Contract Details</summary>

```json
[
  {
    "@type": "/cosmwasm.wasm.v1.MsgExecuteContract",
    "sender": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "contract": "gonka18pkq9mwxxlmyq7kr5txhm060wemg2s4u94wvsfd9w2kdc0u99d6spk8pz2",
    "msg": {
      "withdraw_ibc": {
        "denom": "ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4",
        "amount": "70000000000",
        "recipient": "gonka16j4zv6723mrnycwn0qgw0j48dr9qecyclxg5jh"
      }
    },
    "funds": []
  },
  {
    "@type": "/inference.streamvesting.MsgTransferWithVesting",
    "sender": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "recipient": "gonka16j4zv6723mrnycwn0qgw0j48dr9qecyclxg5jh",
    "amount": [
      {
        "denom": "ngonka",
        "amount": "330000000000000"
      }
    ],
    "vesting_epochs": "180"
  }
]
```

</details>

---