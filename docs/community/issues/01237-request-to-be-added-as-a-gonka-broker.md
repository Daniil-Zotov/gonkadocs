---
title: "#1237 — Request to be added as a Gonka broker"
source: https://github.com/gonka-ai/gonka/issues/1237
issue_number: 1237
synced_at: 2026-07-06T09:51:51Z
---

> 🔄 **Авто-синхронизация:** из [Issue #1237](https://github.com/gonka-ai/gonka/issues/1237) каждые 6 часов. 

# 🔴 Request to be added as a Gonka broker

**Автор:** [@piterberkut](https://github.com/piterberkut) · **Состояние:** Closed · **Создано:** 2026-05-23 13:54 UTC · **Обновлено:** 2026-06-23 22:46 UTC

---

## 📝 Описание

Hi Gonka core team & community,

We're requesting inclusion of the OpenGonka gateway in the public broker
list 

Project: OpenGonka
Contact: [info@gonkakeeper.com](mailto:info@gonkakeeper.com) — Discord/Telegram: @piterberkut

About the team
OpenGonka is built by the same team behind
[GonkaKeeper](https://gonkakeeper.com/) — a native Gonka wallet
with a built-in AI chat. Through GonkaKeeper we already operate
against the live Gonka API on behalf of end users (key management,
signing, on-chain interactions, inference UX), so the broker is a
natural extension of work we're doing daily rather than a greenfield
project. The same operational team, monitoring stack, and on-call
rotation cover both products.

Endpoint

Public gateway URL: https://api.opengonka.com
OpenAI-compatible surface:

POST /v1/chat/completions (streaming supported)
GET  /v1/models
GET  /health, GET /ready

Auth — two modes:

Broker-managed keys — Authorization: Bearer gnk-sk-....
We hold the on-chain identity and sign on the user's behalf.
Client-signed passthrough — we forward native Gonka headers
(Authorization, X-Requester-Address, X-Timestamp) unchanged
when the client signs requests itself.


On-chain identity

Devshard creator address:
gonka1dxgk6x9xts7x34ssgrgqg34rwc2xq46ar5zxpt

Supported models

Qwen/Qwen3-235B-A22B-Instruct-2507
moonshotai/Kimi-K2.6 

OpenRouter is wired as a fallback in the same model family and is
engaged only when our health worker reports Gonka as unavailable. The
billing path makes the routing transparent to the user (see below).
Rate limits

Per source IP: 1 req/sec
Per X-Requester-Address: 30 req/min
Burst / abuse protection via Fastify rate-limit + Redis.
Per-API-key quotas are scheduled for the Hub milestone.

Billing

Accepted at launch: USDT, GNK-credits. Fiat USD planned for a
later milestone.
Markup: flat 10% over upstream cost.

We'll also participate in the on-chain governance vote and respond to
follow-up questions in this thread.
Thanks!
— OpenGonka (@piterberkut)

---

## 💬 Комментарии (2)

### Комментарий 1 — [@piterberkut](https://github.com/piterberkut)

*2026-05-28 18:43 UTC*

@tcharchian , Hi, i see that this issue is completed. What our team should do next to join allowlist with our gonka adress?

### Комментарий 2 — [@tcharchian](https://github.com/tcharchian)

*2026-06-23 22:46 UTC*

Hi! At the moment, the public broker list is not being actively expanded through governance. Inclusion in that list should be handled through the governance process and discussed in the community.

As a practical alternative, there is now a community-operated option for teams that want to start operating as brokers without waiting for direct access https://github.com/gonka-ai/gonka/discussions/1363.

OpenBroker provides access to Gonka inference through devshards v1 and v2 under an already whitelisted escrow-operating wallet. It is intended for teams that want to build or test broker-side products without handling escrow enrollment, escrow funding and rotation, v1/v2 state-root differences, or node4 access.

You can register here:
https://openbroker.gonka.gg/register

Endpoint:
https://openbroker.gonka.gg/v1

Stats:
https://openbroker.gonka.gg/stats

This should let you start while the governance discussion around inclusion/white-listing continues separately.
