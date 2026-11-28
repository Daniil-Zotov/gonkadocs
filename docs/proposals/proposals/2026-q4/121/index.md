---
title: "#121 – Ancapex: Decision Models for Modest Hardware"
description: "Funds two months of work by the Ancapex Team to bring decision models to Gonka: integration into confirmation PoC, validation and tokenomics, a choice of two open-weight base models, a pull request an"
template: proposals-proposals-main.html
---

# #121 – Ancapex: Decision Models for Modest Hardware

<div class="prop-detail-header" markdown="1">

<div class="prop-badge-row"><span class="prop-badge prop-voting">Voting</span><span class="prop-vote-countdown prop-vote-countdown-detail" data-deadline="2026-11-28T17:38:37.076052013Z"></span></div>

**Proposal ID:** `121`

**Type:** Community Pool Spend, Execute Contract

**Submit:** 2026-11-26 17:38 UTC

**Voting:** 2026-11-26 17:38 UTC → 2026-11-28 17:38 UTC

**Proposer:** [`gonka12kq9vvlm658wjx8hmsh56w8u4w46mu44de6lmk`](https://gonka.gg/address/gonka12kq9vvlm658wjx8hmsh56w8u4w46mu44de6lmk){:target="_blank"}

**Metadata:** [https://github.com/alancapex/gonka/blob/0f7926833be2de01a7dee092cfbfa75d2f99de75/proposals/decision-models/README.md](https://github.com/alancapex/gonka/blob/0f7926833be2de01a7dee092cfbfa75d2f99de75/proposals/decision-models/README.md)

<div class="prop-funding-line prop-funding-line-voting">150,000 GNK · Community Pool · $40,000 · Community Sale</div>


[View on gonka.gg](https://gonka.gg/network/proposals/121){:target="_blank"}

</div>

Funds two months of work by the Ancapex Team to bring decision models to Gonka: integration into confirmation PoC, validation and tokenomics, a choice of two open-weight base models, a pull request and a testnet launch, and a reference training scheme. A draft is published as a pull request after one month and the final solution after two. The goal is to get this work done quickly without overloading the core team. The fee is 40,000 USDT and 150,000 GNK, paid in a single transfer. No network parameters change with this vote. The full text is in the proposal metadata.

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:0.0%"></div>
    <div class="prop-tally-no" style="width:0.0%"></div>
    <div class="prop-tally-veto" style="width:40.9%"></div>
    <div class="prop-tally-abstain" style="width:0.0%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes <strong>0.0%</strong> (0)</span>
    <span class="prop-tally-no-text">No <strong>0.0%</strong> (0)</span>
    <span class="prop-tally-veto-text">Veto <strong>100.0%</strong> (553,196)</span>
    <span class="prop-tally-abstain-text">Abstain <strong>0.0%</strong> (0)</span>
    <span class="prop-tally-total-text">Total 553,196 votes</span>
    <span class="prop-tally-yes-text">✓ Turnout <strong>40.9%</strong> (553,196 / 1,354,053) · Quorum <strong>25%</strong> (338,513)</span>
  </div>
</div>



<h2 id="voters">Voters</h2>

<div class="prop-voters-wrap">
<table class="prop-voters">
<thead><tr><th>Voter</th><th>Vote</th></tr></thead>
<tbody>
<tr><td><a href="https://gonka.gg/address/gonka1sk6fh7mm74w6hn5wq0667zca00lt3cpr7pfvyv" target="_blank" class="prop-voter-addr">gonka1sk6fh7…7pfvyv</a></td><td><span class="prop-voter-option prop-vote-veto">No_With_Veto 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka1nurzpppvn0lxg20v2c3gf8zfltpdpz599rggst" target="_blank" class="prop-voter-addr">gonka1nurzpp…9rggst</a></td><td><span class="prop-voter-option prop-vote-veto">No_With_Veto 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka147qfckm9hpdzd9dgfvfj2r5rsv0eeunj4gpvz8" target="_blank" class="prop-voter-addr">gonka147qfck…4gpvz8</a></td><td><span class="prop-voter-option prop-vote-veto">No_With_Veto 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka1kvmerzu64094dt9t62ea0cp75larh39ulzldum" target="_blank" class="prop-voter-addr">gonka1kvmerz…lzldum</a></td><td><span class="prop-voter-option prop-vote-veto">No_With_Veto 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka16dgkvx7mh609ntkzknckwaskgq9lcdp86j0skk" target="_blank" class="prop-voter-addr">gonka16dgkvx…6j0skk</a></td><td><span class="prop-voter-option prop-vote-veto">No_With_Veto 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka1ue6k3pcgdg2g962l2n0g8hpg3r4vf827a4hpgh" target="_blank" class="prop-voter-addr">gonka1ue6k3p…a4hpgh</a></td><td><span class="prop-voter-option prop-vote-no">No 100.0%</span></td></tr>
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
        "amount": "150000000000000"
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
        "amount": "40000000000",
        "recipient": "gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09"
      }
    },
    "funds": []
  }
]
```

</details>
