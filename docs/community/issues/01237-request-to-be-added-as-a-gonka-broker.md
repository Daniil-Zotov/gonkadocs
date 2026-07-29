---
title: "#1237 — Request to be added as a Gonka broker"
source: https://github.com/gonka-ai/gonka/issues/1237
issue_number: 1237
synced_at: 2026-07-29T03:45:32Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Request to be added as a Gonka broker
    <span class="issues-number">#1237</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/piterberkut">@piterberkut</a> opened 2026-05-23 13:54 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-06-23 22:46 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
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
</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/piterberkut">@piterberkut</a></span>
    <span class="issues-meta-item">commented 2026-05-28 18:43 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@tcharchian , Hi, i see that this issue is completed. What our team should do next to join allowlist with our gonka adress?</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-06-23 22:46 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi! At the moment, the public broker list is not being actively expanded through governance. Inclusion in that list should be handled through the governance process and discussed in the community.</p>
<p>As a practical alternative, there is now a community-operated option for teams that want to start operating as brokers without waiting for direct access https://github.com/gonka-ai/gonka/discussions/1363.</p>
<p>OpenBroker provides access to Gonka inference through devshards v1 and v2 under an already whitelisted escrow-operating wallet. It is intended for teams that want to build or test broker-side products without handling escrow enrollment, escrow funding and rotation, v1/v2 state-root differences, or node4 access.</p>
<p>You can register here:
https://openbroker.gonka.gg/register</p>
<p>Endpoint:
https://openbroker.gonka.gg/v1</p>
<p>Stats:
https://openbroker.gonka.gg/stats</p>
<p>This should let you start while the governance discussion around inclusion/white-listing continues separately.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1237](https://github.com/gonka-ai/gonka/issues/1237) every hour.
