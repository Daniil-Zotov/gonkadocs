---
title: "#1262 — Request to be added as a Gonka broker"
source: https://github.com/gonka-ai/gonka/issues/1262
issue_number: 1262
synced_at: 2026-07-07T20:18:33Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Request to be added as a Gonka broker
    <span class="issues-number">#1262</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item">[@anikiyevichm](https://github.com/anikiyevichm) opened 2026-05-27 16:11 UTC</span>
    <span class="issues-meta-item">5 comments</span>
    <span class="issues-meta-item">Updated 2026-06-27 01:27 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Hi Gonka Core Team and Community,
We would like to formally request the inclusion of the Gonka24 gateway in
the public broker list.
Gonka24 is being developed as a gateway focused on providing reliable
access to Gonka inference for both B2B users with existing inference
workloads and B2C users actively working with AI agents.
Operator name: Gonka24
Website: https://gonka24.com
Contact: gonka24support@gmail.com
Public gateway URL: https://api.gonka24.com/v1
Gonka address for devshard creation:
  gonka16msrxqwfedlll09hdwv0zmma6wttxx0wqqlt0y
Supported models:
  - Qwen/Qwen3-235B-A22B-Instruct-2507-FP8
  - moonshotai/Kimi-K2.6
Rate limits (default tier, per-instance counters on Cloud Run):
  Per source IP (enforced pre-auth):
    - 5 requests / second (burst window)
    - 60 requests / minute (sustained window)
  Per API key (enforced post-auth, applied to all /v1/* routes):
    - 30 requests / minute
    - 600 requests / hour
  Health probes and payment webhooks are exempt. Exceeding any window
  returns HTTP 429 in OpenAI-compatible format (type: "rate_limit_error")
  with a Retry-After header.
  For B2B customers, rate limits are flexible and negotiated per contract
  based on the expected workload.
Billing model:
  $0.05 per 1M tokens, flat across all supported models.
Payment methods:
  - Crypto (live, via NOWPayments)
  - Stripe (in progress)
Optional free fallback:
  Users can opt in to a last-resort OpenRouter free-tier fallback from
  their dashboard. When enabled, if both Gonka and the paid OpenRouter
  route fail, the request is routed to a free OpenRouter meta-model and
  the user is not charged for the response. Disabled by default.
Target audience:
  Our target audience includes both B2B and B2C segments.
    - B2B: companies that already have significant inference-related
      costs and are looking for a more efficient, scalable, and
      cost-effective way to run AI workloads.
    - B2C: users who actively use AI agents and need reliable, affordable
      access to inference for daily tasks, automation, and productivity.
</div>

---

## 💬 Comments (5)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@anikiyevichm](https://github.com/anikiyevichm)</span>
    <span class="issues-meta-item">commented 2026-05-28 14:54 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@tcharchian , Hi, i see that this issue is completed. What our team should do next to join allowlist with our gonka adress?</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@tcharchian](https://github.com/tcharchian)</span>
    <span class="issues-meta-item">commented 2026-06-23 22:47 UTC</span>
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
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@anikiyevichm](https://github.com/anikiyevichm)</span>
    <span class="issues-meta-item">commented 2026-06-24 07:42 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@tcharchian 
Hi, thanks for the clarification.</p>
<p>Our team is already going through the onboarding process with OpenBroker, and we appreciate this option as a practical way to start operating.</p>
<p>At the same time, we would still like to continue the discussion around being included in the official broker list, especially here: https://gonka.ai/docs/developer/quickstart/</p>
<p>The reason is that during conversations with potential customers, especially B2B clients and contractors, we are sometimes asked why our service is not listed there. This creates additional friction in sales and makes it harder for us to establish trust as a broker-side provider.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@anikiyevichm](https://github.com/anikiyevichm)</span>
    <span class="issues-meta-item">commented 2026-06-24 10:35 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>https://github.com/gonka-ai/gonka-docs/pull/1252 - We have prepared a PR</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@tcharchian](https://github.com/tcharchian)</span>
    <span class="issues-meta-item">commented 2026-06-27 01:27 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi @anikiyevichm, I wanted to raise a concern about the way your website is currently presented.
All footer links on the site point to the official Gonka channels and gonka.ai. Even the “Docs” link in the website header does not lead to your own documentation, but to the official Gonka docs on gonka.ai.
The site also lists Gonka’s audits and partners in a way that makes it look like those audits and partnerships apply to your service directly.</p>
<p>Overall, the website is structured and presented differently from other brokers’ websites, and I think it may be misleading for users. It creates the impression that this is an official Gonka website, or that Gonka’s official partners, audits, and documentation are associated with your broker specifically.</p>
<p>Could you please review this and adjust the website so that it is clearly positioned as an independent broker, with proper distinction from the official Gonka website and channels?</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1262](https://github.com/gonka-ai/gonka/issues/1262) every hour.
