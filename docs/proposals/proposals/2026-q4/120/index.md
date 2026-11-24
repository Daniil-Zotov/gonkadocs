---
title: "#120 – Quorint: Bridge Relaunch Security Review + 6-Month Attack Registry, Economic Attack Simulator & Upgrade Audits (Roadmap Track 6 P3, Track 5 P1/P2)"
description: "Funds a 24-week security engagement with Quorint (https://quorint.xyz): an independent security review for the Gonka-Ethereum bridge relaunch after the 18 November 2026 incident (Roadmap Track 6 P3), "
template: proposals-proposals-main.html
---

# #120 – Quorint: Bridge Relaunch Security Review + 6-Month Attack Registry, Economic Attack Simulator & Upgrade Audits (Roadmap Track 6 P3, Track 5 P1/P2)

<div class="prop-detail-header" markdown="1">

<div class="prop-badge-row"><span class="prop-badge prop-voting">Voting</span><span class="prop-vote-countdown prop-vote-countdown-detail" data-deadline="2026-11-26T14:01:24.806179168Z"></span></div>

**Proposal ID:** `120`

**Type:** Community Pool Spend, Instantiate Contract2

**Submit:** 2026-11-24 14:01 UTC

**Voting:** 2026-11-24 14:01 UTC → 2026-11-26 14:01 UTC

**Proposer:** [`gonka1ggt0d4jqmztnmh86na3m99c9d3q7s6h2dkd2qv`](https://gonka.gg/address/gonka1ggt0d4jqmztnmh86na3m99c9d3q7s6h2dkd2qv){:target="_blank"}

**Metadata:** [https://github.com/quorint/gonka-security-proposal/blob/dec028b64bd5ec09db2b2a26b858610b1ffd0dfb/README.md](https://github.com/quorint/gonka-security-proposal/blob/dec028b64bd5ec09db2b2a26b858610b1ffd0dfb/README.md)

<div class="prop-funding-line prop-funding-line-voting">1,600,000 GNK · Community Pool</div>


[View on gonka.gg](https://gonka.gg/network/proposals/120){:target="_blank"}

</div>

Funds a 24-week security engagement with Quorint (<https://quorint.xyz>): an independent security review for the Gonka-Ethereum bridge relaunch after the 18 November 2026 incident (Roadmap Track 6 P3), an executable attack registry (Track 5 P1), an economic attack simulator (Track 5 P2) and pre-mainnet upgrade audits. Allocates 1,600,000 GNK from the Community Pool (no USDT) to a new instance of the code_id 107 milestone escrow used by Proposal #82 (escrow [gonka1m5gr4pkemg7fyml3jlkecpvxzprrkglfu05jfe8kmm38780ajp5s9qznhg](https://gonka.gg/address/gonka1m5gr4pkemg7fyml3jlkecpvxzprrkglfu05jfe8kmm38780ajp5s9qznhg), no admin, no migration), paying Quorint ([gonka1ggt0d4jqmztnmh86na3m99c9d3q7s6h2dkd2qv](https://gonka.gg/address/gonka1ggt0d4jqmztnmh86na3m99c9d3q7s6h2dkd2qv)) in six tranches on days 0, 45, 90, 135, 180 and 210: 250,000 / 300,000 / 300,000 / 300,000 / 250,000 / 200,000 GNK. A public milestone report is due 5 days before each unlock. Governance can claw back everything still in the escrow with one vote; after day 270 anyone can sweep the remainder to the Community Pool. Full commit-pinned proposal: <https://github.com/quorint/gonka-security-proposal/blob/dec028b64bd5ec09db2b2a26b858610b1ffd0dfb/README.md>

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:0.0%"></div>
    <div class="prop-tally-no" style="width:0.0%"></div>
    <div class="prop-tally-veto" style="width:0.0%"></div>
    <div class="prop-tally-abstain" style="width:0.0%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes <strong>0.0%</strong> (0)</span>
    <span class="prop-tally-no-text">No <strong>100.0%</strong> (1)</span>
    <span class="prop-tally-veto-text">Veto <strong>0.0%</strong> (0)</span>
    <span class="prop-tally-abstain-text">Abstain <strong>0.0%</strong> (0)</span>
    <span class="prop-tally-total-text">Total 1 votes</span>
    <span class="prop-tally-veto-text">✗ Turnout <strong>0.0%</strong> (1 / 1,908,722) · Quorum <strong>25%</strong> (477,180)</span>
  </div>
</div>



<h2 id="voters">Voters</h2>

<div class="prop-voters-wrap">
<table class="prop-voters">
<thead><tr><th>Voter</th><th>Vote</th></tr></thead>
<tbody>
<tr><td><a href="https://gonka.gg/address/gonka1pdgu7gmuc2w36enw2fag3n24xxhgmfgx9rs7a0" target="_blank" class="prop-voter-addr">gonka1pdgu7g…9rs7a0</a></td><td><span class="prop-voter-option prop-vote-no">No 100.0%</span></td></tr>
</tbody>
</table>
</div>

---
## Messages

| # | Type |
| :- | :--- |
| 1 | `/cosmwasm.wasm.v1.MsgInstantiateContract2` |
| 2 | `/cosmos.distribution.v1beta1.MsgCommunityPoolSpend` |

<details class="prop-contracts" markdown="1">
<summary markdown="1">Contract Details</summary>

```json
[
  {
    "@type": "/cosmwasm.wasm.v1.MsgInstantiateContract2",
    "sender": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "admin": "",
    "code_id": "107",
    "label": "quorint-security-milestone-escrow",
    "msg": {
      "governance": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
      "payouts": [
        {
          "recipient": "gonka1ggt0d4jqmztnmh86na3m99c9d3q7s6h2dkd2qv",
          "denom": "ngonka",
          "amount": "250000000000000",
          "unlock_after_days": 0
        },
        {
          "recipient": "gonka1ggt0d4jqmztnmh86na3m99c9d3q7s6h2dkd2qv",
          "denom": "ngonka",
          "amount": "300000000000000",
          "unlock_after_days": 45
        },
        {
          "recipient": "gonka1ggt0d4jqmztnmh86na3m99c9d3q7s6h2dkd2qv",
          "denom": "ngonka",
          "amount": "300000000000000",
          "unlock_after_days": 90
        },
        {
          "recipient": "gonka1ggt0d4jqmztnmh86na3m99c9d3q7s6h2dkd2qv",
          "denom": "ngonka",
          "amount": "300000000000000",
          "unlock_after_days": 135
        },
        {
          "recipient": "gonka1ggt0d4jqmztnmh86na3m99c9d3q7s6h2dkd2qv",
          "denom": "ngonka",
          "amount": "250000000000000",
          "unlock_after_days": 180
        },
        {
          "recipient": "gonka1ggt0d4jqmztnmh86na3m99c9d3q7s6h2dkd2qv",
          "denom": "ngonka",
          "amount": "200000000000000",
          "unlock_after_days": 210
        }
      ],
      "close_after_days": 270
    },
    "funds": [],
    "salt": "cXVvcmludC1nb25rYS1zZWN1cml0eS0yMDI2",
    "fix_msg": false
  },
  {
    "@type": "/cosmos.distribution.v1beta1.MsgCommunityPoolSpend",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "recipient": "gonka1m5gr4pkemg7fyml3jlkecpvxzprrkglfu05jfe8kmm38780ajp5s9qznhg",
    "amount": [
      {
        "denom": "ngonka",
        "amount": "1600000000000000"
      }
    ]
  }
]
```

</details>
