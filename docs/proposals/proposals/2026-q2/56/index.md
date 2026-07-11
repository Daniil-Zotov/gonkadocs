---
title: "#56 – INC4 | Gonka NOP - grant for the node deployment tool"
description: "# Gonka NOP: grant for the node deployment tool

50,000 USDT from the CommunityPool to INC4
Full proposal: https://github.com/gonka-ai/gonka/discussions/1192

## What it is

gonka-nop (Node Onboarding"
template: proposals-proposals-main.html
---

# #56 – INC4 | Gonka NOP - grant for the node deployment tool

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-rejected">Rejected</span>

**Proposal ID:** `56`

**Type:** Execute Contract

**Submit:** 2026-05-25 15:12 UTC

**Voting:** 2026-05-25 15:12 UTC → 2026-05-27 15:12 UTC

**Proposer:** [`gonka1juwk05glldgn7850a3547jsl7l4vrhx9k5g3cr`](https://gonka.gg/address/gonka1juwk05glldgn7850a3547jsl7l4vrhx9k5g3cr){:target="_blank"}

**Metadata:** [https://github.com/gonka-ai/gonka/discussions/1192](https://github.com/gonka-ai/gonka/discussions/1192)

**Failed reason:** proposal did not get enough votes to pass

<div class="prop-funding-line prop-funding-line-rejected">$50,000 · Community Pool</div>


[View on gonka.gg](https://gonka.gg/network/proposals/56){:target="_blank"}

</div>

# Gonka NOP: grant for the node deployment tool

50,000 USDT from the CommunityPool to INC4
Full proposal: <https://github.com/gonka-ai/gonka/discussions/1192>

## What it is

gonka-nop (Node Onboarding Package) is a tool that reduces launching a Gonka node to a single command. Complex technical details are hidden inside and updated alongside the network. It is already working, open source, and in use by some operators on mainnet.

## What the grant covers

1. Work already delivered - INC4 took on the initial development as a contribution to the network.
2. Support for NOP users - 6 months of help, fixes, updates with every network release.
3. Continued development - expanding functionality, supporting more deployment scenarios, lowering the entry barrier further, etc.

## Why this matters for the network

Today only technical specialists can launch a node. NOP removes that barrier: newcomers can join without diving into the internals, and experienced operators get a consistent foundation for their own automation.

The broader the operator set, the more resilient the network.

## Terms

- Single payment, no vesting or tranches
- Work is open on GitHub: code, releases, issues - this is the report to the DAO

## Links

Repository on GitHub: <https://github.com/inc4/gonka-nop>
Documentation: <https://github.com/inc4/gonka-nop/blob/main/README.md>
Live walkthrough on YouTube (by Gonka.Top@Mitch): <https://www.youtube.com/watch?v=1t9GEMN92Vo>

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:58.6%"></div>
    <div class="prop-tally-no" style="width:17.6%"></div>
    <div class="prop-tally-veto" style="width:23.8%"></div>
    <div class="prop-tally-abstain" style="width:0.0%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes 31,851 (58.6%)</span>
    <span class="prop-tally-no-text">No 9,566 (17.6%)</span>
    <span class="prop-tally-veto-text">Veto 12,961 (23.8%)</span>
    <span class="prop-tally-abstain-text">Abstain 0 (0.0%)</span>
    <span class="prop-tally-total-text">Total 54,378 votes</span>
    
  </div>
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
        "amount": "50000000000",
        "recipient": "gonka14fxt7xlj74h54u5lz8epz0qeuhpka6xjhzsyq3"
      }
    },
    "funds": []
  }
]
```

</details>

---