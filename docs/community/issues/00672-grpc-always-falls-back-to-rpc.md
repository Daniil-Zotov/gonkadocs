---
title: "#672 — gRPC always falls back to RPC"
source: https://github.com/gonka-ai/gonka/issues/672
issue_number: 672
synced_at: 2026-07-06T09:52:50Z
template: issues-main.html
---

> 🔄 **Авто-синхронизация:** из [Issue #672](https://github.com/gonka-ai/gonka/issues/672) каждые 6 часов. 

# 🟢 gRPC always falls back to RPC

**Автор:** [@x0152](https://github.com/x0152) · **Состояние:** Open · **Создано:** 2026-01-30 16:21 UTC · **Обновлено:** 2026-02-12 15:26 UTC

---

## 📝 Описание

gRPC is enabled, but requests still use RPC (#685 )

---

## 💬 Комментарии (2)

### Комментарий 1 — [@AlexeySamosadov](https://github.com/AlexeySamosadov)

*2026-02-08 14:13 UTC*

PR created: https://github.com/gonka-ai/gonka/pull/694

Enables gRPC for chain queries instead of RPC fallback.

### Комментарий 2 — [@AlexeySamosadov](https://github.com/AlexeySamosadov)

*2026-02-12 15:26 UTC*

I have a PR for this: #694 — adds optional gRPC transport for chain queries. Would appreciate a review when you get a chance.
