---
title: "#45 – Governance Architecture Proposal for the Gonka.ai Network"
description: "Replace scattered governance discussions and complex CLI voting with a unified Governance Portal - a single interface for all Gonka governance activity. The portal includes: a proposal feed across Dis"
template: proposals-proposals-main.html
---

# #45 – Governance Architecture Proposal for the Gonka.ai Network

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-rejected">Rejected</span>

**Proposal ID:** `45`

**Type:** Community Pool Spend

**Submit:** 2026-04-29 20:28 UTC

**Voting:** 2026-04-29 20:28 UTC → 2026-05-01 20:28 UTC

**Proposer:** [`gonka1syw6cs7jl5rmz7gpm3rq3836y2t484xp00ywrz`](https://gonka.gg/address/gonka1syw6cs7jl5rmz7gpm3rq3836y2t484xp00ywrz){:target="_blank"}

**Metadata:** [https://github.com/gonka-ai/gonka/discussions/1104](https://github.com/gonka-ai/gonka/discussions/1104)

**Failed reason:** proposal did not get enough votes to pass

<div class="prop-funding-line">119,000 GNK · Community Pool</div>


[View on gonka.gg](https://gonka.gg/network/proposals/45){:target="_blank"}

</div>

Replace scattered governance discussions and complex CLI voting with a unified Governance Portal - a single interface for all Gonka governance activity. The portal includes: a proposal feed across Discussion/Voting/Archive stages, miner-weighted ranking, crowdfunded deposit collection, targeted notifications (Telegram/email/on-site), and browser-based voting via restricted hot keys (no CLI required). Critical point: this is not just a convenient UI - the crowdfunded deposit mechanism acts as an economic quality filter that screens proposals before they reach on-chain voting, preventing low-effort or spam proposals from consuming validator attention. Funding request: 50,000 USDT (~119,000 GNK), split into Phase 1 MVP (30,000 USDT - portal frontend/backend, wallet auth, deposit crowdfunding) and Phase 2 (20,000 USDT - escrow contracts, dynamic quorum, reputation systems). Code will be open-sourced upon launch. We guarantee 90 days of post-launch support; afterwards, the portal becomes community-owned and further support/maintenance will be funded through community governance votes. Prototype: https://vote-demo.gonkabroker.com. Full discussion: https://github.com/gonka-ai/gonka/discussions/1104.

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:25.6%"></div>
    <div class="prop-tally-no" style="width:0.0%"></div>
    <div class="prop-tally-veto" style="width:45.6%"></div>
    <div class="prop-tally-abstain" style="width:28.8%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes 118,126 (25.6%)</span>
    <span class="prop-tally-no-text">No 0 (0.0%)</span>
    <span class="prop-tally-veto-text">Veto 210,906 (45.6%)</span>
    <span class="prop-tally-abstain-text">Abstain 133,057 (28.8%)</span>
  </div>
</div>


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
    "recipient": "gonka14zlgmrd6v5gaqudxmvkn0yg8g55qpvcep9n6ds",
    "amount": [
      {
        "denom": "ngonka",
        "amount": "119000000000000"
      }
    ]
  }
]
```

</details>

---