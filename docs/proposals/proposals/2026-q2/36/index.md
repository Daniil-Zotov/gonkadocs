---
title: "#36 – Register Kava USDT IBC metadata and approve for trading"
description: "Register IBC token metadata and approve the denomination for trading on Gonka mainnet."
template: proposals-proposals-main.html
---

# #36 – Register Kava USDT IBC metadata and approve for trading

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-passed">Passed</span>

**Proposal ID:** `36`

**Type:** Approve Ibc Token For Trading, Register Ibc Token Metadata

**Submit:** 2026-04-01 18:03 UTC

**Voting:** 2026-04-01 18:03 UTC → 2026-04-02 18:03 UTC

**Proposer:** [`gonka1m9sf2rpg635efaw59djqlxkqew9sxvmqd6g343`](https://gonka.gg/address/gonka1m9sf2rpg635efaw59djqlxkqew9sxvmqd6g343){:target="_blank"}



[View on gonka.gg](https://gonka.gg/network/proposals/36){:target="_blank"}

</div>

Register IBC token metadata and approve the denomination for trading on Gonka mainnet.

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:56.8%"></div>
    <div class="prop-tally-no" style="width:0.0%"></div>
    <div class="prop-tally-veto" style="width:0.0%"></div>
    <div class="prop-tally-abstain" style="width:0.2%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes 421,414 (99.6%)</span>
    <span class="prop-tally-no-text">No 0 (0.0%)</span>
    <span class="prop-tally-veto-text">Veto 0 (0.0%)</span>
    <span class="prop-tally-abstain-text">Abstain 1,788 (0.4%)</span>
    <span class="prop-tally-total-text">Total 423,202 votes</span>
    
  </div>
</div>


---

## Messages

| # | Type |
| :- | :--- |
| 1 | `/inference.inference.MsgRegisterIbcTokenMetadata` |
| 2 | `/inference.inference.MsgApproveIbcTokenForTrading` |

<details class="prop-contracts" markdown="1">
<summary markdown="1">Contract Details</summary>

```json
[
  {
    "@type": "/inference.inference.MsgRegisterIbcTokenMetadata",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "chainId": "kava_2222-10",
    "ibcDenom": "ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4",
    "name": "USDT",
    "symbol": "USDT",
    "decimals": 6,
    "overwrite": true
  },
  {
    "@type": "/inference.inference.MsgApproveIbcTokenForTrading",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "chainId": "kava_2222-10",
    "ibcDenom": "ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4"
  }
]
```

</details>
