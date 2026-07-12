---
title: "#43 – Governance Architecture Proposal for the Gonka.ai Network"
description: "Today, participating in Gonka governance requires following multiple channels simultaneously — GitHub, Discord, CLI — just to cast a single vote. Most miners miss proposals entirely or vote too late. "
template: proposals-proposals-main.html
---

# #43 – Governance Architecture Proposal for the Gonka.ai Network

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-rejected">Rejected</span>

**Proposal ID:** `43`

**Type:** Community Pool Spend

**Submit:** 2026-04-25 10:09 UTC

**Voting:** 2026-04-25 10:09 UTC → 2026-04-27 10:09 UTC

**Proposer:** [`gonka1syw6cs7jl5rmz7gpm3rq3836y2t484xp00ywrz`](https://gonka.gg/address/gonka1syw6cs7jl5rmz7gpm3rq3836y2t484xp00ywrz){:target="_blank"}

**Metadata:** [https://github.com/gonka-ai/gonka/discussions/1104](https://github.com/gonka-ai/gonka/discussions/1104)

**Failed reason:** proposal did not get enough votes to pass

<div class="prop-funding-line prop-funding-line-rejected">104,166 GNK · Community Pool</div>


[View on gonka.gg](https://gonka.gg/network/proposals/43){:target="_blank"}

</div>

Today, participating in Gonka governance requires following multiple channels simultaneously — GitHub, Discord, CLI — just to cast a single vote. Most miners miss proposals entirely or vote too late. Low participation threatens quorum and undermines the network's ability to make decisions. We propose a unified Governance Portal that brings all governance activity into one place: a proposal feed, miner-weighted ratings, deposit crowdfunding, and browser-based voting via a restricted hot key. No CLI required. No missed votes. Funding request: 50,000 USDT equivalent in GNK, paid in full upon approval. Full proposal and prototype: <https://github.com/gonka-ai/gonka/discussions/1104>

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:26.5%"></div>
    <div class="prop-tally-no" style="width:72.2%"></div>
    <div class="prop-tally-veto" style="width:1.3%"></div>
    <div class="prop-tally-abstain" style="width:0.0%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes 123,104 (26.5%)</span>
    <span class="prop-tally-no-text">No 335,534 (72.2%)</span>
    <span class="prop-tally-veto-text">Veto 5,913 (1.3%)</span>
    <span class="prop-tally-abstain-text">Abstain 0 (0.0%)</span>
    <span class="prop-tally-total-text">Total 464,551 votes</span>
    
  </div>
</div>


---

## Messages

| # | Type |
| :- | :--- |
| 1 | `/cosmos.distribution.v1beta1.MsgCommunityPoolSpend` |

<details class="prop-contracts" markdown="1">
<summary markdown="1">Contract Details</summary>

```json
[
  {
    "@type": "/cosmos.distribution.v1beta1.MsgCommunityPoolSpend",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "recipient": "gonka14zlgmrd6v5gaqudxmvkn0yg8g55qpvcep9n6ds",
    "amount": [
      {
        "denom": "ngonka",
        "amount": "104166000000000"
      }
    ]
  }
]
```

</details>
