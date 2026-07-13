---
title: "#1257 — Request to be added as a Gonka broker"
source: https://github.com/gonka-ai/gonka/issues/1257
issue_number: 1257
synced_at: 2026-07-13T17:25:00Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Request to be added as a Gonka broker
    <span class="issues-number">#1257</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item">[@len5ky](https://github.com/len5ky) opened 2026-05-26 15:37 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-07-03 00:47 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Hi Gonka core team & community,

We're requesting inclusion of Gonka Relay as a Gonka broker:
adding our on-chain address to
`devshard_escrow_params.allowed_creator_addresses` and listing
alongside the existing community brokers wherever that list lives.

## About the project

Gonka Relay is a Gonka-network-anchored inference operator built on
[OpenGNK](https://github.com/gonkalabs/opengnk) (MIT) for signing
and routing. Home is [gonkarelay.com](https://gonkarelay.com), with
[gonkaport.com](https://gonkaport.com) held as a sibling domain for
future audience-segmented motions.

The name describes the function: we relay signed inference between
the Gonka network and the workloads we run on top of it.

## What we're building on Gonka

The allowlist entry unblocks three uses:

1. **Capacity benchmarking, published back to this repo.** We're
   running a `genai-perf`-style harness against the network at
   varying concurrency (1 / 10 / 100 / 1000 streaming concurrent)
   and prompt sizes (100 / 1k / 10k / 100k tokens), targeting
   Kimi K2.6 and Qwen3-235B. We will publish TTFT, tokens-per-sec,
   tail latency, error rate, and refund rate as a separate issue
   in this repo. These are characteristics the network has not yet
   published sustained numbers for, and the broader ecosystem
   benefits from the data being public regardless of how this
   application resolves.
2. **In-house LLM tooling.** Evaluation harnesses, synthetic
   dataset generation, agentic coding loops, and developer-tool
   prototypes that consume large volumes of Kimi K2.6 and
   Qwen3-235B inference. These workloads need long context and
   tolerate dynamic pricing, which is where the network beats
   closed-API alternatives. Being a direct DevShards creator
   rather than routing through a third-party broker is the right
   operational fit for them.
3. **Network access for open-source agentic projects.** We intend
   to provide Gonka-backed inference to selected open-source
   agentic frameworks and developer-tool projects that currently
   depend on expensive closed APIs. Concrete partners will be
   named as they come online.

A paid customer surface launches on the same ramp, initially with
a waitlist, opening as our capacity numbers and operational tail
stabilize.

## Team and contact

- Operator: len5ky
- Contact: len5ky@gonkarelay.com
- GitHub: [@len5ky](https://github.com/len5ky)
- Discord: nsky9985

## On-chain identity

- Devshard creator address (requested for allowlisting):
  `gonka1jduzghunqzmcddwh5sc52lu75gu8elwywxht6l`
- This account is funded above
  `devshard_escrow_params.min_amount` and has its on-chain pubkey
  published (secp256k1).

## Endpoint

- Public API surface: `https://gonkarelay.com/v1/...`,
  OpenAI-compatible. Not yet live at filing time. We stand it up
  after the validation work below.
- Health: `GET /health`, `GET /ready` (planned).

## Auth modes (planned)

- **Operator-managed keys.** `Authorization: Bearer gnkrelay-sk-...`.
  We hold the on-chain identity and sign on behalf of the upstream
  workload. Default for the LLM-tooling and OSS-agentic use cases
  above.
- **Client-signed passthrough.** We forward native Gonka headers
  (`Authorization`, `X-Requester-Address`, `X-Timestamp`)
  unchanged when the caller signs requests itself. For
  GNK-wallet-native developers and contributors.

## Supported models (intent)

- `moonshotai/Kimi-K2.6` (primary): the model we optimize capacity
  and reliability around.
- `Qwen/Qwen3-235B-A22B-Instruct-2507-FP8` (secondary).
- Model discovery via `GET /v1/models` on the upstream network
  gateway. We will not hard-code the list.

## Rate limit intent (per phase)

- **Phase A, validation:** internal traffic only. Single-digit RPS
  sustained, single-digit concurrent streams.
- **Phase B, limited usage:** in-house LLM tooling and a small
  number of OSS-agentic-project integrations. ~600 RPM per key,
  < 100M tokens/day total. Monitored.
- **Phase C, broader availability:** ceilings set from Phase B
  tail-latency data. We will update this issue before moving to
  Phase C.

Phase ceilings will not be exceeded without first updating this
issue. Standard burst and abuse protection (rate-limit middleware,
per-IP throttling, per-key quotas) will be in place from Phase B
onward.

## Settlement and billing

- We hold GNK in a treasury wallet to settle with the network.
  We do **not** custody GNK on behalf of upstream callers.
- For OSS-agentic and in-house workloads, settlement is internal.
  We absorb network cost; no per-call billing surface is needed at
  filing time.
- If a paid customer surface follows, customer-facing billing will
  be USD via Stripe. Pricing depends on Phase 0.5 capacity data
  and is not finalized.

## Rollout plan

1. **On approval.** OpenGNK is already set up against our wallet
   pending allowlist. On approval, the endpoint stands up at
   `gonkarelay.com` and internal validation traffic begins flowing.
   Capacity-benchmark harness starts running in the same window.
2. **Within the first weeks.** In-house LLM tooling moves onto the
   network at the volumes described in the rate-limit section.
   First OSS-agentic-project integrations come online once partners
   commit.
3. **As capacity-benchmark numbers stabilize.** Paid-customer
   waitlist opens, then converts. Pricing surface goes public.

## Open items

- **Pricing surface:** not finalized. Phase 0.5 capacity data is an
  input. We'll publish a customer-facing pricing page before Phase C
  if a commercial surface launches.
- **Concrete OSS-agentic partners:** category is firm (agentic
  coding assistants, code-review and refactoring bots, evaluation
  harnesses). Specific named partners will be announced as they
  come online.

## Governance and ops commitments

- We will respond to maintainer comments on this issue within one
  business day.
- We are not a Host and hold no GNK collateral for voting weight,
  so we cannot participate in on-chain governance votes ourselves.
  We will engage in any related governance discussion as a
  participant where useful: sharing data, answering operator
  questions, and adjusting our setup based on the outcome.
- If maintainers prefer the request be reframed, scoped down, or
  staged differently, we'll adjust the body of this issue rather
  than open a new one.

Thanks for reviewing.

Gonka Relay
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@tcharchian](https://github.com/tcharchian)</span>
    <span class="issues-meta-item">commented 2026-07-03 00:37 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi @len5ky! Thanks, this is one of the most thorough operator applications filed here. A few things to separate, because you're actually asking for two different things governed differently.</p>
<p>On the allowlist (<code>devshard_escrow_params.allowed_creator_addresses</code>): additions happen only through on-chain governance — a param-change proposal or inclusion in a governance-approved upgrade batch. No maintainer adds an address unilaterally. Filing this issue with a funded, pubkey-published address is exactly the right way to register intent, but inclusion and timing are governance-dependent and not guaranteed, so please don't gate your roadmap on a specific approval date.</p>
<p>On directory listing, stand your endpoint up on a managed devshard backend (more on that below), run real traffic, and let the numbers accumulate — community observability dashboards like G-Meter (https://meter.gonka.gg/), Gonka Power (https://power.gnk.space/), https://openbroker.gonka.gg/stats independently probe public broker endpoints, so your stats become verifiable by anyone. Once gonkarelay.com is live and has a few weeks of good public numbers behind it, a pull request to the docs adding it to the broker list is the natural next step.</p>
<p>One factual update for your plan: <code>Qwen/Qwen3-235B-A22B-Instruct-2507-FP8</code> has been retired from the network, so the benchmarking matrix and the "secondary model" intent should be re-scoped around what's currently active — the model set is decided by governance per epoch, so check the live list via <code>GET /v1/models</code>. </p>
<p>One suggestion that could unblock most of your plan today rather than after a governance vote: your Phase A (validation, benchmarking harness) and Phase B (in-house LLM tooling, OSS-agentic integrations) don't strictly require being the escrow creator — they require throughput against real devshards. OpenBroker (https://openbroker.gonka.gg, https://github.com/gonka-ai/gonka/discussions/1363) provides exactly that: GNK-settled at cost with no markup (ledger deducted 1-to-1 with escrow cost), no enrollment wait, both protocol versions, and no rate caps beyond network capacity. Since you already hold GNK, the economics are equivalent to running your own escrows. The honest caveat, it's custodial (you deposit to an address the operator controls, access via their API key), and your latency numbers would include their proxy hop — worth stating in your methodology if you publish benchmarks gathered through it. But it would let the capacity-benchmarking and in-house workloads start now, and your published TTFT/throughput/tail-latency data would be genuinely valuable to the network either way.</p>
<p>Where your own allowlist entry remains necessary is the part of your design that's creator-specific: client-signed passthrough, controlling your own escrow rotation and settlement, and being a direct on-chain operator for the paid surface. That case stands as filed, and the phased commitments you've laid out are the right kind of material for governance participants to weigh.</p>
<p>Overall, the allowlist request is well-formed for governance consideration as filed. In parallel, nothing blocks you from launching this week on an at-cost managed devshard backend, running the benchmark harness and Phase A/B workloads, building a public track record on the community dashboards — and then bringing both the directory-listing PR and the allowlist case back with real numbers behind them.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1257](https://github.com/gonka-ai/gonka/issues/1257) every hour.
