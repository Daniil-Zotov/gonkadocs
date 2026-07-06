---
title: "#1219 — [P0] Basic primitives for training"
source: https://github.com/gonka-ai/gonka/issues/1219
issue_number: 1219
synced_at: 2026-07-06T09:51:46Z
---

> 🔄 **Авто-синхронизация:** из [Issue #1219](https://github.com/gonka-ai/gonka/issues/1219) каждые 6 часов. 

# 🟢 [P0] Basic primitives for training

**Автор:** [@tcharchian](https://github.com/tcharchian) · **Состояние:** Open · **Создано:** 2026-05-21 21:56 UTC · **Обновлено:** 2026-06-24 23:03 UTC

**Метки:** `Priority: High`

**Веха:** v0.2.15

---

## 📝 Описание

The framing is simple: you can prepare any container, it will run across different GPUs in the network, a protocol layer will coordinate interaction between nodes, they will perform training, and then use a protocol-level voting mechanism to determine which participants behaved correctly.

We intentionally ignore the automatic redeployment problem for now. 
This should be a small-scoped task on mainnet.
Put together a lightweight training flow without the heavy logic we have in devshards

---

## 💬 Комментарии (4)

### Комментарий 1 — [@x0152](https://github.com/x0152)

*2026-06-23 19:38 UTC*

Here's the draft plan and draft of the first-stage PR:

Plan (draft): https://docs.google.com/document/d/1LLZngQ7VoIL3DVT8St40XLE8HcRcxyNXZueyzoQfWuE/edit?tab=t.0
PR (stage 1): #1350 

Any help is welcome, from shaping the plan to implementation and reviews

### Комментарий 2 — [@orvionx](https://github.com/orvionx)

*2026-06-23 21:44 UTC*

Hi @mtvnastya , I’d like to help with this if there is still an open sub-scope.

My understanding is that this should be a lightweight mainnet training primitive, not a full devshards port: define/register a training workload, dispatch it to ML nodes, track basic execution state/result metadata, and leave redeployment/heavy orchestration out of scope.

I can start with a small PR around the training task/request model + API flow + minimal tests, then follow up with ML-node execution hooks if that direction works.

Could you confirm which part you’d prefer contributors to start with?

### Комментарий 3 — [@x0152](https://github.com/x0152)

*2026-06-24 22:54 UTC*

Hi @orvionx, I've already started working on this and opened a draft PR for the first stage: #1350. There's also a draft plan here: https://docs.google.com/document/d/1LLZngQ7VoIL3DVT8St40XLE8HcRcxyNXZueyzoQfWuE/edit?tab=t.0

I'd be happy if you could join. Could you take a look at the plan and share your thoughts? Stage 2 can be implemented in parallel with stage 1



### Комментарий 4 — [@orvionx](https://github.com/orvionx)

*2026-06-24 23:03 UTC*

Hi @x0152 Thanks for the mention — I’d be happy to join and help with this.

I reviewed the Stage 1 direction from PR #1350. My understanding is that Stage 1 mainly covers the on-chain reservation/release lifecycle, while Stage 2 can focus more on the actual training execution layer and coordination flow between reserved nodes.

My initial thoughts:

* Stage 2 should be kept clearly separated from Stage 1 by relying on stable interfaces/events from the reservation lifecycle.
* It would be useful to define the exact state machine for a training run: reserved → container prepared → training started → progress/heartbeat → result submitted → validation/voting → settled/released.
* I think we should pay special attention to failure handling: node timeout, container startup failure, partial participant failure, researcher cancellation, and result mismatch.
* For parallel development, I can work against mocked Stage 1 events/interfaces first, then wire it to the real chain implementation after Stage 1 stabilizes.
* I can also help with tests around edge cases and documentation for how hosts/researchers should use the flow.

I’ll continue reviewing the plan in more detail, but overall I agree that Stage 2 looks suitable to implement in parallel with Stage 1 if the interface boundary is defined clearly.

