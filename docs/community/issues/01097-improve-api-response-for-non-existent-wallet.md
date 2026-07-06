---
title: "#1097 — Improve API response for non-existent wallet"
source: https://github.com/gonka-ai/gonka/issues/1097
issue_number: 1097
synced_at: 2026-07-06T09:52:15Z
---

> 🔄 **Авто-синхронизация:** из [Issue #1097](https://github.com/gonka-ai/gonka/issues/1097) каждые 6 часов. 

# 🔴 Improve API response for non-existent wallet

**Автор:** [@tcharchian](https://github.com/tcharchian) · **Состояние:** Closed · **Создано:** 2026-04-21 19:47 UTC · **Обновлено:** 2026-04-22 22:21 UTC

---

## 📝 Описание

When querying a non-existent wallet via `GET https://node3.gonka.ai/v1/participants/{address}` the API currently returns a 500 Internal Server Error.

Expected Behavior
If the wallet is not found, the API should return `404 Not Found` instead of 500

Rationale
A missing wallet is a valid client-side case, not a server error. Returning 404 improves API correctness and makes error handling more predictable for clients.

---

## 💬 Комментарии (1)

### Комментарий 1 — [@tcharchian](https://github.com/tcharchian)

*2026-04-22 22:21 UTC*

https://github.com/gonka-ai/gonka/pull/750
