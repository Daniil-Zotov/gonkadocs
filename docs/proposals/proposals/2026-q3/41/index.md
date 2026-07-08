---
title: "#41 – INC4 | Gonka Node Observability Platform"
description: "Today's explorers and dashboards only show on-chain data, leaving the off-chain state of validators completely opaque. The few operators who do run their own monitoring use different tools, different "
template: proposals-proposals-main.html
---

# #41 – INC4 | Gonka Node Observability Platform

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-rejected">Rejected</span>

**Proposal ID:** `41`

**Type:** Community Pool Spend

**Submit:** 2026-01-01 00:00 UTC

**Voting:**  → 2026-01-02 00:00 UTC

<div class="prop-funding-line">$96,000 · Community Pool</div>


[View on gonka.gg](https://gonka.gg/network/proposals/41){:target="_blank"}

</div>

Today's explorers and dashboards only show on-chain data, leaving the off-chain state of validators completely opaque. The few operators who do run their own monitoring use different tools, different 

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
    "recipient": "gonka1yf2f23sqx8fradjn7laqp0twamlhy4sj6vzwmg946ux4awfqaaes9avx7a",
    "amount": [
      {
        "denom": "ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4",
        "amount": "96000000000"
      }
    ]
  }
]
```

</details>

---