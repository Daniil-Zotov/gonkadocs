---
title: "#611 — [zpoken] Define and validate scalable off-chain PoC communication beyond Merkle-based commits"
source: https://github.com/gonka-ai/gonka/issues/611
issue_number: 611
synced_at: 2026-07-06T09:52:15Z
---

> 🔄 **Авто-синхронизация:** из [Issue #611](https://github.com/gonka-ai/gonka/issues/611) каждые 6 часов. 

# 🟢 [zpoken] Define and validate scalable off-chain PoC communication beyond Merkle-based commits

**Автор:** [@tcharchian](https://github.com/tcharchian) · **Состояние:** Open · **Создано:** 2026-01-20 21:32 UTC · **Обновлено:** 2026-04-23 01:38 UTC

---

## 📝 Описание

**Problem**
The Merkle tree–based off-chain PoC commit approach is already being implemented as an urgent, short-term solution. 

- https://github.com/gonka-ai/gonka/blob/dl/v0.2.8-poc-v2-offchain/proposals/poc-v2/poc-v2-offchain.md
- https://github.com/gonka-ai/gonka/blob/gm/poc-offchain/proposals/poc/offchain.md

However, it is understood that this approach does not scale to large participant counts on its own.

Because of this, a second approach https://zpoken.notion.site/Andrii-2ea9506ab1488027b6d5e72df66d8654 is proposed as a scalability solution

**Goal**
Formally define, evaluate, and validate the Mesh / Turbine-based off-chain PoC communication approach as the scalable solution, given that Merkle-based commits are already accepted as a non-scalable but necessary interim step.


---

## 💬 Комментарии (1)

### Комментарий 1 — [@akup](https://github.com/akup)

*2026-01-23 11:21 UTC*

Why gossip is just overlooked?

While it will have more latency (this 100ms are neglectable compared to block finalization time), it consumes much less resources and bandwidth.
In article, in comparison it is stated that gossip needs 12 connections, while turbine tree 32 connections.
But to have good protection against nodes control attack, we need to have up to 8 trees, and this is 256 connections, that is 20 times more then gossip.
This multiple connections even with Solomon-reed (additional encoding/decoding resources) will increase bandwidth consumption as well.
Moreover gossip is more adaptive and selfheeling and always will find the route.

I think this points should be taken into account on protocol selection
