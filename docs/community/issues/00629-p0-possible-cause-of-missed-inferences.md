---
title: "#629 — [P0] Possible cause of missed inferences"
source: https://github.com/gonka-ai/gonka/issues/629
issue_number: 629
synced_at: 2026-07-06T09:52:10Z
---

> 🔄 **Авто-синхронизация:** из [Issue #629](https://github.com/gonka-ai/gonka/issues/629) каждые 6 часов. 

# 🔴 [P0] Possible cause of missed inferences

**Автор:** [@tcharchian](https://github.com/tcharchian) · **Состояние:** Closed · **Создано:** 2026-01-23 19:47 UTC · **Обновлено:** 2026-04-28 18:28 UTC

---

## 📝 Описание

We're distributing inference requests on the chain based on the total weight of the participant, not the weight of the participant's mlnode for a specific `model_id`. Seems like it's easy can be the cause of missed inferences (e.g. I have 100 nodes for `model_id1` and 3 nodes for `model_id2`, but I get the amount of requests based on the weight of 103 nodes for `model_id2`)

---

## 💬 Комментарии (4)

### Комментарий 1 — [@x0152](https://github.com/x0152)

*2026-01-26 08:06 UTC*

#642 

### Комментарий 2 — [@tcharchian](https://github.com/tcharchian)

*2026-03-20 23:41 UTC*

@tamazgadaev @IgnatovFedor @0xgonka do we want the same for preserved ML Nodes during PoC phase?

### Комментарий 3 — [@tcharchian](https://github.com/tcharchian)

*2026-03-24 23:12 UTC*

This issue is a subset of multi-model support (https://github.com/gonka-ai/gonka/issues/728)
We'll figure out when to review and merge this issue during work on multimodels https://github.com/gonka-ai/gonka/issues/728
@x0152 @0xgonka 

### Комментарий 4 — [@x0152](https://github.com/x0152)

*2026-04-28 18:28 UTC*

Closing as resolved by the multi-PoC updates
