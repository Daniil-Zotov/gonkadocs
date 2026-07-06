---
title: "#461 — ML node model management edge cases"
source: https://github.com/gonka-ai/gonka/issues/461
issue_number: 461
synced_at: 2026-07-06T09:53:07Z
---

> 🔄 **Авто-синхронизация:** из [Issue #461](https://github.com/gonka-ai/gonka/issues/461) каждые 6 часов. 

# 🔴 ML node model management edge cases

**Автор:** [@tcharchian](https://github.com/tcharchian) · **Состояние:** Closed · **Создано:** 2025-12-02 20:12 UTC · **Обновлено:** 2026-01-24 02:14 UTC

---

## 📝 Описание

# Context

For each mlnode a participant can configure a list of models it supports, it’s done via node management admin API (or via `node-config.json`, but only on the first run of the api container).

Nodes are reported to the chain as HardwareNode proto’s via `MsgSubmitHardwareDiff` transactions.

During each PoC chain, assign a model to each participating mlnode; it should be a model that’s both a governance model (on-chain list) and a node-supported model (admin config). In `decentralized-api` this assigned model is stored in node state: `NodeState.EpochModel`

# Admin config model changes tasks

We need to make sure model changes are handled correctly:

1. A participant changes a list of models their mlnode supports during the Inference phase
2. Make sure the initially assigned `EpochModel` is being served to the end of the epoch
3. Edge case 1: make sure the right `EpochModel` is served even if we restart the api container, meaning that api should fetch `EpochModel`
4. Edge case 2: make sure the right `EpochModel` is being served during PoC if a node is allocated to serve inference during PoC
5. Make sure that starting next epoch, we serve a different model, supported by the admin config list

**Questions:** 

1. What should we do and when should we switch models if it were the only mlnode serving a particular model? 
2. What if we switch too early, and we will have missed validations because of it?

# MLNode disabled tasks

Participants can disable their nodes via `/admin/v1/nodes/:id/disable` endpoint. We need to make sure the behavior is as desired:

1. MLnode continues to serve Inference until the start of the next epoch
2. MLnode serves inference during PoC if it was allocated to do so
3. Mlnode participates in PoC batch validation if it wasn’t allocated to serve inference during PoC, but it should generate batches itself!
4. When a new epoch starts, the node just sits disabled, but in the Inference state with one of the models listed in the config. Participants can later delete it completely. **Question:** let’s choose the least presented model?

# Important
The same edge case could happen, it was the only node serving a particular model, and we may need to run validations on it before `claimReward`

---

## 💬 Комментарии (1)

### Комментарий 1 — [@tcharchian](https://github.com/tcharchian)

*2026-01-24 02:14 UTC*

Postponing and closing for now. 
