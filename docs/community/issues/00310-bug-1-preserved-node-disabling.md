---
title: "#310 — BUG-1: Preserved node disabling"
source: https://github.com/gonka-ai/gonka/issues/310
issue_number: 310
synced_at: 2026-07-06T09:52:49Z
template: issues-main.html
---

> 🔄 **Авто-синхронизация:** из [Issue #310](https://github.com/gonka-ai/gonka/issues/310) каждые 6 часов. 

# 🟢 BUG-1: Preserved node disabling

**Автор:** [@gmorgachev](https://github.com/gmorgachev) · **Состояние:** Open · **Создано:** 2025-09-01 18:19 UTC · **Обновлено:** 2026-02-12 15:34 UTC

**Метки:** `bug` `up-for-grabs`

---

## 📝 Описание

# Description

When MLNodes are disabled `POST 9200/admin/v1/nodes/<id>/disable`

MLNodes have to work till next PoC according to schedule:
```
enum TimeslotType {
  PRE_POC_SLOT = 0;
  POC_SLOT = 1;
}
```

Essentially:  
- work till end of current 
- serve inference during next PoC if POC_SLOT is set to true (on-duty nodes)

It supposed that after end of next PoC, all disabled MLNodes will be have weight 0 and not used anymore. 

Currently, the MLNode which was on-duty has the same weight as in previous epoch and scheduled for the next epoch (can be checked in `/v1/epochs/10/participants`).  
At the same time it's not presented in HardwareNodes (can be checked in: `./inferenced query inference hardware-nodes-all`)



---

## 💬 Комментарии (3)

### Комментарий 1 — [@tcharchian](https://github.com/tcharchian)

*2026-01-28 22:35 UTC*

up-tp-grabs, but needs to be rechecked

### Комментарий 2 — [@AlexeySamosadov](https://github.com/AlexeySamosadov)

*2026-02-08 14:14 UTC*

PR created: https://github.com/gonka-ai/gonka/pull/682

Skips disabled nodes from governance model population.

### Комментарий 3 — [@AlexeySamosadov](https://github.com/AlexeySamosadov)

*2026-02-12 15:34 UTC*

I have a PR for this: #682 — skips disabled nodes from governance model population. Would appreciate a review when you get a chance.
