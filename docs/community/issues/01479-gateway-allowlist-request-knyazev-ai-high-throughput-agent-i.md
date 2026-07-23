---
title: "#1479 — Gateway allowlist request: Knyazev AI high-throughput agent infrastructure"
source: https://github.com/gonka-ai/gonka/issues/1479
issue_number: 1479
synced_at: 2026-07-23T14:37:17Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Gateway allowlist request: Knyazev AI high-throughput agent infrastructure
    <span class="issues-number">#1479</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/knyazev741">@knyazev741</a> opened 2026-07-19 06:12 UTC</span>
    <span class="issues-meta-item">3 comments</span>
    <span class="issues-meta-item">Updated 2026-07-21 05:52 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Operator

- **Name:** Nikita Knyazev
- **GitHub:** [@knyazev741](https://github.com/knyazev741)
- **Project:** Knyazev AI / self-hosted agent infrastructure
- **Contact:** via this GitHub issue

## Requested creator address

```text
gonka1mylwv85v5kv7ty2pg4f3evgsqrj7xxtc2p2tud
```

Public key:

```text
Akh4KxA3B35UI3XU3M4U99tfajeqQSyXLEDrRfUH16yB
```

Please consider adding this address to `devshard_escrow_params.allowed_creator_addresses`.

The key is dedicated exclusively to devshard escrow creation. In accordance with the current self-hosted gateway guide, the creator will be funded only after allowlist membership is confirmed.

## Models

- `MiniMaxAI/MiniMax-M2.7` — primary
- `moonshotai/Kimi-K2.6` — secondary / evaluation

## Use case

We operate a private AI-agent and automation infrastructure with parallel worker pipelines. The immediate workload includes agent orchestration, code and log analysis, structured extraction, evaluation workloads, and high-volume background processing.

Our target operating range is **100–200 concurrent inference requests**. A community broker is useful for initial compatibility testing, but it does not meet our requirements because:

- broker-side concurrency limits are below our target;
- we require direct GNK settlement and self-custody;
- we need control over escrow pooling, rotation, settlement, retry policy, and capacity-aware routing;
- we do not want an intermediary in the request path for internal workloads.

This request is for a **private self-hosted gateway**, not a public broker-directory listing and not resale of raw inference.

## Initial deployment plan

- Gateway-only deployment on an existing private Linux server
- Official `libermans/gonka-devshard-proxy` container
- API bound to localhost/private infrastructure only
- `GATEWAY_MAX_CONCURRENT_REQUESTS=512`
- Multiple devshards pooled for throughput and epoch rotation
- Capacity-aware limits enabled
- Circuit breaker, bounded retries with jitter, and fallback for unavailable network capacity
- Secrets stored with restricted filesystem permissions; the creator key is dedicated and not reused

## Validation and contribution plan

After approval we will stage traffic gradually:

1. One manually managed escrow and deterministic functional checks.
2. Concurrency ramp: 1 / 3 / 10 / 25 / 50 / 100 / 200.
3. Measure success rate, HTTP error distribution, TTFT, p50/p95/p99 latency, output throughput, and settlement/refund behavior.
4. Enable multiple-escrow pooling and controlled rotation only after the single-escrow path is verified.
5. Share anonymized benchmark and reliability results with the Gonka community if useful.

Initial broker-based testing already showed why direct capacity testing matters: MiniMax handled sequential requests reliably during one sample, while a 10-concurrent sample produced substantial upstream 502 variance. We want to test the native devshard/operator path and contribute actionable capacity data rather than hide network behavior behind broker-specific limits.

## Governance and operations commitments

- We understand that allowlist inclusion is an on-chain governance decision and is not guaranteed.
- We will respond to maintainer and community questions promptly.
- We will not fund or attempt to open escrows until the address is confirmed on the allowlist.
- We will start with private/internal traffic and staged load, not an immediate public endpoint.
- We will publish operational findings and adjust limits if governance or network operators request it.

Thank you for considering the request.
</div>

---

## 💬 Comments (3)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/knyazev741">@knyazev741</a></span>
    <span class="issues-meta-item">commented 2026-07-19 06:19 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi @tcharchian — could you please point us to the preferred path for getting this address considered in the next governance-approved allowlist batch, and to the community channel where support should be discussed before a proposal?</p>
<p>To clarify the operator-specific need: this is not a request for a broker-directory listing. We need the creator path itself for self-custodied GNK settlement, control of escrow pooling/rotation, and a private workload targeting 100–200 concurrent requests. We will stage the load and publish anonymized capacity/reliability measurements back to the community.</p>
<p>The dedicated address remains unfunded, following the current gateway guide's instruction not to fund or deploy until allowlist membership is confirmed. We are ready to provide any additional operator details or revise the scope for governance review.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/knyazev741">@knyazev741</a></span>
    <span class="issues-meta-item">commented 2026-07-19 06:52 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Community discussion is now open in Gonka <code>#dev-chat</code>:
https://discord.com/channels/1336477374442770503/1336787104935579668/1528292662245855403</p>
<p>We have asked active hosts what evidence or operational commitments they would want before supporting inclusion in the next governance-approved creator allowlist batch. We will keep this issue updated with any requested details. The dedicated creator address remains unfunded, and the gateway will not be deployed until on-chain allowlist membership is confirmed.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-07-21 05:52 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi @knyazev741, thanks for opening issue and for already opening the discussion in #dev-chat. That's exactly the right move, and it answers your own question about the process better than I could: there's no maintainer-controlled queue here — Gonka is decentralized, so an address gets added to <code>devshard_escrow_params.allowed_creator_addresses</code> only through on-chain governance (a standalone param-change proposal or inclusion in a governance-approved upgrade batch). Building visible support with active hosts/operators in the community <em>before</em> a proposal is assembled is the strongest thing you can do while you wait.</p>
<p>OpenBroker https://github.com/gonka-ai/gonka/discussions/1363 would address the throughput concern — it's GNK-native, no markup, and has been load-tested well past your 100–200 concurrent range — but it's custodial by design (you deposit GNK to an operator-controlled address and run under their API key), and it abstracts the escrow/settlement path away from you. Since your stated requirements are self-custodied GNK settlement, direct control of escrow pooling/rotation/retry, and no intermediary in the request path — plus the explicit goal of measuring the <em>native</em> devshard/operator path rather than broker-specific behavior — a broker doesn't substitute for the creator path here. So the allowlist request is the correct path, not something to redirect.</p>
<p>Keep this issue updated with anything the hosts ask for in #dev-chat, thanks</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1479](https://github.com/gonka-ai/gonka/issues/1479) every hour.
