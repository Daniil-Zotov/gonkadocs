---
title: "#95 – Migrate community-sale and wrapped-token contracts"
description: "Migrate the live community-sale contract and all wrapped-token instances to newly stored CosmWasm code, and register that wrapped-token code for future instantiations. Contract addresses and balances "
template: proposals-proposals-main.html
---

# #95 – Migrate community-sale and wrapped-token contracts

<div class="prop-detail-header" markdown="1">

<div class="prop-badge-row"><span class="prop-badge prop-voting">Voting</span><span class="prop-vote-countdown prop-vote-countdown-detail" data-deadline="2026-08-16T00:01:21.830543380Z"></span></div>

**Proposal ID:** `95`

**Type:** Migrate All Wrapped Tokens, Migrate Contract, Register Wrapped Token Contract

**Submit:** 2026-08-14 00:01 UTC

**Voting:** 2026-08-14 00:01 UTC → 2026-08-16 00:01 UTC

**Proposer:** [`gonka1xhjakeqrm69fvdm38e0rh0suy0kzc4m2ruwlhp`](https://gonka.gg/address/gonka1xhjakeqrm69fvdm38e0rh0suy0kzc4m2ruwlhp){:target="_blank"}



[View on gonka.gg](https://gonka.gg/network/proposals/95){:target="_blank"}

</div>

Migrate the live community-sale contract and all wrapped-token instances to newly stored CosmWasm code, and register that wrapped-token code for future instantiations. Contract addresses and balances are unchanged. No chain binary upgrade. This mitigates a theoretical risk identified in a security report and is not expected to affect normal operation.

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:1.9%"></div>
    <div class="prop-tally-no" style="width:0.0%"></div>
    <div class="prop-tally-veto" style="width:0.0%"></div>
    <div class="prop-tally-abstain" style="width:0.0%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes <strong>100.0%</strong> (11,464)</span>
    <span class="prop-tally-no-text">No <strong>0.0%</strong> (0)</span>
    <span class="prop-tally-veto-text">Veto <strong>0.0%</strong> (0)</span>
    <span class="prop-tally-abstain-text">Abstain <strong>0.0%</strong> (0)</span>
    <span class="prop-tally-total-text">Total 11,464 votes</span>
    <span class="prop-tally-veto-text">✗ Turnout <strong>1.9%</strong> (11,464 / 587,914) · Quorum <strong>25%</strong> (146,978)</span>
  </div>
</div>



<h2 id="voters">Voters</h2>

<div class="prop-voters-wrap">
<table class="prop-voters">
<thead><tr><th>Voter</th><th>Vote</th></tr></thead>
<tbody>
<tr><td><a href="https://gonka.gg/address/gonka1tlvg4kjx7ljd5thgd5fkgh39q6lu8cmxupktgg" target="_blank" class="prop-voter-addr">gonka1tlvg4k…upktgg</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka1d694r00czmq75txghwjcuk07lxvc8d4ekgsha0" target="_blank" class="prop-voter-addr">gonka1d694r0…kgsha0</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka168rtjfkszuhcggg4dfyse4yh7xn9zwfglnkns2" target="_blank" class="prop-voter-addr">gonka168rtjf…lnkns2</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
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
