---
title: "#122 – Ancapex: A DePIN-Native Tokenomics Mechanism for GNK"
description: "Funds two months of work by the Ancapex Team on the design of an alternative GNK tokenomics mechanism: a burn at settlement and emission tied to the work the network does, pricing beyond inference, te"
template: proposals-proposals-main.html
---

# #122 – Ancapex: A DePIN-Native Tokenomics Mechanism for GNK

<div class="prop-detail-header" markdown="1">

<div class="prop-badge-row"><span class="prop-badge prop-voting">Voting</span><span class="prop-vote-countdown prop-vote-countdown-detail" data-deadline="2026-11-28T17:39:10.476229810Z"></span></div>

**Proposal ID:** `122`

**Type:** Community Pool Spend, Execute Contract

**Submit:** 2026-11-26 17:39 UTC

**Voting:** 2026-11-26 17:39 UTC → 2026-11-28 17:39 UTC

**Proposer:** [`gonka12kq9vvlm658wjx8hmsh56w8u4w46mu44de6lmk`](https://gonka.gg/address/gonka12kq9vvlm658wjx8hmsh56w8u4w46mu44de6lmk){:target="_blank"}

**Metadata:** [https://github.com/alancapex/gonka/blob/0c1ec638ba7a79827141b57e11ebaa6f3d635cf0/proposals/depin-tokenomics-mechanism/README.md](https://github.com/alancapex/gonka/blob/0c1ec638ba7a79827141b57e11ebaa6f3d635cf0/proposals/depin-tokenomics-mechanism/README.md)

<div class="prop-funding-line prop-funding-line-voting">200,000 GNK · Community Pool · $50,000 · Community Sale</div>


[View on gonka.gg](https://gonka.gg/network/proposals/122){:target="_blank"}

</div>

Funds two months of work by the Ancapex Team on the design of an alternative GNK tokenomics mechanism: a burn at settlement and emission tied to the work the network does, pricing beyond inference, tested protection against fake work, and an open network model with stress tests. A draft is published as a pull request after one month and the final version after two. The goal is to get this work done quickly without overloading the core team. The fee is 50,000 USDT and 200,000 GNK, paid in a single transfer. No network parameters change with this vote. The full text is in the proposal metadata.

---


<h2 id="voters">Voters</h2>

<div class="prop-voters-wrap">
<table class="prop-voters">
<thead><tr><th>Voter</th><th>Vote</th></tr></thead>
<tbody>
<tr><td><a href="https://gonka.gg/address/gonka1sk6fh7mm74w6hn5wq0667zca00lt3cpr7pfvyv" target="_blank" class="prop-voter-addr">gonka1sk6fh7…7pfvyv</a></td><td><span class="prop-voter-option prop-vote-veto">No_With_Veto 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka1u7s3mpw4654l30vwzlzsxkhfrmscl6p4p80asy" target="_blank" class="prop-voter-addr">gonka1u7s3mp…p80asy</a></td><td><span class="prop-voter-option prop-vote-veto">No_With_Veto 100.0%</span></td></tr>
</tbody>
</table>
</div>

---
## Messages

| # | Type |
| :- | :--- |
| 1 | `/cosmos.distribution.v1beta1.MsgCommunityPoolSpend` |
| 2 | `/cosmwasm.wasm.v1.MsgExecuteContract` |

<details class="prop-contracts" markdown="1">
<summary markdown="1">Contract Details</summary>

```json
[
  {
    "@type": "/cosmos.distribution.v1beta1.MsgCommunityPoolSpend",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "recipient": "gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09",
    "amount": [
      {
        "denom": "ngonka",
        "amount": "200000000000000"
      }
    ]
  },
  {
    "@type": "/cosmwasm.wasm.v1.MsgExecuteContract",
    "sender": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "contract": "gonka18pkq9mwxxlmyq7kr5txhm060wemg2s4u94wvsfd9w2kdc0u99d6spk8pz2",
    "msg": {
      "withdraw_cw20": {
        "contract_addr": "gonka15ggwj9un6qrmu4nj5ev6l7kpdcr00td03ff2mmj4cyhl8u8vjd2qnl3hgk",
        "amount": "50000000000",
        "recipient": "gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09"
      }
    },
    "funds": []
  }
]
```

</details>
