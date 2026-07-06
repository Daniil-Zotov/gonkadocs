---
title: "#343 — BUG-3: Removing models from inference/model_list is not supported"
source: https://github.com/gonka-ai/gonka/issues/343
issue_number: 343
synced_at: 2026-07-06T09:53:05Z
template: issues-main.html
---

> 🔄 **Авто-синхронизация:** из [Issue #343](https://github.com/gonka-ai/gonka/issues/343) каждые 6 часов. 

# 🔴 BUG-3: Removing models from inference/model_list is not supported

**Автор:** [@gmorgachev](https://github.com/gmorgachev) · **Состояние:** Closed · **Создано:** 2025-09-05 07:31 UTC · **Обновлено:** 2026-01-28 22:26 UTC

---

## 📝 Описание

Fix the bug in network inference API where sending a request with an unsupported model name incorrectly returns the error 402 Insufficient balance.
