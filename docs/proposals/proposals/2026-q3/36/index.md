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

**Submit:** 2026-01-01 00:00 UTC

**Voting:**  → 2026-01-02 00:00 UTC



[View on gonka.gg](https://gonka.gg/network/proposals/36){:target="_blank"}

</div>

Register IBC token metadata and approve the denomination for trading on Gonka mainnet.

---

## Messages

| # | Type |
| :- | :--- |
| 1 | `/inference.inference.MsgRegisterIbcTokenMetadata` |
| 2 | `/inference.inference.MsgApproveIbcTokenForTrading` |

<details class="prop-contracts">
<summary>Contract Details</summary>

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

---