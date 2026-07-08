---
title: "#45 – Governance Architecture Proposal for the Gonka.ai Network"
description: "Replace scattered governance discussions and complex CLI voting with a unified Governance Portal - a single interface for all Gonka governance activity. The portal includes: a proposal feed across Dis"
template: proposals-proposals-main.html
---

# #45 – Governance Architecture Proposal for the Gonka.ai Network

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-rejected">Rejected</span>

**Proposal ID:** `45`

**Type:** Community Pool Spend

**Submit:** 2026-01-01 00:00 UTC

**Voting:**  → 2026-01-02 00:00 UTC

<div class="prop-funding-line">119,000 GNK · Community Pool</div>


[View on gonka.gg](https://gonka.gg/network/proposals/45){:target="_blank"}

</div>

Replace scattered governance discussions and complex CLI voting with a unified Governance Portal - a single interface for all Gonka governance activity. The portal includes: a proposal feed across Dis

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
        "amount": "119000000000000"
      }
    ]
  }
]
```

</details>

---