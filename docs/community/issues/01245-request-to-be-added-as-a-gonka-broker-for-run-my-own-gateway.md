---
title: "#1245 — Request to be added as a Gonka broker (for run my own gateway)"
source: https://github.com/gonka-ai/gonka/issues/1245
issue_number: 1245
synced_at: 2026-08-01T19:38:44Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Request to be added as a Gonka broker (for run my own gateway)
    <span class="issues-number">#1245</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/Korolev-Oleg">@Korolev-Oleg</a> opened 2026-05-25 13:27 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-06-23 23:17 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
**Operator name and contact (email or Discord handle).**
1kor.oleg@gmail.com 
@unixverse_cli

**Public endpoint URL of your gateway.**
no public endpoints because its for run own gateway purpose

**Gonka address you intend to use for devshard creation (gonka1...).**
https://note2.gonka.ai:8000
https://node4.gonka.ai

**Supported models and any rate limits you plan to enforce.**
`Qwen/Qwen3-235B-A22B-Instruct-2507`
`moonshotai/Kimi-K2.6`

**A brief description of your billing model (USD / crypto / credits) and target audience.**
experimental, develop an application 
but in future maybe in $T / credits
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-06-23 23:17 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi @Korolev-Oleg! Before anything can move on the self-hosted gateway side, the address field in the request needs fixing: <strong>Devshard creator address</strong> needs to be a <code>gonka1…</code> account address that you control (the one your gateway will sign escrow transactions from).  </p>
<p>On the path itself: running your own devshard gateway means becoming an on-chain escrow operator, which requires your <code>gonka1…</code> creator address on the governance-controlled allowlist (<code>devshard_escrow_params.allowed_creator_addresses</code>). That path is open, but inclusion is an on-chain governance decision — no single operator or org adds an address unilaterally — so it goes through a governance request.</p>
<p>If the goal right now is to build and test against Gonka rather than to operate escrows, there are independent, managed gateways in the community that already run under whitelisted wallets and expose a plain OpenAI-compatible endpoint — so you can start immediately without your own allowlisting. One such community option is <strong>OpenBroker</strong> (run by Gonka Labs): https://github.com/gonka-ai/gonka/discussions/1363</p>
<p>OpenBroker is <strong>independent third party</strong>, not part of the core protocol  </p>
<p>Links: https://openbroker.gonka.gg · https://openbroker.gonka.gg/stats · https://gonkalabs.com</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1245](https://github.com/gonka-ai/gonka/issues/1245) every hour.
