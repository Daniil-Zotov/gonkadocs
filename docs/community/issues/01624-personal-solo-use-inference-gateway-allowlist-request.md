---
title: "#1624 — Personal / Solo-use Inference Gateway — Allowlist Request"
source: https://github.com/gonka-ai/gonka/issues/1624
issue_number: 1624
synced_at: 2026-08-27T09:58:39Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Personal / Solo-use Inference Gateway — Allowlist Request
    <span class="issues-number">#1624</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/AndreyVoenkov">@AndreyVoenkov</a> opened 2026-08-22 11:11 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-08-24 22:29 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Hello Gonka team,

I would like to request allowlisting for a **personal, self-hosted inference gateway**.

This gateway will be used exclusively for my own AI coding and development tasks. It will **not** be operated as a public broker and I do not intend to resell API access.

### Creator address

`gonka1gywfw6kud0rce4qavplur4r4cn9ugh4ffvpeav`

### Intended use

* Personal / solo-use inference gateway
* AI-assisted software development and coding
* OpenAI-compatible API for local coding tools
* Private, non-commercial usage
* No public API service
* No resale of Gonka inference
* Gateway API intended to be accessible locally only

### Environment

* Self-hosted gateway
* Docker
* Linux (Ubuntu 22.04 under WSL2)
* `inferenced` v0.2.15
* Windows 11 host

### Models

I am primarily interested in using:

* DeepSeek V4 Flash
* MiniMax M2.7
* Kimi K2.6

Please add the creator address above to `devshard_escrow_params.allowed_creator_addresses` for personal inference usage.

Thank you.
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-08-24 22:29 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi @AndreyVoenkov!</p>
<p>On the allowlist itself: additions to <code>devshard_escrow_params.allowed_creator_addresses</code> go through a governance-approved upgrade. Filing this issue registers intent, but timing and inclusion depend on governance and aren't guaranteed.</p>
<p>If what you actually need right now is just a personal OpenAI-compatible endpoint for AI-assisted coding, please look at comunity built service — OpenBroker (https://github.com/gonka-ai/gonka/discussions/1363, https://openbroker.gonka.gg). Open Broker is a GNK-native option with no markup — it deducts your balance 1-to-1 with actual escrow cost, supports streaming and function/tool calls, is drop-in OpenAI-compatible, and needs no enrollment or governance wait, so you'd be pointing your coding tools at it within minutes. </p>
<p>If you do try OpenBroker and something about it doesn't fit, please say so here. That feedback either helps improve OpenBroker or makes the case for why a self-hosted creator address is the right call for you.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1624](https://github.com/gonka-ai/gonka/issues/1624) every hour.
