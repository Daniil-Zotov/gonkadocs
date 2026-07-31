---
title: "#1431 — Operator name: Khidi — OpenAI-compatible API reseller service"
source: https://github.com/gonka-ai/gonka/issues/1431
issue_number: 1431
synced_at: 2026-07-31T07:18:44Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Operator name: Khidi — OpenAI-compatible API reseller service
    <span class="issues-number">#1431</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/jack-maguli">@jack-maguli</a> opened 2026-07-09 12:21 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-07-10 20:42 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Discord: jack.maguli 
Creator address to allow-list: gonka127szvy0fnscx03jjejmf6ednj6dezercldzzz4
Models we plan to serve: MiniMaxAI/MiniMax-M2.7, moonshotai/Kimi-K2.6, zai-org/GLM-5.2-FP8

Background: I was an early miner on Gonka (addresses gonka19djgy0erv0wddgynxafe787s25cj8c9evhzuuf, gonka1jprcfmj3x3uddc7tt9ha4zxk6kwy3y87cht4wf, gonka1cx4dkft2kzdzfjcuale2lw5cqaptdzgahwrj90). I'm now building a prepaid, USD and USDT billed API service targeting developers who have never heard of Gonka — bringing net-new inference demand to the network rather than redistributing existing users. Infrastructure is already deployed (Hetzner, LiteLLM billing layer, funded wallets); we're ready to run the official devshardctl gateway and open escrows as soon as the address is approved. Happy to provide any additional information. Initial go-to-market focus is Georgia and the wider Caucasus region — a developer market no existing Gonka broker serves, with local-language onboarding and regional payment habits (USDT-friendly) — expanding globally from there.
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-07-10 20:42 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi @jack-maguli, thanks for the detailed write-up. Good news: for what you're describing (a prepaid USD/USDT reseller on top of Gonka), you probably don't need to be allow-listed at all.</p>
<ul>
<li>Adding a creator address to <code>devshard_escrow_params.allowed_creator_addresses</code> happens only via governance vote — Gonka is a decentralized network, so there's no central team that grants it, and an issue like this registers interest but doesn't grant access or imply a timeline. </li>
<li>But you don't need that path to run Khidi. There's a community project, OpenBroker (https://github.com/gonka-ai/gonka/discussions/1363), built exactly for people who want to resell inference without whitelisting their own wallet or getting a broker key. It runs the devshard/escrow infra under an already-whitelisted wallet and exposes a plain OpenAI-compatible endpoint. From your side it's "register → deposit GNK → grab API key → point your OpenAI client at it".</li>
</ul>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1431](https://github.com/gonka-ai/gonka/issues/1431) every hour.
