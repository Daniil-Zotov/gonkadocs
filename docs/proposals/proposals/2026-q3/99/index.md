---
title: "#99 – Support Gonka's presence at TOKEN2049 Singapore"
description: "6Block proposes that the Gonka community allocate 100,000 USDT from the Community Pool to support Gonka's participation at TOKEN2049 Singapore 2026, taking place on 7-8 October 2026 at Marina Bay Sand"
template: proposals-proposals-main.html
---

# #99 – Support Gonka's presence at TOKEN2049 Singapore

<div class="prop-detail-header" markdown="1">

<div class="prop-badge-row"><span class="prop-badge prop-voting">Voting</span><span class="prop-vote-countdown prop-vote-countdown-detail" data-deadline="2026-09-04T09:53:38.080427980Z"></span></div>

**Proposal ID:** `99`

**Type:** Execute Contract

**Submit:** 2026-09-02 09:53 UTC

**Voting:** 2026-09-02 09:53 UTC → 2026-09-04 09:53 UTC

**Proposer:** [`gonka15p7s7w2hx0y8095lddd4ummm2y0kwpwljk00aq`](https://gonka.gg/address/gonka15p7s7w2hx0y8095lddd4ummm2y0kwpwljk00aq){:target="_blank"}

**Metadata:** [https://github.com/gonka-ai/gonka/discussions/1704](https://github.com/gonka-ai/gonka/discussions/1704)

<div class="prop-funding-line prop-funding-line-voting">$100,000 · Community Pool</div>


[View on gonka.gg](https://gonka.gg/network/proposals/99){:target="_blank"}

</div>

6Block proposes that the Gonka community allocate 100,000 USDT from the Community Pool to support Gonka's participation at TOKEN2049 Singapore 2026, taking place on 7-8 October 2026 at Marina Bay Sands, Singapore.

The requested funds will be used to cover the TOKEN2049 Singapore Gold Sponsorship package and related logistics required to make Gonka's presence effective, including travel, accommodation, local coordination, guest hosting, event operations, and supporting materials.

---

## Messages

| # | Type |
| :- | :--- |
| 1 | `/cosmwasm.wasm.v1.MsgExecuteContract` |

<details class="prop-contracts" markdown="1">
<summary markdown="1">Contract Details</summary>

```json
[
  {
    "@type": "/cosmwasm.wasm.v1.MsgExecuteContract",
    "sender": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "contract": "gonka18pkq9mwxxlmyq7kr5txhm060wemg2s4u94wvsfd9w2kdc0u99d6spk8pz2",
    "msg": {
      "withdraw_ibc": {
        "denom": "ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4",
        "amount": "100000000000",
        "recipient": "gonka1yqj5xf0wtqgpdmv5v68cus0tp2j5fv7lzcfd6g"
      }
    },
    "funds": []
  }
]
```

</details>
