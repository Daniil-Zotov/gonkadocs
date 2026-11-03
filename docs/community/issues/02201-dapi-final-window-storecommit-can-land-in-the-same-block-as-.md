---
title: "#2201 — dapi: final-window StoreCommit can land in the same block as the previous one and is rejected (only one commit per block allowed)"
source: https://github.com/gonka-ai/gonka/issues/2201
issue_number: 2201
synced_at: 2026-11-03T17:54:35Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    dapi: final-window StoreCommit can land in the same block as the previous one and is rejected (only one commit per block allowed)
    <span class="issues-number">#2201</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/maria-mitina">@maria-mitina</a> opened 2026-11-02 17:18 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-11-02 17:22 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

In the last blocks of a PoC generation stage, the dapi can send a `MsgPoCV2StoreCommit` while its previous commit is still in the mempool. When both land in the same block, the chain rejects the second with `only one commit per block allowed` (code 1137). The fee grant still pays for the rejected tx, about 224,000 ngonka at 1 ngonka/gas.

## Observed on testnet4 (build 70ceeb804, stage 32560)

The dapi normally sends one commit per block. When one block has no commit, the next block gets two:

| Participant | ML nodes | Block without a commit | Block with two commits | Rejected count |
|---|---|---|---|---|
| jx6tad | 2 | 32617 | [32618](http://xj7-5.s.filfox.io:19242/dashboard/gonka/block/32618) (count 9408 ok, 9568 rejected) | 9568 |
| 6jw2rm | 1 | 32618 | [32619](http://xj7-5.s.filfox.io:19242/dashboard/gonka/block/32619) (count 8768 ok, 8896 rejected) | 8896 |

This does not depend on how many ML nodes a participant has. The rejected tx's fee came out of the ML-ops key's fee grant. No commit was lost: the next block carried a higher count.

## Cause

`decentralized-api/poc/commit_worker.go`: during the final commit window (`inFinalCommitWindow`, the last 3 blocks before the deadline), the two guards that stop a second in-flight commit are skipped.

- Line 383: `if !finalWindow && height == w.lastAcceptedBroadcastHeight`
- Line 446: `if pending, ok := w.pending[key]; ok && !finalWindow && ...`

If the previous commit misses its block, the worker sends the next one anyway. Both are included together, and the keeper rejects the second (`msg_server_poc_v2_commit.go:251`, where `existing.CommitBlockHeight == currentBlockHeight`). The ante recheck in `poc_period_validation.go:325` only catches this when `entry.Count <= existing.Count`, so a higher count gets through to DeliverTx.

## Impact

Low. It costs about one rejected tx fee per participant per stage when a block is missed near the end of a stage, and adds one failed tx to the chain. Rewards and PoC weight are not affected.

## Possible fix

In the final window, still skip a model that has a pending commit in the mempool, unless that commit's timeout height has passed. Or make sure at most one commit per (stage, model) is in flight at a time.

</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/maria-mitina">@maria-mitina</a></span>
    <span class="issues-meta-item">commented 2026-11-02 17:22 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@tcharchian FYI</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2201](https://github.com/gonka-ai/gonka/issues/2201) every hour.
