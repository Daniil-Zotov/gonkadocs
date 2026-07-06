---
title: "#983 — Bug: GET /api/v1/epochs/{N}/participants returns 500 for past epochs (CreatedAtBlockHeight=0)"
source: https://github.com/gonka-ai/gonka/issues/983
issue_number: 983
synced_at: 2026-07-06T09:52:29Z
---

> 🔄 **Авто-синхронизация:** из [Issue #983](https://github.com/gonka-ai/gonka/issues/983) каждые 6 часов. 

# 🟢 Bug: GET /api/v1/epochs/{N}/participants returns 500 for past epochs (CreatedAtBlockHeight=0)

**Автор:** [@mingles-agent](https://github.com/mingles-agent) · **Состояние:** Open · **Создано:** 2026-03-31 08:51 UTC · **Обновлено:** 2026-03-31 08:51 UTC

---

## 📝 Описание

## Bug

`GET /api/v1/epochs/{N}/participants` returns **500 Internal Server Error** for past epochs. Current epoch works fine.

## Repro

```
GET http://node1.gonka.ai:8000/api/v1/epochs/215/participants
→ 500 Internal Server Error: height must be greater than 0, but got 0
```

Epoch 215 consistently reproduces this. Any past epoch where `CreatedAtBlockHeight` was not yet populated will fail.

## Root Cause

In `queryActiveParticipants` (`get_participants_handler.go`):

1. First query (no height) fetches `activeParticipants`
2. `blockHeight := activeParticipants.CreatedAtBlockHeight` — for old epochs this is **0** (field was not populated at storage time)
3. Second call `QueryByKeyWithOptions(..., height=0, prove=true)` — CometBFT rejects `height=0` with the above error

## Fix

Check if `blockHeight == 0` before the second query. If so, skip the proof query and return the first result directly, with a `Warn` log for observability.

Fix is implemented in PR #973.
