---
title: "#896 — `devshards`: Research aggregated BLS signatures"
source: https://github.com/gonka-ai/gonka/issues/896
issue_number: 896
synced_at: 2026-07-06T09:52:07Z
---

> 🔄 **Авто-синхронизация:** из [Issue #896](https://github.com/gonka-ai/gonka/issues/896) каждые 6 часов. 

# 🟢 `devshards`: Research aggregated BLS signatures

**Автор:** [@heitor-lassarote](https://github.com/heitor-lassarote) · **Состояние:** Open · **Создано:** 2026-03-16 15:10 UTC · **Обновлено:** 2026-04-29 21:30 UTC

**Метки:** `Priority: Low` `devshards`

---

## 📝 Описание

Currently, the design for `devshards` requests a list of all hosts signatures for the settlement transaction. To reduce the transaction size, we'd like to investigate and implement an aggregated BLS signature (plus a bitset for which hosts signed).

To achieve this, one solution is to register the BLS `devshard` public key for each participant in the mainnet.

# Research

* [Applicability of Aggregated BLS Signatures](https://serokell.notion.site/Applicability-of-Aggregated-BLS-Signatures-31a6c9c166b380b49068d5574277dfd8)

---

## 💬 Комментарии (2)

### Комментарий 1 — [@KKizilov](https://github.com/KKizilov)

*2026-03-26 15:16 UTC*

Will be done fast after finishing #913 

### Комментарий 2 — [@tcharchian](https://github.com/tcharchian)

*2026-04-29 21:15 UTC*

postpone review after Upgrade v0.x.x-devshard2
