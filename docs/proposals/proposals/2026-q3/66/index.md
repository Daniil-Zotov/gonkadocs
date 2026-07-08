---
title: "#66 – test proposal - 测试方案"
description: "test proposal - 测试方案"
template: proposals-proposals-main.html
---

# #66 – test proposal - 测试方案

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-rejected">Rejected</span>

**Proposal ID:** `66`

**Type:** Execute Contract

**Submit:** 2026-01-01 00:00 UTC

**Voting:**  → 2026-01-02 00:00 UTC

<div class="prop-funding-line">$1,000,000 · Community Pool</div>


[View on gonka.gg](https://gonka.gg/network/proposals/66){:target="_blank"}

</div>

test proposal - 测试方案

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
        "amount": "1000000000000",
        "denom": "ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4",
        "recipient": "gonka1hwyjwehgp6e5pgpg0ye4a7unwu5q9xzljpuwr5"
      }
    },
    "funds": []
  }
]
```

</details>

---