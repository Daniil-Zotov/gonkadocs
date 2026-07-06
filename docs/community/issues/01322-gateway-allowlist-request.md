---
title: "#1322 — Gateway allowlist request"
source: https://github.com/gonka-ai/gonka/issues/1322
issue_number: 1322
synced_at: 2026-07-06T09:51:53Z
template: issues-main.html
---

> 🔄 **Авто-синхронизация:** из [Issue #1322](https://github.com/gonka-ai/gonka/issues/1322) каждые 6 часов. 

# 🔴 Gateway allowlist request

**Автор:** [@Puyre](https://github.com/Puyre) · **Состояние:** Closed · **Создано:** 2026-06-08 15:13 UTC · **Обновлено:** 2026-06-10 15:20 UTC

---

## 📝 Описание

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

---

## 💬 Комментарии (1)

### Комментарий 1 — [@Puyre](https://github.com/Puyre)

*2026-06-10 15:20 UTC*

Closing this — after checking with the Gonka community, I realized we don't need to run our own devshard. Getting a broker key to send requests through node4 will be enough for our case.
I'll likely open a separate issue requesting a broker key (or asking for documentation on how one can be obtained).
