---
title: "#84 – Bringing $3M+ in New Capital to GONKA via Uniswap — Phase 1/6 ($50k USDT)"
description: "My name is Andrey Orlovsky, and through this proposal I represent our team and an initiative to attract at least $3 million in new long-term capital to GONKA through Uniswap.

Below is a condensed ver"
template: proposals-proposals-main.html
---

# #84 – Bringing $3M+ in New Capital to GONKA via Uniswap — Phase 1/6 ($50k USDT)

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-voting">Voting</span>

**Proposal ID:** `84`

**Type:** Community Pool Spend, Execute Contract

**Submit:** 2026-07-09 18:14 UTC

**Voting:** 2026-07-09 18:14 UTC → 2026-07-11 18:14 UTC

**Proposer:** [`gonka1njlf4guhkf60tt8z4ayf4sx73nkf5vsumjplat`](https://gonka.gg/address/gonka1njlf4guhkf60tt8z4ayf4sx73nkf5vsumjplat){:target="_blank"}

**Metadata:** [https://gonka.vote/proposal/f341b83c-78f0-4ab2-b8fd-ddc7ac5d9c37](https://gonka.vote/proposal/f341b83c-78f0-4ab2-b8fd-ddc7ac5d9c37)

<div class="prop-funding-line prop-funding-line-voting">20,000 GNK · $50,000 · Community Pool</div>


[View on gonka.gg](https://gonka.gg/network/proposals/84){:target="_blank"}

</div>

My name is Andrey Orlovsky, and through this proposal I represent our team and an initiative to attract at least $3 million in new long-term capital to GONKA through Uniswap.

Below is a condensed version of the proposal. The full version, including all calculations, KPIs, the financial model, and supporting materials, is available via the link at the end and in the metadata.

We propose building a long-term capital acquisition system for GONKA through purchases of the GNK token on Uniswap. The objective of the program is to attract no less than $3,000,000 in new capital. Based on our internal estimates, the potential is $6–7 million. Upon completion of the program, GONKA will receive not only new investors but also a fully operational capital acquisition infrastructure that can be used and scaled further.

The overall program is designed around a budget of $300,000 and is divided into six independent phases of $50,000 each. This proposal covers only the first phase, requesting 50,000 USDT and 20,000 GNK.

The key feature of this proposal is milestone-based funding. Each subsequent phase will be submitted as a separate governance proposal only after the KPI of the previous phase has been achieved. This allows the community to maintain full control over the program and approve further funding solely based on verified results.

The KPI for the first phase is 4x the advertising budget. However, the KPI is not calculated based on the total amount of incoming funds, but on the amount of capital that actually remains within the GONKA ecosystem at the time of verification. For the first phase, this means that with a $50,000 budget, wallets belonging to users acquired by our team must hold at least $200,000 at the time the second proposal is submitted. This approach incentivizes us to attract long-term investors rather than short-term speculative buyers.

The proposal's economics are also entirely performance-based. A portion of our team's compensation is paid only after the KPI has been achieved, and all compensation is proposed to be paid exclusively in GNK tokens, further aligning our interests with those of the project.

To acquire users, we utilize our proprietary funnel: Meta Ads → Landing Page → Telegram → AI Agent → Manager → Uniswap → Long-term user support. Our objective is not merely to generate the first purchase but to build a system that maximizes capital retention and encourages repeat investments.

The full proposal below provides detailed information on all calculations, KPIs, and implementation mechanics:

1. Proposal Overview.
2. Who We Are.
3. What We Propose.
4. KPI & Project Economics.
5. How the Funnel Works.
6. User Retention Strategy.
7. Funding.
8. Team Compensation.
9. Reporting & Transparency.
10. What GONKA Receives.
11. Anti-Fraud Protection & KPI Methodology.
12. Additional Materials.

Full PROPOSAL: <https://gonka.vote/proposal/f341b83c-78f0-4ab2-b8fd-ddc7ac5d9c37>

Demo Telegram Channel: <https://t.me/demo_chanel_gonka>

Additional materials, proof of our work, landing page examples, creatives, advertising accounts, and partnership references: <https://t.me/proposaluniswap>

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:0.0%"></div>
    <div class="prop-tally-no" style="width:0.0%"></div>
    <div class="prop-tally-veto" style="width:100.0%"></div>
    <div class="prop-tally-abstain" style="width:0.0%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes 0 (0.0%)</span>
    <span class="prop-tally-no-text">No 0 (0.0%)</span>
    <span class="prop-tally-veto-text">Veto 273,609 (100.0%)</span>
    <span class="prop-tally-abstain-text">Abstain 0 (0.0%)</span>
    <span class="prop-tally-total-text">Total 273,609 votes</span>
  </div>
</div>


---

## Messages

| # | Type |
| :- | :--- |
| 1 | `/cosmwasm.wasm.v1.MsgExecuteContract` |
| 2 | `/cosmos.distribution.v1beta1.MsgCommunityPoolSpend` |

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
        "amount": "50000000000",
        "denom": "ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4",
        "recipient": "gonka1njlf4guhkf60tt8z4ayf4sx73nkf5vsumjplat"
      }
    },
    "funds": []
  },
  {
    "@type": "/cosmos.distribution.v1beta1.MsgCommunityPoolSpend",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "recipient": "gonka1njlf4guhkf60tt8z4ayf4sx73nkf5vsumjplat",
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