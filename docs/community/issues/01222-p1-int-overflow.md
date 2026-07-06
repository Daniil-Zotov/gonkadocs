---
title: "#1222 — [P1] Int overflow"
source: https://github.com/gonka-ai/gonka/issues/1222
issue_number: 1222
synced_at: 2026-07-06T09:51:42Z
---

> 🔄 **Авто-синхронизация:** из [Issue #1222](https://github.com/gonka-ai/gonka/issues/1222) каждые 6 часов. 

# 🟢 [P1] Int overflow

**Автор:** [@tcharchian](https://github.com/tcharchian) · **Состояние:** Open · **Создано:** 2026-05-21 22:30 UTC · **Обновлено:** 2026-06-30 13:00 UTC

**Метки:** `Priority: Medium`

**Веха:** v0.2.15

---

## 📝 Описание

The goal of this is to have in place after this a standard way of handling possible overflows, have it implemented consistently across the entire codebase and to have a check (preferably a static check, an AI persona if necessary as a backup) that flags anything that doesn't use the established pattern

---

## 💬 Комментарии (1)

### Комментарий 1 — [@olegsuhoparov](https://github.com/olegsuhoparov)

*2026-06-30 13:00 UTC*

Opened a surgical first PR against main: #1379.

It ports the already-accepted #1100/#1101 overflow fixes to main and adds two small guards for payout uint64->int64 conversion and validation totalWeight accumulation.

I intentionally left broad static analysis and #1017 supply-cap semantics out of scope so this remains reviewable.
