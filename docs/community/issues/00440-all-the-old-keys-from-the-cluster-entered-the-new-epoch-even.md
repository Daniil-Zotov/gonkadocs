---
title: "#440 — All the old keys from the cluster entered the new epoch, even though that cluster was deleted"
source: https://github.com/gonka-ai/gonka/issues/440
issue_number: 440
synced_at: 2026-07-06T09:53:02Z
---

> 🔄 **Авто-синхронизация:** из [Issue #440](https://github.com/gonka-ai/gonka/issues/440) каждые 6 часов. 

# 🔴 All the old keys from the cluster entered the new epoch, even though that cluster was deleted

**Автор:** [@tcharchian](https://github.com/tcharchian) · **Состояние:** Closed · **Создано:** 2025-11-17 20:12 UTC · **Обновлено:** 2026-01-29 05:48 UTC

**Веха:** v0.2.5

---

## 📝 Описание

All the old keys from the cluster entered the new epoch, even though that cluster was deleted about six hours ago. For some reason, they passed the PoC with a small weight, but it still looks like they shouldn’t have appeared there at all.

The cluster was shut down and the warm keys were deleted.
fs was completely deleted

![Image](https://github.com/user-attachments/assets/de21696d-5fdd-4020-b212-50f44f282e93)
