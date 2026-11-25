---
title: "Quorint: Bridge Relaunch Security Review, Attack Registry and Upgrade Audits"
template: proposals-main.html
---

# Quorint: Bridge Relaunch Security Review, Attack Registry and Upgrade Audits

<div class="preproposal-header" markdown="1">

<div class="preproposal-status">🟢 Active</div>

**Author:** Quorint
**Created:** 2026-11-24 13:13 UTC
**Closes:** 2026-12-08 13:13 UTC
**Language:** EN
**Votes:** 1
**Avg. Bid:** 0.00 GNK

</div>

Independent security review gating the bridge relaunch, then an attack registry, economic attack simulator and upgrade audits. 24 weeks, 1.6M GNK in escrow.

---

## Full Proposal

**Author:** Quorint, registered in the Netherlands · https://quorint.xyz · contact@quorint.xyz  
**Full proposal:** [GitHub Discussion #2322](https://github.com/gonka-ai/gonka/discussions/2322) · repository with the draft `proposal.json` and an escrow verification script: https://github.com/quorint/gonka-security-proposal  
**Roadmap:** Track 6, Project 3 (contract security and cross-chain interop) · Track 5, Project 1 (attack registry and regression checks) · Track 5, Project 2 (economic and incentive attack simulator)  
**Duration:** 24 weeks, four 6-week milestones  
**Request:** 1,600,000 GNK from the Community Pool (≈1.38% of the pool), held in the existing `code_id 107` milestone escrow approved in [Proposal #82](https://gonka.gg/network/proposals/82) and released in six tranches. Hosts can claw back everything still in the escrow with one governance vote. No USDT is requested.  
**Status:** Pre-proposal for community and committee review. Nothing goes on-chain before committee review and an AMA.

This page condenses the full proposal. If anything here differs from it, the full proposal applies.

---

## 1. Summary

On 18 November 2026 an attacker manipulated the key-generation ceremony on the Gonka chain, registered a new epoch key on the Ethereum bridge, and within 72 seconds withdrew the bridge's entire stablecoin reserve (884,150.87 USDT and 647.74 USDC) and minted 22,000,000 unbacked WGNK. After a fast response by core contributors, MillCreek R&D and analytics partners, the attacker returned the assets the next day, and consensus and inference were never affected. The bridge remains disabled, the Ethereum contract cannot be paused, and the community has just started discussing compensation and re-backing ([Discussion #2306](https://github.com/gonka-ai/gonka/discussions/2306)).

Relaunching the bridge will require a fixed key-generation path, a new bridge contract and key ceremony, and re-backing transactions, and hosts will be asked to approve each of them. [Proposal #118](https://gonka.gg/network/proposals/118) puts incident response and bridge security in MillCreek's scope. Quorint proposes to be the independent second pair of eyes, because no team should be the only reviewer of its own security fix.

The first 6 weeks (Milestone 1) are a bridge relaunch security gate. The remaining 18 weeks deliver two roadmap projects that have no funded owner yet, an executable attack registry and an economic attack simulator, plus independent audits of the next high-risk upgrades. These include per-escrow DKG ([#1748](https://github.com/gonka-ai/gonka/discussions/1748)), which brings the same class of key-generation ceremony into every escrow.

## 2. Why now

Three lessons follow from the public record alone, without speculating about the root cause:

1. The key change was visible on-chain 36 seconds before the first withdrawal, and it had no matching signing request on Gonka. A monitor that cross-checks every Ethereum-side key change, withdrawal and mint against Gonka-chain signing requests would have flagged it immediately.
2. Nothing slowed the drain. A timelock on signer-set rotation and per-period caps on withdrawals and mints would have turned 72 seconds into hours.
3. The deployed contract cannot be paused, so the relaunch needs a new contract, a new key ceremony, and a migration and re-backing plan.

Gonka has not published a post-mortem yet, so any root-cause analysis we do goes privately to MillCreek first.

The same areas keep producing findings. Public reports about key generation and bridge key rotation predate the incident, including stale epoch keys that can still authorize withdrawals ([#1080](https://github.com/gonka-ai/gonka/issues/1080), open) and exposed partial signatures ([PR #2302](https://github.com/gonka-ai/gonka/pull/2302), open). We are not implying that any of these caused the incident. The point is that once an attack class is known, it should become an automated regression check. Meanwhile the code keeps changing (devshard v7, Decode-PoC, per-escrow DKG, Confidential MLNode, and Gonka's own Cosmos SDK and CometBFT forks), and point-in-time audits, such as the Trail of Bits and HackerOne engagements reimbursed in [Proposal #117](https://gonka.gg/network/proposals/117), don't leave regression tests behind. To our knowledge, none of the three roadmap projects above has a funded proposal today.

## 3. Who we are

Quorint is an independent security research and audit firm registered in the Netherlands. We work on L1 nodes and consensus (Rust, Go, C++), zero-knowledge circuits and applied cryptography, and smart contracts (EVM/Solidity, SVM, CosmWasm). Every engagement is principal-led: line-by-line manual review combined with custom stateful fuzzing, differential testing and reproducible proofs of concept. Researcher profiles are listed at https://quorint.xyz.

- **Gonka:** in July 2026 Quorint's research team disclosed a Critical consensus-liveness vulnerability in Gonka, awarded a $20,000 bug bounty ([write-up](https://quorint.xyz/research/gonka-decimal-exponent-bomb/)).
- **Zcash:** two Critical pre-release consensus-divergence findings in Zebra ([PR 10461](https://github.com/ZcashFoundation/zebra/pull/10461)); full-node and P2P denial-of-service findings in Zakura (PRs [1911](https://github.com/zakura-core/zakura/pull/1911), [1915](https://github.com/zakura-core/zakura/pull/1915), [1962](https://github.com/zakura-core/zakura/pull/1962)), followed by a commissioned protocol and consensus assessment ([OpenZcash Coinholder Proposal 127](https://openzcash.org/coinholders/proposals/127), $67,500); an ongoing cryptographic assessment of Zcash Voting.
- **Team for this engagement:** a principal researcher leads all manual and cryptographic review and proof-of-concept work for the full 24 weeks. A senior engineer builds the fuzzing suites, the multi-node harness and the simulator.

## 4. Scope by milestone

### Milestone 1 (weeks 1–6): bridge relaunch security gate

- **Private root-cause verification:** reconstruct the incident from public chain data and code, compare it with MillCreek's analysis, and confirm the fix closes every path to an unauthorized epoch key. Shared only with MillCreek and designated maintainers until the fix ships.
- **`x/bls` key generation and group-key validation:** dealing and commitment verification, disputes, slot-weight accounting, epoch transitions, the signing-request lifecycle, exposed partial signatures and stale epoch keys.
- **Bridge v2 contract review** against six properties: signer-set rotation approved by the current set and timelocked; per-period caps on withdrawals and mints; a pause guardian with a governance override; expiry of old epoch keys; domain separation and replay protection; reserve accounting that matches the wrapped supply on Gonka.
- **Gonka-side bridge flows** (wrapped-token mint and burn, `BRIDGE_PENDING` handling, escrow refunds, deposit deduplication), and review of **re-backing and compensation transactions at no extra cost** before they are submitted.
- **Open source:** `gonka-bridge-sentinel` v1, a self-hosted monitor that alerts when an Ethereum-side key change, withdrawal or mint has no matching Gonka signing request, when caps are approached and when the wrapped supply drifts from the reserve; its acceptance test replays the 18 November sequence on a fork. Plus `gonka-bridge-security`, invariant suites for the bridge v2 and wrapped-token contracts.
- **A written relaunch sign-off, or a list of blocking issues,** delivered at least 5 days before hosts vote on the relaunch. Payment does not depend on which of the two we deliver.

The bridge v2 code is written by MillCreek. If it is not ready by week 6, the remaining relaunch review continues into Milestone 2 with priority, and the Milestone 2 scope shifts accordingly, agreed publicly with MillCreek and the Product Committee.

### Milestone 2 (weeks 7–12): L1, P2P and devshard audit plus attack registry

- **Audit** of the `gonka-ai/cosmos-sdk` fork (including unmetered `ValidateBasic()` work before the ante handler, the class of our earlier finding), peer exchange in the CometBFT fork, devshard v7, and the `community-sale` and `liquidity-pool` CosmWasm contracts.
- **`gonka-attack-registry` v1:** at least 20 attack classes encoded as deterministic regression checks, with a Byzantine-peer and malicious-executor harness that runs in `testermint` CI and on the Community DevNet. The 18 November attack class is among the first entries and is published only after the fix ships. The registry plugs into External Test Lab and Community DevNet (Proposal #82) instead of building parallel infrastructure.

### Milestone 3 (weeks 13–18): economic and validation attack simulator

`gonka-econ-sim` v1 is a reproducible discrete-event and Monte Carlo simulator with rational, colluding and griefing hosts, gateways, challengers and consumers. It models billing extraction under sampled replays, PoC and Decode-PoC margin gaming, slot hogging and fee-exemption griefing, and validation and slashing parameter bounds. With its parameter risk report generator, the Product Committee and MillCreek can stress-test a `MsgUpdateParams` proposal before hosts vote on it.

### Milestone 4 (weeks 19–24): pre-mainnet upgrade audits and handoff

- **Per-escrow BLS DKG ([#1748](https://github.com/gonka-ai/gonka/discussions/1748)):** dealing proofs, transcript binding, complaint soundness and reconstruction under adaptive aborts. After 18 November this is the highest-value item.
- **Decode-PoC rollout and image-to-text support** (Proposal #118 scope), and attestation verification for **Confidential MLNode** ([#951](https://github.com/gonka-ai/gonka/discussions/951)).
- Attack registry v2 (≥35 classes), `gonka-econ-sim` v1.2, and a handoff package with a live walkthrough.

If any of these slips past week 24, the hours move to whichever release candidate or roadmap security item carries the highest risk at the time, agreed publicly with MillCreek and the Product Committee.

## 5. Payment schedule and reporting

Each milestone ends with public artifacts and a time and spending report. The report is published 5 days before the next tranche unlocks, which leaves hosts more than one 48-hour voting period to claw back.

| Tranche | Unlock day | GNK | Condition |
|---|---|---|---|
| T1 | 0 | 250,000 | Mobilization; Milestone 1 starts immediately |
| T2 | 45 | 300,000 | M1 report and relaunch sign-off published by day 40 |
| T3 | 90 | 300,000 | M2 report and registry v1 published by day 85 |
| T4 | 135 | 300,000 | M3 report and `gonka-econ-sim` v1 published by day 130 |
| T5 | 180 | 250,000 | M4 final report and handoff published by day 175 |
| T6 | 210 | 200,000 | 30-day post-completion holdback |
| **Total** | | **1,600,000** | No automatic renewal |

## 6. KPIs

| KPI | Target |
|---|---|
| Relaunch gate | 100% of in-scope bridge v2 and `x/bls` changes reviewed; sign-off or blocking-issues list at least 5 days before the relaunch vote |
| Sentinel | Alerts within one Ethereum block on a replay of the 18 November key change; deployed on Community DevNet |
| Invariant fuzzing | 100% of in-scope bridge Solidity and CosmWasm contracts; ≥100,000 randomized sequences per contract |
| Attack registry | ≥20 classes at M2 and ≥35 at M4, all deterministic |
| Economic simulation | ≥12 adversarial models with reproducible parameter sweeps |
| Upgrade audit turnaround | ≤10 business days to first findings after code freeze; ≤72 hours to re-verify a fix |
| Finding quality | Every Critical, High and Medium finding ships with a runnable PoC test, root cause and patch guidance |
| No double-billing | $0 in bounty claims by Quorint for vulnerabilities found in scoped repositories during the engagement |

How each KPI is verified is listed in the full proposal.

## 7. Disclosure and oversight

- **Private first.** Following [Gonka's vulnerability reporting policy](https://gonkadocs.com/gonka/docs/report-vulnerability/), no unpatched vulnerability, exploit or regression test is made public. Findings go privately to MillCreek R&D and designated maintainers, marked "Grant-covered — no bounty claim", and become public only after the fix is merged, released and through the host upgrade window.
- **Oversight.** Milestone reports go in the Governance Proposal Reports category at least 5 days before each unlock. The Governance Support Committee tracks deadlines and can recommend a clawback; the Product Committee reviews results against the KPIs above.

## 8. Budget

- **Total: 1,600,000 GNK from the Community Pool. No USDT.** That is ≈ $208,000 at the 24 November price ($0.13), ≈ $266,000 at the 30-day average ($0.167), and 1.38% of the Community Pool (115.58M GNK). We deliberately do not value GNK at the $0.60 Community Sale price from Proposal #117.
- Amounts are fixed in GNK. Quorint carries all price and liquidity risk after approval: no top-ups and no re-pricing.
- **Why GNK only:** the only stablecoin balance the community controls on-chain in size is bridged USDT, essentially the reserve drained on 18 November. We will not draw on bridged USDT while the community decides on re-backing.

| Line | GNK | ≈ USD at $0.15 |
|---|---|---|
| Principal researcher: manual and cryptographic review across all four workstreams, PoCs, fix verification | 880,000 | $132,000 |
| Senior engineer: invariant suites, multi-node harness, simulator | 560,000 | $84,000 |
| Compute and infrastructure: fuzzing runners, multi-node chaos testbed, archive and RPC access for the sentinel | 160,000 | $24,000 |
| **Total** | **1,600,000** | **$240,000** |

**Selling GNK.** GNK trades thinly: on 24 November the only active market for native GNK listed by CoinGecko and CoinMarketCap was SafeTrade, with a 30-day median volume of about $1,500 a day. To avoid adding sell pressure, Quorint commits to the following:

- Sales go over the counter where possible.
- Public-market sales on any day stay below 10% of that market's trailing 7-day average volume.
- Every sale or transfer out of the recipient address is listed in the next milestone report, with date, amount and venue or destination.

**Reference points.** Proposal #117 reimbursed 607,250 USDT for point-in-time Trail of Bits and HackerOne engagements. Proposal #82 (External Test Lab) received 88,000 USDT and 80,000 GNK for a 4-month pilot through the same escrow contract proposed here. Proposal #118 (MillCreek) received 866,000 USDT for two months of full-team work, paid upfront without escrow. This proposal asks for ≈ $208–266K in value over six months, depending on the GNK price, fully escrowed and subject to clawback.

## 9. Escrow and host protection

Funds go into a new instance of the milestone escrow contract that hosts already approved for Proposal #82 (98.2% Yes), so there is no new contract code to review.

- **Contract:** `code_id 107`, checksum `94b141625b7641e6ad57266420b18a4af72eac49b8110cb92719755590b463bd`.
- **Escrow address:** `gonka1m5gr4pkemg7fyml3jlkecpvxzprrkglfu05jfe8kmm38780ajp5s9qznhg` (Instantiate2 from the governance module, salt `quorint-gonka-security-2026`). Anyone can re-derive it with the script in the proposal repository.
- **Recipient (Quorint):** `gonka1ggt0d4jqmztnmh86na3m99c9d3q7s6h2dkd2qv`. Every transfer out of this address is reported under the selling policy above.
- **No admin and no migration.** The recipient, amounts and unlock days are fixed at instantiation. Claims are permissionless and pay only matured tranches, only to the fixed recipient.
- **Clawback:** one governance vote cancels the escrow and returns everything still in it to the Community Pool. After day 270 anyone can close the escrow and sweep any remainder to the Community Pool.

## 10. Terms

The full proposal contains eleven terms: the nature of the payment (a fixed fee for services, not a grant, loan or investment), source of funds and acceptance, escrow and clawback, use of funds, independent service provider, conflicts of interest, open source, confidentiality, no guarantees, no double-billing, and compliance and taxes. The conflict-of-interest term in full:

**Conflicts of interest.** Quorint is paid in GNK, so it benefits from a healthy network and a working bridge. To keep the review independent, tranches unlock on fixed dates and do not depend on whether Quorint recommends relaunching the bridge; a "not ready" verdict changes nothing in the payout. Each milestone report discloses Quorint's holdings of GNK, WGNK and other Gonka-related assets, and its GNK sales under the selling policy above.

## 11. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Bridge v2 code is not ready in time | The relaunch review continues into M2 with priority; the scope swap is agreed publicly |
| A finding leaks before it is fixed | Private-first disclosure; public tests only after release and the upgrade window |
| Overlap with MillCreek or bounty teams | MillCreek owns the fixes; Quorint reviews and tests. The registry and simulator plug into existing test infrastructure |
| Non-delivery | A report 5 days before each unlock; one-vote clawback of everything still in escrow; the GSC can recommend a clawback |
| Principal researcher unavailable for more than two weeks | Quorint notifies the GSC publicly, and hosts can claw back |
| GNK price or liquidity | Carried entirely by Quorint; no top-ups. Sales follow the selling policy above |
| Conflict of interest, since Quorint is paid in GNK | Tranches are time-based and independent of the relaunch verdict; holdings and sales are disclosed in every milestone report |

## 12. Open questions

1. Should Milestone 1 also cover the IBC routes, or stay focused on the Ethereum bridge relaunch?
2. Would MillCreek prefer we start with root-cause verification or with the bridge v2 design review in week 1?
3. Beyond per-escrow DKG, Decode-PoC, image-to-text support and Confidential MLNode, which upgrades should Milestone 4 prioritize?
4. How should the registry and the sentinel be packaged for External Test Lab: as `testermint` suites or as standalone Docker Compose jobs?
5. If the bridged USDT reserve is restored, would hosts or the Gonka Foundation prefer to convert later tranches to USDT through a separate proposal?

## 13. Decision requested

Approve a 24-week engagement with Quorint covering an independent security review for the bridge relaunch (Roadmap Track 6, Project 3), an executable attack registry (Track 5, Project 1), an economic attack simulator (Track 5, Project 2) and pre-mainnet upgrade audits. It is funded with 1,600,000 GNK from the Community Pool through a new instance of the `code_id 107` milestone escrow, released in six tranches and subject to a one-vote governance clawback.


---

<div class="preproposal-link" markdown="1">

[View on gonka.vote](https://gonka.vote/proposal/e81cd79e-b001-47bd-a8ab-3dc8be2f32b2)

</div>
