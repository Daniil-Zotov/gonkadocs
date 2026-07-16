---
title: "#1371 — Request for DevShards creator allowlist access"
source: https://github.com/gonka-ai/gonka/issues/1371
issue_number: 1371
synced_at: 2026-07-16T09:32:46Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Request for DevShards creator allowlist access
    <span class="issues-number">#1371</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item">[@GERAunits](https://github.com/GERAunits) opened 2026-06-28 11:40 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-07-03 00:13 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Request to add my address to devshard_escrow_params.allowed_creator_addresses for a self-hosted gateway.

Address: gonka1a02jacrjca02f0805v9kpx0h2axjdfxx4vmwls
Pubkey: A3X9+ooArJ8UyJX1WpvhnH7JFBcU6OrbaQtYtUF0lcDX
Registration tx: D398545C1EDB469490EC07D2BF83D9854C3E376F88122EED90FE5B45FAD6D850 (block 4796580)
Balance: above min_amount

Operator: Pavel Gerasimov
GitHub: @GERAunits
Contact: gerasape@gmail.com

Models: Kimi K2.6 for programming and text processing tasks. Also interested in other available models.

Use case: personal self-hosted gateway for AI-assisted programming, code review, documentation, and text work. Low volume, no public endpoint, no resale.
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@tcharchian](https://github.com/tcharchian)</span>
    <span class="issues-meta-item">commented 2026-07-03 00:13 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi @GERAunits! Additions to <code>devshard_escrow_params.allowed_creator_addresses</code> happen only through on-chain governance — a param-change proposal or inclusion in a governance-approved upgrade batch. No maintainer adds an address unilaterally, so filing this issue registers your intent, but inclusion and timing are governance-dependent and not guaranteed.</p>
<p>Given your use case — personal, low-volume, no public endpoint, no resale — it's worth asking what running your own gateway actually buys you here. It gives you two things: paying for inference with your own GNK directly, with no third party holding a balance for you, and no operator between you and the network (relevant if you don't want anyone else seeing your code and documents in transit). In exchange you take on escrow funding, rotation, and settlement, plus the governance wait before any of it works.</p>
<p>If what you need is simply an OpenAI-compatible endpoint for AI-assisted coding and text work, that exists today. Community brokers are listed in the developer quickstart, and OpenBroker (https://openbroker.gonka.gg, discussion #1363) is a GNK-native option with no markup — it deducts your balance 1-to-1 with actual escrow cost, no enrollment or approval wait, and Kimi K2.6 is served there alongside the other network models. The honest trade-off is that it's custodial: you deposit GNK to an address the operator controls, and access runs under their API key. If self-custody or keeping your request content away from any intermediary is the reason you want your own gateway, that doesn't replace this request — say so and it stands as-is for governance consideration. If not, a managed endpoint will get you working today, and the operator path stays open if you want it later. </p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1371](https://github.com/gonka-ai/gonka/issues/1371) every hour.
