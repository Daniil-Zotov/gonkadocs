---
title: "#983 — Bug: GET /api/v1/epochs/{N}/participants returns 500 for past epochs (CreatedAtBlockHeight=0)"
source: https://github.com/gonka-ai/gonka/issues/983
issue_number: 983
synced_at: 2026-07-25T06:34:09Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Bug: GET /api/v1/epochs/{N}/participants returns 500 for past epochs (CreatedAtBlockHeight=0)
    <span class="issues-number">#983</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/mingles-agent">@mingles-agent</a> opened 2026-03-31 08:51 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-03-31 08:51 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
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
</div>

---

> 🔄 **Auto-synced** from [Issue #983](https://github.com/gonka-ai/gonka/issues/983) every hour.
