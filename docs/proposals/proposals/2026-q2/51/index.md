---
title: "#51 – Support Gonka's presence at WebX Asia"
description: "6Block, a long-term Gonka mining and infrastructure participant, proposes that the Gonka community allocate 75,000 USDT to support Gonka's participation at WebX Asia / WebX 2026 in Tokyo. 6Block has a"
template: proposals-proposals-main.html
---

# #51 – Support Gonka's presence at WebX Asia

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-passed">Passed</span>

**Proposal ID:** `51`

**Type:** Execute Contract

**Submit:** 2026-05-13 13:17 UTC

**Voting:** 2026-05-13 13:17 UTC → 2026-05-15 13:17 UTC

**Proposer:** [`gonka15p7s7w2hx0y8095lddd4ummm2y0kwpwljk00aq`](https://gonka.gg/address/gonka15p7s7w2hx0y8095lddd4ummm2y0kwpwljk00aq){:target="_blank"}

**Metadata:** [https://github.com/6block/gonka-webx-proposal/blob/main/README.md](https://github.com/6block/gonka-webx-proposal/blob/main/README.md)

<div class="prop-funding-line">$75,000 · Community Pool</div>


[View on gonka.gg](https://gonka.gg/network/proposals/51){:target="_blank"}

</div>

6Block, a long-term Gonka mining and infrastructure participant, proposes that the Gonka community allocate 75,000 USDT to support Gonka's participation at WebX Asia / WebX 2026 in Tokyo. 6Block has already committed 50% of the needed 150,000 USDT of its own funds for the official Platinum sponsorship. If approved, the funds will be transferred to 6Block's designated wallet and used for event execution (team travel, accommodation, booth production, materials, media support, partner coordination). 6Block will provide a post-event summary to the community. Full proposal: <https://github.com/6block/gonka-webx-proposal/blob/main/README.md>

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:62.8%"></div>
    <div class="prop-tally-no" style="width:0.3%"></div>
    <div class="prop-tally-veto" style="width:10.2%"></div>
    <div class="prop-tally-abstain" style="width:26.7%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes 395,003 (62.8%)</span>
    <span class="prop-tally-no-text">No 1,767 (0.3%)</span>
    <span class="prop-tally-veto-text">Veto 64,217 (10.2%)</span>
    <span class="prop-tally-abstain-text">Abstain 168,275 (26.7%)</span>
    <span class="prop-tally-total-text">Total 629,262 votes</span>
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
        "amount": "75000000000",
        "recipient": "gonka1yqj5xf0wtqgpdmv5v68cus0tp2j5fv7lzcfd6g"
      }
    },
    "funds": []
  }
]
```

</details>

---