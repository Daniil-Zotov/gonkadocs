---
title: "#772 — Slashed coins should not be burned"
source: https://github.com/gonka-ai/gonka/issues/772
issue_number: 772
synced_at: 2026-07-06T09:52:41Z
template: issues-main.html
---

> 🔄 **Авто-синхронизация:** из [Issue #772](https://github.com/gonka-ai/gonka/issues/772) каждые 6 часов. 

# 🔴 Slashed coins should not be burned

**Автор:** [@tcharchian](https://github.com/tcharchian) · **Состояние:** Closed · **Создано:** 2026-02-18 01:36 UTC · **Обновлено:** 2026-03-12 18:09 UTC

**Веха:** v0.2.11

---

## 📝 Описание

Currently, slashed coins are burned.
This behavior should be changed.

Instead of burning slashed funds, they must be redirected to the Governance module account, consistent with how we handle rewards that are withheld from miners during penalties.

Expected behavior:

- [ ] Slashed coins must not be burned.
- [ ] Slashed coins must be transferred to the Governance module account.
- [ ] Implementation should reuse or mirror the existing logic that handles redistribution of miner rewards that are not paid out due to penalties

---

## 💬 Комментарии (2)

### Комментарий 1 — [@x0152](https://github.com/x0152)

*2026-02-18 09:23 UTC*

#775 

### Комментарий 2 — [@gmorgachev](https://github.com/gmorgachev)

*2026-02-26 18:29 UTC*

@patimen 
