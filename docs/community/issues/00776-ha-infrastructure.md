---
title: "#776 — HA infrastructure"
source: https://github.com/gonka-ai/gonka/issues/776
issue_number: 776
synced_at: 2026-07-06T09:52:45Z
---

> 🔄 **Авто-синхронизация:** из [Issue #776](https://github.com/gonka-ai/gonka/issues/776) каждые 6 часов. 

# 🔴 HA infrastructure

**Автор:** [@Laboltus](https://github.com/Laboltus) · **Состояние:** Closed · **Создано:** 2026-02-18 09:41 UTC · **Обновлено:** 2026-03-03 23:52 UTC

---

## 📝 Описание

I'm trying to figure out how to create a highly available node. My understanding at the time is following
1. Full-node can be started in multiple instances and we can use some LB for balance and failover
2. Validator - with tmkms we can have only one active validator to avoid double-sign. For multiple active validators we need to adapt horcrux
3. Decentralized API - There can only be one active instance, and we should use custom scripts to synchronize SQLite database from the active instance to the standby one.

Am I right ? Is there some guide on this that I missed ?

---

## 💬 Комментарии (1)

### Комментарий 1 — [@blizko](https://github.com/blizko)

*2026-03-03 08:44 UTC*

This topic is raised as discussion https://github.com/gonka-ai/gonka/discussions/837
