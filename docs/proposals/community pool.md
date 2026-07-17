---
title: Community Pool
description: "Community Pool, Community Sale wallet, and Gov Module — addresses, balances, inflow/outflow mechanics, and full history of MsgCommunityPoolSpend"
hide:
  - navigation
  - toc
---

# Community Pool

The Gonka network maintains three key addresses that collectively manage community funds. This page documents their current balances (updated hourly), how funds flow between them, and every successful governance proposal that has spent from the Community Pool.

<small>Last updated: <!-- UPDATE_TIMESTAMP -->
2026-07-17 14:41 UTC
<!-- /UPDATE_TIMESTAMP --></small>

---

## Community Pool (distribution module)

**Address:** [`gonka1jv65s3grqf6v6jl3dp4t6c9t9rk99cd8h2rzwa`](https://gonka.gg/address/gonka1jv65s3grqf6v6jl3dp4t6c9t9rk99cd8h2rzwa)

The Community Pool is the protocol-controlled treasury of the Gonka network. It accrues value through a **2% community tax** applied to every inflation reward and network fee. These funds can only be spent through a successful governance vote — no single key controls them.

**Current balance:**

<!-- BALANCES_START -->
| Address | Asset | Balance |
| :------ | :---- | :------ |
| Community Pool | GNK | 102.7M GNK |
| Community Pool | USDT | $10,000.00 |
<!-- BALANCES_END -->

**Inflow rate:** ~13,150 GNK/day (varies with block time, fee volume, and staking ratio).

??? info "Verify on-chain"
    ```
    curl -s https://node3.gonka.ai/chain-api/cosmos/distribution/v1beta1/community_pool
    ```

---

## Community Sale

**Address:** [`gonka18pkq9mwxxlmyq7kr5txhm060wemg2s4u94wvsfd9w2kdc0u99d6spk8pz2`](https://gonka.gg/address/gonka18pkq9mwxxlmyq7kr5txhm060wemg2s4u94wvsfd9w2kdc0u99d6spk8pz2)

This address was created by **[proposal #14](/proposals/proposals/2025-q4/14/)** (passed 2025-11-27), which transferred **20,000,000 GNK** from the Community Pool to seed a community sale programme.

The mechanism works as a simple swap: participants deposit **USDT** and receive **GNK** at a predetermined rate. The address holds both assets — USDT collected from buyers and the remaining GNK inventory.

**Important:** The GNK held here is **not part of the Community Pool**. It is the undistributed balance of the sale contract — already allocated in proposal #14 and awaiting exchange. Only the USDT received from buyers is new value entering the Gonka ecosystem.

**Current balance:**

<!-- SALE_BALANCE_START -->
| Asset | Balance |
| :---- | :------ |
| GNK | 17.5M GNK |
| USDT | $814,325.00 |
<!-- SALE_BALANCE_END -->

??? info "Verify on-chain"
    ```
    curl -s https://node3.gonka.ai/chain-api/cosmos/bank/v1beta1/balances/gonka18pkq9mwxxlmyq7kr5txhm060wemg2s4u94wvsfd9w2kdc0u99d6spk8pz2
    ```

---

## Gov Module (authority)

**Address:** [`gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33`](https://gonka.gg/address/gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33)

The Gov Module authority is the only address permitted to execute `MsgCommunityPoolSpend` transfers from the Community Pool. When a governance proposal passes, this address signs and sends the requested funds to the specified recipient.

It also holds unallocated GNK set aside for governance-approved programmes that use batch-vesting or multi-send distributions.

**Current balance:**

<!-- GOV_BALANCE_START -->
| Asset | Balance |
| :---- | :------ |
| GNK | 2.2M GNK |
<!-- GOV_BALANCE_END -->

??? info "Verify on-chain"
    ```
    curl -s https://node3.gonka.ai/chain-api/cosmos/bank/v1beta1/balances/gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33
    ```

---

## How Community Pool Spending Works

1. A governance proposal includes one or more `MsgCommunityPoolSpend` messages specifying a recipient address and amount (GNK and/or USDT via IBC).
2. If the proposal **passes**, the Gov Module authority address ([`gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33`](https://gonka.gg/address/gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33)) signs and executes the transfer from the Community Pool distribution account.
3. USDT is held in the Community Pool as the IBC denom `ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4` and transferred via `MsgExecuteContract` (withdraw_ibc).

**Key constraint:** Only the Gov Module authority can spend from the Community Pool. No single key controls these funds — every spend requires a passed governance vote.

---

## Historical Spend

All `MsgCommunityPoolSpend` messages from **passed** governance proposals, sorted by descending proposal number.

<!-- SPENT_HISTORY_START -->
| # | Proposal | Date | Recipient | Amount GNK | Amount USDT |
| :-: | :------ | :--: | :-------- | ---------: | ---------: |
| 1 | [#82](https://gonkadocs.com/proposals/proposals/2026-q3/82/) | 2026-07-10 | [`gonka1g57f…lj8ayw`](https://gonka.gg/address/gonka1g57f45qjvn0529vpgj8x8mzt8r5k4audchm3pp9pezywxwf4rexqlj8ayw) | 80,000.0 | — |
| 2 | [#65](https://gonkadocs.com/proposals/proposals/2026-q2/65/) | 2026-06-04 | [`gonka1s3tn…sdcvvm`](https://gonka.gg/address/gonka1s3tnqglxt6xwy9ttuedtz8cp4x9tlwp8sdcvvm) | 100,000.0 | — |
| 3 | [#64](https://gonkadocs.com/proposals/proposals/2026-q2/64/) | 2026-06-04 | [`gonka1s3tn…sdcvvm`](https://gonka.gg/address/gonka1s3tnqglxt6xwy9ttuedtz8cp4x9tlwp8sdcvvm) | 28,000.0 | — |
| 4 | [#55](https://gonkadocs.com/proposals/proposals/2026-q2/55/) | 2026-05-23 | [`gonka14fxt…hzsyq3`](https://gonka.gg/address/gonka14fxt7xlj74h54u5lz8epz0qeuhpka6xjhzsyq3) | 4,500.0 | — |
| 5 | [#55](https://gonkadocs.com/proposals/proposals/2026-q2/55/) | 2026-05-23 | [`gonka16j4z…lxg5jh`](https://gonka.gg/address/gonka16j4zv6723mrnycwn0qgw0j48dr9qecyclxg5jh) | 8,875.0 | — |
| 6 | [#55](https://gonkadocs.com/proposals/proposals/2026-q2/55/) | 2026-05-23 | [`gonka100s7…3a9dn6`](https://gonka.gg/address/gonka100s7x2t0npruu9ta02306qfmaened3vg3a9dn6) | 11,062.5 | — |
| 7 | [#55](https://gonkadocs.com/proposals/proposals/2026-q2/55/) | 2026-05-23 | [`gonka197hq…fw3y6k`](https://gonka.gg/address/gonka197hqnwcl30x4js3egvaujjmfknlxy7rmfw3y6k) | 15,284.7 | — |
| 8 | [#50](https://gonkadocs.com/proposals/proposals/2026-q2/50/) | 2026-05-09 | [`gonka14fxt…hzsyq3`](https://gonka.gg/address/gonka14fxt7xlj74h54u5lz8epz0qeuhpka6xjhzsyq3) | 20,000.0 | — |
| 9 | [#39](https://gonkadocs.com/proposals/proposals/2026-q2/39/) | 2026-04-10 | [`gonka1snq0…y3l4t4`](https://gonka.gg/address/gonka1snq0m4rdvq0sswm03r5jsmtzw3p384qsy3l4t4) | 31,250.0 | — |
| 10 | [#33](https://gonkadocs.com/proposals/proposals/2026-q1/33/) | 2026-03-27 | [`gonka197hq…fw3y6k`](https://gonka.gg/address/gonka197hqnwcl30x4js3egvaujjmfknlxy7rmfw3y6k) | 2,500.0 | — |
| 11 | [#33](https://gonkadocs.com/proposals/proposals/2026-q1/33/) | 2026-03-27 | [`gonka12jaf…kvcleq`](https://gonka.gg/address/gonka12jaf7m4eysyqt32mrgarum6z96vt55tckvcleq) | 100.0 | — |
| 12 | [#33](https://gonkadocs.com/proposals/proposals/2026-q1/33/) | 2026-03-27 | [`gonka170gv…ktjw75`](https://gonka.gg/address/gonka170gvlkfx4vg267y7mx0d5nexlf3lxs8nktjw75) | 100.0 | — |
| 13 | [#33](https://gonkadocs.com/proposals/proposals/2026-q1/33/) | 2026-03-27 | [`gonka1uvk3…8a2fr7`](https://gonka.gg/address/gonka1uvk3w9sswd8nnzt29yjyw94vwmuq6g6h8a2fr7) | 100.0 | — |
| 14 | [#33](https://gonkadocs.com/proposals/proposals/2026-q1/33/) | 2026-03-27 | [`gonka1ss36…spahay`](https://gonka.gg/address/gonka1ss36q35zmqhpj83vctedd25s34qz7d5vspahay) | 100.0 | — |
| 15 | [#33](https://gonkadocs.com/proposals/proposals/2026-q1/33/) | 2026-03-27 | [`gonka1ajxy…xt0zhf`](https://gonka.gg/address/gonka1ajxyae8vgzlh3t6frq64e7vj3fnga7vuxt0zhf) | 100.0 | — |
| 16 | [#33](https://gonkadocs.com/proposals/proposals/2026-q1/33/) | 2026-03-27 | [`gonka1d5nn…h96dzd`](https://gonka.gg/address/gonka1d5nn7u0hq0pumgmfxk95nj5h3zkuskkdh96dzd) | 100.0 | — |
| 17 | [#32](https://gonkadocs.com/proposals/proposals/2026-q1/32/) | 2026-03-24 | [`gonka1t7mc…sv4yzu`](https://gonka.gg/address/gonka1t7mcnc8zjkkvhwmfmst54sasulj68e5zsv4yzu) | 500.0 | — |
| 18 | [#14](https://gonkadocs.com/proposals/proposals/2025-q4/14/) | 2025-11-27 | [`gonka18pkq…pk8pz2`](https://gonka.gg/address/gonka18pkq9mwxxlmyq7kr5txhm060wemg2s4u94wvsfd9w2kdc0u99d6spk8pz2) | 20,000,000.0 | — |

| Metric | Value |
| :----- | :---- |
| Total `MsgCommunityPoolSpend` messages | 18 |
| Proposals with `MsgCommunityPoolSpend` | 9 |
| Total GNK spent | 20,302,572 GNK |
| Total USDT spent | $0 |
| Largest spend | #14 — 20,000,000 GNK |
| Most recent | #82 — 80,000 GNK |
<!-- SPENT_HISTORY_END -->

---

*Data synced hourly from [rpc.gonka.gg](https://rpc.gonka.gg). Source: [`buildtools/update-community-pool.py`](https://github.com/Daniil-Zotov/gonkadocs/blob/main/buildtools/update-community-pool.py)*
