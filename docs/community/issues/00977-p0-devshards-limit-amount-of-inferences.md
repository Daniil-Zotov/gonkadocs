---
title: "#977 — [P0] `devshards`: Limit amount of inferences"
source: https://github.com/gonka-ai/gonka/issues/977
issue_number: 977
synced_at: 2026-07-06T09:51:56Z
---

> 🔄 **Авто-синхронизация:** из [Issue #977](https://github.com/gonka-ai/gonka/issues/977) каждые 6 часов. 

# 🔴 [P0] `devshards`: Limit amount of inferences

**Автор:** [@dcastro](https://github.com/dcastro) · **Состояние:** Closed · **Создано:** 2026-03-30 11:17 UTC · **Обновлено:** 2026-06-01 22:04 UTC

**Метки:** `enhancement` `devshards`

**Веха:** v0.2.13-devshard2

---

## 📝 Описание

As described in https://github.com/gonka-ai/gonka/issues/914#issuecomment-4090483233, we want to limit the amount of inferences that can be done in a `devshard`, as a way of limiting the amount of damage a hijacked `devshard` can cause on the network.

For now, let's say each `devshard` can run up to 2k inferences.

Upon settlement, the protocol should verify "Missed inferences + Invalidated inferences" does not exceed 2k, for the whole group.


---

## 💬 Комментарии (1)

### Комментарий 1 — [@a-kuprin](https://github.com/a-kuprin)

*2026-05-26 21:49 UTC*

At 0.2.13 nonce limit was introduced. Inference count could be limited by nonces limit and there is no need in extra parameter.
Handling on devshard side is implemented at https://github.com/gonka-ai/gonka/pull/1258 
