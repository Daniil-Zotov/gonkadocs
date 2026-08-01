---
title: "#1385 — Gateway allowlist request - dev server personal gateway"
source: https://github.com/gonka-ai/gonka/issues/1385
issue_number: 1385
synced_at: 2026-08-01T17:26:20Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Gateway allowlist request - dev server personal gateway
    <span class="issues-number">#1385</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/scodeit">@scodeit</a> opened 2026-07-01 16:41 UTC</span>
    <span class="issues-meta-item">3 comments</span>
    <span class="issues-meta-item">Updated 2026-07-10 21:03 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Operator
- Name: Viacheslav Nikitin
- Contact: via GitHub issue replies

## Intended creator address
`gonka1qh620unjez7552csz9mklhjjtl9p7ty5vpznag`

## Models to serve
- MiniMaxAI/MiniMax-M2.7
- (optional later) moonshotai/Kimi-K2.6

## Setup context
- Self-hosted gateway-only deployment on private VPS
- Docker image: `libermans/gonka-devshard-proxy:latest`
- API bound to localhost only (`127.0.0.1:18080`)
- Personal / solo-use inference gateway (not a public broker)

## Funding
Creator address will be funded with native GNK for escrow deposits once allowlisted.

Please consider adding this address to `devshard_escrow_params.allowed_creator_addresses`.
</div>

---

## 💬 Comments (3)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-07-03 00:09 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi @scodeit!</p>
<p>On the allowlist itself: additions to <code>devshard_escrow_params.allowed_creator_addresses</code> happen only through on-chain governance — either a standalone param-change proposal or inclusion in a governance-approved upgrade batch. No maintainer adds an address unilaterally. Filing this issue is the right way to register intent, but inclusion and timing are governance-dependent and not guaranteed, so I want to set expectations honestly rather than leave this sitting as an implied "pending approval."</p>
<p>Before that though, one question worth asking, because it changes what the fastest path is for you. Your stated use case is a personal, solo-use gateway — not a public broker. Running your own devshard gateway buys you two specific things: you pay for inference with your own GNK directly (no third party holding a balance for you), and no operator sits between you and the network. It also costs you the operator side: escrow funding, rotation, settlement, and the governance wait before any of it works.</p>
<p>If what you actually need is just a personal OpenAI-compatible endpoint, that exists today without any of the above. Community brokers are listed in the developer quickstart, and OpenBroker (https://openbroker.gonka.gg, https://github.com/gonka-ai/gonka/discussions/1363) is a GNK-native option with no markup — it deducts your balance 1-to-1 with actual escrow cost, no enrollment or approval wait, and you'd be sending requests within minutes. The honest trade-off: it's custodial (you deposit GNK to an address the operator controls, access runs under their API key), so if self-custody or full control over your request path is the reason you want your own gateway, it doesn't replace this allowlist request — but if the goal is simply "my own inference endpoint for personal use," it answers it completely.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/scodeit">@scodeit</a></span>
    <span class="issues-meta-item">commented 2026-07-03 19:06 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi @tcharchian ! </p>
<p>Thanks for the explanation.</p>
<p>I did look at OpenBroker, but it's not really what I'm trying to build.</p>
<p>The main reason for requesting a creator address is that I don't want an intermediary between my infrastructure and the network. I prefer to operate my own gateway, manage my own escrow, and keep the entire request path under my control.</p>
<p>Right now this is for personal use, but it's also part of a longer-term evaluation. I'm building and experimenting with AI agent systems, automation pipelines, and integrations around the metarhia ecosystem. One of the projects involves trading-related automation, where I want to understand how Gonka behaves in real workloads before deciding whether to build on top of it.</p>
<p>My interest isn't simply reselling inference or adding a margin on top of token usage. I'm interested in building products that create additional value through the services they provide—automation, orchestration, agent workflows, integrations, and domain-specific functionality. In that model, inference is only one component of a larger system, not the product itself.</p>
<p>Running my own gateway would also allow me to evaluate the network under real production-like workloads and provide practical feedback whenever I encounter issues, limitations, or opportunities for improvement. I expect that kind of hands-on experience to be more useful than testing through a broker.</p>
<p>If the platform proves to be a good fit, I'd also be interested in running a gateway for others in the future. I'd rather learn how to operate the full stack now than start with a broker and redesign everything later.</p>
<p>I understand that the allowlist is controlled through governance and that there's no guarantee or fixed timeline. That's completely fine. I just wanted to register my interest so the address can be considered whenever the next proposal is put together.</p>
<p>Thanks again for taking the time to explain the process.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-07-10 21:03 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi @scodeit. Your intent is registered. The strongest thing you can do while you wait is be visible in the community. Governance proposals are discussed and gain support in the community channels (Discord/Telegram). Sharing what you're building and gaining support increases your chances of being approved by governance.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1385](https://github.com/gonka-ai/gonka/issues/1385) every hour.
