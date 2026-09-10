---
title: "#103 – Reimbursement of Expenses for Daniil and David Liberman's Participation in All-In Summit 2026"
description: "We are proposing to allocate 15,500 USDT from the Gonka Community Pool to reimburse the cost of two tickets for All-In Summit 2026 for Daniil and David Liberman, co-creators of the Gonka protocol.
All"
template: proposals-proposals-main.html
---

# #103 – Reimbursement of Expenses for Daniil and David Liberman's Participation in All-In Summit 2026

<div class="prop-detail-header" markdown="1">

<div class="prop-badge-row"><span class="prop-badge prop-voting">Voting</span><span class="prop-vote-countdown prop-vote-countdown-detail" data-deadline="2026-09-12T13:31:12.594032166Z"></span></div>

**Proposal ID:** `103`

**Type:** Execute Contract

**Submit:** 2026-09-10 13:31 UTC

**Voting:** 2026-09-10 13:31 UTC → 2026-09-12 13:31 UTC

**Proposer:** [`gonka12m252y2vfy25ygwgzl4gn7fusds7p0ak2klxf7`](https://gonka.gg/address/gonka12m252y2vfy25ygwgzl4gn7fusds7p0ak2klxf7){:target="_blank"}

**Metadata:** [https://github.com/gonka-ai/gonka/discussions/1747](https://github.com/gonka-ai/gonka/discussions/1747)

<div class="prop-funding-line prop-funding-line-voting">$15,500 · Community Pool</div>


[View on gonka.gg](https://gonka.gg/network/proposals/103){:target="_blank"}

</div>

We are proposing to allocate 15,500 USDT from the Gonka Community Pool to reimburse the cost of two tickets for All-In Summit 2026 for Daniil and David Liberman, co-creators of the Gonka protocol.
All-In Summit will take place on September 13–15, 2026, in Los Angeles and will bring together more than 2,500 hand-selected attendees, including tech founders, investors, executives, and leaders from the AI industry.
The standard Attendee Pass costs $7,500 per person. The tickets have already been paid for. The requested reimbursement covers only the cost of the two tickets plus transaction fees for withdrawing the funds. Flights, accommodation, and any other expenses are not being requested from the Community Pool under this proposal.

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
        "amount": "15500000000",
        "recipient": "gonka1xpm5dlr8mpn9s4z4lzz8pvwt9y2t0kwgsfm2w2"
      }
    },
    "funds": []
  }
]
```

</details>
