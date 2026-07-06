---
title: "#315 — [P0] Move config to DB (like seed, etc)"
source: https://github.com/gonka-ai/gonka/issues/315
issue_number: 315
synced_at: 2026-07-06T09:53:28Z
---

> 🔄 **Авто-синхронизация:** из [Issue #315](https://github.com/gonka-ai/gonka/issues/315) каждые 6 часов. 

# 🔴 [P0] Move config to DB (like seed, etc)

**Автор:** [@tcharchian](https://github.com/tcharchian) · **Состояние:** Closed · **Создано:** 2025-09-03 22:44 UTC · **Обновлено:** 2026-01-15 22:00 UTC

**Веха:** v0.2.4

---

## 📝 Описание

- [ ] The `api-config.yml` file often goes missing, and this part is needs to be rewritten: https://github.com/gonka-ai/gonka/blob/bacddd41f257b459d85b04786bee06b49a084dff/decentralized-api/apiconfig/config_manager.go#L302
- [ ] The `api-config` should be split into two parts:
      - a static configuration file
      - some kind of state (either in MySQL or a JSON file, but one that is updated strictly atomically). Consider leaning toward using MySQL right away, as it remains a standard and straightforward option, yet allows for the safe storage of as much data as needed. For debugging, a human-readable export is fine.
