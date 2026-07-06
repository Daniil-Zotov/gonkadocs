---
title: "#337 — [P1] Config update process"
source: https://github.com/gonka-ai/gonka/issues/337
issue_number: 337
synced_at: 2026-07-06T09:53:24Z
template: issues-main.html
---

> 🔄 **Авто-синхронизация:** из [Issue #337](https://github.com/gonka-ai/gonka/issues/337) каждые 6 часов. 

# 🔴 [P1] Config update process

**Автор:** [@tcharchian](https://github.com/tcharchian) · **Состояние:** Closed · **Создано:** 2025-09-03 23:19 UTC · **Обновлено:** 2026-01-15 23:10 UTC

**Веха:** v0.2.4

---

## 📝 Описание

- [x] The `node-config.json`, which contains the initial configuration, should not be applied automatically at the start — it should only be applied after an explicit command (otherwise, it creates a mess).
- [x] We need an `UPDATE nodes/:id` endpoint to modify node parameters, and some way to understand what exactly is being changed — so that a node’s status updates after the next PoC. Right now, when you delete and re-add a node, it results in chaos.

---

## 💬 Комментарии (1)

### Комментарий 1 — [@tcharchian](https://github.com/tcharchian)

*2026-01-15 23:10 UTC*

#390 #281 #240 
