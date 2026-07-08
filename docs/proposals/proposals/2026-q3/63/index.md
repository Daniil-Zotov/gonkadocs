---
title: "#63 – TheSoul - Offer 2.1: Website and landings (10,000 USDT)"
description: "Full redesign of gonka.ai plus dedicated landing pages for miners, inference buyers, and investors, built on the brandbook from Offer 1.2. Single-tranche payment of 10,000 USDT to TheSoul on proposal "
template: proposals-proposals-main.html
---

# #63 – TheSoul - Offer 2.1: Website and landings (10,000 USDT)

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-passed">Passed</span>

**Proposal ID:** `63`

**Type:** Execute Contract

**Submit:** 2026-01-01 00:00 UTC

**Voting:**  → 2026-01-02 00:00 UTC

<div class="prop-funding-line">$10,000 · Community Pool</div>


[View on gonka.gg](https://gonka.gg/network/proposals/63){:target="_blank"}

</div>

Full redesign of gonka.ai plus dedicated landing pages for miners, inference buyers, and investors, built on the brandbook from Offer 1.2. Single-tranche payment of 10,000 USDT to TheSoul on proposal 

---

## Messages

| # | Type |
| :- | :--- |
| 1 | `/cosmwasm.wasm.v1.MsgExecuteContract` |

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
        "amount": "10000000000",
        "recipient": "gonka1s3tnqglxt6xwy9ttuedtz8cp4x9tlwp8sdcvvm"
      }
    },
    "funds": []
  }
]
```

</details>

---