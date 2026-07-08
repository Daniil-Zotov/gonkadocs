---
title: "#51 – Support Gonka's presence at WebX Asia"
description: "6Block, a long-term Gonka mining and infrastructure participant, proposes that the Gonka community allocate 75,000 USDT to support Gonka's participation at WebX Asia / WebX 2026 in Tokyo. 6Block has a"
template: proposals-proposals-main.html
---

# #51 – Support Gonka's presence at WebX Asia

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-passed">Passed</span>

**Proposal ID:** `51`

**Type:** Execute Contract

**Submit:** 2026-01-01 00:00 UTC

**Voting:**  → 2026-01-02 00:00 UTC

<div class="prop-funding-line">$75,000 · Community Pool</div>


[View on gonka.gg](https://gonka.gg/network/proposals/51){:target="_blank"}

</div>

6Block, a long-term Gonka mining and infrastructure participant, proposes that the Gonka community allocate 75,000 USDT to support Gonka's participation at WebX Asia / WebX 2026 in Tokyo. 6Block has a

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
        "amount": "75000000000",
        "recipient": "gonka1yqj5xf0wtqgpdmv5v68cus0tp2j5fv7lzcfd6g"
      }
    },
    "funds": []
  }
]
```

</details>

---