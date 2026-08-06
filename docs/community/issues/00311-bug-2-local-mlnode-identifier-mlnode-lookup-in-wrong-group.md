---
title: "#311 — BUG-2: Local MLNode identifier & MLNode lookup in wrong group"
source: https://github.com/gonka-ai/gonka/issues/311
issue_number: 311
synced_at: 2026-08-06T14:43:12Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    BUG-2: Local MLNode identifier & MLNode lookup in wrong group
    <span class="issues-number">#311</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/gmorgachev">@gmorgachev</a> opened 2025-09-02 09:28 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-01-28 22:34 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span></div>
</div>

<div class="issues-content" markdown="1">
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
</div>

---

> 🔄 **Auto-synced** from [Issue #311](https://github.com/gonka-ai/gonka/issues/311) every hour.
