---
title: "#899 — [P0] `devshards`: Add end-to-end inference validation tests"
source: https://github.com/gonka-ai/gonka/issues/899
issue_number: 899
synced_at: 2026-07-06T09:52:24Z
---

> 🔄 **Авто-синхронизация:** из [Issue #899](https://github.com/gonka-ai/gonka/issues/899) каждые 6 часов. 

# 🔴 [P0] `devshards`: Add end-to-end inference validation tests

**Автор:** [@heitor-lassarote](https://github.com/heitor-lassarote) · **Состояние:** Closed · **Создано:** 2026-03-16 18:50 UTC · **Обновлено:** 2026-04-07 16:10 UTC

**Метки:** `Priority: High` `devshards`

**Веха:** v0.2.12

---

## 📝 Описание

We should write testermint tests to ensure that inference validations in `devshards` work as expected. Such tests already exist for mainnet, but we should reimplement them according to the `devshards` design and implementation.

---

## 💬 Комментарии (3)

### Комментарий 1 — [@heitor-lassarote](https://github.com/heitor-lassarote)

*2026-03-19 17:46 UTC*

Note: I took a little detour from this task to see if I can make the development loop with testermint a bit quicker, by writing a small REPL to interact with the `devshard`.

### Комментарий 2 — [@KKizilov](https://github.com/KKizilov)

*2026-03-26 15:14 UTC*

Will be done by March 27th.

### Комментарий 3 — [@heitor-lassarote](https://github.com/heitor-lassarote)

*2026-03-26 15:31 UTC*

I've written a couple of Testermint tests and added an endpoint to get the inference from the proxy server.

Recently I've been trying to see about changing the session configuration for tests. Although not sure yet if that's the best path forward.

I expect to push a PR with these tests very soon.
