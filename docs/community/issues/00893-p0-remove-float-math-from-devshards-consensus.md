---
title: "#893 — [P0] Remove float math from `devshards` consensus"
source: https://github.com/gonka-ai/gonka/issues/893
issue_number: 893
synced_at: 2026-07-06T09:52:06Z
template: issues-main.html
---

> 🔄 **Авто-синхронизация:** из [Issue #893](https://github.com/gonka-ai/gonka/issues/893) каждые 6 часов. 

# 🔴 [P0] Remove float math from `devshards` consensus

**Автор:** [@Brgndy25](https://github.com/Brgndy25) · **Состояние:** Closed · **Создано:** 2026-03-16 13:52 UTC · **Обновлено:** 2026-04-29 21:44 UTC

**Метки:** `Priority: High` `devshards`

**Веха:** v0.2.12

---

## 📝 Описание

DeterministicFloat, ShouldValidate, and penalizeUnrevealedSeeds use float64 and math.Ceil. 

Floating-point arithmetic is not deterministicacross architectures and can produce different results on different
machines, which can lead to state root divergence and consensus splits.


---

## 💬 Комментарии (1)

### Комментарий 1 — [@KKizilov](https://github.com/KKizilov)

*2026-03-26 15:17 UTC*

Will be done by March 27th. 
