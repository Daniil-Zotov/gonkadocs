---
title: "#1824 — Gateway allowlist request"
source: https://github.com/gonka-ai/gonka/issues/1824
issue_number: 1824
synced_at: 2026-09-26T07:51:10Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Gateway allowlist request
    <span class="issues-number">#1824</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/samuelonn1993">@samuelonn1993</a> opened 2026-09-23 12:01 UTC</span>
    <span class="issues-meta-item">6 comments</span>
    <span class="issues-meta-item">Updated 2026-09-23 20:38 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
# Gateway allowlist request

## Operator

- Name: Samuel Onn
- GitHub: @samuelonn1993

## Creator address

`gonka1u54tux4u26vy9s207088v607a0kkjr9tgxsqdl`

Please consider adding this address to:

`devshard_escrow_params.allowed_creator_addresses`

## Intended models

- `MiniMaxAI/MiniMax-M2.7`
- `deepseek-ai/DeepSeek-V4-Flash-0731`
- `zai-org/GLM-5.3-Flash`

## Use case

Personal, private, single-user self-hosted gateway for my own AI-assisted software development.

The gateway will initially run locally on my own Windows PC and will be used on demand. It is not intended to operate as a public inference service or broker.

I will fund the creator address only after allowlist membership has been confirmed on-chain.
</div>

---

## 💬 Comments (6)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-09-23 18:20 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi @samuelonn1993!</p>
<p>Allowlisting is an on-chain governance decision, so this registers intent but timing/inclusion aren't guaranteed. Before waiting on that, one question, since it changes the fastest path: for personal, on-demand coding use, do you actually need to self-host?</p>
<p>If what you need is just a private OpenAI-compatible endpoint for your own AI-assisted development, that exists today via OpenBroker (https://github.com/gonka-ai/gonka/discussions/1363, https://openbroker.gonka.gg): GNK-native, no markup (1-to-1 with escrow cost), streaming + tool calls, no enrollment or governance wait — you'd be pointing your coding tools at it within minutes, and it fits on-demand use well since you only spend against actual usage.</p>
<p>If you try it and something doesn't fit, say so here. </p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/samuelonn1993">@samuelonn1993</a></span>
    <span class="issues-meta-item">commented 2026-09-23 18:56 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi @tcharchian </p>
<p>Thanks for the clarification.</p>
<p>Yes, I specifically want to self-host my own gateway. My goal is to run a private, single-user gateway for my own AI-assisted development, initially on my own Windows PC and potentially move it to my existing Linux VPS later.</p>
<p>The gateway would be used on demand for my own development and is not intended to operate as a public inference service or broker.</p>
<p>I understand that allowlisting is an on-chain governance decision and that timing and inclusion are not guaranteed. I am willing to wait for the governance process rather than use OpenBroker.</p>
<p>If my creator address is eventually added to the allowlist, is there any way I would be notified or informed that the request has been processed?</p>
<p>Thank you for registering the request.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-09-23 19:53 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>To be clear, though: this issue isn't a promise or a queue with a guaranteed outcome — it just records your intent. Allowlisting is an on-chain governance decision, so inclusion and timing aren't guaranteed. Worth knowing that, since it's governance, submitting a param-change proposal for <code>devshard_escrow_params.allowed_creator_addresses</code> is itself an option open to anyone — just so you're aware of the path, not something you have to do.</p>
<p>No automated notice when/if it lands (it's decentralized), so to track it: watch on-chain governance / upgrade release notes, or query <code>devshard_escrow_params.allowed_creator_addresses</code> directly any time.  </p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/samuelonn1993">@samuelonn1993</a></span>
    <span class="issues-meta-item">commented 2026-09-23 20:14 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Thanks for clarifying.</p>
<p>Just to make sure I understand the process correctly: is my current Issue #1824 request sufficient for my creator address to be considered for inclusion in the allowlist, or would I need to submit a formal governance proposal myself?</p>
<p>I understand that neither route guarantees inclusion; I just want to make sure I am using the right process.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-09-23 20:25 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Short answer: this issue is a valid way to register intent. But it's not the only route: since allowlisting is on-chain governance, you can always pursue it yourself directly — submitting a param-change proposal and building support for it in the community is an option open to anyone at any time. So you're not limited to waiting on a batch; you can drive the outcome through governance yourself if you prefer.</p>
<p>What helps your odds either way: visibility and contribution in the community, a track record/reputation, and more detail about your project and why the creator address matters for it. Concrete context — what you're building, how you'll use the gateway, and your engagement in Gonka Discord and other community chats makes an address much easier to include. None of that guarantees inclusion or timing, but it meaningfully strengthens the case.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/samuelonn1993">@samuelonn1993</a></span>
    <span class="issues-meta-item">commented 2026-09-23 20:38 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Thanks for clarifying. That makes sense.</p>
<p>I’ll keep my request on Issue #1824 for now and wait for the governance process. I’ll also monitor the on-chain allowlist for my creator address.</p>
<p>I appreciate the explanation.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1824](https://github.com/gonka-ai/gonka/issues/1824) every hour.
