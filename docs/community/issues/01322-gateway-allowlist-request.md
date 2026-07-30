---
title: "#1322 — Gateway allowlist request"
source: https://github.com/gonka-ai/gonka/issues/1322
issue_number: 1322
synced_at: 2026-07-30T14:37:52Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Gateway allowlist request
    <span class="issues-number">#1322</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/Puyre">@Puyre</a> opened 2026-06-08 15:13 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-06-10 15:20 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
# Request to be added as a Gonka gateway operator (devshard creator allowlist)

Hi Gonka core team & community,

We're requesting inclusion of our on-chain address in
`devshard_escrow_params.allowed_creator_addresses` so we can operate
our own devshard gateway rather than routing through a third-party
broker.

## On-chain identity

- Devshard creator address (requested for allowlisting):
  `gonka15y6xg0ps5w0u4w3ttx557mf46v82ms8svcavy2`
- This account is funded above `devshard_escrow_params.min_amount` and
  has its on-chain pubkey published (secp256k1).

## About the project

We're building an OpenAI-compatible inference gateway that uses Gonka
as its primary backend — a drop-in replacement for closed AI APIs
(developers change one `base_url` and keep their existing OpenAI SDK
code).

Under the hood, the gateway routes requests to Gonka by default and
automatically falls back to a stable provider (OpenRouter) when the
network is unavailable. The goal is to let end users run their
workloads on Gonka — capturing the cost savings — without being exposed
to the network's current instability, since the fallback transparently
covers the downtime.

## Why this helps the network

- **Opens new demand that Gonka can't currently capture.** A
  transparent fallback to stable providers makes the network usable for
  the large set of users who today can't rely on Gonka directly because
  of its uptime variance. They get Gonka-level pricing for the majority
  of traffic that does land on the network, instead of avoiding it
  entirely.
- **Reliability engineering published back.** We run automatic failover
  and capacity-aware routing in front of the network; we're willing to
  publish anonymized reliability and latency data (TTFT, tokens/sec,
  tail latency, error/refund rate), which the
  ecosystem currently lacks sustained public numbers for.

## Supported models (intent)

We intend to serve all three currently governance-approved models:

- `qwen/qwen3-235b-a22b-instruct-2507-fp8`
- `moonshotai/kimi-k2.6`
- `minimaxai/minimax-m2.7`

## Governance and ops commitments

- We will respond to maintainer comments on this issue within one
  business day.
- We will adjust scope, staging, or framing in this issue rather than
  open a new one if maintainers prefer.

## Team and contact

- Contact: `andres@rogilabs.com`
- TG: `@puyre`

Thanks for reviewing.

Rogi AI
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Puyre">@Puyre</a></span>
    <span class="issues-meta-item">commented 2026-06-10 15:20 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Closing this — after checking with the Gonka community, I realized we don't need to run our own devshard. Getting a broker key to send requests through node4 will be enough for our case.
I'll likely open a separate issue requesting a broker key (or asking for documentation on how one can be obtained).</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1322](https://github.com/gonka-ai/gonka/issues/1322) every hour.
