---
title: "#2106 — Preserved nodes carry stale weight indefinitely and ignore node changes (v0.2.17)"
source: https://github.com/gonka-ai/gonka/issues/2106
issue_number: 2106
synced_at: 2026-10-25T22:38:56Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Preserved nodes carry stale weight indefinitely and ignore node changes (v0.2.17)
    <span class="issues-number">#2106</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/maria-mitina">@maria-mitina</a> opened 2026-10-23 12:51 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-10-24 00:19 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span></div>
</div>

<div class="issues-content" markdown="1">
## Summary

On `upgrade-v0.2.17` (checked at `fc65e8ec0`), a preserved ML node is never re-measured or re-checked once it is preserved. Its `PocWeight` is copied forward from the current epoch, the same node can be preserved in consecutive episodes, and changes to the node (status, hardware, fresh PoC result) are ignored. A single PoC measurement can therefore be carried indefinitely.

## Mechanism (as implemented)

1. **Sampling**: `SamplePreservedForEpisode` (`x/inference/module/model_assignment.go`), at each PoC start and each cPoC trigger.
   - Candidates are the current epoch's subgroup `ValidationWeights`, minus reserved (training) nodes.
   - Participant gates: live member, not a guardian, `EpochPerformanceSummary.RewardedCoins > 0` in the previous epoch, per-participant and IQR weight thresholds.
   - Selection: seeded shuffle keeps N/2+1 participants, nodes are allocated smallest-first up to `PocSlotAllocation` (default 50%), and non-voting power is capped at 34%.
   - The result is stored in `PreservedNodesSnapshot`.
2. **Carry**: `PreservedParticipantsFromCurrentEpoch` / `GetPreservedNodesByParticipant` (`chainvalidation.go`).
   - The preserved node's `PocWeight` is copied from the current epoch's subgroup `ValidationWeights`.
   - Its PoC distributions are dropped by `filterStoreCommitsFromInferenceNodes`.
   - In `mergeByModel` the preserved entry is added first, so it wins over a PoC entry with the same `NodeId`.
3. **cPoC**: `evaluateConfirmation` (`confirmation_poc.go`).
   - The reading is `preserved + measured`, where `preserved` is the stored weight of the snapshot's nodes (`preservedWeightByParticipant`).
   - Preserved nodes are never tested.
4. **Only node-level check**: `setModelsForParticipants` drops a carried node at epoch formation only if it is missing from `HardwareNodes` or the inventory no longer lists the model.

## Problems

1. **Weight is never re-measured.** The value carried into epoch N+1 is whatever epoch N held. If the node was also preserved in N, that value is itself a carry. Nothing limits consecutive preservations or forces a fresh PoC every K epochs. cPoC credits the stored weight, so it cannot catch this either.
2. **Node state changes are ignored.**
   - `HardwareNode.status` (`STOPPED` / `FAILED` / `TRAINING`) is not read by the sampler or the carry.
   - Hardware changes (GPU type or count) have no effect.
   - The sampler does not consult `HardwareNodes`, so a node removed from the inventory can still be written into the episode snapshot; it is dropped only later, at seating. Related: #310.
3. **A fresh PoC result cannot replace the carried weight.** If a preserved node also mined PoC, its distribution is filtered out and the preserved entry wins the merge. A host that upgraded the node is stuck at the old weight, and one whose node degraded keeps it.
4. **Eligibility is participant-level, not node-level.** The only history gate is that the participant was rewarded last epoch. Nothing checks whether the specific node served inference or missed requests. A preserved host is rewarded, so it stays eligible.

## Observed on testnet

Over epochs 379–419, every readable snapshot (21 PoC and cPoC episodes) preserved exactly two single-node hosts, rotating among the same four participants (`…32vrcn`, `…kyc325`, `…pcgs0y`, `…4sgtd5`), always `node1`. With one node per host, their weight cannot change while they keep being preserved.

## Suggested fixes

- Disallow preserving the same node in consecutive episodes, or require a fresh PoC at least every K epochs (track the last measured epoch per node).
- At sampling time, exclude nodes that are missing from `HardwareNodes`, have a status other than `INFERENCE` / `POC`, or no longer list the model.
- When a preserved node also has a valid fresh PoC distribution, use the fresh weight (or `min(carried, fresh)`) instead of always preferring the preserved entry.
- Optionally, include preserved nodes in cPoC measurement instead of crediting their stored weight.

Related: #310, #1805.

</div>

---

> 🔄 **Auto-synced** from [Issue #2106](https://github.com/gonka-ai/gonka/issues/2106) every hour.
