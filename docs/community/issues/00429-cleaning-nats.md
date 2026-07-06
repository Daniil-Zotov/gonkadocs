---
title: "#429 — Cleaning nats"
source: https://github.com/gonka-ai/gonka/issues/429
issue_number: 429
synced_at: 2026-07-06T09:53:26Z
---

> 🔄 **Авто-синхронизация:** из [Issue #429](https://github.com/gonka-ai/gonka/issues/429) каждые 6 часов. 

# 🔴 Cleaning nats

**Автор:** [@tcharchian](https://github.com/tcharchian) · **Состояние:** Closed · **Создано:** 2025-11-12 19:08 UTC · **Обновлено:** 2026-01-15 22:19 UTC

**Веха:** v0.2.6

---

## 📝 Описание

Problem with .nats queue being quite big
```
root@CL-Gonka1-NetNode:~/gonka/deploy/join# du -d1 -h .dapi/.nats
3.6G .dapi/.nats/jetstream
3.6G .dapi/.nats
```

Add some cleaning, maybe find a way to clean manually
