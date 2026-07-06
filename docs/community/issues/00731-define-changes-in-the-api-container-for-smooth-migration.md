---
title: "#731 — Define changes in the API container for smooth migration"
source: https://github.com/gonka-ai/gonka/issues/731
issue_number: 731
synced_at: 2026-07-06T09:52:44Z
template: issues-main.html
---

> 🔄 **Авто-синхронизация:** из [Issue #731](https://github.com/gonka-ai/gonka/issues/731) каждые 6 часов. 

# 🔴 Define changes in the API container for smooth migration

**Автор:** [@tcharchian](https://github.com/tcharchian) · **Состояние:** Closed · **Создано:** 2026-02-11 01:28 UTC · **Обновлено:** 2026-03-11 19:54 UTC

**Веха:** v0.2.11

---

## 📝 Описание

*(пусто)*

---

## 💬 Комментарии (3)

### Комментарий 1 — [@tamazgadaev](https://github.com/tamazgadaev)

*2026-03-02 01:18 UTC*

- Fix the 400/422 issue in API container
- Adjust thresholds a little bit (onchain, not API)
- Do one of the two: a) ignore -9999 logprobs in validation b) enforce top_p and top_k in requests (a) preferred)

### Комментарий 2 — [@tamazgadaev](https://github.com/tamazgadaev)

*2026-03-03 03:06 UTC*

Actually, we don't strictly need any of these 3 for smooth migration. 1 is desirable, 2 nice to have (and we'll get the threshold values), 3 is not needed

### Комментарий 3 — [@gmorgachev](https://github.com/gmorgachev)

*2026-03-11 19:54 UTC*

i think we need to close this one. fix 400/422 is independent bug to fix
