---
title: "#50 – Retroactive bounty: open-source PoC throughput optimization (+10–12% measured) with 250 total installations"
description: "Retroactive 20K GNK bounty for an open-sourced PoC optimization measuring +10.2% on B200 and +12.5% on H100 with Qwen3-235B-FP8. One-line patch, verified on-chain by independent miners. Details: https"
template: proposals-proposals-main.html
---

# #50 – Retroactive bounty: open-source PoC throughput optimization (+10–12% measured) with 250 total installations

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-passed">Passed</span>

**Proposal ID:** `50`

**Type:** Community Pool Spend

**Submit:** 2026-01-01 00:00 UTC

**Voting:**  → 2026-01-02 00:00 UTC

<div class="prop-funding-line">20,000 GNK · Community Pool</div>


[View on gonka.gg](https://gonka.gg/network/proposals/50){:target="_blank"}

</div>

Retroactive 20K GNK bounty for an open-sourced PoC optimization measuring +10.2% on B200 and +12.5% on H100 with Qwen3-235B-FP8. One-line patch, verified on-chain by independent miners. Details: https

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
    "recipient": "gonka14fxt7xlj74h54u5lz8epz0qeuhpka6xjhzsyq3",
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