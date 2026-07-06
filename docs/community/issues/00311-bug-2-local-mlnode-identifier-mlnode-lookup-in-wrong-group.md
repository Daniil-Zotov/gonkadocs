---
title: "#311 — BUG-2: Local MLNode identifier & MLNode lookup in wrong group"
source: https://github.com/gonka-ai/gonka/issues/311
issue_number: 311
synced_at: 2026-07-06T09:53:03Z
---

> 🔄 **Авто-синхронизация:** из [Issue #311](https://github.com/gonka-ai/gonka/issues/311) каждые 6 часов. 

# 🔴 BUG-2: Local MLNode identifier & MLNode lookup in wrong group

**Автор:** [@gmorgachev](https://github.com/gmorgachev) · **Состояние:** Closed · **Создано:** 2025-09-02 09:28 UTC · **Обновлено:** 2026-01-28 22:34 UTC

**Метки:** `bug`

---

## 📝 Описание

# BUG-2: Local MLNode identifier & MLNode lookup in wrong group

In function getInferenceServingNodeIds

``` 
// getInferenceServingNodeIds returns a set of node IDs that have POC_SLOT = true in the current epoch
func (am AppModule) getInferenceServingNodeIds(ctx context.Context, upcomingEpoch types.Epoch) map[string]bool {
	inferenceServingNodeIds := make(map[string]bool)

	// Skip for first epoch
	if upcomingEpoch.Index <= 1 {
		return inferenceServingNodeIds
	}

	// Get current epoch group data
	currentEpochGroup, err := am.keeper.GetCurrentEpochGroup(ctx)
	if err != nil {
		am.LogError("getInferenceServingNodeIds: Unable to get current epoch group", types.PoC, "error", err.Error())
		return inferenceServingNodeIds
	}

	// Find all nodes with POC_SLOT = true
	for _, validationWeight := range currentEpochGroup.GroupData.ValidationWeights {
		for _, mlNode := range validationWeight.MlNodes {
			if len(mlNode.TimeslotAllocation) > 1 && mlNode.TimeslotAllocation[1] { // POC_SLOT = true
				inferenceServingNodeIds[mlNode.NodeId] = true
				am.LogInfo("getInferenceServingNodeIds: Found inference-serving node", types.PoC,
					"nodeId", mlNode.NodeId,
					"participantAddress", validationWeight.MemberAddress)
			}
		}
	}

	return inferenceServingNodeIds
}
```

`mlNode.NodeId` is used as key for `inferenceServingNodeIds`. This is local MLNode identifier which might not be unique between different participants which might lead to collisions


----

## MLNode lookup in wrong group

Related, larger issue in the same area: the top-level epoch group `currentEpochGroup.GroupData.ValidationWeights` has empty `MlNodes` because no mlnodes stored in root group (only in model sub-groups). As a result, this scan always returns none and `getInferenceServingNodeIds` is empty.

That's why we have everywhere in logs:
```
11:47AM INF ComputeNewWeights: Found inference-serving nodes inferenceServingNodeIds={} module=x/inference subsystem=PoC
```
=> the original issue was not active in practice.


**Impact of both issues is minimal**. This result is only used for an extra PoC-batch filtering pass; it's effectively a non-essential double-check, but which is actually disabled now. Even with an empty set, core behavior remains unaffected:
```
originalBatches := am.filterPoCBatchesFromInferenceNodes(allOriginalBatches, inferenceServingNodeIds)
```

### Suggested fixes:
- Build the set from the previous epoch's ActiveParticipants via `am.GetPreservedNodesByParticipant(ctx, upcomingEpoch.Index-1)` and convert it into a set keyed by `(participantAddress, nodeId)`.
- Avoid `NodeId` collisions by using a composite key `(participantAddress, nodeId)` instead of bare `NodeId`.

Priority: not urgent but should be fixed but
