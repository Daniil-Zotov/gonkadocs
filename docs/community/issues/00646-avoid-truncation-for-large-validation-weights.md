---
title: "#646 — Avoid truncation for large validation weights"
source: https://github.com/gonka-ai/gonka/issues/646
issue_number: 646
synced_at: 2026-07-06T09:51:55Z
---

> 🔄 **Авто-синхронизация:** из [Issue #646](https://github.com/gonka-ai/gonka/issues/646) каждые 6 часов. 

# 🔴 Avoid truncation for large validation weights

**Автор:** [@x0152](https://github.com/x0152) · **Состояние:** Closed · **Создано:** 2026-01-26 18:10 UTC · **Обновлено:** 2026-06-02 17:54 UTC

**Веха:** v0.2.14

---

## 📝 Описание

#1101 

---

## 💬 Комментарии (1)

### Комментарий 1 — [@AlexeySamosadov](https://github.com/AlexeySamosadov)

*2026-02-08 14:14 UTC*

PR created: https://github.com/gonka-ai/gonka/pull/655

Fixes uint32 truncation for large validation weights by using int64.
