---
title: "#1321 — Gateway allowlist request"
source: https://github.com/gonka-ai/gonka/issues/1321
issue_number: 1321
synced_at: 2026-07-27T07:57:28Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Gateway allowlist request
    <span class="issues-number">#1321</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/bruev">@bruev</a> opened 2026-06-08 14:26 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-06-23 23:03 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
name: Andrei
company: Lunaro
project: Lunaro Gonka Gateway
github: @bruev
Gonka address: gonka1yfr6fcatj5hvx25ucy7uswwsdzdw7aql4uhug3
Models: Qwen/Qwen3-235B-A22B-Instruct-2507-FP8
Purpose: Self-hosted devshard gateway on the linux server



</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-06-23 23:03 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi @bruev!</p>
<p>To set expectations on the self-hosted path you asked for: running your own devshard gateway means becoming an on-chain escrow operator. Your <code>gonka1…</code> creator address has to be on the governance-controlled allowlist (<code>devshard_escrow_params.allowed_creator_addresses</code>) before it can open escrows, and you take on the operator side yourself — funding, rotating, and settling escrows, handling v1/v2 state roots, etc. That path stays fully open: inclusion is an on-chain governance decision (no single operator adds an address), so the way to pursue it is to request consideration via governance.  </p>
<p>If you'd rather not wait on a governance vote, there are independent, managed gateways in the community that already operate under whitelisted wallets and expose a plain OpenAI-compatible endpoint — so you can start now without your own allowlisting or enrollment. One such community option is <strong>OpenBroker</strong> (run by Gonka Labs) https://github.com/gonka-ai/gonka/discussions/1363</p>
<p>OpenBroker is <strong>independent third party</strong>, not part of the core protocol. </p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1321](https://github.com/gonka-ai/gonka/issues/1321) every hour.
