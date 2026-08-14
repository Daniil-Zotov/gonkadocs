---
title: "#95 – Migrate community-sale and wrapped-token contracts"
description: "Migrate the live community-sale contract and all wrapped-token instances to newly stored CosmWasm code, and register that wrapped-token code for future instantiations. Contract addresses and balances "
template: proposals-proposals-main.html
---

# #95 – Migrate community-sale and wrapped-token contracts

<div class="prop-detail-header" markdown="1">

<div class="prop-badge-row"><span class="prop-badge prop-voting">Voting</span><span class="prop-vote-countdown prop-vote-countdown-detail" data-deadline="2026-08-14T12:01:21.830543380Z"></span></div>

**Proposal ID:** `95`

**Type:** Migrate All Wrapped Tokens, Migrate Contract, Register Wrapped Token Contract

**Submit:** 2026-08-14 00:01 UTC

**Voting:** 2026-08-14 00:01 UTC → 2026-08-14 12:01 UTC

**Expedited:** Yes

**Proposer:** [`gonka1xhjakeqrm69fvdm38e0rh0suy0kzc4m2ruwlhp`](https://gonka.gg/address/gonka1xhjakeqrm69fvdm38e0rh0suy0kzc4m2ruwlhp){:target="_blank"}



[View on gonka.gg](https://gonka.gg/network/proposals/95){:target="_blank"}

</div>

Migrate the live community-sale contract and all wrapped-token instances to newly stored CosmWasm code, and register that wrapped-token code for future instantiations. Contract addresses and balances are unchanged. No chain binary upgrade. This mitigates a theoretical risk identified in a security report and is not expected to affect normal operation.

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:2.1%"></div>
    <div class="prop-tally-no" style="width:0.2%"></div>
    <div class="prop-tally-veto" style="width:0.0%"></div>
    <div class="prop-tally-abstain" style="width:0.7%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes <strong>67.8%</strong> (11,361)</span>
    <span class="prop-tally-no-text">No <strong>7.8%</strong> (1,312)</span>
    <span class="prop-tally-veto-text">Veto <strong>0.0%</strong> (0)</span>
    <span class="prop-tally-abstain-text">Abstain <strong>24.3%</strong> (4,074)</span>
    <span class="prop-tally-total-text">Total 16,747 votes</span>
    <span class="prop-tally-veto-text">✗ Turnout <strong>3.0%</strong> (16,747 / 554,181) · Quorum <strong>25%</strong> (138,545)</span>
  </div>
</div>



<h2 id="voters">Voters</h2>

<div class="prop-voters-wrap">
<table class="prop-voters">
<thead><tr><th>Voter</th><th>Vote</th></tr></thead>
<tbody>
<tr><td><a href="https://gonka.gg/address/gonka1qh2qe4y988c92wl6l3mn0xp9dvzvnavayy3k5f" target="_blank" class="prop-voter-addr">gonka1qh2qe4…yy3k5f</a></td><td><span class="prop-voter-option prop-vote-no">No 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka1p2lhgng7tcqju7emk989s5fpdr7k2c3ek6h26m" target="_blank" class="prop-voter-addr">gonka1p2lhgn…k6h26m</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka1z5vtvu3vv6jcvqzsk6k9kghunjstllyzjwzxa4" target="_blank" class="prop-voter-addr">gonka1z5vtvu…jwzxa4</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka1ym3np7guxart483yfdxnlztuazx22cjt0e4a2p" target="_blank" class="prop-voter-addr">gonka1ym3np7…0e4a2p</a></td><td><span class="prop-voter-option prop-vote-abstain">Abstain 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka1xwkesaxvdadh9wt9yyladu0r260s7whklcktds" target="_blank" class="prop-voter-addr">gonka1xwkesa…lcktds</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka18xeqnspxpg2vncufnjne485rkaagwvz7whyn0d" target="_blank" class="prop-voter-addr">gonka18xeqns…whyn0d</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka1830lqug50lse998x2lakk4pj5ypfumz5pasz0y" target="_blank" class="prop-voter-addr">gonka1830lqu…pasz0y</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka1d7p03cu2y2yt3vytq9wlfm6tlz0lfhlgv9h82p" target="_blank" class="prop-voter-addr">gonka1d7p03c…v9h82p</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka1wknl635whfevh45stw0ethcm9hrw0jrvgeuytr" target="_blank" class="prop-voter-addr">gonka1wknl63…geuytr</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09" target="_blank" class="prop-voter-addr">gonka10mmdja…vqgz09</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 37.0%</span> <span class="prop-voter-option prop-vote-no">No 34.0%</span> <span class="prop-voter-option prop-vote-abstain">Abstain 29.0%</span></td></tr>
</tbody>
</table>
</div>

---
## Messages

| # | Type |
| :- | :--- |
| 1 | `/cosmwasm.wasm.v1.MsgMigrateContract` |
| 2 | `/inference.inference.MsgRegisterWrappedTokenContract` |
| 3 | `/inference.inference.MsgMigrateAllWrappedTokens` |

<details class="prop-contracts" markdown="1">
<summary markdown="1">Contract Details</summary>

```json
[
  {
    "@type": "/cosmwasm.wasm.v1.MsgMigrateContract",
    "sender": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "contract": "gonka18pkq9mwxxlmyq7kr5txhm060wemg2s4u94wvsfd9w2kdc0u99d6spk8pz2",
    "code_id": "113",
    "msg": {}
  },
  {
    "@type": "/inference.inference.MsgRegisterWrappedTokenContract",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "code_id": "114"
  },
  {
    "@type": "/inference.inference.MsgMigrateAllWrappedTokens",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "new_code_id": "114",
    "migrate_msg_json": "{}",
    "limit": 0
  }
]
```

</details>
