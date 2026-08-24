---
title: "#1624 — Personal / Solo-use Inference Gateway — Allowlist Request"
source: https://github.com/gonka-ai/gonka/issues/1624
issue_number: 1624
synced_at: 2026-08-24T10:56:53Z
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
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-08-22 11:11 UTC</span>
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

> 🔄 **Auto-synced** from [Issue #1624](https://github.com/gonka-ai/gonka/issues/1624) every hour.
