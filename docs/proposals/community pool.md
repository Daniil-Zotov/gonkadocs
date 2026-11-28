---
title: Community Pool
description: "Community Pool, Community Sale wallet, and Gov Module — addresses, balances, inflow/outflow mechanics, and full funding history of passed governance proposals"
hide:
  - toc
---

# Community Pool

The Gonka network maintains three key addresses that collectively manage community funds. This page documents their current balances, how funds flow between them, and every passed governance proposal that has received funding.

<small>Last updated: <!-- UPDATE_TIMESTAMP -->
2026-11-28 00:58 UTC
<!-- /UPDATE_TIMESTAMP --></small>

---

## Community Pool (distribution module)

**Address:** [`gonka1jv65s3grqf6v6jl3dp4t6c9t9rk99cd8h2rzwa`](https://gonka.gg/address/gonka1jv65s3grqf6v6jl3dp4t6c9t9rk99cd8h2rzwa)

<!-- BALANCES_START -->
<p style="margin:0.2rem 0">
<strong>Current balance:</strong> <span style="color:var(--md-accent-fg-color,#5468ff);font-size:0.95rem;font-weight:600">115,620,110 GNK</span>
</p>
<!-- BALANCES_END -->

The Community Pool is the protocol-controlled treasury of the Gonka network. It accrues value through a **2% community tax** applied to inflation rewards and network fees — although chain inflation is currently **disabled** (mint inflation max/min = 0), so the steady accrual comes only from fees. These funds can only be spent through a successful governance vote — no single key controls them.

Since the network genesis, the Community Pool has received inflows from the 2% community tax (fees and, historically, inflation rewards), funding ecosystem development, marketing initiatives, and community programmes through passed governance proposals.

**Direct deposits:** anyone can fund the pool with `MsgFundCommunityPool`. On **2026-11-19** two deposits landed within minutes of each other — **11,999,999.999 GNK** from [`gonka1qekvfdemp…`](https://gonka.gg/address/gonka1qekvfdempdq5vvqz26sts79zh6zv85su34p6u3) ([tx B879F107…](https://gonka.gg/transactions/B879F1076D8A4C5BDECA0E5EABAFFA21FB0DF1C30A0AA4D6882F0054AC252A6B)) and **900,401.005 GNK** from [`gonka1gk48e8tz9…`](https://gonka.gg/address/gonka1gk48e8tz9y85j9fpeyh6gww3rks98ht2d6s26v) ([tx FA6CBC63…](https://gonka.gg/transactions/FA6CBC63F0950B508AE25A4B92EE85F57777D3A4793328CD56B2978FF5BB2EEA)) — a combined **+12,900,401 GNK**, by far the largest one-day inflow to the pool.

*Returned USDT sits in the pool as the IBC denom `ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4` until it is spent through a governance vote — e.g. the **$10,000** returned from **[proposal #42](https://gonkadocs.com/proposals/proposals/2026-q2/42/)** after the planned Global Compute Sovereignty Summit was cancelled (see the [return instructions](https://gonkadocs.com/community/discussion/show-and-tell/1390-how-to-return-funds-to-the-community-pool-ibc-usdt/)). Note that most USDT payouts to contractors and bounty hunters are funded from the **Community Sale contract** below rather than from the distribution-module pool.*

**Steady inflow:** with inflation disabled, the 2% fee tax adds effectively nothing right now (measured: the pool balance stays static over hours — nano-GNK drift at most) — one-off deposits like the 2026-11-19 ones dominate balance movements. Verified on-chain: `inflation = 0`, `annual_provisions = 0` (`curl https://node3.gonka.ai/chain-api/cosmos/mint/v1beta1/inflation`), and the chain wires the standard cosmos-sdk mint module with no custom minting into the pool.

<details style="font-size:0.8rem;opacity:0.7;padding-left:0.5rem;margin:0.2rem 0">
<summary style="cursor:pointer;font-weight:500;padding-left:2.5em!important">Verify on-chain</summary>

```
curl -s https://node3.gonka.ai/chain-api/cosmos/distribution/v1beta1/community_pool
```

</details>

---

## Community Sale

**Address:** [`gonka18pkq9mwxxlmyq7kr5txhm060wemg2s4u94wvsfd9w2kdc0u99d6spk8pz2`](https://gonka.gg/address/gonka18pkq9mwxxlmyq7kr5txhm060wemg2s4u94wvsfd9w2kdc0u99d6spk8pz2)

<!-- SALE_BALANCE_START -->
<p style="margin:0.2rem 0">
<strong>Current balance:</strong> <span style="color:grey;font-size:0.95rem;font-weight:600">14,583,332 GNK</span> <span style="color:var(--md-accent-fg-color,#5468ff);font-size:0.95rem;font-weight:600">(~$8,749,999 USDT)</span> · <span style="color:var(--md-accent-fg-color,#5468ff);font-size:0.95rem;font-weight:600">$1,425 USDT</span> · <span style="color:var(--md-accent-fg-color,#5468ff);font-size:0.95rem;font-weight:600">$276,751 USDT (CW20 bridged)</span>
</p>
<!-- SALE_BALANCE_END -->

This address was created by **[proposal #14](/proposals/proposals/2025-q4/14/)** (passed 2025-11-27), which transferred **20,000,000 GNK** from the Community Pool to seed a community sale programme at a fixed price of **$0.60 per GNK**.

The mechanism works as a simple swap: participants deposit **USDT** and receive **GNK** at the predetermined rate. The address holds both assets — USDT collected from buyers and the remaining GNK inventory.

Buyer USDT arrives in two forms: the IBC denom `ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4`, and the **bridged CW20 USDT** — token contract [`gonka15ggwj9un6qrmu4nj5ev6l7kpdcr00td03ff2mmj4cyhl8u8vjd2qnl3hgk`](https://gonka.gg/address/gonka15ggwj9un6qrmu4nj5ev6l7kpdcr00td03ff2mmj4cyhl8u8vjd2qnl3hgk) ("Tether USD", 6 decimals, bridged from Ethereum `0xdAC17f958D2ee523a2206206994597C13d831ec7`).

**[Proposal #117](/proposals/proposals/2026-q4/117/)** (passed 2026-11-13) used the CW20 route: Bitfury paid **1,750,000 USDT** for the next tranche of the previously approved 12M USDT Community Sale commitment at $0.60 per GNK. Of that, **607,250 USDT** was paid back to Bitfury as reimbursement for the HackerOne and Trail of Bits security costs it had covered in fiat directly to vendors, so the net **+1,142,750 USDT** stayed in the Community Sale contract (community treasury side), and **2,916,666 GNK** (1.75M ÷ $0.60) left the sale inventory.

For security, sale proceeds are distributed in **tranches** rather than all at once. The contract releases batches of GNK gradually to mitigate risk and ensure safe execution.

The USDT held here is used to pay **bug bounties and development rewards** — distributed automatically through the chain's **upgrade handler** during network hard forks, without requiring individual governance votes. Each upgrade version embeds a `distributeBountyRewards()` call that withdraws USDT directly from this contract to recipient addresses.

**Important:** The GNK held here is **not part of the Community Pool**. It is the undistributed balance of the sale contract — already allocated in proposal #14 and awaiting exchange. Only the USDT received from buyers is new value entering the Gonka ecosystem.

<details style="font-size:0.8rem;opacity:0.7;padding-left:0.5rem;margin:0.2rem 0">
<summary style="cursor:pointer;font-weight:500;padding-left:2.5em!important">Verify on-chain</summary>

```
# GNK + IBC USDT held by the Community Sale contract
curl -s https://node3.gonka.ai/chain-api/cosmos/bank/v1beta1/balances/gonka18pkq9mwxxlmyq7kr5txhm060wemg2s4u94wvsfd9w2kdc0u99d6spk8pz2
# CW20 bridged USDT held by the Community Sale contract
curl -s "https://node3.gonka.ai/chain-api/cosmwasm/wasm/v1/contract/gonka15ggwj9un6qrmu4nj5ev6l7kpdcr00td03ff2mmj4cyhl8u8vjd2qnl3hgk/smart/eyJiYWxhbmNlIjp7ImFkZHJlc3MiOiJnb25rYTE4cGtxOW13eHhsbXlxN2tyNXR4aG0wNjB3ZW1nMnM0dTk0d3ZzZmQ5dzJrZGMwdTk5ZDZzcGs4cHoyIn19"
```

</details>

---

## Gov Module (authority)

**Address:** [`gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33`](https://gonka.gg/address/gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33)

<!-- GOV_BALANCE_START -->
<p style="margin:0.2rem 0">
<strong>Current balance:</strong> <span style="color:var(--md-accent-fg-color,#5468ff);font-size:0.95rem;font-weight:600">8,461,740 GNK</span>
</p>
<!-- GOV_BALANCE_END -->

The Gov Module authority is the only address permitted to execute `MsgCommunityPoolSpend` transfers from the Community Pool. When a governance proposal passes, this address signs and sends the requested funds to the specified recipient.

It also holds unallocated GNK set aside for governance-approved programmes that use batch-vesting or multi-send distributions.

<details style="font-size:0.8rem;opacity:0.7;padding-left:0.5rem;margin:0.2rem 0">
<summary style="cursor:pointer;font-weight:500;padding-left:2.5em!important">Verify on-chain</summary>

```
curl -s https://node3.gonka.ai/chain-api/cosmos/bank/v1beta1/balances/gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33
```

</details>

---

## How Community Pool Spending Works

1. A governance proposal includes one or more funding messages — `MsgCommunityPoolSpend` (GNK/USDT from the Community Pool), `MsgExecuteContract` (USDT from the Community Sale contract), or batch-vesting transfers (GNK from the Gov Module).
2. If the proposal **passes**, the Gov Module authority address executes the transfers.
3. USDT is paid out from the **Community Sale contract** via `MsgExecuteContract` — either as the IBC denom `ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4` (`withdraw_ibc`, e.g. #113, #116) or as the bridged CW20 USDT `gonka15ggwj9un6qrmu4nj5ev6l7kpdcr00td03ff2mmj4cyhl8u8vjd2qnl3hgk` (`withdraw_cw20`, e.g. #117, #118). USDT held in the Community Pool itself sits as the IBC denom.

**Key constraint:** No single key controls these funds — every spend requires a passed governance vote.

---

## Historical Funding

All **passed** governance proposals that moved funds through the Community Pool, the Community Sale contract, or the Gov Module, sorted by descending proposal number. Amounts are shown **gross** — inflows and payouts are separate rows, never netted together. Rows marked **(inflow)** are deposits into community-controlled addresses rather than spending. Example — **#117**: Bitfury's **1,750,000 USDT** tranche came in, and **607,250 USDT** was immediately paid back out to Bitfury as reimbursement for audit costs, leaving a net of **+$1,142,750** in the Community Sale contract.

<!-- SPENT_HISTORY_START -->
| Proposal | Date | Description | Source | Amount GNK | Amount USDT |
| :------ | :--: | :---------- | :---- | ---------: | ---------: |
| [#118](https://gonkadocs.com/proposals/proposals/2026-q4/118/) | 2026-11-13 | Dev Team Funding | Community Sale | — | $866,000 |
| [#117](https://gonkadocs.com/proposals/proposals/2026-q4/117/) | 2026-11-13 | Bitfury buys another tranche of GNK for 1.75M USDT as part … | Community Sale (inflow) | — | +$1,750,000 |
| [#117](https://gonkadocs.com/proposals/proposals/2026-q4/117/) | 2026-11-13 | Bitfury buys another tranche of GNK for 1.75M USDT as part … | Community Sale | — | $607,250 |
| [#116](https://gonkadocs.com/proposals/proposals/2026-q4/116/) | 2026-11-11 | Approve DevShard v6 and distribute bounty rewards | Community Pool + Community Sale + Gov Module | 170,000 | $69,425 |
| [#113](https://gonkadocs.com/proposals/proposals/2026-q4/113/) | 2026-10-08 | Distribute v0.2.16 bounty rewards | Community Sale | — | $104,150 |
| [#110](https://gonkadocs.com/proposals/proposals/2026-q4/110/) | 2026-10-03 | GRC Proposal #4 - Restitution | Community Sale + Gov Module | 132,896 | $2,100 |
| [#105](https://gonkadocs.com/proposals/proposals/2026-q3/105/) | 2026-09-18 | Approve devshard v5 and bounty payouts | Community Sale | — | $91,300 |
| [#103](https://gonkadocs.com/proposals/proposals/2026-q3/103/) | 2026-09-12 | Reimbursement of Expenses for Daniil and David Liberman's P… | Community Sale | — | $15,500 |
| [#102](https://gonkadocs.com/proposals/proposals/2026-q3/102/) | 2026-09-11 | Ratify Quant Mesh Limited as the Ledger Integration Counter… | Community Sale | — | $350,350 |
| [#99](https://gonkadocs.com/proposals/proposals/2026-q3/99/) | 2026-09-04 | Support Gonka's presence at TOKEN2049 Singapore | Community Sale | — | $100,000 |
| [#82](https://gonkadocs.com/proposals/proposals/2026-q3/82/) | 2026-07-10 | External Test Lab x Community DevNet | Community Pool + Community Sale | 80,000 | $88,000 |
| [#77](https://gonkadocs.com/proposals/proposals/2026-q2/77/) | 2026-06-26 | Gonka PR Proposal for US/Global Regions | Community Sale | — | $75,000 |
| [#76](https://gonkadocs.com/proposals/proposals/2026-q2/76/) | 2026-06-17 | Governance 16: devshard v2 and bounty payouts | Community Sale | — | $93,600 |
| [#74](https://gonkadocs.com/proposals/proposals/2026-q2/74/) | 2026-06-12 | Gonka Labs: Maintaining Infrastructure, Improving Products,… | Community Sale + Gov Module | 330,000 | $70,000 |
| [#68](https://gonkadocs.com/proposals/proposals/2026-q2/68/) | 2026-06-07 | Big YouTube Deep-Dive on Falcon Finance (Alexander Sokolovs… | Community Sale | — | $70,000 |
| [#67](https://gonkadocs.com/proposals/proposals/2026-q2/67/) | 2026-06-05 | Kimi Restitution (epochs 265-276) | Gov Module | 946,509 | — |
| [#65](https://gonkadocs.com/proposals/proposals/2026-q2/65/) | 2026-06-04 | TheSoul - Offer 2.3: Digital strategy (100,000 GNK) | Community Pool | 100,000 | — |
| [#64](https://gonkadocs.com/proposals/proposals/2026-q2/64/) | 2026-06-04 | TheSoul - Offer 2.2: Analytics and attribution (28,000 GNK) | Community Pool | 28,000 | — |
| [#63](https://gonkadocs.com/proposals/proposals/2026-q2/63/) | 2026-06-04 | TheSoul - Offer 2.1: Website and landings (10,000 USDT) | Community Sale | — | $10,000 |
| [#62](https://gonkadocs.com/proposals/proposals/2026-q2/62/) | 2026-06-04 | TheSoul - Offer 1.3: Influencer pilot (50,000 USDT) | Community Sale | — | $50,000 |
| [#61](https://gonkadocs.com/proposals/proposals/2026-q2/61/) | 2026-06-04 | TheSoul - Offer 1.2: Brandbook (20,000 USDT) | Community Sale | — | $20,000 |
| [#60](https://gonkadocs.com/proposals/proposals/2026-q2/60/) | 2026-06-04 | TheSoul - Offer 1.1: Brand positioning (25,000 USDT) | Community Sale | — | $25,000 |
| [#55](https://gonkadocs.com/proposals/proposals/2026-q2/55/) | 2026-05-23 | GRC Proposal #2 - Restitution (epochs 248-254) | Community Pool + Gov Module | 346,029 | — |
| [#51](https://gonkadocs.com/proposals/proposals/2026-q2/51/) | 2026-05-15 | Support Gonka's presence at WebX Asia | Community Sale | — | $75,000 |
| [#50](https://gonkadocs.com/proposals/proposals/2026-q2/50/) | 2026-05-09 | Retroactive bounty: open-source PoC throughput optimization… | Community Pool | 20,000 | — |
| [#49](https://gonkadocs.com/proposals/proposals/2026-q2/49/) | 2026-05-07 | Gonka Media Dominance in TechL/AI with 5 AI Influencers | Community Sale | — | $45,000 |
| [#46](https://gonkadocs.com/proposals/proposals/2026-q2/46/) | 2026-05-04 | Epochs 132-247 compensation payout from gov module (batch v… | Gov Module | 3,053,800 | — |
| [#42](https://gonkadocs.com/proposals/proposals/2026-q2/42/) | 2026-04-19 | Support Gonka at Global Compute Sovereignty Summit | Community Sale | — | $10,000 |
| [#39](https://gonkadocs.com/proposals/proposals/2026-q2/39/) | 2026-04-10 | Community Series Film — Why Gonka Exists | Community Pool | 31,250 | — |
| [#33](https://gonkadocs.com/proposals/proposals/2026-q1/33/) | 2026-03-27 | Epochs 132-133 compensation payout from gov module | Community Pool + Gov Module | 27,906 | — |
| [#32](https://gonkadocs.com/proposals/proposals/2026-q1/32/) | 2026-03-24 | Epoch 158 compensation payout from gov module (batch vestin… | Community Pool + Gov Module | 30,538 | — |
| [#14](https://gonkadocs.com/proposals/proposals/2025-q4/14/) | 2025-11-27 | Sale GNK from Community Fund | Community Pool | 20,000,000 | — |
| [PR #919](https://github.com/gonka-ai/gonka/pull/919) | 2026-03 | v0.2.11 bounty distribution | Upgrade Handler (Gov Module) | 150,750 | — |
| [PR #1446](https://github.com/gonka-ai/gonka/pull/1446) | 2026-07 | v0.2.14 bounty distribution | Upgrade Handler (Community Sale) | — | $50,250 |
| [PR #1503](https://github.com/gonka-ai/gonka/pull/1503) | 2026-07 | v0.2.15 bounty distribution | Upgrade Handler (Community Sale) | — | $39,825 |
| [PR #1113](https://github.com/gonka-ai/gonka/pull/1113) | 2026-04 | v0.2.12 bounty distribution | Upgrade Handler (Community Sale) | — | $35,200 |
| [PR #497](https://github.com/gonka-ai/gonka/pull/497) | 2026-01 | v0.2.6 bounty distribution | Upgrade Handler (Gov Module) | 30,000 | — |
| [PR #733](https://github.com/gonka-ai/gonka/pull/733) | 2026-02 | v0.2.10 bounty distribution | Upgrade Handler (Gov Module) | 23,000 | — |
| [PR #1168](https://github.com/gonka-ai/gonka/pull/1168) | 2026-05 | v0.2.13 bounty distribution | Upgrade Handler (Community Sale) | — | $18,875 |

| Metric | Value |
| :----- | :---- |
| Total governance proposals | 31 |
| Total GNK approved (proposals) | 25,296,928 GNK |
| Total USDT approved (proposals) | $2,837,675 |
| From Community Pool | 20,387,572 GNK + $10,000 |
| From Community Sale (proposals) | 0 GNK + $2,827,675 |
| From Gov Module | 4,909,356 GNK |
| Community Sale inflows (proposals) | +$1,750,000 |
| Community Sale net (deposits − same-source payouts) | +$1,142,750 |
| Largest funding | #14 — 20,000,000 GNK |
| Most recent | #118 — $866,000 USDT |
| **Bounty distributions** | **8** |
| Total GNK distributed (bounties) | 203,750 GNK |
| Total USDT distributed (bounties) | $248,300 |
| From Community Sale contract | $248,300 USDT |
| From Gov Module | 203,750 GNK |
<!-- SPENT_HISTORY_END -->

---

## Bounty Distribution

Bounties are paid through the chain's **upgrade handler** — hardcoded in each network upgrade and executed automatically when validators update.

USDT bounties are paid from the **Community Sale contract** via `withdraw_ibc`. GNK bounties are distributed from the **Gov Module**.

Exception: the **v0.2.16** bounties were distributed by governance proposal **[#113](/proposals/proposals/2026-q4/113/)** (16 payments, $104,150) — the upgrade handler defines `distributeBountyRewards` for that version but never calls it, so the identical list went through an on-chain vote instead.

<!-- BOUNTY_TABLE_START -->
| Version | PR | Status | Date | Recipients | Total GNK | Total USDT | Source
| :------ | :- | :----- | :--- | :--------- | --------: | --------: | :----
| v0.2.16 | [Proposal #113](https://gonkadocs.com/proposals/proposals/2026-q4/113/) | Passed | 2026-10 | 16 recipients | — | $104,150 | Community Sale |
| v0.2.15 | [PR #1503](https://github.com/gonka-ai/gonka/pull/1503) | Merged | 2026-07 | 8 recipients | — | $39,825 | Community Sale |
| v0.2.14 | [PR #1446](https://github.com/gonka-ai/gonka/pull/1446) | Merged | 2026-07 | 17 recipients | — | $50,250 | Community Sale |
| v0.2.13 | [PR #1168](https://github.com/gonka-ai/gonka/pull/1168) | Merged | 2026-05 | 4 recipients | — | $18,875 | Community Sale |
| v0.2.12 | [PR #1113](https://github.com/gonka-ai/gonka/pull/1113) | Merged | 2026-04 | 13 recipients | — | $35,200 | Community Sale |
| v0.2.11 | [PR #919](https://github.com/gonka-ai/gonka/pull/919) | Merged | 2026-03 | 26 recipients | 150,750 | — | Gov Module |
| v0.2.10 | [PR #733](https://github.com/gonka-ai/gonka/pull/733) | Merged | 2026-02 | 11 recipients | 23,000 | — | Gov Module |
| v0.2.6 | [PR #497](https://github.com/gonka-ai/gonka/pull/497) | Merged | 2026-01 | 2 recipients | 30,000 | — | Gov Module |
<!-- BOUNTY_TABLE_END -->

### Recipient Details

<!-- BOUNTY_DETAIL_START -->
### v0.2.16 — [Proposal #113](https://gonkadocs.com/proposals/proposals/2026-q4/113/) (Passed)

| Recipient | Address | Amount | Description |
| :------- | :------ | ----: | :---------- |
| kaitaku.ai (@baychak, @clanster) | [`gonka1x45hruazmcqxslj3g8a08988hr5fr3wx33drhp`](https://gonka.gg/address/gonka1x45hruazmcqxslj3g8a08988hr5fr3wx33drhp) | $12,000 USDT | ML-node observability: metrics exporter, DAPI federation endpoint, Grafana dashboards (gonka-grafana) + hosting monitoring.kaitaku.ai |
| @qdanik | [`gonka1j3f2xkapx8cmczpjqcsrh7cc3peyj3ngkjv4p8`](https://gonka.gg/address/gonka1j3f2xkapx8cmczpjqcsrh7cc3peyj3ngkjv4p8) | $500 USDT | Contribution to the ML-node observability track |
| kaitaku.ai (@baychak, @clanster) | [`gonka1x45hruazmcqxslj3g8a08988hr5fr3wx33drhp`](https://gonka.gg/address/gonka1x45hruazmcqxslj3g8a08988hr5fr3wx33drhp) | $20,000 USDT | decode-PoC: vLLM port and experiments with reevaluation on all hardware schemes and models |
| Axel-t | [`gonka1yhdhp4vwsvdsplv4acksntx0zxh8saueq6lj9m`](https://gonka.gg/address/gonka1yhdhp4vwsvdsplv4acksntx0zxh8saueq6lj9m) | $18,000 USDT | CUDA Graph Support for Decode PoC |
| kaitaku.ai (@baychak, @clanster) | [`gonka1x45hruazmcqxslj3g8a08988hr5fr3wx33drhp`](https://gonka.gg/address/gonka1x45hruazmcqxslj3g8a08988hr5fr3wx33drhp) | $5,000 USDT | gonka-poc as plugin: removes re-porting PoC on every vLLM release |
| kaitaku.ai (@baychak, @clanster) | [`gonka1x45hruazmcqxslj3g8a08988hr5fr3wx33drhp`](https://gonka.gg/address/gonka1x45hruazmcqxslj3g8a08988hr5fr3wx33drhp) | $5,000 USDT | DeepSeek-V4-Flash: experiments and new model proposal |
| kaitaku.ai (@baychak, @clanster) | [`gonka1x45hruazmcqxslj3g8a08988hr5fr3wx33drhp`](https://gonka.gg/address/gonka1x45hruazmcqxslj3g8a08988hr5fr3wx33drhp) | $4,000 USDT | GLM-5.3-Flash: experiments and new model proposal |
| kaitaku.ai (@baychak, @clanster) | [`gonka1x45hruazmcqxslj3g8a08988hr5fr3wx33drhp`](https://gonka.gg/address/gonka1x45hruazmcqxslj3g8a08988hr5fr3wx33drhp) | $2,000 USDT | GLM-5.2: experiments, images for B300/B200/H200 |
| kaitaku.ai (@baychak, @clanster) | [`gonka1x45hruazmcqxslj3g8a08988hr5fr3wx33drhp`](https://gonka.gg/address/gonka1x45hruazmcqxslj3g8a08988hr5fr3wx33drhp) | $2,000 USDT | Hy3 evaluation experiments |
| kaitaku.ai (@baychak, @clanster) | [`gonka1x45hruazmcqxslj3g8a08988hr5fr3wx33drhp`](https://gonka.gg/address/gonka1x45hruazmcqxslj3g8a08988hr5fr3wx33drhp) | $9,600 USDT | GPU rental reimbursement for model and PoC experiments since 2026-06-01 (Verda, Vast, Dataoorts, Nebius), at cost |
| @x0152 | [`gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe`](https://gonka.gg/address/gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe) | $8,000 USDT | Release management: PR reviews, HackerOne report reviews, Trainshards v0 (PR #1350, #1618) |
| @vitaly-andr | [`gonka1uqt4hue8tljwwgdkvtthyl3n8kkkqtydyns4cm`](https://gonka.gg/address/gonka1uqt4hue8tljwwgdkvtthyl3n8kkkqtydyns4cm) | $5,000 USDT | Chain-halt bug report (Issue #1205) + fix (cosmos-sdk PR #16) |
| @vitaly-andr | [`gonka1uqt4hue8tljwwgdkvtthyl3n8kkkqtydyns4cm`](https://gonka.gg/address/gonka1uqt4hue8tljwwgdkvtthyl3n8kkkqtydyns4cm) | $1,000 USDT | v0.2.16 upgrade review |
| @bonujel | [`gonka1zqss46r6jf6dhhyaa777kc2ppvjhn0ufkx4y57`](https://gonka.gg/address/gonka1zqss46r6jf6dhhyaa777kc2ppvjhn0ufkx4y57) | $1,000 USDT | v0.2.16 upgrade review |
| @staaason / @zpoken | [`gonka1s8zggm642e3kncy48c7vxwmeclt2wxyyd8qtdt`](https://gonka.gg/address/gonka1s8zggm642e3kncy48c7vxwmeclt2wxyyd8qtdt) | $8,050 USDT | HackerOne report reviews + PR #1767, #1552 (landed as PR #1623) |
| @cyberdelamain | [`gonka15u0r3mf6t7zsfuslusnyt7hsjrq357yumpe8st`](https://gonka.gg/address/gonka15u0r3mf6t7zsfuslusnyt7hsjrq357yumpe8st) | $3,000 USDT | v0.2.16 review and fixes: PR #1828, #1846, #1845, #1859 |
| **Total** | | **$104,150 USDT** | |


### v0.2.15 — [PR #1503](https://github.com/gonka-ai/gonka/pull/1503) (Merged)

| Recipient | Address | Amount | Description |
| :------- | :------ | ----: | :---------- |
| @akup | [`gonka1ejkupq3cy6p8xd64ew2wlzveml86ckpzn9dl56`](https://gonka.gg/address/gonka1ejkupq3cy6p8xd64ew2wlzveml86ckpzn9dl56) | $22,000 USDT | RM: devshard v4 release management |
| @Ryanchen911 | [`gonka1zqss46r6jf6dhhyaa777kc2ppvjhn0ufkx4y57`](https://gonka.gg/address/gonka1zqss46r6jf6dhhyaa777kc2ppvjhn0ufkx4y57) | $1,000 USDT | RM: devshard v4 upgrade review |
| @redstartechno | [`gonka105ce4495mj0mwkxqeasgdzqfq5jjrfq32eza5l`](https://gonka.gg/address/gonka105ce4495mj0mwkxqeasgdzqfq5jjrfq32eza5l) | $200 USDT | PR #1308: devshard contribution |
| @0xMayoor | [`gonka1s8szs7n43jxgz4a4xaxmzm5emh7fmjxhach7w8`](https://gonka.gg/address/gonka1s8szs7n43jxgz4a4xaxmzm5emh7fmjxhach7w8) | $3,000 USDT | PR #1283: report and fix of medium severity vulnerability |
| @0xMayoor | [`gonka1s8szs7n43jxgz4a4xaxmzm5emh7fmjxhach7w8`](https://gonka.gg/address/gonka1s8szs7n43jxgz4a4xaxmzm5emh7fmjxhach7w8) | $500 USDT | PR #1311: report and fix of low severity vulnerability |
| @pixelplex | [`gonka1vu28c7w5zxqe28lakrrfdrkvscft326rxur3dv`](https://gonka.gg/address/gonka1vu28c7w5zxqe28lakrrfdrkvscft326rxur3dv) | $7,000 USDT | PR #1144, #1152, #1126, #1154: devshard contribution |
| @aikuznetsov | [`gonka1frlfyz2wtltdy47dq3w9pwc8ruvjvlthp2lh53`](https://gonka.gg/address/gonka1frlfyz2wtltdy47dq3w9pwc8ruvjvlthp2lh53) | $3,125 USDT | PR #1332, #1295: testing proposal and implementation |
| @snevolin | [`gonka1vnupswg7qz2w5k5ax6zrp02mxmln6arnvjc87h`](https://gonka.gg/address/gonka1vnupswg7qz2w5k5ax6zrp02mxmln6arnvjc87h) | $3,000 USDT | PR #1437, #1490: devshard contribution |
| **Total** | | **$39,825 USDT** | |


### v0.2.14 — [PR #1446](https://github.com/gonka-ai/gonka/pull/1446) (Merged)

| Recipient | Address | Amount | Description |
| :------- | :------ | ----: | :---------- |
| @akup | [`gonka1ejkupq3cy6p8xd64ew2wlzveml86ckpzn9dl56`](https://gonka.gg/address/gonka1ejkupq3cy6p8xd64ew2wlzveml86ckpzn9dl56) | $5,000 USDT | devshards v3 RM, upgrade review, HackerOne reviews |
| @x0152 | [`gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe`](https://gonka.gg/address/gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe) | $6,000 USDT | RM, HackerOne reviews |
| @qdanik | [`gonka1j3f2xkapx8cmczpjqcsrh7cc3peyj3ngkjv4p8`](https://gonka.gg/address/gonka1j3f2xkapx8cmczpjqcsrh7cc3peyj3ngkjv4p8) | $11,500 USDT | RM, HackerOne reviews, MiniMax M2.7 R&D, PoC (incl. GPU), SMST optimization (PR #1432) |
| @ouicate | [`gonka1f0elpwnx7ezytdlck35003nz6qk8kzvurvnj4a`](https://gonka.gg/address/gonka1f0elpwnx7ezytdlck35003nz6qk8kzvurvnj4a) | $1,000 USDT | PR #1253: stop stale PoC validation |
| @ouicate | [`gonka1f0elpwnx7ezytdlck35003nz6qk8kzvurvnj4a`](https://gonka.gg/address/gonka1f0elpwnx7ezytdlck35003nz6qk8kzvurvnj4a) | $1,000 USDT | PR #1255: settle before releasing unbonding |
| @ouicate | [`gonka1f0elpwnx7ezytdlck35003nz6qk8kzvurvnj4a`](https://gonka.gg/address/gonka1f0elpwnx7ezytdlck35003nz6qk8kzvurvnj4a) | $1,000 USDT | PR #1278: bound event-listener tx queue |
| @0xMayoor | [`gonka1s8szs7n43jxgz4a4xaxmzm5emh7fmjxhach7w8`](https://gonka.gg/address/gonka1s8szs7n43jxgz4a4xaxmzm5emh7fmjxhach7w8) | $500 USDT | PR #1100: prevent uint64 wrap in settle |
| @0xMayoor | [`gonka1s8szs7n43jxgz4a4xaxmzm5emh7fmjxhach7w8`](https://gonka.gg/address/gonka1s8szs7n43jxgz4a4xaxmzm5emh7fmjxhach7w8) | $750 USDT | PR #1101: widen ShouldValidate to uint64 |
| @0xMayoor | [`gonka1s8szs7n43jxgz4a4xaxmzm5emh7fmjxhach7w8`](https://gonka.gg/address/gonka1s8szs7n43jxgz4a4xaxmzm5emh7fmjxhach7w8) | $500 USDT | PR #1347: distribute unsettled escrow per slot |
| @0xMayoor | [`gonka1s8szs7n43jxgz4a4xaxmzm5emh7fmjxhach7w8`](https://gonka.gg/address/gonka1s8szs7n43jxgz4a4xaxmzm5emh7fmjxhach7w8) | $2,000 USDT | PR #1376: bridge block sync vulnerability |
| @alancapex | [`gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09`](https://gonka.gg/address/gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09) | $3,000 USDT | PR #889: on-chain configurable reward recipients |
| @Ryanchen911 | [`gonka1zqss46r6jf6dhhyaa777kc2ppvjhn0ufkx4y57`](https://gonka.gg/address/gonka1zqss46r6jf6dhhyaa777kc2ppvjhn0ufkx4y57) | $7,500 USDT | PR #998: implementing maintenance windows |
| @redstartechno | [`gonka105ce4495mj0mwkxqeasgdzqfq5jjrfq32eza5l`](https://gonka.gg/address/gonka105ce4495mj0mwkxqeasgdzqfq5jjrfq32eza5l) | $500 USDT | PR #1307: avoid query-gas-limit on grant check |
| @Lelouch33 | [`gonka128nd36m2pz5qcs4q6rd69622flyls05nleazqq`](https://gonka.gg/address/gonka128nd36m2pz5qcs4q6rd69622flyls05nleazqq) | $5,000 USDT | Vulnerability report 1 |
| @Lelouch33 | [`gonka128nd36m2pz5qcs4q6rd69622flyls05nleazqq`](https://gonka.gg/address/gonka128nd36m2pz5qcs4q6rd69622flyls05nleazqq) | $1,000 USDT | Vulnerability report 2 |
| @maksimenkoff | [`gonka1gmuxdcxlsxn5z72elx77w9zym7yrgfxqgzg6ry`](https://gonka.gg/address/gonka1gmuxdcxlsxn5z72elx77w9zym7yrgfxqgzg6ry) | $3,000 USDT | Vulnerability report and fix #1415 |
| @blizko | [`gonka12jaf7m4eysyqt32mrgarum6z96vt55tckvcleq`](https://gonka.gg/address/gonka12jaf7m4eysyqt32mrgarum6z96vt55tckvcleq) | $1,000 USDT | v0.2.13 upgrade review |
| **Total** | | **$50,250 USDT** | |


### v0.2.13 — [PR #1168](https://github.com/gonka-ai/gonka/pull/1168) (Merged)

| Recipient | Address | Amount | Description |
| :------- | :------ | ----: | :---------- |
| @blizko | [`gonka12jaf7m4eysyqt32mrgarum6z96vt55tckvcleq`](https://gonka.gg/address/gonka12jaf7m4eysyqt32mrgarum6z96vt55tckvcleq) | $8,000 USDT | Prompt of death: vLLM crash via structured outputs |
| kaitaku.ai | [`gonka1x45hruazmcqxslj3g8a08988hr5fr3wx33drhp`](https://gonka.gg/address/gonka1x45hruazmcqxslj3g8a08988hr5fr3wx33drhp) | $10,000 USDT | Kimi experiments report |
| @ouicate | [`gonka1f0elpwnx7ezytdlck35003nz6qk8kzvurvnj4a`](https://gonka.gg/address/gonka1f0elpwnx7ezytdlck35003nz6qk8kzvurvnj4a) | $500 USDT | PR #826: Partial Payment on Claim Failure Causes Permanent Reward Loss |
| @ouicate | [`gonka1f0elpwnx7ezytdlck35003nz6qk8kzvurvnj4a`](https://gonka.gg/address/gonka1f0elpwnx7ezytdlck35003nz6qk8kzvurvnj4a) | $375 USDT | PR #826: Underfunded Work Payout Still Removes Settle Amount |
| **Total** | | **$18,875 USDT** | |


### v0.2.12 — [PR #1113](https://github.com/gonka-ai/gonka/pull/1113) (Merged)

| Recipient | Address | Amount | Description |
| :------- | :------ | ----: | :---------- |
| @x0152 | [`gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe`](https://gonka.gg/address/gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe) | $6,000 USDT | CertiK audit fixes (GEB-29, GEB-35, …) |
| @x0152 | [`gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe`](https://gonka.gg/address/gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe) | $3,000 USDT | DKG dealer consensus — PR #825 |
| @x0152 | [`gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe`](https://gonka.gg/address/gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe) | $1,000 USDT | Developer inference access / account API |
| @x0152 | [`gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe`](https://gonka.gg/address/gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe) | $500 USDT | OpenAI compatibility and API error handling |
| @x0152 | [`gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe`](https://gonka.gg/address/gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe) | $2,500 USDT | v0.2.12 release management |
| @akup | [`gonka1ejkupq3cy6p8xd64ew2wlzveml86ckpzn9dl56`](https://gonka.gg/address/gonka1ejkupq3cy6p8xd64ew2wlzveml86ckpzn9dl56) | $5,000 USDT | v0.2.12 release management |
| — | [`gonka1yhdhp4vwsvdsplv4acksntx0zxh8saueq6lj9m`](https://gonka.gg/address/gonka1yhdhp4vwsvdsplv4acksntx0zxh8saueq6lj9m) | $9,000 USDT | Inference validation optimization — Issue #929 |
| — | [`gonka1vu28c7w5zxqe28lakrrfdrkvscft326rxur3dv`](https://gonka.gg/address/gonka1vu28c7w5zxqe28lakrrfdrkvscft326rxur3dv) | $3,000 USDT | Acquire node gRPC — PR #945 |
| @0xMayoor | [`gonka1s8szs7n43jxgz4a4xaxmzm5emh7fmjxhach7w8`](https://gonka.gg/address/gonka1s8szs7n43jxgz4a4xaxmzm5emh7fmjxhach7w8) | $2,000 USDT | Fund atomicity error safety — PR #789 |
| @qdanik | [`gonka1j3f2xkapx8cmczpjqcsrh7cc3peyj3ngkjv4p8`](https://gonka.gg/address/gonka1j3f2xkapx8cmczpjqcsrh7cc3peyj3ngkjv4p8) | $1,500 USDT | Align validator slashing — PR #940 |
| — | [`gonka1c34w3r45f0uftjckt2yy4k22vnc3zqjnp0umyz`](https://gonka.gg/address/gonka1c34w3r45f0uftjckt2yy4k22vnc3zqjnp0umyz) | $500 USDT | Free inference vulnerability report |
| — | [`gonka139f7x4gur2yuyty64dkqxep8jk3d7ku8ayjaqg`](https://gonka.gg/address/gonka139f7x4gur2yuyty64dkqxep8jk3d7ku8ayjaqg) | $200 USDT | Chat completions fix — Issue #499 |
| @blizko | [`gonka12jaf7m4eysyqt32mrgarum6z96vt55tckvcleq`](https://gonka.gg/address/gonka12jaf7m4eysyqt32mrgarum6z96vt55tckvcleq) | $1,000 USDT | Review of upgrade v0.2.11 |
| **Total** | | **$35,200 USDT** | |


### v0.2.11 — [PR #919](https://github.com/gonka-ai/gonka/pull/919) (Merged)

| Recipient | Address | Amount | Description |
| :------- | :------ | ----: | :---------- |
| @x0152 | [`gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe`](https://gonka.gg/address/gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe) | 2,500 GNK | Data race conditions fix review — PR #543 |
| — | [`gonka1yhdhp4vwsvdsplv4acksntx0zxh8saueq6lj9m`](https://gonka.gg/address/gonka1yhdhp4vwsvdsplv4acksntx0zxh8saueq6lj9m) | 25,000 GNK | PoC Integration into vLLM v0.11.1 — Issue #628 |
| @blizko | [`gonka12jaf7m4eysyqt32mrgarum6z96vt55tckvcleq`](https://gonka.gg/address/gonka12jaf7m4eysyqt32mrgarum6z96vt55tckvcleq) | 10,000 GNK | vLLM HTTP 502 via prompt series |
| @blizko | [`gonka12jaf7m4eysyqt32mrgarum6z96vt55tckvcleq`](https://gonka.gg/address/gonka12jaf7m4eysyqt32mrgarum6z96vt55tckvcleq) | 1,000 GNK | Dust transaction vulnerability report |
| @ouicate | [`gonka1f0elpwnx7ezytdlck35003nz6qk8kzvurvnj4a`](https://gonka.gg/address/gonka1f0elpwnx7ezytdlck35003nz6qk8kzvurvnj4a) | 5,000 GNK | Remote DoS of Validator PoC |
| @ouicate | [`gonka1f0elpwnx7ezytdlck35003nz6qk8kzvurvnj4a`](https://gonka.gg/address/gonka1f0elpwnx7ezytdlck35003nz6qk8kzvurvnj4a) | 5,000 GNK | State Bloat PoC / End-Block DoS |
| @ouicate | [`gonka1f0elpwnx7ezytdlck35003nz6qk8kzvurvnj4a`](https://gonka.gg/address/gonka1f0elpwnx7ezytdlck35003nz6qk8kzvurvnj4a) | 750 GNK | Bridge ETH address parsing vuln |
| @x0152 | [`gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe`](https://gonka.gg/address/gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe) | 1,000 GNK | Planned task — PR #775 |
| @x0152 | [`gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe`](https://gonka.gg/address/gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe) | 1,250 GNK | Planned task — PR #773 |
| @qdanik | [`gonka1j3f2xkapx8cmczpjqcsrh7cc3peyj3ngkjv4p8`](https://gonka.gg/address/gonka1j3f2xkapx8cmczpjqcsrh7cc3peyj3ngkjv4p8) | 12,000 GNK | vLLM 0.15.1 compatibility experiments |
| @qdanik | [`gonka1j3f2xkapx8cmczpjqcsrh7cc3peyj3ngkjv4p8`](https://gonka.gg/address/gonka1j3f2xkapx8cmczpjqcsrh7cc3peyj3ngkjv4p8) | 15,000 GNK | vLLM simultaneous PoC + inference |
| @qdanik | [`gonka1j3f2xkapx8cmczpjqcsrh7cc3peyj3ngkjv4p8`](https://gonka.gg/address/gonka1j3f2xkapx8cmczpjqcsrh7cc3peyj3ngkjv4p8) | 5,000 GNK | Wind down window vulnerability — PR #767 |
| @akup | [`gonka1ejkupq3cy6p8xd64ew2wlzveml86ckpzn9dl56`](https://gonka.gg/address/gonka1ejkupq3cy6p8xd64ew2wlzveml86ckpzn9dl56) | 1,000 GNK | Nodes unable to join from snapshots |
| @x0152 | [`gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe`](https://gonka.gg/address/gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe) | 3,000 GNK | Nodes unable to join (source problem) |
| — | [`gonka17kmfwzthep3alxt57vqcqr48uv7swp0u63gcnj`](https://gonka.gg/address/gonka17kmfwzthep3alxt57vqcqr48uv7swp0u63gcnj) | 750 GNK | StartInference/FinishInference — Issue #780 |
| @x0152 | [`gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe`](https://gonka.gg/address/gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe) | 5,000 GNK | StartInference/FinishInference — Issue #781 |
| @akup | [`gonka1ejkupq3cy6p8xd64ew2wlzveml86ckpzn9dl56`](https://gonka.gg/address/gonka1ejkupq3cy6p8xd64ew2wlzveml86ckpzn9dl56) | 5,000 GNK | StartInference/FinishInference — Issue #782 |
| @Lelouch33 | [`gonka128nd36m2pz5qcs4q6rd69622flyls05nleazqq`](https://gonka.gg/address/gonka128nd36m2pz5qcs4q6rd69622flyls05nleazqq) | 7,500 GNK | Important issue + testing with fix — PR #867 |
| kaitaku.ai | [`gonka1x45hruazmcqxslj3g8a08988hr5fr3wx33drhp`](https://gonka.gg/address/gonka1x45hruazmcqxslj3g8a08988hr5fr3wx33drhp) | 22,500 GNK | vLLM 0.15.1 compatibility — Issue #730 |
| — | [`gonka100s7x2t0npruu9ta02306qfmaened3vg3a9dn6`](https://gonka.gg/address/gonka100s7x2t0npruu9ta02306qfmaened3vg3a9dn6) | 5,000 GNK | Batch Transfer With Vesting — PR #835 |
| @qdanik | [`gonka1j3f2xkapx8cmczpjqcsrh7cc3peyj3ngkjv4p8`](https://gonka.gg/address/gonka1j3f2xkapx8cmczpjqcsrh7cc3peyj3ngkjv4p8) | 5,000 GNK | Collateral slashing vulnerability — PR #868 |
| @akup | [`gonka1ejkupq3cy6p8xd64ew2wlzveml86ckpzn9dl56`](https://gonka.gg/address/gonka1ejkupq3cy6p8xd64ew2wlzveml86ckpzn9dl56) | 7,500 GNK | v0.2.11 release management |
| @x0152 | [`gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe`](https://gonka.gg/address/gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe) | 7,500 GNK | v0.2.11 release management |
| @0xMayoor | [`gonka1s8szs7n43jxgz4a4xaxmzm5emh7fmjxhach7w8`](https://gonka.gg/address/gonka1s8szs7n43jxgz4a4xaxmzm5emh7fmjxhach7w8) | 2,500 GNK | v0.2.10 upgrade review |
| @blizko | [`gonka12jaf7m4eysyqt32mrgarum6z96vt55tckvcleq`](https://gonka.gg/address/gonka12jaf7m4eysyqt32mrgarum6z96vt55tckvcleq) | 2,500 GNK | v0.2.10 upgrade review |
| @x0152 | [`gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe`](https://gonka.gg/address/gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe) | 2,500 GNK | v0.2.10 upgrade review |
| **Total** | | **150,750 GNK** | |


### v0.2.10 — [PR #733](https://github.com/gonka-ai/gonka/pull/733) (Merged)

| Recipient | Address | Amount | Description |
| :------- | :------ | ----: | :---------- |
| @x0152 | [`gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe`](https://gonka.gg/address/gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe) | 500 GNK | Minor vulnerability fix — PR #661 |
| @x0152 | [`gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe`](https://gonka.gg/address/gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe) | 700 GNK | Planned task — PR #644 |
| @akup | [`gonka1ejkupq3cy6p8xd64ew2wlzveml86ckpzn9dl56`](https://gonka.gg/address/gonka1ejkupq3cy6p8xd64ew2wlzveml86ckpzn9dl56) | 10,000 GNK | Medium risk vulnerability report + fix — PR #659 |
| — | [`gonka1c34w3r45f0uftjckt2yy4k22vnc3zqjnp0umyz`](https://gonka.gg/address/gonka1c34w3r45f0uftjckt2yy4k22vnc3zqjnp0umyz) | 5,000 GNK | First report of vulnerability fixed in #659 |
| @x0152 | [`gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe`](https://gonka.gg/address/gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe) | 1,000 GNK | Low risk vulnerability — PR #545 |
| — | [`gonka1jkydytz99gkh0t42gjj4lz0mmdeumqp7mtzke3`](https://gonka.gg/address/gonka1jkydytz99gkh0t42gjj4lz0mmdeumqp7mtzke3) | 100 GNK | Minor bug fix — PR #640 |
| — | [`gonka123khww9elhtj49zumz0daleaudl6jn9y87tf23`](https://gonka.gg/address/gonka123khww9elhtj49zumz0daleaudl6jn9y87tf23) | 500 GNK | First report + suggested fix — Issue #422 |
| — | [`gonka1jkydytz99gkh0t42gjj4lz0mmdeumqp7mtzke3`](https://gonka.gg/address/gonka1jkydytz99gkh0t42gjj4lz0mmdeumqp7mtzke3) | 100 GNK | Minor bug fix — PR #638 |
| — | [`gonka1jkydytz99gkh0t42gjj4lz0mmdeumqp7mtzke3`](https://gonka.gg/address/gonka1jkydytz99gkh0t42gjj4lz0mmdeumqp7mtzke3) | 100 GNK | Minor bug fix — PR #634 |
| @ouicate | [`gonka1f0elpwnx7ezytdlck35003nz6qk8kzvurvnj4a`](https://gonka.gg/address/gonka1f0elpwnx7ezytdlck35003nz6qk8kzvurvnj4a) | 5,000 GNK | Independent report on issue in PR #710 |
| @x0152 | [`gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe`](https://gonka.gg/address/gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe) | 500 GNK | Low risk vulnerability — PR #643 |
| **Total** | | **23,000 GNK** | |


### v0.2.6 — [PR #497](https://github.com/gonka-ai/gonka/pull/497) (Merged)

| Recipient | Address | Amount | Description |
| :------- | :------ | ----: | :---------- |
| — | [`gonka1gmuxdcxlsxn5z72elx77w9zym7yrgfxqgzg6ry`](https://gonka.gg/address/gonka1gmuxdcxlsxn5z72elx77w9zym7yrgfxqgzg6ry) | 20,000 GNK | Vulnerability in Confirmation PoC — PR #459 |
| @0xMayoor | [`gonka1s8szs7n43jxgz4a4xaxmzm5emh7fmjxhach7w8`](https://gonka.gg/address/gonka1s8szs7n43jxgz4a4xaxmzm5emh7fmjxhach7w8) | 10,000 GNK | Bridge Exchange Double Vote Case Bypass |
| **Total** | | **30,000 GNK** | |
<!-- BOUNTY_DETAIL_END -->

---