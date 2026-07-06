---
title: "#351 — BUG: Wrong error message for unsupported models in /chat/completions"
source: https://github.com/gonka-ai/gonka/issues/351
issue_number: 351
synced_at: 2026-07-06T09:52:10Z
template: issues-main.html
---

> 🔄 **Авто-синхронизация:** из [Issue #351](https://github.com/gonka-ai/gonka/issues/351) каждые 6 часов. 

# 🔴 BUG: Wrong error message for unsupported models in /chat/completions

**Автор:** [@gmorgachev](https://github.com/gmorgachev) · **Состояние:** Closed · **Создано:** 2025-09-10 23:19 UTC · **Обновлено:** 2026-04-28 18:50 UTC

---

## 📝 Описание

When inference for unsupported message requested, system returns:

"HTTP/1.1 402 Payment Required"

---

## 💬 Комментарии (5)

### Комментарий 1 — [@tcharchian](https://github.com/tcharchian)

*2026-01-28 22:23 UTC*

Needs to be rechecked

### Комментарий 2 — [@AlexeySamosadov](https://github.com/AlexeySamosadov)

*2026-02-08 14:14 UTC*

PR created: https://github.com/gonka-ai/gonka/pull/679

Fixes wrong error message for unsupported models in /chat/completions.

### Комментарий 3 — [@AlexeySamosadov](https://github.com/AlexeySamosadov)

*2026-02-12 15:26 UTC*

I already have a PR for this: #679 — fixes the wrong error message for unsupported models. Would appreciate a review when you get a chance.

### Комментарий 4 — [@unameisfine](https://github.com/unameisfine)

*2026-03-19 22:42 UTC*

Starting work on this. Previous PR was closed as stale — will investigate the current error handling path and submit a fix. ETA: 2-3 days.

### Комментарий 5 — [@x0152](https://github.com/x0152)

*2026-04-28 17:15 UTC*

Already fixed in #614. Closing
