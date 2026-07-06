---
title: "#706 — Inference Slot Hogging"
source: https://github.com/gonka-ai/gonka/issues/706
issue_number: 706
synced_at: 2026-07-06T09:52:47Z
template: issues-main.html
---

> 🔄 **Авто-синхронизация:** из [Issue #706](https://github.com/gonka-ai/gonka/issues/706) каждые 6 часов. 

# 🟢 Inference Slot Hogging

**Автор:** [@huxuxuya](https://github.com/huxuxuya) · **Состояние:** Open · **Создано:** 2026-02-05 18:52 UTC · **Обновлено:** 2026-03-02 12:27 UTC

---

## 📝 Описание

**Vulnerability:** Inference Slot Hogging
**Severity:** Medium 
**Component:** model_assignment.go

### Description
The system always picks the node with the smallest weight for the "safe" inference slot. If a validator has multiple nodes, the same small node will keep getting the safe slot every single epoch, avoiding PoC verification indefinitely.

### The Problem
Verification Avoidance: The smallest node is never checked because it stays in the safe slot.
Guaranteed Rewards: This node earns rewards every epoch without risk, while the other nodes of the same validator are always forced to undergo PoC checks.

### Example
Validator has: Node A (weight 10) and Node B (weight 20).

Epoch 1: Node A is smallest -> Safe Slot.
Epoch 2: Node A is smallest -> Safe Slot.
Result: Node A never performs PoC, but always gets paid.

### Fix
A mandatory rotation. If a node was in the safe slot in the previous epoch, it is moved to the end of the queue for the next epoch. This forces the validator's other nodes to take turns in the safe slot and undergo verification.

---

## 💬 Комментарии (4)

### Комментарий 1 — [@AlexeySamosadov](https://github.com/AlexeySamosadov)

*2026-02-08 14:13 UTC*

PR created: https://github.com/gonka-ai/gonka/pull/718

Implements rotation logic to prevent the same node from always getting the safe inference slot.

### Комментарий 2 — [@AlexeySamosadov](https://github.com/AlexeySamosadov)

*2026-02-12 15:26 UTC*

I have a PR for this: #718 — implements deterministic rotation for PoC slot allocation to prevent hogging. Would appreciate a review when you get a chance.

### Комментарий 3 — [@huxuxuya](https://github.com/huxuxuya)

*2026-02-24 19:31 UTC*

 This task was created in parallel with this PR #707

### Комментарий 4 — [@huxuxuya](https://github.com/huxuxuya)

*2026-03-02 12:27 UTC*

Assign to me plz. Task already done.
#707 
