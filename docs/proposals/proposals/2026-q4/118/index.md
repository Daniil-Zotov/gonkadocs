---
title: "#118 – Dev Team Funding"
description: "This proposal is to cover two months of work on the Gonka network by MillCreek R&D, Inc., a company founded by Gonka contributors Gleb Morgachev and Anastasia Matveeva. The work includes engineering, "
template: proposals-proposals-main.html
---

# #118 – Dev Team Funding

<div class="prop-detail-header" markdown="1">

<div class="prop-badge-row"><span class="prop-badge prop-voting">Voting</span><span class="prop-vote-countdown prop-vote-countdown-detail" data-deadline="2026-11-13T17:29:39.951923264Z"></span></div>

**Proposal ID:** `118`

**Type:** Execute Contract

**Submit:** 2026-11-11 17:29 UTC

**Voting:** 2026-11-11 17:29 UTC → 2026-11-13 17:29 UTC

**Proposer:** [`gonka18vmr86x9pjmldpckswsfc6lpvapm6u7zm47cn2`](https://gonka.gg/address/gonka18vmr86x9pjmldpckswsfc6lpvapm6u7zm47cn2){:target="_blank"}

**Metadata:** [https://github.com/millcreek-rd/gonka-public/blob/f91e281fd9cb16e2a362dd1a4870c8b1d8b0eefc/proposals/funding/README.md](https://github.com/millcreek-rd/gonka-public/blob/f91e281fd9cb16e2a362dd1a4870c8b1d8b0eefc/proposals/funding/README.md)



[View on gonka.gg](https://gonka.gg/network/proposals/118){:target="_blank"}

</div>

This proposal is to cover two months of work on the Gonka network by MillCreek R&D, Inc., a company founded by Gonka contributors Gleb Morgachev and Anastasia Matveeva. The work includes engineering, technical review and guidance for external teams, technical marketing, and support for hosts and brokers. The fee is 866,000 USDT, paid from the community pool to MillCreek in a single transfer. The two months run from November 9, 2026 through January 8, 2027. The full scope of work and the terms are in the proposal metadata.

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
      "withdraw_cw20": {
        "contract_addr": "gonka15ggwj9un6qrmu4nj5ev6l7kpdcr00td03ff2mmj4cyhl8u8vjd2qnl3hgk",
        "amount": "866000000000",
        "recipient": "gonka18vmr86x9pjmldpckswsfc6lpvapm6u7zm47cn2"
      }
    },
    "funds": []
  }
]
```

</details>
