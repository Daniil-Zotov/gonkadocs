---
title: "#74 – Gonka Labs: Maintaining Infrastructure, Improving Products, and Launching New Ones"
description: "Full proposal: https://gonkalabs.com/proposal

This proposal funds the next six months of work for the Gonka ecosystem.

The focus is production-grade infrastructure and high-use products: Gonka.gg V2"
template: proposals-proposals-main.html
---

# #74 – Gonka Labs: Maintaining Infrastructure, Improving Products, and Launching New Ones

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-passed">Passed</span>

**Proposal ID:** `74`

**Type:** Execute Contract, Transfer With Vesting

**Submit:** 2026-06-10 20:42 UTC

**Voting:** 2026-06-10 20:42 UTC → 2026-06-12 20:42 UTC

**Proposer:** [`gonka1e3pepqllu89t8l2acw86fgp5jjkw8m7kcl47nk`](https://gonka.gg/address/gonka1e3pepqllu89t8l2acw86fgp5jjkw8m7kcl47nk){:target="_blank"}

**Metadata:** [https://gonkalabs.com/proposal](https://gonkalabs.com/proposal)

<div class="prop-funding-line">$70,000 · Community Pool · 330,000 GNK · Gov Module</div>


[View on gonka.gg](https://gonka.gg/network/proposals/74){:target="_blank"}

</div>

Full proposal: <https://gonkalabs.com/proposal>

This proposal funds the next six months of work for the Gonka ecosystem.

The focus is production-grade infrastructure and high-use products: Gonka.gg V2 as the default explorer and data hub, rpc.gonka.gg as reliable public RPC, proxy.gonka.gg for business inference access and API-key management, a mobile Gonka app based on GG Wallet, governance tooling through Gonkavote, and a public open-source Marketing Transparency Dashboard. Existing tools such as Gonkablocks, meter.gonka.gg, and other Gonka Labs projects will continue to receive maintenance, fixes, and support.

Gonka Labs products will remain non-commercial: no ads, paid placements, PR slots, or profit markups. Any fees are intended only to cover infrastructure and operating costs.

Accountability commitments include monthly public progress and spending reports, an 80%+ open-source code commitment, and on-chain transparency for both the USDT payment and GNK vesting.

Budget: 70,000 USDT paid immediately to cover six months of server infrastructure, monitoring, operations, and guaranteed stablecoin compensation; plus 330,000 GNK vested to the core team over 180 Gonka vesting epochs, aligning the team with long-term network growth.

Full proposal: <https://gonkalabs.com/proposal>

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:41.1%"></div>
    <div class="prop-tally-no" style="width:0.5%"></div>
    <div class="prop-tally-veto" style="width:0.0%"></div>
    <div class="prop-tally-abstain" style="width:10.0%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes 305,163 (79.6%)</span>
    <span class="prop-tally-no-text">No 3,791 (1.0%)</span>
    <span class="prop-tally-veto-text">Veto 15 (0.0%)</span>
    <span class="prop-tally-abstain-text">Abstain 74,304 (19.4%)</span>
    <span class="prop-tally-total-text">Total 383,273 votes</span>
    
  </div>
</div>


## Messages

| # | Type |
| :- | :--- |
| 1 | `/cosmwasm.wasm.v1.MsgExecuteContract` |
| 2 | `/inference.streamvesting.MsgTransferWithVesting` |

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
        "amount": "70000000000",
        "recipient": "gonka16j4zv6723mrnycwn0qgw0j48dr9qecyclxg5jh"
      }
    },
    "funds": []
  },
  {
    "@type": "/inference.streamvesting.MsgTransferWithVesting",
    "sender": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "recipient": "gonka16j4zv6723mrnycwn0qgw0j48dr9qecyclxg5jh",
    "amount": [
      {
        "denom": "ngonka",
        "amount": "330000000000000"
      }
    ],
    "vesting_epochs": "180"
  }
]
```

</details>
