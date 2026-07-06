---
title: "#464 — Difficulty with PoC, defined by `RTarget`"
source: https://github.com/gonka-ai/gonka/issues/464
issue_number: 464
synced_at: 2026-07-06T09:53:25Z
---

> 🔄 **Авто-синхронизация:** из [Issue #464](https://github.com/gonka-ai/gonka/issues/464) каждые 6 часов. 

# 🔴 Difficulty with PoC, defined by `RTarget`

**Автор:** [@tcharchian](https://github.com/tcharchian) · **Состояние:** Closed · **Создано:** 2025-12-03 21:23 UTC · **Обновлено:** 2026-01-15 22:20 UTC

**Веха:** v0.2.6

---

## 📝 Описание

There is a difficulty with PoC, defined by `RTarget` in the repo. It essentially defines the percentage of "correct" nonces from all nonces => how many nonces participants has to check to find the correct one. 

Let's say we:
- increase complexity 
- add coefficient which transforn new weight to ~old weight (just to maintain same numbers in dashboard)

Please figure out how we're doing that. The open question - how we check which nodes were preserved, which are not, and which we preserved for > 1 epochs
=> to understand which weight to transform and which not 

There is some simple and elegant solution for that, e.g., use this coefficient at transforming len(nonces) -> weight
=> already transformed weight will be recorded in further preserved nodes

