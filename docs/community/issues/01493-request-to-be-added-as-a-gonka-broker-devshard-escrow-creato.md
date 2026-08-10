---
title: "#1493 — Request to be added as a Gonka broker (devshard escrow creator allowlist)"
source: https://github.com/gonka-ai/gonka/issues/1493
issue_number: 1493
synced_at: 2026-08-10T06:45:42Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Request to be added as a Gonka broker (devshard escrow creator allowlist)
    <span class="issues-number">#1493</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/nikshh">@nikshh</a> opened 2026-07-21 13:07 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-07-22 13:51 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
```markdown
Hi Gonka core team & community,

Requesting inclusion of our escrow creator address in
`devshard_escrow_params.allowed_creator_addresses` to operate a
self-hosted devshard gateway.

## Escrow creator address

`gonka179ktce899cu28f666as7gqe3we638tv0fuhn4f`

(funded, pubkey published on-chain)

## About us

Operator: Nikita Shanin (sole proprietor; Chatbotiq — software development
studio). Contact: mr.shanin.nikitos@gmail.com / GitHub: nikshh.

## What we're building on Gonka

Internal AI coding agents (Telegram-based assistant products) consuming
inference for agentic coding loops — initially our own workloads
(~10–50M tokens/day), potentially broker access for our clients later.

We have already:
- tested the network as developers (community broker + signed direct requests
  with our own patched Windows build of gonka-openai);
- deployed the devshard gateway (`libermans/gonka-devshard-proxy`) on a
  dedicated GCP server — container healthy, chain-synced, waiting on allowlist;
- hold GNK for escrow funding (min_amount covered, rotation reserve planned).

## Models

moonshotai/Kimi-K2.6 (primary), MiniMaxAI/MiniMax-M2.7

## Infrastructure

Dedicated Linux server (GCP), Docker deployment, 24/7 monitoring
(Uptime Kuma). Gateway exposed via reverse proxy with TLS and bearer auth.

We understand inclusion is an on-chain governance decision with no guaranteed
timeline; meanwhile we'll run our workloads via OpenBroker. Filing this to
register intent per the process described in #1257/#1245.

Thanks!
```

</div>

---

> 🔄 **Auto-synced** from [Issue #1493](https://github.com/gonka-ai/gonka/issues/1493) every hour.
