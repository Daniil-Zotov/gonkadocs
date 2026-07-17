---
title: Community Pool
description: "Community Pool, Community Sale wallet, and Gov Module — addresses, balances, inflow/outflow mechanics, and full funding history of passed governance proposals"
hide:
  - toc
---

# Community Pool

The Gonka network maintains three key addresses that collectively manage community funds. This page documents their current balances, how funds flow between them, and every passed governance proposal that has received funding.

<small>Last updated: <!-- UPDATE_TIMESTAMP -->
2026-07-17 15:13 UTC
<!-- /UPDATE_TIMESTAMP --></small>

---

## Community Pool (distribution module)

**Address:** [`gonka1jv65s3grqf6v6jl3dp4t6c9t9rk99cd8h2rzwa`](https://gonka.gg/address/gonka1jv65s3grqf6v6jl3dp4t6c9t9rk99cd8h2rzwa)

<!-- BALANCES_START -->
<p style="margin:0.2rem 0">
<strong>Current balance:</strong> <span style="color:var(--md-accent-fg-color,#5468ff);font-size:1.05rem;font-weight:600">103M GNK</span> · <span style="color:var(--md-accent-fg-color,#5468ff);font-size:1.05rem;font-weight:600">$10,000 USDT</span>
</p>
<!-- BALANCES_END -->

The Community Pool is the protocol-controlled treasury of the Gonka network. It accrues value through a **2% community tax** applied to every inflation reward and network fee. These funds can only be spent through a successful governance vote — no single key controls them.

The USDT in the Community Pool was returned from **[proposal #42](https://gonkadocs.com/proposals/proposals/2026-q2/42/)** — the planned Global Compute Sovereignty Summit was cancelled, and the proposer returned the allocated funds. See the [return instructions](https://gonkadocs.com/community/discussion/show-and-tell/1390-how-to-return-funds-to-the-community-pool-ibc-usdt/) for details.

**Inflow rate:** ~13,150 GNK/day (varies with block time, fee volume, and staking ratio).

<details style="margin:0.5rem 0;padding:0.6rem 1rem;border:1px solid var(--md-default-fg-color--lightest);border-radius:6px;background:var(--md-code-bg-color,#00000008)">
<summary style="cursor:pointer;font-weight:600;font-size:0.9rem">Verify on-chain</summary>

```
curl -s https://node3.gonka.ai/chain-api/cosmos/distribution/v1beta1/community_pool
```

</details>

---

## Community Sale

**Address:** [`gonka18pkq9mwxxlmyq7kr5txhm060wemg2s4u94wvsfd9w2kdc0u99d6spk8pz2`](https://gonka.gg/address/gonka18pkq9mwxxlmyq7kr5txhm060wemg2s4u94wvsfd9w2kdc0u99d6spk8pz2)

This address was created by **[proposal #14](/proposals/proposals/2025-q4/14/)** (passed 2025-11-27), which transferred **20,000,000 GNK** from the Community Pool to seed a community sale programme.

The mechanism works as a simple swap: participants deposit **USDT** and receive **GNK** at a predetermined rate. The address holds both assets — USDT collected from buyers and the remaining GNK inventory.

**Important:** The GNK held here is **not part of the Community Pool**. It is the undistributed balance of the sale contract — already allocated in proposal #14 and awaiting exchange. Only the USDT received from buyers is new value entering the Gonka ecosystem.

<!-- SALE_BALANCE_START -->
<p style="margin:0.2rem 0">
<strong>Current balance:</strong> <span style="color:var(--md-accent-fg-color,#5468ff);font-size:1.05rem;font-weight:600">17M GNK (~$10M USDT)</span> · <span style="color:var(--md-accent-fg-color,#5468ff);font-size:1.05rem;font-weight:600">$814,325 USDT</span>
</p>
<!-- SALE_BALANCE_END -->

<details style="margin:0.5rem 0;padding:0.6rem 1rem;border:1px solid var(--md-default-fg-color--lightest);border-radius:6px;background:var(--md-code-bg-color,#00000008)">
<summary style="cursor:pointer;font-weight:600;font-size:0.9rem">Verify on-chain</summary>

```
curl -s https://node3.gonka.ai/chain-api/cosmos/bank/v1beta1/balances/gonka18pkq9mwxxlmyq7kr5txhm060wemg2s4u94wvsfd9w2kdc0u99d6spk8pz2
```

</details>

---

## Gov Module (authority)

**Address:** [`gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33`](https://gonka.gg/address/gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33)

The Gov Module authority is the only address permitted to execute `MsgCommunityPoolSpend` transfers from the Community Pool. When a governance proposal passes, this address signs and sends the requested funds to the specified recipient.

It also holds unallocated GNK set aside for governance-approved programmes that use batch-vesting or multi-send distributions.

<!-- GOV_BALANCE_START -->
<p style="margin:0.2rem 0">
<strong>Current balance:</strong> <span style="color:var(--md-accent-fg-color,#5468ff);font-size:1.05rem;font-weight:600">2M GNK</span>
</p>
<!-- GOV_BALANCE_END -->

<details style="margin:0.5rem 0;padding:0.6rem 1rem;border:1px solid var(--md-default-fg-color--lightest);border-radius:6px;background:var(--md-code-bg-color,#00000008)">
<summary style="cursor:pointer;font-weight:600;font-size:0.9rem">Verify on-chain</summary>

```
curl -s https://node3.gonka.ai/chain-api/cosmos/bank/v1beta1/balances/gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33
```

</details>

---

## How Community Pool Spending Works

1. A governance proposal includes one or more funding messages — `MsgCommunityPoolSpend` (GNK/USDT from the Community Pool) or batch-vesting transfers (GNK from the Gov Module).
2. If the proposal **passes**, the Gov Module authority address executes the transfers.
3. USDT is held in the Community Pool as the IBC denom `ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4` and transferred via `MsgExecuteContract` (withdraw_ibc).

**Key constraint:** No single key controls these funds — every spend requires a passed governance vote.

---

## Historical Funding

All **passed** governance proposals that received funding from the Community Pool or Gov Module, sorted by descending proposal number.

<!-- SPENT_HISTORY_START -->
| Proposal | Date | Description | Source | Amount GNK | Amount USDT |
| :------ | :--: | :---------- | :---- | ---------: | ---------: |
| [#82](https://gonkadocs.com/proposals/proposals/2026-q3/82/) | 2026-07-10 | External Test Lab x Community DevNet | Community Pool | 80,000 | $88,000 |
| [#77](https://gonkadocs.com/proposals/proposals/2026-q2/77/) | 2026-06-26 | Gonka PR Proposal for US/Global Regions | Community Pool | — | $75,000 |
| [#76](https://gonkadocs.com/proposals/proposals/2026-q2/76/) | 2026-06-17 | Governance 16: devshard v2 and bounty payouts | Community Pool | — | $93,600 |
| [#74](https://gonkadocs.com/proposals/proposals/2026-q2/74/) | 2026-06-12 | Gonka Labs: Maintaining Infrastructure, Improving Products,… | Community Pool + Gov Module | 330,000 | $70,000 |
| [#68](https://gonkadocs.com/proposals/proposals/2026-q2/68/) | 2026-06-07 | Big YouTube Deep-Dive on Falcon Finance (Alexander Sokolovs… | Community Pool | — | $70,000 |
| [#67](https://gonkadocs.com/proposals/proposals/2026-q2/67/) | 2026-06-05 | Kimi Restitution (epochs 265-276) | Gov Module | 946,509 | — |
| [#65](https://gonkadocs.com/proposals/proposals/2026-q2/65/) | 2026-06-04 | TheSoul - Offer 2.3: Digital strategy (100,000 GNK) | Community Pool | 100,000 | — |
| [#64](https://gonkadocs.com/proposals/proposals/2026-q2/64/) | 2026-06-04 | TheSoul - Offer 2.2: Analytics and attribution (28,000 GNK) | Community Pool | 28,000 | — |
| [#63](https://gonkadocs.com/proposals/proposals/2026-q2/63/) | 2026-06-04 | TheSoul - Offer 2.1: Website and landings (10,000 USDT) | Community Pool | — | $10,000 |
| [#62](https://gonkadocs.com/proposals/proposals/2026-q2/62/) | 2026-06-04 | TheSoul - Offer 1.3: Influencer pilot (50,000 USDT) | Community Pool | — | $50,000 |
| [#61](https://gonkadocs.com/proposals/proposals/2026-q2/61/) | 2026-06-04 | TheSoul - Offer 1.2: Brandbook (20,000 USDT) | Community Pool | — | $20,000 |
| [#60](https://gonkadocs.com/proposals/proposals/2026-q2/60/) | 2026-06-04 | TheSoul - Offer 1.1: Brand positioning (25,000 USDT) | Community Pool | — | $25,000 |
| [#55](https://gonkadocs.com/proposals/proposals/2026-q2/55/) | 2026-05-23 | GRC Proposal #2 - Restitution (epochs 248-254) | Community Pool + Gov Module | 346,029 | — |
| [#51](https://gonkadocs.com/proposals/proposals/2026-q2/51/) | 2026-05-15 | Support Gonka's presence at WebX Asia | Community Pool | — | $75,000 |
| [#50](https://gonkadocs.com/proposals/proposals/2026-q2/50/) | 2026-05-09 | Retroactive bounty: open-source PoC throughput optimization… | Community Pool | 20,000 | — |
| [#49](https://gonkadocs.com/proposals/proposals/2026-q2/49/) | 2026-05-07 | Gonka Media Dominance in TechL/AI with 5 AI Influencers | Community Pool | — | $45,000 |
| [#46](https://gonkadocs.com/proposals/proposals/2026-q2/46/) | 2026-05-04 | Epochs 132-247 compensation payout from gov module (batch v… | Gov Module | 3,053,800 | — |
| [#42](https://gonkadocs.com/proposals/proposals/2026-q2/42/) | 2026-04-19 | Support Gonka at Global Compute Sovereignty Summit | Community Pool | — | $10,000 |
| [#39](https://gonkadocs.com/proposals/proposals/2026-q2/39/) | 2026-04-10 | Community Series Film — Why Gonka Exists | Community Pool | 31,250 | — |
| [#33](https://gonkadocs.com/proposals/proposals/2026-q1/33/) | 2026-03-27 | Epochs 132-133 compensation payout from gov module | Community Pool + Gov Module | 27,906 | — |
| [#32](https://gonkadocs.com/proposals/proposals/2026-q1/32/) | 2026-03-24 | Epoch 158 compensation payout from gov module (batch vestin… | Community Pool + Gov Module | 30,538 | — |
| [#14](https://gonkadocs.com/proposals/proposals/2025-q4/14/) | 2025-11-27 | Sale GNK from Community Fund | Community Pool | 20,000,000 | — |

| Metric | Value |
| :----- | :---- |
| Total funded proposals | 22 |
| Total GNK approved | 24,994,032 GNK |
| Total USDT approved | $631,600 |
| From Community Pool | 20,993,723 GNK + $631,600 |
| From Gov Module | 4,734,782 GNK |
| Largest funding | #14 — 20,000,000 GNK |
| Most recent | #82 — 80,000 GNK + $88,000 USDT |
<!-- SPENT_HISTORY_END -->

---

