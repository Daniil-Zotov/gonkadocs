---
title: "#2322 — Proposal #120 (Quorint): Independent Security Review for the Bridge Relaunch, plus Attack Registry, Economic Attack Simulator and Upgrade Audits"
source: https://github.com/gonka-ai/gonka/discussions/2322
discussion_number: 2322
category: protocol-improvements
synced_at: 2026-11-26T23:44:44Z
---

> 🔄 **Auto-sync:** from [Discussion #2322](https://github.com/gonka-ai/gonka/discussions/2322) every hour. 

# Proposal #120 (Quorint): Independent Security Review for the Bridge Relaunch, plus Attack Registry, Economic Attack Simulator and Upgrade Audits

**Автор:** [@quorint](https://github.com/quorint) · **Категория:** :gear: Protocol Improvements · **Создано:** 2026-11-24 12:50 UTC · **Обновлено:** 2026-11-24 14:06 UTC

---

## 📝 Описание

**Update, 24 November:** this proposal is now on-chain as [Proposal #120](https://gonka.gg/network/proposals/120). Host voting is open until Thursday 26 November 2026, 14:01 UTC, and hosts can vote on [gonka.vote](https://gonka.vote/governance/120).

Quorint (https://quorint.xyz) proposes an independent security review for the Gonka bridge relaunch, followed by an executable attack registry, an economic attack simulator and audits of the next high-risk upgrades. The engagement runs 24 weeks and is paid with 1,600,000 GNK from the Community Pool through a new instance of the `code_id 107` milestone escrow from [Proposal #82](https://gonka.gg/network/proposals/82), with a public report before every unlock and a one-vote clawback.

The full proposal is below. The version-controlled copy, the submitted `proposal.json` and a script that re-derives the escrow address are at https://github.com/quorint/gonka-security-proposal. The on-chain metadata links to the README at tag `v1.0` (commit `dec028b`), which later pushes cannot change.

Questions and objections are welcome here and on [gonka.vote](https://gonka.vote/governance/120) during the vote. We would especially value input from MillCreek R&D, the Product Committee and the Governance Support Committee on the open questions in Section 13.

---

**Author:** Quorint, registered in the Netherlands · https://quorint.xyz · contact@quorint.xyz  
**Category:** Protocol Improvements  
**Roadmap:** Track 6, Project 3 (contract security and cross-chain interop) · Track 5, Project 1 (attack registry and regression checks) · Track 5, Project 2 (economic and incentive attack simulator)  
**Duration:** 24 weeks, four 6-week milestones  
**Request:** 1,600,000 GNK from the Community Pool (≈1.38% of the pool), held in the existing `code_id 107` milestone escrow approved in [Proposal #82](https://gonka.gg/network/proposals/82) and released in six tranches. Hosts can claw back everything still in the escrow with one governance vote. No USDT is requested.  
**Status:** On-chain as [Proposal #120](https://gonka.gg/network/proposals/120), with host voting open until 26 November 2026, 14:01 UTC. The submitted text is tag [`v1.0`](https://github.com/quorint/gonka-security-proposal/tree/v1.0). Questions are welcome on [GitHub Discussion #2322](https://github.com/gonka-ai/gonka/discussions/2322) and on [gonka.vote](https://gonka.vote/governance/120) during the vote.

---

## 1. Summary

On 18 November 2026 an attacker manipulated the key-generation ceremony on the Gonka chain, registered a new epoch key on the Ethereum bridge, and within 72 seconds withdrew the bridge's entire stablecoin reserve (884,150.87 USDT and 647.74 USDC) and minted 22,000,000 unbacked WGNK. After a fast response by core contributors, MillCreek R&D and analytics partners, the attacker returned the assets the next day, and consensus and inference were never affected. The bridge remains disabled, the Ethereum contract cannot be paused, and the community has just started discussing compensation and re-backing (Discussion #2306).

Relaunching the bridge will require a fixed key-generation path, a new bridge contract and key ceremony, and re-backing transactions, and hosts will be asked to approve each of them. [Proposal #118](https://gonka.gg/network/proposals/118) puts incident response and bridge security in MillCreek's scope. Quorint proposes to be the independent second pair of eyes, because no team should be the only reviewer of its own security fix.

The first 6 weeks (Milestone 1) are a bridge relaunch security gate. The remaining 18 weeks deliver two roadmap projects that have no funded owner yet, an executable attack registry (Track 5, Project 1) and an economic attack simulator (Track 5, Project 2), plus independent audits of the next high-risk upgrades. These include per-escrow DKG (#1748), which brings the same class of key-generation ceremony into every escrow.

| Item | Detail |
|---|---|
| Milestone 1 (weeks 1–6) | Bridge relaunch security gate: private root-cause verification, `x/bls` key-generation audit, bridge v2 contract review, re-backing transaction review, `gonka-bridge-sentinel` and invariant suites |
| Milestone 2 (weeks 7–12) | L1, P2P, devshard v7 and CosmWasm treasury audit; `gonka-attack-registry` v1 (≥20 attack classes) |
| Milestone 3 (weeks 13–18) | `gonka-econ-sim` v1 and a quantitative parameter risk report |
| Milestone 4 (weeks 19–24) | Audits of per-escrow DKG (#1748), Decode-PoC and image-to-text support ([Proposal #118](https://gonka.gg/network/proposals/118) scope) and Confidential MLNode (#951); registry v2 (≥35 classes); handoff |
| Payment | 1,600,000 GNK in six tranches (days 0, 45, 90, 135, 180, 210), ≈ $208K at today's price ($0.13) |
| Host protection | Immutable escrow with no admin, a public report 5 days before every unlock, and a one-vote clawback |
| Output | Four permanent open-source repositories (Apache-2.0/MIT); every audit report published once fixes ship |

---

## 2. Motivation

### 2.1 What a safe bridge relaunch requires

According to the preliminary statement of 19 November ("WGNK bridge incident: statement on the first 24 hours"), the attacker "obtained the ability to produce valid threshold signatures for the bridge's newest signing epoch by manipulating the key-generation ceremony on the Gonka chain", and "no signing requests for these operations were ever created on the Gonka chain". On Ethereum, the sequence was:

| Time (UTC, 18 Nov) | Action on bridge `0x972a7A92D92796a98801A8818bcF91f1648f2F68` |
|---|---|
| 18:00:59 | `submitGroupKey` installs the attacker's epoch key |
| 18:01:35 | Withdrawal of 884,150.87 USDT |
| 18:01:59 | Withdrawal of 647.74 USDC |
| 18:02:11 | Mint of 22,000,000 WGNK |

Three lessons follow from the public record alone, without speculating about the root cause:

1. The key change was visible on-chain 36 seconds before the first withdrawal, and it had no matching signing request on Gonka. A monitor that cross-checks every Ethereum-side key change, withdrawal and mint against Gonka-chain signing requests would have flagged it immediately.
2. Nothing slowed the drain. A timelock on signer-set rotation and per-period caps on withdrawals and mints would have turned 72 seconds into hours.
3. The deployed contract cannot be paused, so the relaunch needs a new contract, a new key ceremony, and a migration and re-backing plan. Until the reserve is restored, bridged USDT and USDC on Gonka cannot be redeemed.

We do not speculate about the root cause in public. Gonka has not published a post-mortem yet, and parts of the key-generation code may still be in use. Any root-cause analysis we do goes privately to MillCreek first.

### 2.2 Key generation and bridge key rotation keep producing findings

Public reports about this surface predate the incident: weak dealer approval (#823), a group-key validation fallback to self-validation (#848, fixed), dealer consensus counted against slot weights (#849), unverified dealer commitments and unproven verification votes (#1079), stale epoch keys that can still authorize withdrawals (#1080, open), and exposed partial signatures (PR #2302, open). We are not implying that any of these caused the incident. The point is that the same areas keep producing findings, which is exactly what Track 5, Project 1 is meant to stop: once an attack class is known, it should become an automated regression check.

### 2.3 Beyond the bridge: a fast-moving codebase

- devshard v6 went live with [Proposal #116](https://gonka.gg/network/proposals/116), and a v7 prerelease reached testnet on 19 November.
- [Proposal #118](https://gonka.gg/network/proposals/118) includes the Decode-PoC mainnet rollout and image-to-text support. Per-escrow BLS DKG (#1748) and Confidential MLNode (#951) are in design.
- Gonka maintains its own Cosmos SDK and CometBFT forks; PR #2319 most recently added a PEX request guard for the v0.2.18 halt reported in #2299.
- Open issues show economic and settlement edge cases that need quantitative answers: executor-reported output tokens checked only on sampled replays (#2000), unbounded validations in flight (#2298), an unbounded `validation_sample_size` (#2210), and mis-wired or unused slashing parameters (#2208, #1726).

The most recent public vendor findings we could find are CertiK's (Ethereum bridge preliminary report in February 2026, GEB-series issues through April 2026). Trail of Bits and HackerOne were engaged through Bitfury and reimbursed in [Proposal #117](https://gonka.gg/network/proposals/117) (607,250 USDT). Point-in-time audits are valuable, but they don't leave regression tests behind while the code keeps changing.

### 2.4 Three roadmap projects without a funded owner

- **Track 6, Project 3 — Contract security and cross-chain interop:** "A security review process for bridge- and interop-related contracts, configurations, and integrations. The scope includes threat modeling, internal or external review where needed, upgrade planning, regression checks after changes, and documented bridge-facing flows for integrators."
- **Track 5, Project 1 — Attack registry and regression check suite:** "Known attack classes and exploit scenarios become testable regression checks. The network does not repeat the same mistakes after upgrades, new model launches, or parameter changes."
- **Track 5, Project 2 — Economic and incentive attack simulator:** "A set of scenarios and simulations to test whether participants can gain an unfair advantage through pricing, rewards, validation, penalties, collateral, spam, or optimization against the mechanics."

To our knowledge, none of these has a funded proposal today.

---

## 3. Who we are

Quorint is an independent security research and audit firm registered in the Netherlands. We work on L1 nodes and consensus (Rust, Go, C++), zero-knowledge circuits and applied cryptography, and smart contracts (EVM/Solidity, SVM, CosmWasm). Every engagement is principal-led: line-by-line manual review combined with custom stateful fuzzing, differential testing and reproducible proofs of concept. Researcher profiles are listed at https://quorint.xyz.

**Prior work on Gonka.** In July 2026 Quorint's research team disclosed a Critical consensus-liveness vulnerability in Gonka, awarded a $20,000 bug bounty; the full write-up was published after remediation ([Decimal-Exponent Bomb in Gonka](https://quorint.xyz/research/gonka-decimal-exponent-bomb/)). An unbounded `int32` exponent in Gonka's custom `Decimal` type made `MsgValidation.ValidateBasic()` materialize `10^|exponent|` before gas metering or signature checks. Wrapped in `authz.MsgExec`, a transaction from an attacker with no participant key and no `authz` grant passed `CheckTx` and crashed every validator in `FinalizeBlock`, before the grant check was reached.

**Other L1 and cryptography work.**
- Zcash Zebra: two Critical pre-release consensus-divergence findings (ZcashFoundation/zebra#10461).
- Zcash Zakura: full-node and P2P denial-of-service findings (zakura-core/zakura#1911, zakura-core/zakura#1915, zakura-core/zakura#1962), followed by a commissioned protocol and consensus assessment ([OpenZcash Coinholder Proposal #127](https://openzcash.org/coinholders/proposals/127), $67,500).
- Zcash Voting: ongoing cryptographic protocol assessment.

**Team for this engagement.** A principal researcher leads all manual and cryptographic review and proof-of-concept work for the full 24 weeks. A senior engineer builds the fuzzing suites, the multi-node harness and the simulator.

---

## 4. Scope and deliverables

### Workstream A — Bridge relaunch security gate (Track 6, Project 3) — Milestone 1

1. **Private root-cause verification.** Reconstruct the incident from public chain data and code, compare it with MillCreek's analysis, and confirm the fix closes every path to an unauthorized epoch key. Shared only with MillCreek and designated maintainers until the fix ships.
2. **`x/bls` key generation and group-key validation.** Dealing and commitment verification (valid, subgroup-checked G2 points), complaint and dispute resolution, slot-weight accounting, epoch transitions, the signing-request lifecycle, exposed partial signatures (#2302) and stale epoch keys (#1080).
3. **Bridge v2 contract design and code review**, against six properties:
   - signer-set rotation requires approval by the current set and a timelock;
   - per-period caps on withdrawals and mints;
   - a pause guardian with a governance override;
   - expiry of old epoch keys;
   - domain separation and replay protection;
   - reserve accounting that matches the wrapped supply on Gonka.
4. **Gonka-side bridge flows.** Wrapped-token CW20 mint and burn, `BRIDGE_PENDING` handling, escrow refunds (#1352) and deposit deduplication.
5. **Re-backing and compensation transactions, at no extra cost.** When a re-backing or compensation proposal (for example from Discussion #2306) is drafted, we review its on-chain messages before submission.
6. **Open-source deliverables.**
   - `gonka-bridge-sentinel` v1: a self-hosted monitor (Prometheus metrics and alert rules, no SaaS). It alerts when an Ethereum-side `submitGroupKey`, `withdraw` or `mintWithSignature` has no matching Gonka signing request, when caps are approached, when the wrapped supply drifts from the Ethereum reserve, and when an IBC light client nears expiry (#1667). Its acceptance test replays the 18 November sequence on a fork.
   - `gonka-bridge-security`: Foundry invariant suites for the bridge v2 contract, plus `cw-multi-test` and `proptest` suites for the wrapped-token contract.
   - A written relaunch sign-off, or a list of blocking issues, delivered at least 5 days before hosts vote on the relaunch. Payment does not depend on which of the two we deliver.

The bridge v2 code is written by MillCreek. If it is not ready by week 6, the remaining relaunch review continues into Milestone 2 with priority, and the Milestone 2 scope shifts accordingly, agreed publicly with MillCreek and the Product Committee.

### Workstream B — L1, P2P and devshard audit plus attack registry (Track 5, Project 1) — Milestone 2

1. **Audit.**
   - The `gonka-ai/cosmos-sdk` fork: unmetered `ValidateBasic()` work before the ante handler (the class of our earlier finding), `authz.MsgExec` and `feegrant` wrapper asymmetries, and the network-duty fee bypass (#1539).
   - The CometBFT fork: peer exchange and peer scoring after #2299 and PR #2319.
   - devshard v7: mempool message limits (#2249), catch-up consistency (#2037, #2079), validations in flight (#2298), settlement decisions across restarts (#1906) and gateway signing keys (#1940).
   - The `community-sale` and `liquidity-pool` CosmWasm contracts.
2. **`gonka-attack-registry` v1.** At least 20 attack classes encoded as deterministic regression checks, with a Byzantine-peer and malicious-executor harness that runs in `testermint` CI and on the Community DevNet. First entries include the 18 November attack class (published only after the fix ships), the public key-generation and bridge classes above, pre-ante resource bombs, `authz` wrapper bypasses, stream truncation (#1841, #2104) and cPoC segment edge cases (#2013, #2015).

This complements `@vitaly-andr`'s in-process Cosmos SDK simulation work (#982, #1228) rather than duplicating it: the registry runs out-of-process, multi-node scenarios. It also plugs into the External Test Lab and Community DevNet ([Proposal #82](https://gonka.gg/network/proposals/82)) instead of building parallel infrastructure.

### Workstream C — Economic and validation attack simulator (Track 5, Project 2) — Milestone 3

`gonka-econ-sim` v1 is a reproducible discrete-event and Monte Carlo simulator with rational, colluding and griefing hosts, gateways, challengers and consumers. Planned models:

- billing extraction under sampled replays (#2000);
- PoC and Decode-PoC margin gaming (quantization substitution, KV-cache shortcuts, cPoC segment shrinking);
- slot hogging and fee-exemption griefing (#706, #2244, #2146);
- validation sample size and slashing parameter bounds (#2210, #2208, #1726);
- Track 10 transition risks: wash trading around the 40%+ utilization trigger, demand-based per-model token pricing, and rewards proportional to work-cons earnings;
- Confidential MLNode economics, which the current draft in #951 leaves as a TODO (§10).

It ships with CLI scenarios, parameter-sweep notebooks and a parameter risk report generator, so the Product Committee and MillCreek can stress-test a `MsgUpdateParams` proposal before hosts vote on it.

### Workstream D — Pre-mainnet upgrade audits — Milestone 4

1. **Per-escrow BLS DKG (#1748):** NIZK dealing proofs, Fiat-Shamir transcript binding, complaint soundness, on-chain verification cost and reconstruction under adaptive aborts. After 18 November this is the highest-value item.
2. **Decode-PoC rollout and image-to-text support ([Proposal #118](https://gonka.gg/network/proposals/118) scope; #1198):** parser bounds, deterministic image-token hashing between executor and validator, and memory amplification.
3. **Confidential MLNode (#951):** attestation verification (Intel TDX, AMD SEV-SNP, NVIDIA CC), on-chain version pinning and `report_data` binding.

If any of these slips past week 24, the hours move to whichever release candidate or roadmap security item carries the highest risk at the time, agreed publicly with MillCreek and the Product Committee.

---

## 5. Milestones and payment gates

Each milestone ends with public artifacts and a time and spending report. The report is published 5 days before the next tranche unlocks, which leaves hosts more than one 48-hour voting period to claw back.

| Milestone | Days | Public artifacts | Tranche |
|---|---|---|---|
| M1: Bridge relaunch security gate | 1–45 (report by day 40) | Bridge and `x/bls` report (published once fixes ship); relaunch sign-off; `gonka-bridge-sentinel` v1 on Community DevNet; `gonka-bridge-security` suites in CI | T2, day 45 |
| M2: L1, P2P and devshard audit plus registry | 46–90 (report by day 85) | L1, P2P and devshard assessment; `gonka-attack-registry` v1 (≥20 classes); CI integration PRs and an External Test Lab runbook | T3, day 90 |
| M3: Economic simulator | 91–135 (report by day 130) | `gonka-econ-sim` v1; quantitative economic and validation report with parameter recommendations | T4, day 135 |
| M4: Upgrade audits and handoff | 136–180 (final report by day 175) | Upgrade audit reports and fix verification; registry v2 (≥35 classes); `gonka-econ-sim` v1.2; handoff package and live walkthrough | T5, day 180 |
| Holdback | 180–210 | 30-day verification window after the final report | T6, day 210 |

T1 (day 0) funds mobilization so Milestone 1 can start immediately.

---

## 6. KPIs and how to verify them

| KPI | Target | Verification |
|---|---|---|
| Relaunch gate | 100% of in-scope bridge v2 and `x/bls` changes reviewed; sign-off or blocking-issues list at least 5 days before the relaunch vote | Timestamped report in the Governance Proposal Reports category |
| Sentinel | Alerts within one Ethereum block on a replay of the 18 November key change; deployed on Community DevNet | Public repo, replay test in CI, DevNet dashboard |
| Invariant fuzzing | 100% of in-scope bridge Solidity and CosmWasm contracts; ≥100,000 randomized sequences per contract | `gonka-bridge-security` CI runs |
| Attack registry | ≥20 classes at M2 and ≥35 at M4, all deterministic | `gonka-attack-registry` CI and DevNet logs |
| Economic simulation | ≥12 adversarial models with reproducible parameter sweeps | `gonka-econ-sim` repo and report |
| Upgrade audit turnaround | ≤10 business days to first findings after code freeze; ≤72 hours to re-verify a fix | Timestamps in milestone reports |
| Finding quality | Every Critical, High and Medium finding ships with a runnable PoC test, root cause and patch guidance | Verified privately by MillCreek, published once fixes ship |
| No double-billing | $0 in bounty claims by Quorint for vulnerabilities found in scoped repositories during the engagement | Attestation in every milestone report; HackerOne records |

---

## 7. Disclosure and coordination

- **Private first.** Following https://gonkadocs.com/gonka/docs/report-vulnerability/, no unpatched vulnerability, exploit or regression test is pushed to a public branch, issue or chat. Findings go to MillCreek R&D and designated maintainers through private GitHub Security Advisories or HackerOne, marked "Grant-covered — no bounty claim".
- **Publication after the fix.** Regression tests and advisories become public only after the fix is merged, released and through the host upgrade window.
- **Working with MillCreek and External Test Lab.** Bi-weekly syncs with MillCreek to line up code freezes, and Docker Compose and `testermint` targets with runbooks so External Test Lab can run every suite on `gonka-devnet-community` before upgrade votes.
- **Oversight.** Milestone reports go in the Governance Proposal Reports category at least 5 days before each unlock. The Governance Support Committee tracks deadlines and can recommend a clawback; the Product Committee reviews results against the KPIs above.

---

## 8. Budget and funding structure

### 8.1 Amount and pricing

- **Total: 1,600,000 GNK from the Community Pool. No USDT.**
- That is ≈ $208,000 at the 24 November price ($0.13) and ≈ $266,000 at the 30-day average ($0.167). The cost breakdown in 8.4 uses a $0.15 reference price between the two. We deliberately do not value GNK at the $0.60 Community Sale price from [Proposal #117](https://gonka.gg/network/proposals/117).
- It is 1.38% of the Community Pool (115.58M GNK on 24 November).
- Amounts are fixed in GNK. Quorint carries all price and liquidity risk after approval: no top-ups and no re-pricing.

### 8.2 Why GNK only

The only stablecoin balance the community controls on-chain in size is the bridged USDT held by `community-sale` (276,751 of the CW20 token labelled "Bridged Token ethereum:0xdac17f…"). That token's total supply on Gonka is 884,150.86, essentially the reserve drained on 18 November, and the IBC USDT balance is $1,425. We will not draw on bridged USDT while the community decides on re-backing. If hosts or the Gonka Foundation later prefer to convert the remaining tranches to USDT, that would be a separate proposal.

### 8.3 Selling GNK

GNK trades thinly. On 24 November the only active market for native GNK listed by CoinGecko and CoinMarketCap was SafeTrade, with a 30-day median volume of about $1,500 a day, and the WGNK pairs on Ethereum will not be usable until the bridge relaunches. To avoid adding sell pressure, Quorint commits to the following:

- Sales go over the counter where possible.
- Public-market sales on any day stay below 10% of that market's trailing 7-day average volume.
- Every sale or transfer out of the recipient address is listed in the next milestone report, with date, amount and venue or destination.

### 8.4 Cost breakdown (24 weeks)

| Line | GNK | ≈ USD at the $0.15 reference price |
|---|---|---|
| Principal researcher: manual and cryptographic review across all four workstreams, PoCs, fix verification | 880,000 | $132,000 |
| Senior engineer: invariant suites, multi-node harness, simulator | 560,000 | $84,000 |
| Compute and infrastructure: fuzzing runners, multi-node chaos testbed, archive and RPC access for the sentinel | 160,000 | $24,000 |
| **Total** | **1,600,000** | **$240,000** |

### 8.5 Reference points

- [Proposal #117](https://gonka.gg/network/proposals/117) reimbursed 607,250 USDT for point-in-time Trail of Bits and HackerOne engagements.
- [Proposal #82](https://gonka.gg/network/proposals/82) (External Test Lab) received 88,000 USDT and 80,000 GNK for a 4-month pilot through the same escrow contract proposed here.
- [Proposal #118](https://gonka.gg/network/proposals/118) (MillCreek) received 866,000 USDT for two months of full-team work, paid upfront without escrow.

This proposal asks for ≈ $208–266K in value over six months, depending on the GNK price, fully escrowed and subject to clawback, and leaves four open-source repositories behind.

---

## 9. Escrow and host protection

Funds go into a new instance of the milestone escrow contract that hosts already approved for [Proposal #82](https://gonka.gg/network/proposals/82) (98.2% Yes), so there is no new contract code to review.

- **Contract:** `code_id 107`, checksum `94b141625b7641e6ad57266420b18a4af72eac49b8110cb92719755590b463bd`, source https://github.com/paranjko/testlab-devnet-escrow/tree/1b2e529876141816b5c2130840d04fb93694bf72
- **Escrow address** (Instantiate2, creator = governance module, salt `quorint-gonka-security-2026`): `gonka1m5gr4pkemg7fyml3jlkecpvxzprrkglfu05jfe8kmm38780ajp5s9qznhg`. The same derivation reproduces the [Proposal #82](https://gonka.gg/network/proposals/82) escrow address (`gonka1g57f45qjvn0529vpgj8x8mzt8r5k4audchm3pp9pezywxwf4rexqlj8ayw`), so anyone can check it with the script in https://github.com/quorint/gonka-security-proposal/tree/main/verify.
- **Recipient (Quorint):** `gonka1ggt0d4jqmztnmh86na3m99c9d3q7s6h2dkd2qv`. Every transfer out of this address is reported under Section 8.3.
- **No admin and no migration.** The recipient, amounts and unlock days are fixed at instantiation.
- **Claim** is permissionless and pays only matured tranches, only to the fixed recipient.
- **Clawback:** one governance vote cancels the escrow and returns everything still in it to the Community Pool.
- **Backstop:** after day 270 anyone can close the escrow and sweep any remainder to the Community Pool.
- Unlocks are time-based, as in [Proposal #82](https://gonka.gg/network/proposals/82). Enforcement is the public report 5 days before each unlock plus the clawback.

| Tranche | Unlock day | GNK | Condition |
|---|---|---|---|
| T1 | 0 | 250,000 | Mobilization; Milestone 1 starts immediately |
| T2 | 45 | 300,000 | M1 report and relaunch sign-off published by day 40 |
| T3 | 90 | 300,000 | M2 report and registry v1 published by day 85 |
| T4 | 135 | 300,000 | M3 report and `gonka-econ-sim` v1 published by day 130 |
| T5 | 180 | 250,000 | M4 final report and handoff published by day 175 |
| T6 | 210 | 200,000 | 30-day post-completion holdback |
| **Total** | | **1,600,000** | No automatic renewal |

---

## 10. Terms

1. **Nature of the payment.** The GNK is a fixed fee for the services in this proposal. It is not a grant, donation, loan or investment, and it is not paid in exchange for equity or any other interest in Quorint.
2. **Source of funds and acceptance.** The fee comes from the Community Pool and is released only through this governance vote and the escrow schedule. If the proposal passes, the vote and the funding of the escrow constitute the Gonka network's approval of these terms, and Quorint's receipt of the first tranche constitutes its acceptance.
3. **Escrow and clawback.** Governance can claw back unreleased tranches at any time. Released tranches are payment for work performed and are not refundable. Quorint can also return funds voluntarily through the escrow's `ReturnFunds` function.
4. **Use of funds.** Compensation of Quorint's researchers and contractors, compute and infrastructure, and administrative, legal, accounting and tax costs.
5. **Independent service provider.** Quorint is not an employee, agent or representative of the Gonka network, the Gonka Foundation or any host. It does not operate the network, hold administrative keys, take custody of user or host funds, or manage any treasury. Changes Quorint proposes take effect only if adopted through Gonka governance and run by hosts.
6. **Conflicts of interest.** Quorint is paid in GNK, so it benefits from a healthy network and a working bridge. To keep the review independent, tranches unlock on fixed dates and do not depend on whether Quorint recommends relaunching the bridge; a "not ready" verdict changes nothing in the payout. Each milestone report discloses Quorint's holdings of GNK, WGNK and other Gonka-related assets, and its GNK sales under Section 8.3.
7. **Open source.** Tooling built under this proposal is released under Apache-2.0 or MIT; contributions to Gonka repositories use those repositories' licenses.
8. **Confidentiality.** Vulnerability details stay confidential until a fix is released and deployed, as described in Section 7.
9. **No guarantees.** No audit can prove the absence of vulnerabilities. Timelines and targets are good-faith plans, and Quorint may reprioritize, in coordination with MillCreek, in response to live incidents.
10. **No double-billing.** Quorint makes no bug bounty claims for vulnerabilities found in scoped repositories during the engagement.
11. **Compliance and taxes.** Quorint complies with applicable laws, including sanctions and anti-money-laundering laws, and is responsible for its own taxes.

---

## 11. Sustainability and exit

- Everything we build is open source and self-hostable with no SaaS dependency: `gonka-bridge-sentinel`, `gonka-bridge-security`, `gonka-attack-registry`, `gonka-econ-sim`, threat models, PoC tests and reports.
- By day 180, External Test Lab, MillCreek and any contributor can run every suite, alert and parameter sweep with single-command `make` or Docker workflows.
- There is no automatic renewal. Any follow-on work requires a new proposal or a Gonka Foundation contract.

---

## 12. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Bridge v2 code is not ready in time | The relaunch review continues into M2 with priority; the scope swap is agreed publicly |
| A finding leaks before it is fixed | Private-first disclosure; public tests only after release and the upgrade window |
| Overlap with MillCreek or bounty teams | MillCreek owns the fixes; Quorint reviews and tests. The registry and simulator plug into existing test infrastructure |
| Non-delivery | A report 5 days before each unlock; one-vote clawback of everything still in escrow; the GSC can recommend a clawback |
| Principal researcher unavailable for more than two weeks | Quorint notifies the GSC publicly, and hosts can claw back |
| GNK price or liquidity | Carried entirely by Quorint; no top-ups. Sales follow the policy in Section 8.3 |
| Conflict of interest, since Quorint is paid in GNK | Tranches are time-based and independent of the relaunch verdict; holdings and sales are disclosed in every milestone report |

---

## 13. Open questions

1. Should Milestone 1 also cover the IBC routes (#1667), or stay focused on the Ethereum bridge relaunch?
2. Would MillCreek prefer we start with root-cause verification or with the bridge v2 design review in week 1?
3. Beyond #1748, Decode-PoC, image-to-text support and #951, which upgrades should Workstream D prioritize?
4. How should the registry and the sentinel be packaged for External Test Lab: as `testermint` suites or as standalone Docker Compose jobs?
5. If the bridged USDT reserve is restored, would hosts or the Gonka Foundation prefer to convert later tranches to USDT through a separate proposal?

---

## 14. Decision requested

Approve a 24-week engagement with Quorint covering an independent security review for the bridge relaunch (Roadmap Track 6, Project 3), an executable attack registry (Track 5, Project 1), an economic attack simulator (Track 5, Project 2) and pre-mainnet upgrade audits. It is funded with 1,600,000 GNK from the Community Pool through a new instance of the `code_id 107` milestone escrow, released in six tranches and subject to a one-vote governance clawback.

### Links

- Quorint: https://quorint.xyz · research: https://quorint.xyz/research/ · audits: https://quorint.xyz/audits/ · contact@quorint.xyz
- Gonka disclosure: https://quorint.xyz/research/gonka-decimal-exponent-bomb/
- OpenZcash Coinholder Proposal 127: https://openzcash.org/coinholders/proposals/127
- Incident summaries: https://gnk.space/news/2026-11-21 · https://blockint.ai/blog/gonka-bridge-exploit-606-eth-to-bitcoin-and-back-593-eth-returned
- Compensation discussion: https://github.com/gonka-ai/gonka/discussions/2306
- Escrow precedent ([Proposal #82](https://gonka.gg/network/proposals/82)): https://github.com/gonka-ai/gonka/discussions/1388


---

## 💬 Комментарии (2)

### Комментарий 1 — [@quorint](https://github.com/quorint)

*2026-11-24 13:22 UTC*

The pre-proposal is now on gonka.vote: https://gonka.vote/proposal/dyel8w (open until 8 December). It is a condensed version of this post; this post and the repository remain the full reference. Questions are welcome in either place.

### Комментарий 2 — [@quorint](https://github.com/quorint)

*2026-11-24 14:06 UTC*

[Proposal #120](https://gonka.gg/network/proposals/120) is now on-chain. Host voting is open until Thursday 26 November 2026, 14:01 UTC, on [gonka.vote](https://gonka.vote/governance/120).

The on-chain text is the same as this Discussion apart from the status line, and is pinned at tag [`v1.0`](https://github.com/quorint/gonka-security-proposal/tree/v1.0). We moved straight to a standard 48-hour vote instead of holding an AMA first, so we will answer questions here as they come in.

