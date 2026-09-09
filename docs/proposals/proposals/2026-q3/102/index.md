---
title: "#102 – Ratify Quant Mesh Limited as the Ledger Integration Counterparty and Fund the Initial Ledger Integration Payment"
description: "6Block proposes that the Gonka community ratify and authorize Quant Mesh Limited as the legal contracting counterparty for the Gonka-Ledger integration and allocate 350,350 USDT from the Community Poo"
template: proposals-proposals-main.html
---

# #102 – Ratify Quant Mesh Limited as the Ledger Integration Counterparty and Fund the Initial Ledger Integration Payment

<div class="prop-detail-header" markdown="1">

<div class="prop-badge-row"><span class="prop-badge prop-voting">Voting</span><span class="prop-vote-countdown prop-vote-countdown-detail" data-deadline="2026-09-11T09:28:14.306648256Z"></span></div>

**Proposal ID:** `102`

**Type:** Execute Contract

**Submit:** 2026-09-09 09:28 UTC

**Voting:** 2026-09-09 09:28 UTC → 2026-09-11 09:28 UTC

**Proposer:** [`gonka15p7s7w2hx0y8095lddd4ummm2y0kwpwljk00aq`](https://gonka.gg/address/gonka15p7s7w2hx0y8095lddd4ummm2y0kwpwljk00aq){:target="_blank"}

**Metadata:** [https://github.com/gonka-ai/gonka/discussions/1589](https://github.com/gonka-ai/gonka/discussions/1589)

<div class="prop-funding-line prop-funding-line-voting">$350,350 · Community Pool</div>


[View on gonka.gg](https://gonka.gg/network/proposals/102){:target="_blank"}

</div>

6Block proposes that the Gonka community ratify and authorize Quant Mesh Limited as the legal contracting counterparty for the Gonka-Ledger integration and allocate 350,350 USDT from the Community Pool to Quant Mesh Limited at [gonka1yqj5xf0wtqgpdmv5v68cus0tp2j5fv7lzcfd6g](https://gonka.gg/address/gonka1yqj5xf0wtqgpdmv5v68cus0tp2j5fv7lzcfd6g).

The allocation consists of 350,000 USDT for the initial Ledger integration payment (275,000 USDT Phase 1 Launch Fees and 75,000 USDT first-year Annual Activation Fee) plus 350 USDT for processing costs. This authorization and funding are strictly limited to the Ledger integration described in the full proposal.

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:0.3%"></div>
    <div class="prop-tally-no" style="width:0.0%"></div>
    <div class="prop-tally-veto" style="width:0.0%"></div>
    <div class="prop-tally-abstain" style="width:0.0%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes <strong>100.0%</strong> (1,742)</span>
    <span class="prop-tally-no-text">No <strong>0.0%</strong> (0)</span>
    <span class="prop-tally-veto-text">Veto <strong>0.0%</strong> (0)</span>
    <span class="prop-tally-abstain-text">Abstain <strong>0.0%</strong> (0)</span>
    <span class="prop-tally-total-text">Total 1,742 votes</span>
    <span class="prop-tally-veto-text">✗ Turnout <strong>0.3%</strong> (1,742 / 513,386) · Quorum <strong>25%</strong> (128,346)</span>
  </div>
</div>



<h2 id="voters">Voters</h2>

<div class="prop-voters-wrap">
<table class="prop-voters">
<thead><tr><th>Voter</th><th>Vote</th></tr></thead>
<tbody>
<tr><td><a href="https://gonka.gg/address/gonka1p2lhgng7tcqju7emk989s5fpdr7k2c3ek6h26m" target="_blank" class="prop-voter-addr">gonka1p2lhgn…k6h26m</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
</tbody>
</table>
</div>

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
        "amount": "350350000000",
        "recipient": "gonka1yqj5xf0wtqgpdmv5v68cus0tp2j5fv7lzcfd6g"
      }
    },
    "funds": []
  }
]
```

</details>
