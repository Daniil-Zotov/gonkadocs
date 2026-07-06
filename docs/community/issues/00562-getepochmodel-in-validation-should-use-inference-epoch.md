---
title: "#562 — GetEpochModel in validation should use inference epoch"
source: https://github.com/gonka-ai/gonka/issues/562
issue_number: 562
synced_at: 2026-07-06T09:52:59Z
---

> 🔄 **Авто-синхронизация:** из [Issue #562](https://github.com/gonka-ai/gonka/issues/562) каждые 6 часов. 

# 🔴 GetEpochModel in validation should use inference epoch

**Автор:** [@x0152](https://github.com/x0152) · **Состояние:** Closed · **Создано:** 2026-01-15 10:00 UTC · **Обновлено:** 2026-02-06 00:58 UTC

**Веха:** v0.2.10

---

## 📝 Описание

Follow-up to #553. Line 68 uses GetEpochModel (current epoch) instead of GetEpochModelForEpoch(ctx, inference.EpochId, inference.Model)

---

## 💬 Комментарии (1)

### Комментарий 1 — [@DimaOrekhovPS](https://github.com/DimaOrekhovPS)

*2026-02-06 00:58 UTC*

Resolved with #545 
