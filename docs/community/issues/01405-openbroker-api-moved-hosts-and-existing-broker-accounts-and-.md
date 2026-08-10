---
title: "#1405 — OpenBroker API moved hosts and existing broker accounts (and balances) are gone — follow-up to #1319"
source: https://github.com/gonka-ai/gonka/issues/1405
issue_number: 1405
synced_at: 2026-08-10T21:05:51Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    OpenBroker API moved hosts and existing broker accounts (and balances) are gone — follow-up to #1319
    <span class="issues-number">#1405</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/dufok">@dufok</a> opened 2026-07-06 00:16 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-07-06 01:14 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Hi @tcharchian — follow-up to #1319, where you recommended OpenBroker as the official developer path ("GNK-settled, 1:1 at cost, no markup, no approval wait"). I took that advice, and I'm reporting what happened, because it will bite other developers onboarding the same way.

## What happened

I had an active OpenBroker account (email `stepan.vladovskiy@gmail.com`), activated with the standard **100 GNK deposit** from my on-chain wallet `gonka12wmxxm9l4ern8wcdpr4lr750km2l7l58stsvdt` (the same funded wallet from #1319). I was using it for MiniMax-M2.7 inference in my pipeline; total spend was a fraction of a GNK, so essentially the whole deposit should still be on the balance.

Recently, without any notice I could find:

1. The old API endpoint `https://openbroker.gonka.gg/v1` started returning **404** (the bare domain now serves only the dashboard site); the API answers on `https://api.openbroker.gonka.gg/v1`.
2. My existing `obk-…` key returns **401 "invalid API key"** on the new host.
3. "Reset password" sends me the 6-digit code by email, but submitting the form fails with **"no account found with this email"** — the account (and its balance) appears to be gone.
4. I could find no announcement about any of this on the site, the docs, or the dev blog — from the outside it just looks like the deposit vanished.

## Ask

- Restore my broker account (or credit the remaining balance to a fresh account, or refund it to the wallet above). I can prove ownership: the 100 GNK activation tx is visible on-chain from my wallet, and I can sign any challenge message with the wallet key.
- Consider a breaking-change / relaunch notice for OpenBroker onboarding — silent account resets on the officially recommended path undermine exactly the trust that path is supposed to provide.

I've also contacted Gonka Labs via their Telegram, but since OpenBroker has no public repo or issue tracker, and it's the path recommended here, this seemed like the right place for the public part of the report.

For context, I'm building on Gonka: a ComfyUI node pack for Gonka inference (https://github.com/dufok/GonkaAI-forComfyUI) — I'd like to keep GNK-settled inference as its default path.

</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/dufok">@dufok</a></span>
    <span class="issues-meta-item">commented 2026-07-06 01:04 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Resolved — Gonka Labs restored my broker account after I reached out via their Telegram (t.me/gonka_gg). Dashboard access is back, the wallet link is intact, and the balance was restored in full (topped up a little, even — appreciated).</p>
<p>For anyone hitting the same symptoms after the host change:
- the API now lives at <code>https://api.openbroker.gonka.gg/v1</code> (the bare domain serves only the dashboard);
- old <code>obk-…</code> keys are invalid — create a fresh one in the dashboard;
- if your login says "no account found", contact Gonka Labs with your linked wallet address — they sort it out quickly.</p>
<p>Thanks @tcharchian for the pointers in #1319, and thanks to the Gonka Labs team for the fast resolution. Closing.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/gonkalabs">@gonkalabs</a></span>
    <span class="issues-meta-item">commented 2026-07-06 01:09 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi, @dufok, thanks for pointing it out! </p>
<p>informing everyone that issue is solved and access is restored for the user. </p>
<p>This was caused by registration action happening during infrastructure migration and is not a subject for any more occurances in the future (<em>that was forced due to datacenter malfunction that required swift actions and full infra migration. All users who did complete the registration flow before migration - were moved correctly</em>). <strong>System is operational (including registrations)</strong>.</p>
<p>All updates and notices happen in our tg chat prior to changes. To mitigate all the potential miscommunications in the future, we will mirror notifications about breaking changes in discussion (if there will be any).</p>
<p>Thank You for being the early supporter of the Product 🤝</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1405](https://github.com/gonka-ai/gonka/issues/1405) every hour.
