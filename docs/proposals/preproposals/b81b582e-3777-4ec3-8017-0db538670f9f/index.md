---
title: "Bringing AMD and AI ASICs to Gonka"
template: proposals-main.html
---

# Bringing AMD and AI ASICs to Gonka

<div class="preproposal-header" markdown="1">

<div class="preproposal-status">🟢 Active</div>

**Author:** David
**Created:** 2026-10-01 23:35 UTC
**Closes:** 2026-10-08 23:34 UTC
**Language:** EN
**Votes:** 0
**Avg. Bid:** 0.00 GNK

</div>

Gonka's approved hardware list contains six NVIDIA GPU models. Every other accelerator is excluded, including the purpose-built inference ASICs that now form the fastest-growing segment of AI compute.

---

## Full Proposal

Bringing AMD and AI ASICs to Gonka

**A funding proposal from Wayfaster.**

| | |
|---|---|
| **Requested** | $480,000 USDT: $160,000 on approval, $320,000 on completion less GNK mined |
| **Duration** | 20 weeks |
| **Team** | 4 engineers and a project manager, full time |
| **Roadmap** | Track 3, Project 1: hardware-neutral inference |
| **Contact** | [wayfaster.org](https://wayfaster.org) · hi@wayfaster.org |

---

## 1. Summary

Gonka's approved hardware list contains six NVIDIA GPU models. Every other accelerator is excluded, including the purpose-built inference ASICs that now form the fastest-growing segment of AI compute. Twelve of the fifteen platforms here are ASICs.

Over 20 weeks the project delivers:

- **Hardware classes**: the mechanism allowing the network to approve any accelerator by governance vote, without further protocol work. Everything else proves it.
- **AMD support end to end**: the first vendor through the mechanism, and the shortest path to demonstrating it works.
- **ASIC validation on real silicon**: Tenstorrent and Intel Gaudi 3 conformance, a Furiosa adapter design, Qualcomm and Positron fit assessments.
- **A measured class for NVIDIA's Vera Rubin generation**, prepared before that hardware reaches hosts.
- **Written assessments for four further ASIC platforms** against the same class definition.

This is Track 3, Project 1 of the Gonka roadmap, currently unassigned.

---

## 2. The problem

The host software assumes NVIDIA throughout. The installation guide requires NVIDIA's container toolkit, hardware detection speaks only to NVIDIA cards, and the configuration reserving hardware names NVIDIA explicitly. An operator holding AMD cards, or Tenstorrent or Furiosa silicon, has no route in.

Three consequences follow:

| | |
|---|---|
| **Cost** | Hosts compete for NVIDIA capacity at one supplier's prices. |
| **Growth** | Operators with non-NVIDIA fleets cannot contribute capacity at all. |
| **Concentration** | Network supply depends on one vendor's allocation decisions. |

---

## 3. Why ASICs matter to Gonka

An inference ASIC performs one task. It omits the silicon a general-purpose GPU spends on training, graphics and flexibility, and spends that area on memory bandwidth and the arithmetic serving a model requires. That is the basis on which these vendors compete.

The market direction is not in question. Google, AWS, Qualcomm and Broadcom all build inference silicon, and Tenstorrent, Furiosa, Positron, SambaNova, Cerebras and Intel sell theirs openly.

For a decentralized network this matters more than for a single operator. A host's return is the gap between what inference costs it and what the network pays. On general-purpose GPUs that difference is narrowest, as every buyer bids for the same parts. Purpose-built silicon is where it widens, and a network that cannot accept it will not attract the operators who own it.

**ASICs are also the case a single global margin cannot serve.** AMD and NVIDIA GPUs share enough arithmetic behaviour that one margin might stretch across both. An ASIC with a different numeric pipeline is far less likely to fall inside a margin calibrated on NVIDIA, and the network cannot widen that margin enough to admit it without abandoning verification for everyone else. Per-class margins are not a convenience for ASICs; they are the only mechanism that admits them.

This is why the project is sequenced as it is. AMD proves the mechanism end to end inside 20 weeks, as its support already exists in the serving engine. The ASIC work then runs against a demonstrated mechanism.

---

## 4. How verification works, and why it blocks new hardware

When a node claims to have run a model, Gonka re-runs part of that work elsewhere and compares the results. The two never match exactly, because different chips order the arithmetic differently. The network therefore permits a margin: a difference below it counts as honest, above it as evidence of cheating.

Setting that margin is a trade-off. Too tight, and honest hosts are penalised for hardware differences outside their control. Too loose, and a node can serve a cheaper, lower-precision model and keep the difference in operating cost.

At present a single margin applies to every model and card, so admitting new hardware requires widening it for all participants. That is the principal reason the work has not been undertaken.

### What the published measurements show

The figures come from Gonka's published validation data. They are dimensionless; zero would mean identical results.

| Comparison | Typical difference | Largest observed |
|---|---:|---:|
| Two honest nodes on different NVIDIA generations (A100, H100, B200) | 0.07 | 0.52 |
| A node substituting a cheaper, lower-precision model | 0.24 | 1.48 |

At a margin of **0.174** the two cases separate cleanly. In Gonka's 377-participant simulation an honest node was penalised in zero rounds out of 100,000, and a cheating node was detected in 74%.

The equivalent figures for AMD and ASIC hardware have not been published by anyone. Establishing them is the first measurement task of this project.

### The margins currently in force

The margins active on the network are **0.2, 0.4 and 0.75**, wide enough to cover every model and card under one value. Gonka's `docs/release-candidate-gpu-profile.md` reports that at a candidate value of 0.41 the honest and substituted distributions become statistically indistinguishable, and states that the parameters "do not create quantization separability."

Detection of lower-precision substitution is therefore already weak on NVIDIA-only hardware, independent of this proposal. Per-class margins do not weaken a protection the network relies on. They make a tight margin practical again, because a margin covering one class need not accommodate all of them.

### Why the change is achievable

Verification was never bit-exact: the plugin source states that "bitwise equality of outputs is neither required nor checked." The code is already portable, using standard PyTorch operations with no NVIDIA-only kernels. And cross-generation verification already works, with an A100 checked against an H100 differing by 0.070 under one margin. All three are verifiable in Gonka's public repositories.

---

## 5. What we build

**A hardware class** is a declared combination of vendor, chip family, numeric precision and software version. Verification takes place within a class, against a margin measured for that class. Approving one is a governance vote, as approving a new model is today.

Gonka already operates this way along one axis: each model carries its own verification settings, and adding a model is routine governance, as with Kimi-K2.6 in v0.2.12 and MiniMax-M2.7 in v0.2.13. Hardware classes reuse that machinery rather than adding new machinery.

**What does not change.** Existing hosts are unaffected on day one. The current fleet maps into NVIDIA classes carrying exactly today's values, and no existing margin is widened. A new class is opt-in, requires a vote, and can be removed by a single proposal.

**What changes in the node software.** Hardware detection and fault reporting cease to be NVIDIA-specific, and configuration gains non-NVIDIA device mapping. Images pin an exact driver, framework, compiler and serving-engine combination per accelerator, which matters more for ASICs than GPUs, as their software stacks move faster.

**Review before code.** The design, covering class declaration, validator pairing, uncompared class pairs, and limits preventing advantage from an unusual class, is published for open review before any consensus code is written.

---

## 6. Hardware coverage

"ASIC" denotes a chip built specifically for AI workloads rather than a general-purpose GPU.

### GPUs: delivered end to end

| Vendor | Chip | Basis | Deliverable |
|---|---|---|---|
| **AMD** | MI300X, MI325X, MI355X, MI455X | Already supported by Gonka's serving engine. | Host image, verification operational, full cross-vendor measurement |
| **NVIDIA** | Vera Rubin | Same software path, but a new generation computes differently and needs its own margin. | Class defined and measured against Hopper and Blackwell, ready for a vote before the hardware ships |

### ASICs: validated on hardware we obtain

| Vendor | Chip | Basis | Deliverable |
|---|---|---|---|
| **Tenstorrent** | Blackhole | Serving-engine plugin exists; cards sold directly. | Cards purchased and operated, verification conformance established |
| **Intel** | Gaudi 3 | Runs Gonka's serving engine; cards and cloud instances available. | Evaluation programme, verification conformance established |
| **Furiosa** | RNGD | Serving-engine compatible but not a plugin, so it needs its own adapter. | Evaluation programme, adapter design |
| **Qualcomm** | AI200, AI250 | Rack-scale inference, substantial memory per card. | Evaluation programme, fit assessment |
| **Positron** | Atlas | Inference only, limited public software surface. | Evaluation programme, fit assessment |

### ASICs: assessed against the class definition

| Vendor | Chip | Status |
|---|---|---|
| **Google** | Ironwood (TPU) | Maintained serving-engine plugin; cloud-only access |
| **AWS** | Trainium, Inferentia | Vendor SDK with a plugin; cloud-only access |
| **SambaNova** | SN50 | Vendor SDK, cloud access |
| **Cerebras** | WSE-3 | Proprietary SDK, very low latency |

Each receives a written assessment. Four more are tracked without committed work, as no independent host can operate them today: Groq LPU (now within the NVIDIA stack), Taalas HC1 (fixed-model silicon needing its own class rules), Broadcom Jalapeño and Intel Crescent Island. Huawei Ascend is excluded on export-control grounds, and we recommend that position be maintained.

Several assessed platforms are cloud-only today, which matters for a network whose hosts own their hardware. Specifications for vendors other than AMD and Tenstorrent come from public vendor material, and are presented as assessments rather than commitments.

---

## 7. Plan

20 weeks in four phases. ASIC procurement begins in week one, because lead times on silicon and vendor agreements exceed any single phase.

| Phase | Weeks | Work | Output |
|---|---|---|---|
| **P1** | 3 | Sign the five ASIC evaluation programmes and order Tenstorrent hardware immediately. Reproduce Gonka's published reference results on rented NVIDIA capacity, extend the test harness across vendors, and establish automated builds and the conformance suite. | Public reproduction report and harness. Programmes signed, silicon ordered. |
| **P2** | 6 | AMD host image with verification operational, pinned per card model. Measurement campaign across MI300X, MI325X and MI355X against A100, H100 and B200 on at least two models, with Vera Rubin added as capacity is released. Each image is checked against reference hardware first. | Working AMD image, measured differences for each pair of cards, and a recommended margin for admitting a second vendor. |
| **P3** | 6 | Implement the class mechanism: declaration, class-aware verification, safety limits and automated tests covering mixed-hardware rounds. Design published for review first. | Merge-ready code, tests passing, and a migration leaving NVIDIA hosts on identical settings. |
| **P4** | 5 | Verification conformance on the Tenstorrent cards and Intel Gaudi 3, against the mechanism built in P3. Furiosa adapter design, Qualcomm and Positron fit assessments, and the four written ASIC assessments. A mixed-vendor test network running real rounds, an independent security review, and the governance proposal. | Test network validating GPU and ASIC hosts together, one assessment per platform, review report, and an upgrade proposal. |

**After delivery.** A further month of support is budgeted for the governance process and onboarding the first non-NVIDIA hosts.

**Relationship to existing work.** Gonka's existing hardware-profile and validation experiments are credited to the Kaitaku team in `docs/release-candidate-gpu-profile.md`, and the verification plugin is installed from their repository. Their method is the one this project extends, and Phase 1 exists so we demonstrate reproduction of their results first. We will coordinate with them and with the External Test Lab rather than run a competing track.

---

## 8. Team

Wayfaster is an inference engineering studio: serving optimisation, quantization with quality gates, hardware portability and capacity planning.

| Role | Months | Responsibility |
|---|---|---|
| Protocol engineer | 5 | Go and Cosmos-SDK: parameters, declaration, class-aware verification, tests |
| ML systems engineer | 5 | Serving-engine internals, AMD and ASIC bring-up, container images, per-model pinning, adapters |
| ML engineer, measurement | 5 | Test harness, measurement campaigns, margin calibration, simulation |
| DevOps and test engineer | 5 | Automated builds and image registry, test network operation, conformance gates |
| Project manager | 5 | Vendor contracts and procurement, coordination, reporting, governance process |

**Scope of the testing role.** The failure mode this project must detect is silent: on unfamiliar hardware a model loads normally, runs at normal speed, and produces incorrect values. Nothing fails visibly, so a check establishing only whether the model started accepts it. The risk is highest on ASICs, whose software stacks are younger than CUDA and change faster. Detecting it requires one image per accelerator model, built automatically and compared against reference hardware.

The project manager's scope is five vendor programmes, silicon procurement and 20 weeks of coordination, keeping the engineers on technical work.

---

## 9. Budget

| Category | Amount | Share | Basis |
|---|---:|---:|---|
| Engineering | $210,000 | 43.8% | 15 engineer-months × $14,000 |
| DevOps and testing | $60,000 | 12.5% | 5 months × $12,000 |
| Project management | $45,000 | 9.4% | 5 months × $9,000 |
| Hardware, capacity, vendor programmes | $131,000 | 27.3% | Itemised below |
| Independent security review | $12,000 | 2.5% | External review in P4 |
| Post-delivery support | $12,000 | 2.5% | One month: governance and host onboarding |
| Hardware price reserve | $10,000 | 2.1% | 7.6% of the hardware line |
| **Total** | **$480,000** | **100%** | $160,000 on approval, $320,000 on completion |

The weighting of the hardware line reflects the priority: ASIC silicon and vendor access account for $79,000, against $24,980 of AMD rental. Hardware is quoted as a range, as rates move between contract dates and most ASICs have no public price. Each line is **budgeted at the top of its range**; the reserve covers movement above it, and unspent amounts return.

### 9.1 ASIC silicon and vendor programmes, paid at order

| Item | Unit | Qty | Range | Budgeted |
|---|---:|---:|---:|---:|
| Tenstorrent Blackhole p150a cards | $1,350–1,450 | 4 | $5,400–5,800 | $5,800 |
| Host servers for those cards | $2,200–2,600 | 2 | $4,400–5,200 | $5,200 |
| Tenstorrent multi-card access | n/a | 1 | $7,000–9,000 | $9,000 |
| Intel Gaudi 3 access | n/a | 1 | $6,000–8,000 | $8,000 |
| Furiosa RNGD programme | n/a | 1 | $10,000–13,000 | $13,000 |
| Qualcomm AI200 programme | n/a | 1 | $10,000–13,000 | $13,000 |
| Positron Atlas programme | n/a | 1 | $8,000–11,000 | $11,000 |
| SambaNova and Cerebras credits | n/a | 1 | $4,500–6,000 | $6,000 |
| TPU and Trainium credits | n/a | 1 | $6,000–8,000 | $8,000 |
| | | **Subtotal** | **$61,300–79,000** | **$79,000** |

### 9.2 Rented GPU capacity, prepaid on committed terms

| Item | Rate | Quantity | Range | Budgeted |
|---|---:|---:|---:|---:|
| AMD MI300X | $2.30–2.50/hr | 5,000 GPU-hr | $11,500–12,500 | $12,500 |
| AMD MI325X | $2.15–2.40/hr | 1,200 GPU-hr | $2,580–2,880 | $2,880 |
| AMD MI355X | $2.80–3.20/hr | 3,000 GPU-hr | $8,400–9,600 | $9,600 |
| NVIDIA Vera Rubin | $12.00–15.00/hr | 400 GPU-hr | $4,800–6,000 | $6,000 |
| NVIDIA H100 SXM5 | $3.80–4.20/hr | 1,200 GPU-hr | $4,560–5,040 | $5,040 |
| NVIDIA B200 | $8.90–9.80/hr | 300 GPU-hr | $2,670–2,940 | $2,940 |
| NVIDIA A100 80GB | $1.40–1.70/hr | 500 GPU-hr | $700–850 | $850 |
| | | **Subtotal** | **$35,210–39,810** | **$39,810** |

### 9.3 Infrastructure

Test network chain nodes, 3 for 6 months at $420–480/mo ($8,640); model storage and transfer ($1,450); build runners and image registry ($2,100). Subtotal $10,160–12,190, budgeted at **$12,190**.

**Hardware total: $106,670–131,000, budgeted at $131,000.**

Tenstorrent card prices are retail. The other ASIC programmes have no public price or rental channel, so their ranges reflect comparable engagements. AMD rates are committed-term pricing verified against current on-demand listings. Vera Rubin has no settled market rate, so its hour count is small by design: enough to define a class, not run a fleet.

---

## 10. Payment

| Tranche | Amount | Covers |
|---|---:|---|
| **On approval** | $160,000 | ASIC silicon and programmes ($79,000), prepaid GPU capacity ($39,810), infrastructure ($12,190), and $29,000 toward the team |
| **On completion** | $320,000 | Remaining team cost ($286,000), independent review ($12,000), post-delivery support ($12,000), price reserve ($10,000). **Less any GNK mined during the project.** |
| **Total** | **$480,000** | Two thirds contingent on delivery |

**GNK offset.** Our nodes will earn GNK during testing and test-network operation. The amount will be small and irregular, but whatever is mined is reported and deducted from the final payment.

### Terms

- Two thirds of the total, $320,000, is contingent on delivery. The first tranche barely exceeds the hardware it buys, leaving Wayfaster to fund roughly 18 of the 20 weeks of salary.
- A spend report with invoices is published, and any line procured below its budgeted top is returned.
- All work is public from week one. Hardware bought with grant funds transfers to the network on completion.

---

## 11. Questions and answers

**Why begin with AMD if the goal is ASICs?**
AMD is the shortest route to proving the mechanism. Support already exists in the serving engine, so a working second vendor can be demonstrated end to end within 20 weeks, and the ASIC work then runs against a proven mechanism rather than one on paper. ASIC procurement still begins in week one, as lead times are long.

**I operate NVIDIA hardware today. Does this change anything for me?**
No. On day one your machines map into an NVIDIA class carrying exactly today's settings. No existing margin is widened, and no host needs to reinstall anything.

**Does admitting other vendors make cheating easier?**
It should make it harder. One margin currently covers every model and card, and at a candidate value of 0.41 honest and substituted results are already indistinguishable. A per-class margin can be tightened.

**What if the measurements show differences too large to verify safely?**
The class is not approved, and the network holds the measurement establishing why. That data does not exist publicly for any non-NVIDIA accelerator. Phase 2 answers the question with figures before any consensus code is written.

**Why is a third paid before the work?**
$131,000 of the first tranche is hardware, including $79,000 of silicon and vendor access that does not exist until purchased. Tenstorrent cards are bought outright, and Furiosa, Qualcomm and Positron access comes through programmes agreed in advance, with no rental channel. Only $29,000 reaches the team, so Wayfaster funds roughly 18 of the 20 weeks of salary.

**What happens if the project is not completed?**
The remaining $320,000 is not paid, and the code, harness and measurements remain with the network, public from the first week.

**When could a non-NVIDIA host join?**
Code is merge-ready at week 14 and the governance proposal at week 20. Admission is a vote, on the network's schedule. A class is opt-in and removable by a single later proposal.


---

<div class="preproposal-link" markdown="1">

[View on gonka.vote](https://gonka.vote/proposal/b81b582e-3777-4ec3-8017-0db538670f9f)

</div>
