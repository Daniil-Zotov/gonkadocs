---
title: "#1397 — Gateway allowlist request"
source: https://github.com/gonka-ai/gonka/issues/1397
issue_number: 1397
synced_at: 2026-07-06T09:51:37Z
---

> 🔄 **Авто-синхронизация:** из [Issue #1397](https://github.com/gonka-ai/gonka/issues/1397) каждые 6 часов. 

# 🟢 Gateway allowlist request

**Автор:** [@yuritsin-code](https://github.com/yuritsin-code) · **Состояние:** Open · **Создано:** 2026-07-04 15:26 UTC · **Обновлено:** 2026-07-04 17:14 UTC

---

## 📝 Описание

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

---

## 💬 Комментарии (1)

### Комментарий 1 — [@yuritsin-code](https://github.com/yuritsin-code)

*2026-07-04 17:14 UTC*


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

