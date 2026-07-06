---
title: "#976 — [P0] `devshards`: Distribute `WorkCoins` at the end of the epoch"
source: https://github.com/gonka-ai/gonka/issues/976
issue_number: 976
synced_at: 2026-07-06T09:52:17Z
---

> 🔄 **Авто-синхронизация:** из [Issue #976](https://github.com/gonka-ai/gonka/issues/976) каждые 6 часов. 

# 🔴 [P0] `devshards`: Distribute `WorkCoins` at the end of the epoch

**Автор:** [@dcastro](https://github.com/dcastro) · **Состояние:** Closed · **Создано:** 2026-03-30 11:10 UTC · **Обновлено:** 2026-04-21 23:43 UTC

**Метки:** `enhancement` `devshards`

**Веха:** v0.2.12

---

## 📝 Описание

As described in https://github.com/gonka-ai/gonka/issues/914#issuecomment-4090483233, we want to:

* Distribute `WorkCoins` at the end of the epoch, instead of upon settlement.
* Take `devshards` stats into account when 
    * calculating punishments `WorkCoins`/`RewardCoins` (see `bitcoin_rewards.go`)
    * participant's inactivity status (see `status.go` -> `ComputeStatus`)


---

## 💬 Комментарии (1)

### Комментарий 1 — [@tcharchian](https://github.com/tcharchian)

*2026-04-21 23:42 UTC*

Very close logic is implemented and merged in https://github.com/gonka-ai/gonka/pull/1087 & https://github.com/gonka-ai/gonka/pull/1069
