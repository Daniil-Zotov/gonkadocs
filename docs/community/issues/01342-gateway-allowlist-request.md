---
title: "#1342 — Gateway allowlist request"
source: https://github.com/gonka-ai/gonka/issues/1342
issue_number: 1342
synced_at: 2026-07-14T23:14:59Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Gateway allowlist request
    <span class="issues-number">#1342</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item">[@appgencore](https://github.com/appgencore) opened 2026-06-13 07:39 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-06-23 22:52 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Hi Gonka team,

Requesting to join the Gateway allowlist.
We are a bootstrapped startup studio building AI agents and automation tools. We are exploring decentralized AI infrastructure and would like to run inference directly on Gonka via a self-hosted gateway, paying GNK on-chain per request, rather than going through a third-party broker.

Operator: Den
Contact Discord: gendevik
GitHub: appgencore

Gonka creator address:
gonka1cavsfewz9jrgqxeh5u55y37qxevyueglddtl63

Models planned:
moonshotai/Kimi-K2.6
Qwen/Qwen3-235B-A22B-Instruct-2507-FP8
MiniMaxAI/MiniMax-M2.7

Purpose:
Initial usage will be low-volume and private/internal only. Our goal is to understand the protocol, test the developer experience, and evaluate what products could be built on top of Gonka.
We want to validate the full self-hosted flow end to end: devshard escrow creation, OpenAI-compatible API calls, inference reliability, settlement, and direct on-chain GNK payments.

If local validation works well, we may later submit a separate public broker request with a final project name, public endpoint, rate limits, billing model, and rollout plan.

Thanks!
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@tcharchian](https://github.com/tcharchian)</span>
    <span class="issues-meta-item">commented 2026-06-23 22:52 UTC</span>
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

> 🔄 **Auto-synced** from [Issue #1342](https://github.com/gonka-ai/gonka/issues/1342) every hour.
