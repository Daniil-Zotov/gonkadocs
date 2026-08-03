---
title: "#85 – Internal Go-To-Market Team for 3 Month"
description: "We will run hundreds of experiments across different target audience hypotheses and set up the basis: acquisition funnels, analytics, sharable target audience deep understanding. Our key performance m"
template: proposals-proposals-main.html
---

# #85 – Internal Go-To-Market Team for 3 Month

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-rejected">Rejected</span>

**Proposal ID:** `85`

**Type:** Community Pool Spend, Execute Contract, Instantiate Contract2

**Submit:** 2026-07-10 00:41 UTC

**Voting:** 2026-07-10 00:41 UTC → 2026-07-12 00:41 UTC

**Proposer:** [`gonka1vfafh4jq674227q8j0h33fwz4jmgtxmp4vsd93`](https://gonka.gg/address/gonka1vfafh4jq674227q8j0h33fwz4jmgtxmp4vsd93){:target="_blank"}

**Metadata:** [https://app.integrity.sh/p/SuMCnGQBhz-0asAYBUz1U](https://app.integrity.sh/p/SuMCnGQBhz-0asAYBUz1U)

**Failed reason:** proposal did not get enough votes to pass

<div class="prop-funding-line prop-funding-line-rejected">600,000 GNK · $36,000 · Community Pool</div>


[View on gonka.gg](https://gonka.gg/network/proposals/85){:target="_blank"}

</div>

We will run hundreds of experiments across different target audience hypotheses and set up the basis: acquisition funnels, analytics, sharable target audience deep understanding. Our key performance metric is the number of non-ru-speaking users, who pay for inference or invest in GNK.
The full proposal: <https://app.integrity.sh/p/SuMCnGQBhz-0asAYBUz1U>

The budget of 600K GNK and 36K USDT is held by an immutable escrow contract and released as:
180K GNK and 12K USDT in the day 0,
130K GNK and 12K USDT in the day 30,
130K GNK and 12K USDT in the day 60,
160K GNK in the day 99
 — as we need them to promise rewards. We will not sell them by ourselves at least during the 6-month period and we will organise vesting-like payments for the other contributors.

Governance holds an option to cancel the initiative and returns all remaining funds to the Community Pool. We use contract described in <https://github.com/paranjko/testlab-devnet-escrow/tree/1b2e529876141816b5c2130840d04fb93694bf72> (that Sega used in <https://gonka.vote/governance/82>)

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:5.6%"></div>
    <div class="prop-tally-no" style="width:0.0%"></div>
    <div class="prop-tally-veto" style="width:2.0%"></div>
    <div class="prop-tally-abstain" style="width:0.0%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes <strong>73.5%</strong> (41,668)</span>
    <span class="prop-tally-no-text">No <strong>0.0%</strong> (8)</span>
    <span class="prop-tally-veto-text">Veto <strong>26.4%</strong> (14,932)</span>
    <span class="prop-tally-abstain-text">Abstain <strong>0.1%</strong> (45)</span>
    <span class="prop-tally-total-text">Total 56,653 votes</span>
    <span class="prop-tally-veto-text">✗ Turnout <strong>7.6%</strong> (56,653 / 741,825) · Quorum <strong>25%</strong> (185,456)</span>
  </div>
</div>


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
    "label": "go-to-market-team-milestone-escrow",
    "msg": {
      "governance": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
      "payouts": [
        {
          "recipient": "gonka1zhcn5yz86z0jlsyzm9xkkhx6km5p8a4apw9rsj",
          "denom": "ngonka",
          "amount": "10000000000000",
          "unlock_after_days": 0
        },
        {
          "recipient": "gonka1zhcn5yz86z0jlsyzm9xkkhx6km5p8a4apw9rsj",
          "denom": "ngonka",
          "amount": "10000000000000",
          "unlock_after_days": 60
        },
        {
          "recipient": "gonka1zhcn5yz86z0jlsyzm9xkkhx6km5p8a4apw9rsj",
          "denom": "ngonka",
          "amount": "30000000000000",
          "unlock_after_days": 99
        },
        {
          "recipient": "gonka15at6rrk3tspus7mu0t2yg26r4guq7sqkpq3wf4",
          "denom": "ngonka",
          "amount": "30000000000000",
          "unlock_after_days": 0
        },
        {
          "recipient": "gonka15at6rrk3tspus7mu0t2yg26r4guq7sqkpq3wf4",
          "denom": "ngonka",
          "amount": "10000000000000",
          "unlock_after_days": 30
        },
        {
          "recipient": "gonka15at6rrk3tspus7mu0t2yg26r4guq7sqkpq3wf4",
          "denom": "ngonka",
          "amount": "50000000000000",
          "unlock_after_days": 99
        },
        {
          "recipient": "gonka1eym0g7fye3rzn6tj03qwfy0xeqkad6d5stdyaw",
          "denom": "ngonka",
          "amount": "40000000000000",
          "unlock_after_days": 0
        },
        {
          "recipient": "gonka1eym0g7fye3rzn6tj03qwfy0xeqkad6d5stdyaw",
          "denom": "ngonka",
          "amount": "25000000000000",
          "unlock_after_days": 30
        },
        {
          "recipient": "gonka1eym0g7fye3rzn6tj03qwfy0xeqkad6d5stdyaw",
          "denom": "ngonka",
          "amount": "25000000000000",
          "unlock_after_days": 60
        },
        {
          "recipient": "gonka1qederwp6etpnzm0et6d924c5n08cycauhdqwuy",
          "denom": "ngonka",
          "amount": "40000000000000",
          "unlock_after_days": 0
        },
        {
          "recipient": "gonka1qederwp6etpnzm0et6d924c5n08cycauhdqwuy",
          "denom": "ngonka",
          "amount": "35000000000000",
          "unlock_after_days": 30
        },
        {
          "recipient": "gonka1qederwp6etpnzm0et6d924c5n08cycauhdqwuy",
          "denom": "ngonka",
          "amount": "35000000000000",
          "unlock_after_days": 60
        },
        {
          "recipient": "gonka1k7400padt0g0kreh364c8vfsn58eg8r566yvnd",
          "denom": "ngonka",
          "amount": "30000000000000",
          "unlock_after_days": 0
        },
        {
          "recipient": "gonka1k7400padt0g0kreh364c8vfsn58eg8r566yvnd",
          "denom": "ngonka",
          "amount": "30000000000000",
          "unlock_after_days": 30
        },
        {
          "recipient": "gonka1k7400padt0g0kreh364c8vfsn58eg8r566yvnd",
          "denom": "ngonka",
          "amount": "30000000000000",
          "unlock_after_days": 60
        },
        {
          "recipient": "gonka1k7400padt0g0kreh364c8vfsn58eg8r566yvnd",
          "denom": "ngonka",
          "amount": "50000000000000",
          "unlock_after_days": 99
        },
        {
          "recipient": "gonka137zkmd6msle3556h2gls9t0tyqvathpzad2ev3",
          "denom": "ngonka",
          "amount": "30000000000000",
          "unlock_after_days": 0
        },
        {
          "recipient": "gonka137zkmd6msle3556h2gls9t0tyqvathpzad2ev3",
          "denom": "ngonka",
          "amount": "30000000000000",
          "unlock_after_days": 30
        },
        {
          "recipient": "gonka137zkmd6msle3556h2gls9t0tyqvathpzad2ev3",
          "denom": "ngonka",
          "amount": "30000000000000",
          "unlock_after_days": 60
        },
        {
          "recipient": "gonka137zkmd6msle3556h2gls9t0tyqvathpzad2ev3",
          "denom": "ngonka",
          "amount": "30000000000000",
          "unlock_after_days": 99
        },
        {
          "recipient": "gonka1eym0g7fye3rzn6tj03qwfy0xeqkad6d5stdyaw",
          "denom": "ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4",
          "amount": "3000000000",
          "unlock_after_days": 0
        },
        {
          "recipient": "gonka1eym0g7fye3rzn6tj03qwfy0xeqkad6d5stdyaw",
          "denom": "ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4",
          "amount": "3000000000",
          "unlock_after_days": 30
        },
        {
          "recipient": "gonka1eym0g7fye3rzn6tj03qwfy0xeqkad6d5stdyaw",
          "denom": "ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4",
          "amount": "3000000000",
          "unlock_after_days": 60
        },
        {
          "recipient": "gonka1zhcn5yz86z0jlsyzm9xkkhx6km5p8a4apw9rsj",
          "denom": "ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4",
          "amount": "9000000000",
          "unlock_after_days": 0
        },
        {
          "recipient": "gonka1zhcn5yz86z0jlsyzm9xkkhx6km5p8a4apw9rsj",
          "denom": "ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4",
          "amount": "9000000000",
          "unlock_after_days": 30
        },
        {
          "recipient": "gonka1zhcn5yz86z0jlsyzm9xkkhx6km5p8a4apw9rsj",
          "denom": "ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4",
          "amount": "9000000000",
          "unlock_after_days": 60
        }
      ],
      "close_after_days": 300
    },
    "funds": [],
    "salt": "Z3RtLXRlYW0tMjAyNg==",
    "fix_msg": false
  },
  {
    "@type": "/cosmos.distribution.v1beta1.MsgCommunityPoolSpend",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "recipient": "gonka1stfulpj6t5mc0nekph7g7tcf7dv5mszm95xtvt6rc5repv7t5yvq28h3ja",
    "amount": [
      {
        "denom": "ngonka",
        "amount": "600000000000000"
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
        "amount": "36000000000",
        "recipient": "gonka1stfulpj6t5mc0nekph7g7tcf7dv5mszm95xtvt6rc5repv7t5yvq28h3ja"
      }
    },
    "funds": []
  }
]
```

</details>
