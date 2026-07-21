---
title: Community Pool
description: "Community Pool, Community Sale wallet, and Gov Module — addresses, balances, inflow/outflow mechanics, and full funding history of passed governance proposals"
hide:
  - toc
---

# Community Pool

The Gonka network maintains three key addresses that collectively manage community funds. This page documents their current balances, how funds flow between them, and every passed governance proposal that has received funding.

<small>Last updated: <!-- UPDATE_TIMESTAMP -->
2026-07-21 15:40 UTC
<!-- /UPDATE_TIMESTAMP --></small>

---

## Community Pool (distribution module)

**Address:** [`gonka1jv65s3grqf6v6jl3dp4t6c9t9rk99cd8h2rzwa`](https://gonka.gg/address/gonka1jv65s3grqf6v6jl3dp4t6c9t9rk99cd8h2rzwa)

<!-- BALANCES_START -->
<p style="margin:0.2rem 0">
<strong>Current balance:</strong> <span style="color:var(--md-accent-fg-color,#5468ff);font-size:0.95rem;font-weight:600">102,705,110 GNK</span> · <span style="color:var(--md-accent-fg-color,#5468ff);font-size:0.95rem;font-weight:600">$10,000 USDT</span>
</p>
<!-- BALANCES_END -->

The Community Pool is the protocol-controlled treasury of the Gonka network. It accrues value through a **2% community tax** applied to every inflation reward and network fee. These funds can only be spent through a successful governance vote — no single key controls them.

Since the network genesis, the Community Pool has received continuous inflows from transaction fees and inflation rewards, funding ecosystem development, marketing initiatives, and community programmes through passed governance proposals.

*The $10,000 USDT held here was returned from **[proposal #42](https://gonkadocs.com/proposals/proposals/2026-q2/42/)** — the planned Global Compute Sovereignty Summit was cancelled, and the proposer returned the allocated funds. See the [return instructions](https://gonkadocs.com/community/discussion/show-and-tell/1390-how-to-return-funds-to-the-community-pool-ibc-usdt/) for details.*

**Inflow rate:** ~13,150 GNK/day (varies with block time, fee volume, and staking ratio).

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
<strong>Current balance:</strong> <span style="color:grey;font-size:0.95rem;font-weight:600">17,500,000 GNK</span> <span style="color:var(--md-accent-fg-color,#5468ff);font-size:0.95rem;font-weight:600">(~$10,500,000 USDT)</span> · <span style="color:var(--md-accent-fg-color,#5468ff);font-size:0.95rem;font-weight:600">$814,325 USDT</span>
</p>
<!-- SALE_BALANCE_END -->

This address was created by **[proposal #14](/proposals/proposals/2025-q4/14/)** (passed 2025-11-27), which transferred **20,000,000 GNK** from the Community Pool to seed a community sale programme at a fixed price of **$0.60 per GNK**.

The mechanism works as a simple swap: participants deposit **USDT** and receive **GNK** at the predetermined rate. The address holds both assets — USDT collected from buyers and the remaining GNK inventory.

For security, sale proceeds are distributed in **tranches** rather than all at once. The contract releases batches of GNK gradually to mitigate risk and ensure safe execution.

The USDT held here is used to pay **bug bounties and development rewards** — distributed automatically through the chain's **upgrade handler** during network hard forks, without requiring individual governance votes. Each upgrade version embeds a `distributeBountyRewards()` call that withdraws USDT directly from this contract to recipient addresses.

**Important:** The GNK held here is **not part of the Community Pool**. It is the undistributed balance of the sale contract — already allocated in proposal #14 and awaiting exchange. Only the USDT received from buyers is new value entering the Gonka ecosystem.

<details style="font-size:0.8rem;opacity:0.7;padding-left:0.5rem;margin:0.2rem 0">
<summary style="cursor:pointer;font-weight:500;padding-left:2.5em!important">Verify on-chain</summary>

```
curl -s https://node3.gonka.ai/chain-api/cosmos/bank/v1beta1/balances/gonka18pkq9mwxxlmyq7kr5txhm060wemg2s4u94wvsfd9w2kdc0u99d6spk8pz2
```

</details>

---

## Gov Module (authority)

**Address:** [`gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33`](https://gonka.gg/address/gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33)

<!-- GOV_BALANCE_START -->
<p style="margin:0.2rem 0">
<strong>Current balance:</strong> <span style="color:var(--md-accent-fg-color,#5468ff);font-size:0.95rem;font-weight:600">2,410,736 GNK</span>
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
| [PR #919](https://github.com/gonka-ai/gonka/pull/919) | 2026-03 | v0.2.11 bounty distribution | Upgrade Handler (Gov Module) | 150,750 | — |
| [PR #1446](https://github.com/gonka-ai/gonka/pull/1446) | 2026-07 | v0.2.14 bounty distribution | Upgrade Handler (Community Sale) | — | $45,250 |
| [PR #1113](https://github.com/gonka-ai/gonka/pull/1113) | 2026-04 | v0.2.12 bounty distribution | Upgrade Handler (Community Sale) | — | $35,200 |
| [PR #497](https://github.com/gonka-ai/gonka/pull/497) | 2026-01 | v0.2.6 bounty distribution | Upgrade Handler (Gov Module) | 30,000 | — |
| [PR #733](https://github.com/gonka-ai/gonka/pull/733) | 2026-02 | v0.2.10 bounty distribution | Upgrade Handler (Gov Module) | 23,000 | — |
| [PR #1168](https://github.com/gonka-ai/gonka/pull/1168) | 2026-05 | v0.2.13 bounty distribution | Upgrade Handler (Community Sale) | — | $18,000 |

| Metric | Value |
| :----- | :---- |
| Total governance proposals | 22 |
| Total GNK approved (proposals) | 24,994,032 GNK |
| Total USDT approved (proposals) | $631,600 |
| From Community Pool | 20,993,723 GNK + $631,600 |
| From Gov Module | 4,734,782 GNK |
| Largest funding | #14 — 20,000,000 GNK |
| Most recent | #82 — 80,000 GNK + $88,000 USDT |
| **Upgrade distributions** | **6** |
| Total GNK distributed (upgrades) | 203,750 GNK |
| Total USDT distributed (upgrades) | $98,450 |
| From Community Sale contract | $98,450 USDT |
| From Gov Module | 203,750 GNK |
<!-- SPENT_HISTORY_END -->

---

## Bounty Distribution

Bounties are paid through the chain's **upgrade handler** — hardcoded in each network upgrade and executed automatically when validators update.

USDT bounties are paid from the **Community Sale contract** via `withdraw_ibc`. GNK bounties are distributed from the **Gov Module**.

<!-- BOUNTY_TABLE_START -->
| Version | PR | Status | Date | Recipients | Total GNK | Total USDT | Source
| :------ | :- | :----- | :--- | :--------- | --------: | --------: | :----
| v0.2.14 | [PR #1446](https://github.com/gonka-ai/gonka/pull/1446) | Open | 2026-07 | 16 recipients | — | $45,250 | Community Sale |
| v0.2.13 | [PR #1168](https://github.com/gonka-ai/gonka/pull/1168) | Merged | 2026-05 | 2 recipients | — | $18,000 | Community Sale |
| v0.2.12 | [PR #1113](https://github.com/gonka-ai/gonka/pull/1113) | Merged | 2026-04 | 13 recipients | — | $35,200 | Community Sale |
| v0.2.11 | [PR #919](https://github.com/gonka-ai/gonka/pull/919) | Merged | 2026-03 | 26 recipients | 150,750 | — | Gov Module |
| v0.2.10 | [PR #733](https://github.com/gonka-ai/gonka/pull/733) | Merged | 2026-02 | 11 recipients | 23,000 | — | Gov Module |
| v0.2.6 | [PR #497](https://github.com/gonka-ai/gonka/pull/497) | Merged | 2026-01 | 2 recipients | 30,000 | — | Gov Module |
<!-- BOUNTY_TABLE_END -->

### Recipient Details

<!-- BOUNTY_DETAIL_START -->
### v0.2.14 — [PR #1446](https://github.com/gonka-ai/gonka/pull/1446) (Open)

| Recipient | Address | Amount | Description |
| :------- | :------ | ----: | :---------- |
| @akup | [`gonka1ejkupq3cy6p8xd64ew2wlzveml86ckpzn9dl56`](https://gonka.gg/address/gonka1ejkupq3cy6p8xd64ew2wlzveml86ckpzn9dl56) | $5,000 USDT | devshards v3 RM, upgrade review, HackerOne reviews |
| @x0152 | [`gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe`](https://gonka.gg/address/gonka18enyz7h6hh5zjveee5wnhkhrcexamfz0zdxxqe) | $6,000 USDT | RM, HackerOne reviews |
| @qdanik | [`gonka1j3f2xkapx8cmczpjqcsrh7cc3peyj3ngkjv4p8`](https://gonka.gg/address/gonka1j3f2xkapx8cmczpjqcsrh7cc3peyj3ngkjv4p8) | $10,000 USDT | RM, HackerOne reviews, MiniMax R&D, PoC (incl. GPU) |
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
| @blizko | [`gonka12jaf7m4eysyqt32mrgarum6z96vt55tckvcleq`](https://gonka.gg/address/gonka12jaf7m4eysyqt32mrgarum6z96vt55tckvcleq) | $1,000 USDT | v0.2.13 upgrade review |
| **Total** | | **$45,250 USDT** | |


### v0.2.13 — [PR #1168](https://github.com/gonka-ai/gonka/pull/1168) (Merged)

| Recipient | Address | Amount | Description |
| :------- | :------ | ----: | :---------- |
| @blizko | [`gonka12jaf7m4eysyqt32mrgarum6z96vt55tckvcleq`](https://gonka.gg/address/gonka12jaf7m4eysyqt32mrgarum6z96vt55tckvcleq) | $8,000 USDT | Prompt of death: vLLM crash via structured outputs |
| kaitaku.ai | [`gonka1x45hruazmcqxslj3g8a08988hr5fr3wx33drhp`](https://gonka.gg/address/gonka1x45hruazmcqxslj3g8a08988hr5fr3wx33drhp) | $10,000 USDT | Kimi experiments report |
| **Total** | | **$18,000 USDT** | |


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