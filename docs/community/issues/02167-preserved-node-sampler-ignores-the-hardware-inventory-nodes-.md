---
title: "#2167 — Preserved-node sampler ignores the hardware inventory: nodes that a host removed (or that are FAILED) are still preserved and carry their weight into the next epoch"
source: https://github.com/gonka-ai/gonka/issues/2167
issue_number: 2167
synced_at: 2026-10-30T02:00:26Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Preserved-node sampler ignores the hardware inventory: nodes that a host removed (or that are FAILED) are still preserved and carry their weight into the next epoch
    <span class="issues-number">#2167</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/Aktum1">@Aktum1</a> opened 2026-10-28 23:49 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-10-29 00:44 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

`SamplePreservedForEpisode` picks preserved (POC_SLOT) nodes only from the current epoch group (`ValidationWeights[].MlNodes`). It never looks at the participant's on-chain hardware inventory (`HardwareNodes`). As a result:

- A node that the host **removed** (`DELETE /admin/v1/nodes/<id>` → `MsgSubmitHardwareDiff.Removed`) long before the PoC is still sampled as preserved.
- A node that the host **disabled** (`POST /admin/v1/nodes/<id>/disable`) is still sampled. Disable is local to the API node and the chain never learns about it.
- A node reported **FAILED** or **STOPPED** is still sampled.

The allocator also goes smallest-weight-first (`getSmallestUnallocatedMLNode`). Nodes that are being retired are usually the old, weaker ones, so they are the most likely to be picked.

There is no way for a host to say "this node will not be in the next epoch". A host that loses its hardware (rental ended, GPU died), or that replaces a node with a new one, can't keep the dead node out of the preserved snapshot.

### Related

- #2106, problem 2: describes this sampler gap from the code and testnet ("a node removed from the inventory can still be written into the episode snapshot"). This issue is the mainnet case, with block-level evidence, and a PR for that one point.
- #310: the disable case. PR #682 changes routing in the broker (`UpdateNodeWithEpochData`). It does not reach the chain, so it does not stop a disabled node from being preserved.
- PR #2158 bounds carry to one epoch in the same function. The change proposed here is orthogonal: it filters by inventory, not by carry history.

## What happened (mainnet, participant `gonka1xvlfshxznnuftsv2lke98rv9eqkjr0v6z8c3uk`)

Everything below can be reproduced against any archive-enough node with `inferenced q ... --height <h>`.

### Epoch 439: three nodes disabled 18–26 min before PoC, all three preserved

We replaced `node59`, `node61` (MiniMax) and `node60` (DeepSeek) with new nodes `node64`, `node66`, `node65`. Each old node was disabled (`POST /admin/v1/nodes/<id>/disable`) right after its replacement was registered and healthy (our script log, UTC):

| node | disabled at (UTC) | ≈ block | blocks before PoC 439 |
|---|---|---|---|
| node59 | 27.10 20:14:37 | 6767717 | 287 |
| node60 | 27.10 20:15:02 | 6767722 | 282 |
| node61 | 27.10 20:22:02 | 6767800 | 204 |

PoC 439 started at block **6768004** (2026-10-27T20:40:08Z). Disable is local to the API node, so the chain inventory at that block still had the old nodes:

```
$ inferenced q inference hardware-nodes-all --height 6768004    # our participant
[node59 INFERENCE, node60 INFERENCE, node61 INFERENCE, node64 INFERENCE, node65 INFERENCE, node66 INFERENCE]

$ inferenced q inference preserved-nodes-snapshot --height 6768004
episode_anchor_height: 6768004
MiniMaxAI/MiniMax-M2.7            gonka1xvlfsh...  [node59, node61]
deepseek-ai/DeepSeek-V4-Flash-... gonka1xvlfsh...  [node60]
```

The three disabled nodes carried their epoch-438 weight into 439 unchanged, so we had to re-enable them and keep them serving for the whole epoch:

```
$ inferenced q inference show-epoch-group-data 438 --model-id <m>   /   ... 439 --model-id <m>
epoch 438  MiniMax   node59 12118, node61 11361          DeepSeek  node60 8963
epoch 439  MiniMax   node59 12118, node61 11361,         DeepSeek  node60 8963,
                     node64 16442, node66 16359                    node65 10906
```

### Epoch 440: three nodes removed on-chain 651 blocks before PoC, all three preserved

This time we deleted the same three nodes (`DELETE /admin/v1/nodes/<id>`). The API node submitted the removal on-chain:

```
tx  ECE52F24653DF9D79FBF34E40FEE765E5A3593E3A0AFA745EC60D67C531A2066
height 6782744, 2026-10-28T18:33:37Z, code 0
MsgExec{ MsgSubmitHardwareDiff{ creator: gonka1xvlfsh..., newOrModified: [], removed: [node59, node60, node61] } }

$ inferenced q inference hardware-nodes-all --height 6782743   -> [node59, node60, node61, node64, node65, node66]
$ inferenced q inference hardware-nodes-all --height 6782744   -> [node64, node65, node66]
```

PoC 440 started at block **6783395** (2026-10-28T19:31:40Z), 651 blocks (58 min) later. At that block the inventory no longer had these nodes, and the snapshot sampled in that same block still picked all three:

```
$ inferenced q inference hardware-nodes-all --height 6783395    # our participant
[node64 INFERENCE, node66 INFERENCE, node67 INFERENCE]

$ inferenced q inference preserved-nodes-snapshot --height 6783395
episode_anchor_height: 6783395
MiniMaxAI/MiniMax-M2.7            gonka1xvlfsh...  [node59, node61, node66]
deepseek-ai/DeepSeek-V4-Flash-... gonka1xvlfsh...  [node60]
```

The weight is meant to be served, so after the snapshot we re-registered the three nodes (tx `4D27C21685335FDA4B58511891525B4F008A687D4567CDF426330604FAFDB7B9`, height 6783483, 19:39:32Z). That was before epoch formation at block 6783795, so they got the same weight a third epoch in a row:

```
epoch 440  MiniMax   node59 12118, node61 11361, node64 16176, node66 16359    DeepSeek  node60 8963, node67 10951
```

Without the re-registration, `setModelsForParticipants` would have dropped them at formation (judging by the code; we did not observe that directly). The preserved slots were still spent on nodes that no longer existed.

## Why this is a problem

1. **Weight for a node that does not serve.** If the node is still in the inventory (disabled, FAILED, hardware gone without a clean delete), `setModelsForParticipants` keeps it. Its old weight is seated in the next epoch, but nothing serves the requests routed to it. The host takes misses. At settlement the inactive or reduced share stays in the denominator (`totalFullWeight` in `bitcoin_rewards.go`) and goes to governance, so other hosts' rewards drop. Every host whose hardware rental ends mid-cycle runs into this, through no fault of their own.
2. **A wasted preserved slot when the node was removed.** `setModelsForParticipants` drops a node that is absent from the inventory at epoch formation ("node id absent from the hardware inventory -> dropped before any weight consumer"). The sampler doesn't, so the removed node uses up part of the `PocSlotAllocation` target. Fewer real nodes stay on inference during the PoC, which is the reason preservation exists, and the ghost's weight is then discarded anyway.
3. **A dead node can pass cPoC.** The snapshot is re-sampled at every cPoC trigger. A FAILED or removed node that is sampled as preserved is exempt from the confirmation check.
4. **No clean way to leave or replace a node.** Disable doesn't reach the chain and delete is ignored by the sampler. The only workaround is to delete and re-add a node around the PoC block, which is fragile.

## Proposed fix (two small changes, no proto change)

### 1. Chain: the sampler uses the same availability rule as epoch formation

A node can be preserved only if:

- its id is in the participant's `HardwareNodes`,
- that record still lists the model, and
- its status is not `FAILED` or `STOPPED`.

If the participant has no `HardwareNodes` record (genesis bootstrap), the filter is skipped, as in `setModelsForParticipants`.

Eligibility, thresholds and the 34 % non-voting check use the available nodes only. A participant whose only remaining node for a model is preserved really has no PoC power left in that model, so the non-voting cap must see that. The preservation target stays `PocSlotAllocation × full model weight`, and the participant-hash seed is unchanged, so sampling of unaffected participants doesn't shift.

**If every node is unavailable, nothing is preserved.** Everyone runs regular PoC, which is the behaviour from before POC_SLOT. We don't fall back to unavailable nodes: a preserved node that is gone serves nothing, so the fallback would only bring the problem back.

### 2. API node: disable reaches the chain

The API node already gives disable a "drain" meaning: `ShouldBeOperational` keeps a node disabled in epoch E working until E ends (inference and any cPoC of E), and stops it from E+1. Only the chain never hears about it.

The change: a disabled node is reported in `MsgSubmitHardwareDiff` with an empty `models` list, and its status stays as is. The chain already treats "the inventory no longer lists the model" as "this node does not serve it next epoch":

- with change 1, the sampler does not preserve it;
- `setModelsForParticipants` drops it at formation, as it already does today.

Nothing else on the chain reads `HardwareNode.models` (only seating and the sampler), and routing for the current epoch goes through the epoch group, so the node keeps serving the epoch it was paid for. Re-enable reports the models again.

The diff already compares model lists (`hardwareEquals`), so disable and re-enable are sent within a minute by the regular node sync.

If you prefer an explicit field (for example `HardwareNode.draining`) over the empty model list, the logic stays the same, but it needs a proto change.

### Why the chain should not drop FAILED nodes at epoch formation

The obvious next idea is to drop a preserved node whose status is `FAILED` at the formation block. Our data says no. The API node sets `FAILED` after a single failed probe (`queryNodeStatus`: one `NodeState` error, one failed `InferenceHealth`, or one model mismatch). The episodes are short and recover. On our network node on 28.10 (hardware diffs, UTC):

| node | FAILED | back to INFERENCE | duration |
|---|---|---|---|
| node64 | 17:06 | 17:32 | 26 min |
| node59 | 19:39 | 19:48 | 9 min |
| node59 | 19:57 | 20:04 | 7 min |
| node61 | 19:39 | 20:28 | 49 min |
| node60 | 19:39 | 20:36 | 57 min |
| node67 | 20:26 | 20:33 | 7 min |
| node66 | 20:26 | 20:41 | 15 min |

The epoch-440 formation block 6783795 (2026-10-28T20:07:29Z) fell inside the FAILED windows of node60 and node61. A "FAILED at formation" rule would have taken away their whole epoch-440 weight, although both were serving again 20–30 minutes later.

In the sampler (change 1) the cost of a transient FAILED is small: the node is not preserved, runs PoC and earns fresh weight. For dead hardware, the absent-or-FAILED check at the anchor block plus the miss accounting during the epoch are enough.

A draft of both changes with tests is in branch `fix/preserved-skip-removed-hw-nodes`:

- chain: `x/inference/module/model_assignment.go` (`availableForPreservation`, used in `SamplePreservedForEpisode`) plus three tests;
- API node: `decentralized-api/broker/broker.go` (`convertInferenceNodeToHardwareNode`) plus two tests.

We'd be glad to open it as a PR.

### Trade-off for maintainers

With the status check, a host can avoid being preserved by reporting FAILED at the anchor block, or by disabling the node and re-enabling it right after. The node then runs PoC like any non-preserved node: the host gains no weight, and the allocator fills the target from other nodes. If you'd rather not allow this, keep only the inventory and model check in the sampler. That still covers the delete and disable cases.

## Code references (main = v0.2.16, unchanged in `upgrade-v0.2.17`)

- `x/inference/module/model_assignment.go` `SamplePreservedForEpisode`: candidates are `currentSubData.ValidationWeights[].MlNodes`, filtered only by live subgroup membership.
- `x/inference/module/model_assignment.go` `samplePreservedForModel` / `getSmallestUnallocatedMLNode`: smallest-weight-first allocation.
- `x/inference/module/model_assignment.go` `setModelsForParticipants` / `resolveUniqueCompatibleClaims`: the inventory filter applied at epoch formation, but not in the sampler.
- `decentralized-api/broker/broker.go` `calculateNodesDiff`: delete becomes `Removed`. Disable changes only the local `AdminState` (`ShouldBeOperational`: works to the end of its epoch) and never reaches the chain.
- `x/inference/keeper/bitcoin_rewards.go`: unpaid shares stay in `totalFullWeight` and go to governance.

</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/cyberdelamain">@cyberdelamain</a></span>
    <span class="issues-meta-item">commented 2026-10-29 00:44 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Thanks for the detailed write-up. I re-checked the mainnet data and it matches: <code>hardware-nodes-all</code> at 6782743 / 6782744 / 6783395 and <code>preserved-nodes-snapshot</code> at 6768004 and 6783395 show exactly what you list. <code>SamplePreservedForEpisode</code> reads only <code>ValidationWeights[].MlNodes</code> and never looks at the inventory.</p>
<p>To separate what the chain does from what the node changes did:</p>
<ul>
<li><strong>A clean delete costs only a slot.</strong> In epoch 440 the delete at 6782744 was correct, and the sampler still picked the three removed nodes at 6783395. Had they stayed deleted, <code>setModelsForParticipants</code> would have dropped them at formation (its own comment says preserved carry goes through the same path; I read this from the code, I have not seen it on mainnet). So the weight is not carried, but the removed nodes take preserved slots that real nodes should hold during the PoC.</li>
<li><strong>The third carry came from the re-registration.</strong> The re-registration at 6783483, before formation at 6783795, put the nodes back into the inventory, and that is what gave them their weight again. In epoch 439, disable did not help either: it changes only the API node's local state and the chain never sees it.</li>
<li><strong>The strongest case for the fix is a node that is broken but still in the inventory.</strong> A GPU dies or a rental ends, and the node sits in the inventory as FAILED. The sampler can still pick it, its weight goes into the next epoch, and nothing serves it. The host takes misses and the unpaid share goes to governance. Here the host did nothing wrong, and today the chain has no rule against it.</li>
</ul>
<p>How to retire a node with the current code:</p>
<ol>
<li>Add the replacement first and make sure the chain has it (<code>hardware-nodes-all</code> shows it as INFERENCE) before the next PoC starts.</li>
<li>Use <code>DELETE /admin/v1/nodes/&lt;id&gt;</code>, not disable. Best timing is after the next epoch's PoC ends and before formation: the old node serves the current epoch through the PoC, and the only gap is the few minutes between the delete and formation (DELETE unregisters the node from the broker at once, there is no drain).</li>
<li>Don't re-register it before formation.</li>
</ol>
<p>Two small notes on #2168:
- It targets <code>main</code>, while #2158, which changes the same function, targets <code>upgrade-v0.2.17</code>. It is worth retargeting and checking the overlap.
- The participant-hash seed indeed stays the same (keys are kept even when the list is empty), but the thresholds (IQR cap, per-participant minimum) are now computed on the available view. So a FAILED node of one host shifts them slightly for others. That looks acceptable, but the description could say so.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2167](https://github.com/gonka-ai/gonka/issues/2167) every hour.
