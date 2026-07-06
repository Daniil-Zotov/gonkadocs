---
title: "#381 — [P0] How to change `inference_url`"
source: https://github.com/gonka-ai/gonka/issues/381
issue_number: 381
synced_at: 2026-07-06T09:53:34Z
---

> 🔄 **Авто-синхронизация:** из [Issue #381](https://github.com/gonka-ai/gonka/issues/381) каждые 6 часов. 

# 🔴 [P0] How to change `inference_url`

**Автор:** [@tcharchian](https://github.com/tcharchian) · **Состояние:** Closed · **Создано:** 2025-09-30 16:43 UTC · **Обновлено:** 2025-12-08 21:16 UTC

---

## 📝 Описание

1. Change `inference_url`. Probably, it should happen immediately and propagate everywhere.
2. Vefigy `inference_url`. Let's think on how can it be verified, at least asynchronousl,y whena  node with that URL is already running
Example: `api` container has a new endpoint /v1/verify, which returns:
```
{
    "requester_address": "gonka...",
    "timestamps": <timestamp in last Xmin>,
    "signature": <singature of timestamps by this node's warm key>
}
```
The signature should not be refreshed more than once within X minutes.
Such an endpoint should be enough to have voting for claiming the wrong address. Ideally, every `api` node should verify all `inference_url` once in an epoch automatically and initiate this voting, but it's hard to estimate it for now, it might be okay to leave it manual at the moment.
3. Add a check that a new participant can't be created if there is the same URL across active participants (are all?), and also a participant can't be edited to set the existing URL.

---

## 💬 Комментарии (1)

### Комментарий 1 — [@tcharchian](https://github.com/tcharchian)

*2025-12-08 21:16 UTC*

https://gonka.ai/FAQ/#how-to-change-inference_url
