---
title: "#43 – Governance Architecture Proposal for the Gonka.ai Network"
description: "Today, participating in Gonka governance requires following multiple channels simultaneously — GitHub, Discord, CLI — just to cast a single vote. Most miners miss proposals entirely or vote too late. "
template: proposals-proposals-main.html
---

# #43 – Governance Architecture Proposal for the Gonka.ai Network

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-rejected">Rejected</span>

**Proposal ID:** `43`

**Type:** Community Pool Spend

**Submit:** 2026-01-01 00:00 UTC

**Voting:**  → 2026-01-02 00:00 UTC

<div class="prop-funding-line">104,166 GNK · Community Pool</div>


[View on gonka.gg](https://gonka.gg/network/proposals/43){:target="_blank"}

</div>

Today, participating in Gonka governance requires following multiple channels simultaneously — GitHub, Discord, CLI — just to cast a single vote. Most miners miss proposals entirely or vote too late. 

---

## Messages

| # | Type |
| :- | :--- |
| 1 | `/cosmos.distribution.v1beta1.MsgCommunityPoolSpend` |

<details class="prop-contracts">
<summary>Contract Details</summary>

```json
[
  {
    "@type": "/cosmos.distribution.v1beta1.MsgCommunityPoolSpend",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "recipient": "gonka14zlgmrd6v5gaqudxmvkn0yg8g55qpvcep9n6ds",
    "amount": [
      {
        "denom": "ngonka",
        "amount": "104166000000000"
      }
    ]
  }
]
```

</details>

---