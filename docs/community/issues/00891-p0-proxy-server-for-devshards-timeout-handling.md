---
title: "#891 — [P0] Proxy server for `devshards`: timeout handling"
source: https://github.com/gonka-ai/gonka/issues/891
issue_number: 891
synced_at: 2026-07-06T09:52:27Z
---

> 🔄 **Авто-синхронизация:** из [Issue #891](https://github.com/gonka-ai/gonka/issues/891) каждые 6 часов. 

# 🔴 [P0] Proxy server for `devshards`: timeout handling

**Автор:** [@dcastro](https://github.com/dcastro) · **Состояние:** Closed · **Создано:** 2026-03-16 13:45 UTC · **Обновлено:** 2026-04-01 03:20 UTC

**Метки:** `devshards`

**Веха:** v0.2.12

---

## 📝 Описание

At the moment, the proxy server in `/subnet/cmd/subnetctl` handles 3 types of actions: chat completions (with diff propagation), finalizing `devshards`, and querying the `devshards` status.

It should also handle timeout-related mechanisms.

---

## 💬 Комментарии (2)

### Комментарий 1 — [@dcastro](https://github.com/dcastro)

*2026-03-20 08:35 UTC*

Closed in favor of #911

### Комментарий 2 — [@tcharchian](https://github.com/tcharchian)

*2026-03-20 22:41 UTC*

@gmorgachev, you wanted to include this issue in the upgrade v0.2.12. Does https://github.com/gonka-ai/gonka/pull/911 cover everything you expected here?
