---
title: "#1397 — Gateway allowlist request"
source: https://github.com/gonka-ai/gonka/issues/1397
issue_number: 1397
synced_at: 2026-07-24T06:42:44Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Gateway allowlist request
    <span class="issues-number">#1397</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/yuritsin-code">@yuritsin-code</a> opened 2026-07-04 15:26 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-07-08 00:51 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Operator

Victor Yuritsyn — independent operator
Contact: GitHub @yuritsin-code

## Address

gonka1calhwf505afx0aeeuzjsraw0y3wvak06gklee2

## Models

- MiniMaxAI/MiniMax-M2.7
- moonshotai/Kimi-K2.6

## Use case

We run production Telegram assistant bots (property management / supplier
ordering) with an async LLM cascade. Gonka currently serves our non-PII text
tier via a community broker; we already operate continuous canary monitoring
of network availability (30/60/120s backoff, circuit breaker with local
fallback) and would like to move to direct devshard escrow to pay inference
from our own GNK.

Expected volume is modest initially (thousands of requests/day ceiling),
growing with our bot fleet. Happy to share our availability telemetry with
the network if useful.
</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/yuritsin-code">@yuritsin-code</a></span>
    <span class="issues-meta-item">commented 2026-07-04 17:14 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi Gonka team,</p>
<p>We've been analyzing the devshard protocol to understand how multi-turn agent workloads perform on the network, and we have two questions based on our code review.</p>
<h3>1. Executor affinity for consecutive nonces</h3>
<p>We traced the routing logic in the open-source code:</p>
<ul>
<li><code>devshard/user/session.go:592</code>: <code>hostIdx := int(nonce % uint64(len(s.group)))</code></li>
<li><code>devshard/host/host.go:743</code>: <code>executorSlot := h.group[start.InferenceId%uint64(len(h.group))].SlotID</code></li>
<li><code>devshard/user/session.go:724</code>: <code>InferenceId: nonce</code></li>
</ul>
<p>This means each nonce is routed to <code>nonce % len(group)</code>, and since InferenceId == nonce, the target host IS the executor. Consecutive nonces are distributed round-robin across the group.</p>
<p><strong>Question:</strong> For multi-turn agent conversations where each turn is a new nonce, does the round-robin rotation mean that turns go to different executors (breaking KV-cache affinity), or is there a mechanism (group_size=1 for agent sessions, sticky routing, or a different code path) that keeps a conversation on the same executor?</p>
<h3>2. vLLM prefix caching status</h3>
<p>We reviewed the reference <code>node-config.json</code> files in <code>deploy/join/</code> and the participant quickstart docs. None include <code>--enable-prefix-caching</code>. Since vLLM 0.6.0+ requires this flag explicitly (it was default before), we cannot determine if prefix caching is active on Gonka nodes.</p>
<p><strong>Question:</strong> Is vLLM Automatic Prefix Caching enabled on Gonka inference nodes? What vLLM version does MLNode use?</p>
<p>Thanks for your time — this helps us understand the right strategy for deploying agent workloads on Gonka.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-07-08 00:51 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi @yuritsin-code. As with any <code>devshard_escrow_params.allowed_creator_addresses</code> change, this happens only through on-chain governance (a param-change proposal or a governance-approved upgrade batch) — filing the issue registers intent, but inclusion and timing are governance-dependent, not a maintainer toggle.</p>
<p>Your trace is right, and there is no hidden sticky path. </p>
<p>The group is not operator-selectable and there is no per-session / per-agent group_size. Slots are sampled on-chain at escrow creation (weighted-random by each participant's PoC validation weight for the model), sized to the governance parameter DevshardEscrowParams.GroupSize — currently 16. The creator can't pin members or force group_size=1.
The group is a verification/redundancy set, not a cache-affinity router. For each nonce exactly one slot executes (nonce % group); the others are verifiers that validate the result. Rotating the executor is intentional, so consecutive-turn KV/prefix-cache affinity is not a design goal today. The routing is determined entirely by the on-chain group + nonce, not by the gateway. So it is identical whether you stay on a community broker, use OpenBroker, or run your own devshard gateway — self-hosting will not buy you KV-cache affinity.</p>
<p>Given you're already in production and the goal is GNK-native, no-markup, self-paid inference, the option that works today without the governance wait is OpenBroker (https://openbroker.gonka.gg/, discussion #1363): it deducts your balance 1-to-1 with actual escrow cost (no markup, no enrollment/approval), and serves the network models.  </p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1397](https://github.com/gonka-ai/gonka/issues/1397) every hour.
