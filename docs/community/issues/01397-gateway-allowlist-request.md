---
title: "#1397 — Gateway allowlist request"
source: https://github.com/gonka-ai/gonka/issues/1397
issue_number: 1397
synced_at: 2026-07-07T04:27:54Z
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
    <span class="issues-meta-item">[@yuritsin-code](https://github.com/yuritsin-code) opened 2026-07-04 15:26 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-07-04 17:14 UTC</span>
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

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@yuritsin-code](https://github.com/yuritsin-code)</span>
    <span class="issues-meta-item">commented 2026-07-04 17:14 UTC</span>
  </div>
  <div class="issues-comment-body issues-content" markdown="1">
    
Hi Gonka team,

We've been analyzing the devshard protocol to understand how multi-turn agent workloads perform on the network, and we have two questions based on our code review.

### 1. Executor affinity for consecutive nonces

We traced the routing logic in the open-source code:

- `devshard/user/session.go:592`: `hostIdx := int(nonce % uint64(len(s.group)))`
- `devshard/host/host.go:743`: `executorSlot := h.group[start.InferenceId%uint64(len(h.group))].SlotID`
- `devshard/user/session.go:724`: `InferenceId: nonce`

This means each nonce is routed to `nonce % len(group)`, and since InferenceId == nonce, the target host IS the executor. Consecutive nonces are distributed round-robin across the group.

**Question:** For multi-turn agent conversations where each turn is a new nonce, does the round-robin rotation mean that turns go to different executors (breaking KV-cache affinity), or is there a mechanism (group_size=1 for agent sessions, sticky routing, or a different code path) that keeps a conversation on the same executor?

### 2. vLLM prefix caching status

We reviewed the reference `node-config.json` files in `deploy/join/` and the participant quickstart docs. None include `--enable-prefix-caching`. Since vLLM 0.6.0+ requires this flag explicitly (it was default before), we cannot determine if prefix caching is active on Gonka nodes.

**Question:** Is vLLM Automatic Prefix Caching enabled on Gonka inference nodes? What vLLM version does MLNode use?

Thanks for your time — this helps us understand the right strategy for deploying agent workloads on Gonka.

  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1397](https://github.com/gonka-ai/gonka/issues/1397) every hour.
