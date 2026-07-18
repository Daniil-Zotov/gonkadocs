---
title: "#1247 — Request to be added as a Gonka broker"
source: https://github.com/gonka-ai/gonka/issues/1247
issue_number: 1247
synced_at: 2026-07-18T09:50:03Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Request to be added as a Gonka broker
    <span class="issues-number">#1247</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/olkwwuah">@olkwwuah</a> opened 2026-05-26 07:27 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-06-23 23:10 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Hi Gonka team & community,

I'm requesting inclusion as a Gonka broker and inclusion of our address in the devshard creator allow-list.

Operator: Daniel
Contact: Discord @labdalab, Telegram @That_metalhead
Public URL: https://gonkadalab.com

About us:
We are a team building infrastructure around Gonka. We aim to help expand the ecosystem, attract new users, and provide practical tools and services that make Gonka easier to access and use.

Devshard creator address:
gonka15uuzwv36ln8mlsmu7ccg6rr3ntj9mh7t9x6n8u

Supported models:
Qwen/Qwen3-235B-A22B-Instruct-2507
moonshotai/Kimi-K2.6

Initial rate limits:
60 RPM per API key

Billing:
Crypto / GNK

Thanks,
Daniel
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-06-23 23:10 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi @olkwwuah!</p>
<p>Two parts to your ask — broker listing and allowlisting your devshard creator address — so a quick note on how each works:</p>
<p><strong>Allowlisting <code>gonka15uuzwv36ln8mlsmu7ccg6rr3ntj9mh7t9x6n8u</code>.</strong> Operating your own devshard gateway means becoming an on-chain escrow operator, which requires your creator address on the governance-controlled allowlist (<code>devshard_escrow_params.allowed_creator_addresses</code>). That path is open, but inclusion is an on-chain governance decision — no single operator or org adds an address unilaterally — so it goes through a governance request. On top of the allowlist, you'd own the escrow lifecycle yourself: funding, rotation, v1/v2 state roots, and settlement.</p>
<p><strong>Broker listing.</strong> The community broker directory is a curated, non-exhaustive set from the early rollout and isn't being actively expanded.</p>
<p>If you'd rather not wait on a governance vote, there are independent, managed gateways in the community that already operate under whitelisted wallets and expose a plain OpenAI-compatible endpoint — so you can start serving inference now without your own allowlisting. One such community option is <strong>OpenBroker</strong> (run by Gonka Labs): https://github.com/gonka-ai/gonka/discussions/1363</p>
<p>OpenBroker is <strong>independent third party</strong>, not part of the core protocol  </p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1247](https://github.com/gonka-ai/gonka/issues/1247) every hour.
