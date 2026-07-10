---
title: "#82 – External Test Lab x Community DevNet"
description: "4-month pilot of the External Test Lab & Community DevNet: a community-owned testing layer for Gonka. Full proposal and discussion: https://github.com/gonka-ai/gonka/discussions/1388

The budget is he"
template: proposals-proposals-main.html
---

# #82 – External Test Lab x Community DevNet

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-voting">Voting</span>

**Proposal ID:** `82`

**Type:** Community Pool Spend, Execute Contract, Instantiate Contract2

**Submit:** 2026-07-08 11:31 UTC

**Voting:** 2026-07-08 11:31 UTC → 2026-07-10 11:31 UTC

**Proposer:** [`gonka1k6p754pyhxud2399knyccgjpjvdafj2u9xlgyf`](https://gonka.gg/address/gonka1k6p754pyhxud2399knyccgjpjvdafj2u9xlgyf){:target="_blank"}

**Metadata:** [https://github.com/gonka-ai/gonka/discussions/1388](https://github.com/gonka-ai/gonka/discussions/1388)

<div class="prop-funding-line prop-funding-line-voting">80,000 GNK · $88,000 · Community Pool</div>


[View on gonka.gg](https://gonka.gg/network/proposals/82){:target="_blank"}

</div>

4-month pilot of the External Test Lab & Community DevNet: a community-owned testing layer for Gonka. Full proposal and discussion: <https://github.com/gonka-ai/gonka/discussions/1388>

The budget is held by an immutable escrow contract and released as 4 monthly tranches of 22,000 USDT plus 2x40,000 GNK recognition to the Project and Infrastructure Leads at the end of the pilot. Month 1 is prepaid; each next tranche unlocks 4 days after the month ends. Hosts can always cancel via a one-time governance clawback that returns all remaining funds to the Community Pool.

Contract: code_id 107, checksum 94b141625b7641e6ad57266420b18a4af72eac49b8110cb92719755590b463bd, escrow address [gonka1g57f45qjvn0529vpgj8x8mzt8r5k4audchm3pp9pezywxwf4rexqlj8ayw](https://gonka.gg/address/gonka1g57f45qjvn0529vpgj8x8mzt8r5k4audchm3pp9pezywxwf4rexqlj8ayw). No admin, no migration - recipients and amounts can never change. Source and verification: <https://github.com/paranjko/testlab-devnet-escrow/tree/1b2e529876141816b5c2130840d04fb93694bf72>

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:98.2%"></div>
    <div class="prop-tally-no" style="width:0.1%"></div>
    <div class="prop-tally-veto" style="width:0.0%"></div>
    <div class="prop-tally-abstain" style="width:1.6%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes 365,526 (98.2%)</span>
    <span class="prop-tally-no-text">No 468 (0.1%)</span>
    <span class="prop-tally-veto-text">Veto 94 (0.0%)</span>
    <span class="prop-tally-abstain-text">Abstain 6,141 (1.6%)</span>
    <span class="prop-tally-total-text">Total 372,229 votes</span>
  </div>
</div>


---

## Messages

| # | Type |
| :- | :--- |
| 1 | `/cosmwasm.wasm.v1.MsgInstantiateContract2` |
| 2 | `/cosmos.distribution.v1beta1.MsgCommunityPoolSpend` |
| 3 | `/cosmwasm.wasm.v1.MsgExecuteContract` |

<details class="prop-contracts" markdown="1">
<summary markdown="1">Contract Details</summary>

```json
[
  {
    "@type": "/cosmwasm.wasm.v1.MsgInstantiateContract2",
    "sender": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "admin": "",
    "code_id": "107",
    "label": "testlab-devnet-milestone-escrow",
    "msg": {
      "governance": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
      "payouts": [
        {
          "recipient": "gonka1pn5953zm5j29w23u8csz4uuqwpg486j05e9aj4",
          "denom": "ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4",
          "amount": "22000000000",
          "unlock_after_days": 0
        },
        {
          "recipient": "gonka1pn5953zm5j29w23u8csz4uuqwpg486j05e9aj4",
          "denom": "ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4",
          "amount": "22000000000",
          "unlock_after_days": 34
        },
        {
          "recipient": "gonka1pn5953zm5j29w23u8csz4uuqwpg486j05e9aj4",
          "denom": "ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4",
          "amount": "22000000000",
          "unlock_after_days": 64
        },
        {
          "recipient": "gonka1pn5953zm5j29w23u8csz4uuqwpg486j05e9aj4",
          "denom": "ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4",
          "amount": "22000000000",
          "unlock_after_days": 94
        },
        {
          "recipient": "gonka1pn5953zm5j29w23u8csz4uuqwpg486j05e9aj4",
          "denom": "ngonka",
          "amount": "40000000000000",
          "unlock_after_days": 124
        },
        {
          "recipient": "gonka1fx65y7jfce6q4cj3zf7wvfuse3juu7c8gg0hqp",
          "denom": "ngonka",
          "amount": "40000000000000",
          "unlock_after_days": 124
        }
      ],
      "close_after_days": 200
    },
    "funds": [],
    "salt": "dGVzdGxhYi1kZXZuZXQtcGlsb3Q=",
    "fix_msg": false
  },
  {
    "@type": "/cosmos.distribution.v1beta1.MsgCommunityPoolSpend",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "recipient": "gonka1g57f45qjvn0529vpgj8x8mzt8r5k4audchm3pp9pezywxwf4rexqlj8ayw",
    "amount": [
      {
        "denom": "ngonka",
        "amount": "80000000000000"
      }
    ]
  },
  {
    "@type": "/cosmwasm.wasm.v1.MsgExecuteContract",
    "sender": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "contract": "gonka18pkq9mwxxlmyq7kr5txhm060wemg2s4u94wvsfd9w2kdc0u99d6spk8pz2",
    "msg": {
      "withdraw_ibc": {
        "denom": "ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4",
        "amount": "88000000000",
        "recipient": "gonka1g57f45qjvn0529vpgj8x8mzt8r5k4audchm3pp9pezywxwf4rexqlj8ayw"
      }
    },
    "funds": []
  }
]
```

</details>

---