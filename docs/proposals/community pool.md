---
title: Community Pool
description: "Community Pool, Community Sale wallet, and Gov Module — addresses, balances, inflow/outflow mechanics, and full history of MsgCommunityPoolSpend"
hide:
  - navigation
  - toc
---

# Community Pool

The Gonka network maintains three key addresses that collectively manage community funds. This page documents their current balances (updated hourly), how funds flow between them, and every governance proposal that has spent from the Community Pool.

---

## Addresses

| Address | Label | Purpose |
| :------ | :---- | :------ |
| `gonka1jv65s3grqf6v6jl3dp4t6c9t9rk99cd8h2rzwa` | **Community Pool** (distribution module) | Holds 2% of all inflation and network fees; spent only through governance |
| `gonka18pkq9mwxxlmyq7kr5txhm060wemg2s4u94wvsfd9w2kdc0u99d6spk8pz2` | **Community Sale** | Receives GNK from the initial community sale; used for ecosystem grants |
| `gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33` | **Gov Module** (authority) | Executes `MsgCommunityPoolSpend` on behalf of passed proposals; holds unallocated gov-module funds |

??? info "How to verify these addresses on-chain"

    - **Community Pool**: query the distribution module  
      ```
      curl -s https://node3.gonka.ai/chain-api/cosmos/distribution/v1beta1/community_pool
      ```
    - **Account balances**: query the bank module  
      ```
      curl -s https://node3.gonka.ai/chain-api/cosmos/bank/v1beta1/balances/{address}
      ```
    - **Transactions**: use the Tendermint RPC  
      ```
      curl -s 'https://rpc.gonka.gg/tx_search?query="transfer.recipient='"'"'{address}'"'"'"&per_page=10'
      ```

---

## Current Balances

<small>Last updated: <!-- UPDATE_TIMESTAMP -->
2026-07-17 14:10 UTC
<!-- /UPDATE_TIMESTAMP --></small>

<!-- BALANCES_START -->
| Community Pool | 102.7M GNK |
| Community Pool | $10,000.00 |
| Community Sale | 17.5M GNK |
| Community Sale | $814,325.00 |
| Gov Module | 2.2M GNK |
<!-- BALANCES_END -->

### Inflow Estimate

- **Source:** 2 % community tax on every inflation reward and network fee
- **Rate:** ~13,150 GNK / day (based on recent epochs)
- **Varies with:** block time, fee volume, and staking ratio

---

## How Community Pool Spending Works

1. A governance proposal includes one or more `MsgCommunityPoolSpend` messages specifying a recipient address and amount (GNK and/or USDT via IBC).
2. If the proposal **passes**, the Gov Module authority address (`gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33`) signs and executes the transfer from the Community Pool distribution account.
3. USDT is held in the Community Pool as the IBC denom `ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4` and transferred via `MsgExecuteContract` (withdraw_ibc).

**Key constraint:** Only the Gov Module authority can spend from the Community Pool. No single key controls these funds — every spend requires a passed governance vote.

---

## Historical Spend

All `MsgCommunityPoolSpend` transactions across all governance proposals. Data sourced from on-chain proposal messages.

| # | Proposal | Date | Recipient | Amount GNK | Amount USDT | Status |
| :-: | :------ | :--: | :-------- | ---------: | ---------: | :----: |

<!-- SPENT_HISTORY_START -->
| 1 | [#14](https://gonkadocs.com/proposals/proposals/2025-q4/14/) | 2025-11-27 | `gonka18pkq…pk8pz2` | 20,000,000.0 | — | Passed |
| 2 | [#32](https://gonkadocs.com/proposals/proposals/2026-q1/32/) | 2026-03-24 | `gonka1t7mc…sv4yzu` | 500.0 | — | Passed |
| 3 | [#33](https://gonkadocs.com/proposals/proposals/2026-q1/33/) | 2026-03-27 | `gonka197hq…fw3y6k` | 2,500.0 | — | Passed |
| 4 | [#33](https://gonkadocs.com/proposals/proposals/2026-q1/33/) | 2026-03-27 | `gonka12jaf…kvcleq` | 100.0 | — | Passed |
| 5 | [#33](https://gonkadocs.com/proposals/proposals/2026-q1/33/) | 2026-03-27 | `gonka170gv…ktjw75` | 100.0 | — | Passed |
| 6 | [#33](https://gonkadocs.com/proposals/proposals/2026-q1/33/) | 2026-03-27 | `gonka1uvk3…8a2fr7` | 100.0 | — | Passed |
| 7 | [#33](https://gonkadocs.com/proposals/proposals/2026-q1/33/) | 2026-03-27 | `gonka1ss36…spahay` | 100.0 | — | Passed |
| 8 | [#33](https://gonkadocs.com/proposals/proposals/2026-q1/33/) | 2026-03-27 | `gonka1ajxy…xt0zhf` | 100.0 | — | Passed |
| 9 | [#33](https://gonkadocs.com/proposals/proposals/2026-q1/33/) | 2026-03-27 | `gonka1d5nn…h96dzd` | 100.0 | — | Passed |
| 10 | [#34](https://gonkadocs.com/proposals/proposals/2026-q1/34/) | 2026-03-31 | `gonka1ls44…tkevej` | 970,000.0 | — | Rejected |
| 11 | [#35](https://gonkadocs.com/proposals/proposals/2026-q1/35/) | 2026-03-31 | `gonka1ls44…tkevej` | 970,000.0 | — | Rejected |
| 12 | [#37](https://gonkadocs.com/proposals/proposals/2026-q2/37/) | 2026-04-08 | `gonka1ry4u…spd0v2` | 1.0 | — | Rejected |
| 13 | [#38](https://gonkadocs.com/proposals/proposals/2026-q2/38/) | 2026-04-09 | `gonka1lqjj…9j3r2l` | 20,000.0 | — | Rejected |
| 14 | [#39](https://gonkadocs.com/proposals/proposals/2026-q2/39/) | 2026-04-10 | `gonka1snq0…y3l4t4` | 31,250.0 | — | Passed |
| 15 | [#41](https://gonkadocs.com/proposals/proposals/2026-q2/41/) | 2026-04-18 | `gonka1yf2f…9avx7a` | — | $96,000 | Rejected |
| 16 | [#43](https://gonkadocs.com/proposals/proposals/2026-q2/43/) | 2026-04-27 | `gonka14zlg…p9n6ds` | 104,166.0 | — | Rejected |
| 17 | [#45](https://gonkadocs.com/proposals/proposals/2026-q2/45/) | 2026-05-01 | `gonka14zlg…p9n6ds` | 119,000.0 | — | Rejected |
| 18 | [#47](https://gonkadocs.com/proposals/proposals/2026-q2/47/) | 2026-05-06 | `gonka14fxt…hzsyq3` | 20,000.0 | — | Rejected |
| 19 | [#50](https://gonkadocs.com/proposals/proposals/2026-q2/50/) | 2026-05-09 | `gonka14fxt…hzsyq3` | 20,000.0 | — | Passed |
| 20 | [#55](https://gonkadocs.com/proposals/proposals/2026-q2/55/) | 2026-05-23 | `gonka14fxt…hzsyq3` | 4,500.0 | — | Passed |
| 21 | [#55](https://gonkadocs.com/proposals/proposals/2026-q2/55/) | 2026-05-23 | `gonka16j4z…lxg5jh` | 8,875.0 | — | Passed |
| 22 | [#55](https://gonkadocs.com/proposals/proposals/2026-q2/55/) | 2026-05-23 | `gonka100s7…3a9dn6` | 11,062.5 | — | Passed |
| 23 | [#55](https://gonkadocs.com/proposals/proposals/2026-q2/55/) | 2026-05-23 | `gonka197hq…fw3y6k` | 15,284.7 | — | Passed |
| 24 | [#64](https://gonkadocs.com/proposals/proposals/2026-q2/64/) | 2026-06-04 | `gonka1s3tn…sdcvvm` | 28,000.0 | — | Passed |
| 25 | [#65](https://gonkadocs.com/proposals/proposals/2026-q2/65/) | 2026-06-04 | `gonka1s3tn…sdcvvm` | 100,000.0 | — | Passed |
| 26 | [#70](https://gonkadocs.com/proposals/proposals/2026-q2/70/) | 2026-06-08 | `gonka13kzs…9unpcq` | 246,000.0 | — | Rejected |
| 27 | [#80](https://gonkadocs.com/proposals/proposals/2026-q3/80/) | 2026-07-07 | `gonka100s7…3a9dn6` | 13,950.0 | — | Rejected |
| 28 | [#80](https://gonkadocs.com/proposals/proposals/2026-q3/80/) | 2026-07-07 | `gonka123pr…ug5f9a` | 4,600.0 | — | Rejected |
| 29 | [#80](https://gonkadocs.com/proposals/proposals/2026-q3/80/) | 2026-07-07 | `gonka16j4z…lxg5jh` | 10,800.0 | — | Rejected |
| 30 | [#80](https://gonkadocs.com/proposals/proposals/2026-q3/80/) | 2026-07-07 | `gonka1gmux…gzg6ry` | 12,300.0 | — | Rejected |
| 31 | [#80](https://gonkadocs.com/proposals/proposals/2026-q3/80/) | 2026-07-07 | `gonka1ppn5…mw6a3q` | 6,200.0 | — | Rejected |
| 32 | [#82](https://gonkadocs.com/proposals/proposals/2026-q3/82/) | 2026-07-10 | `gonka1g57f…lj8ayw` | 80,000.0 | — | Passed |
| 33 | [#84](https://gonkadocs.com/proposals/proposals/2026-q3/84/) | 2026-07-11 | `gonka1njlf…mjplat` | 20,000.0 | — | Rejected |
| 34 | [#85](https://gonkadocs.com/proposals/proposals/2026-q3/85/) | 2026-07-12 | `gonka1stfu…28h3ja` | 600,000.0 | — | Rejected |

| Proposals with `MsgCommunityPoolSpend` | 21 (34 individual messages) |
| Passed proposals | 9 |
| Rejected proposals | 12 |
| Total GNK passed | 20,302,572 GNK |
| Total USDT passed | $0 |
| Total GNK rejected | 3,117,017 GNK |
| Total USDT rejected | $96,000 |
| Largest passed spend | #14 — 20,000,000 GNK |
| Most recent passed spend | #82 — 80,000 GNK |
<!-- SPENT_HISTORY_END -->

---

## Community Sale Wallet

The `community-sale` address (`gonka18pkq9mwxxlmyq7kr5txhm060wemg2s4u94wvsfd9w2kdc0u99d6spk8pz2`) holds proceeds from the initial community sale. These funds are disbursed through governance-approved ecosystem grants.

*Data synced hourly from [rpc.gonka.gg](https://rpc.gonka.gg). Source: [`buildtools/update-community-pool.py`](https://github.com/Daniil-Zotov/gonkadocs/blob/main/buildtools/update-community-pool.py)*
