---
title: "#1510 — Gateway allowlist request - Bagtyyar Kovusov"
source: https://github.com/gonka-ai/gonka/issues/1510
issue_number: 1510
synced_at: 2026-08-21T16:55:39Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Gateway allowlist request - Bagtyyar Kovusov
    <span class="issues-number">#1510</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/bagtyyarkovusov">@bagtyyarkovusov</a> opened 2026-07-27 20:18 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-08-19 20:34 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Operator information

- Operator name: Bagtyyar Kovusov
- Contact: Discord: key_b.official
- Devshard creator address: gonka1zsy3dqrc0h889u32jk40kl7hd2tugt0ymtfy7y
- Deployment region: China

## Intended gateway usage

- Models planned: moonshotai/Kimi-K2.6
- Use case: A self-hosted Gonka devshard gateway for OpenCode coding-agent inference, including streaming responses and function tool calls.
- Expected traffic: Initially low and variable personal-development traffic while testing OpenCode compatibility. Usage may increase after reliability and tool-calling behavior are validated; I do not yet have a reliable requests-per-day estimate.

I am requesting consideration for adding the creator address above to devshard_escrow_params.allowed_creator_addresses so I can fund and operate a self-hosted gateway and pay for inference directly through Gonka devshards.

I understand that inclusion requires an on-chain governance decision and that submitting this request does not guarantee approval or a timeline.
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-08-19 20:34 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi @key_b.official! Additions to <code>devshard_escrow_params.allowed_creator_addresses</code> go through a governance-approved upgrade — creator addresses get bundled into a batch by the maintainers/authors who assemble an upgrade, and that upgrade is ratified on-chain.  Running your own devshard gateway buys you two specific things: you settle inference in GNK yourself, and no operator sits in your request path. It also costs you the operator side — escrow funding, rotation, settlement — plus the governance wait before any of it works. If what you actually need right now is just a personal OpenAI-compatible endpoint to test OpenCode against <code>moonshotai/Kimi-K2.6</code>, that exists today with none of the above. Community members built OpenBroker (https://github.com/gonka-ai/gonka/discussions/1363, https://openbroker.gonka.gg), a GNK-native option with no markup — it deducts your balance 1-to-1 with actual escrow cost, supports streaming and function/tool calls, is drop-in OpenAI-compatible, and needs no enrollment or governance wait, so you'd be running OpenCode against it within minutes. The honest trade-off: it's custodial (you deposit GNK to an operator-controlled address and run under their API key). So if self-custody or full control of your request path is the actual reason you want your own gateway, OpenBroker doesn't replace this request and the allowlist path stands — but if the goal is simply "my own inference endpoint to validate OpenCode," it answers it completely and unblocks you today.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1510](https://github.com/gonka-ai/gonka/issues/1510) every hour.
