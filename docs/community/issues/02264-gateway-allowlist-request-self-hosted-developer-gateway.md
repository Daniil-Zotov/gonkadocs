---
title: "#2264 — Gateway allowlist request - self-hosted developer gateway"
source: https://github.com/gonka-ai/gonka/issues/2264
issue_number: 2264
synced_at: 2026-11-13T08:08:01Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Gateway allowlist request - self-hosted developer gateway
    <span class="issues-number">#2264</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/jgfb9271-cyber">@jgfb9271-cyber</a> opened 2026-11-13 01:05 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-11-13 01:05 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Operator: jgfb9271-cyber.

Public contact: https://github.com/jgfb9271-cyber

Creator address: `gonka1sz6nmkhmafq654r27mh382glue8m448kad593p`

We request consideration for adding this dedicated escrow creator address to
`devshard_escrow_params.allowed_creator_addresses` on gonka-mainnet.

We have staged the official devshard gateway in an isolated deployment. We intend
to retain custody of the escrow keys and operate our own gateway and lifecycle,
including controlled concurrency and observability for coding-agent workloads.
This is why a fully managed OpenBroker gateway would not satisfy this setup.

Planned initial model: `MiniMaxAI/MiniMax-M2.7`.
Potential later models, after validation: `deepseek-ai/DeepSeek-V4-Flash-0731`
and `zai-org/GLM-5.3-Flash`.

The endpoint is currently private and staged; no funded escrow exists and no
public inference availability is claimed. Initial testing will use bounded
concurrency rather than claiming a guaranteed network capacity.

We understand that inclusion is a governance decision and that submitting this
request does not guarantee inclusion or a review timeline.

</div>

---

> 🔄 **Auto-synced** from [Issue #2264](https://github.com/gonka-ai/gonka/issues/2264) every hour.
