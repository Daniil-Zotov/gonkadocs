---
title: "#2079 — Issue: hosts behind at finalize must pull the missing diffs"
source: https://github.com/gonka-ai/gonka/issues/2079
issue_number: 2079
synced_at: 2026-10-22T05:01:34Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Issue: hosts behind at finalize must pull the missing diffs
    <span class="issues-number">#2079</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/a-kuprin">@a-kuprin</a> opened 2026-10-21 21:21 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-10-21 21:21 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #a2eeef; color: #24292f; border-color: #a2eeef;">enhancement</span></div>
</div>

<div class="issues-content" markdown="1">
# Issue: hosts behind at finalize must pull the missing diffs

**Milestone:** Devshard v7

**Follows:** [#1785](https://github.com/gonka-ai/gonka/pull/1785) (`fix/devshard-finalize-resume-v6`)

## Summary

[#1785](https://github.com/gonka-ai/gonka/pull/1785) can merge. It makes `Finalize` resume from `PhaseFinalizing` and skip a host whose reply is rejected. It does not bring a lagging host up to the tip.

Commit `af125be` removed the only catch-up push that PR added. On resume, `refreshPendingTxsFromHosts` sends one request per host at the current nonce with an empty `Diffs` slice (`TestFinalize_ResumeRefreshDoesNotPushCatchUpToLaggingHost`). A host that is behind is left behind. No host in this tree pulls diffs or snapshots to close that gap.

v7 should add that pull. A host that is behind during finalization fetches the diffs it lacks and applies them before the remaining settlement diffs close.

## What is left after #1785

`Settlement` is reached when `LatestNonce >= FinalizeNonce + groupSize`. That is `groupSize + 1` nonces after the last active nonce, the same budget as `FinalizeNonceReserve`. The phase changes on that nonce whether or not every host has applied the journal.

Two older pushes are still in `Finalize`:

- `finalizeDiffRound` calls `sendDiffRound`, which still runs `catchUpForSend` for the host selected for that round. The diff is composed first. The mempool in the reply is queued for a later diff.
- After `Settlement`, `CollectSignatures` still falls back from `GET /signatures` to `sendCatchUpWith`.

A host the round-robin still contacts can receive the journal that way. A host that is only probed by the resume refresh receives nothing. A finish that the host produces only after it applies the gap misses the drain when no later diff is composed in time. `settleLiveRecordLocked` then closes a still-live inference at `ReservedCost`.

The PR discussion treats this as the host catching up on its own. That pull is the v7 work. It is not in the tree, and #1785 does not wait for it.

## Work

A host that finds itself behind the finalize tip pulls the missing diffs (and a snapshot, when that is the cheaper prefix) and applies them on its own.

The pull has to land in time for the host's mempool — finishes and the other host-proposed txs — to be back on the gateway before the diff that crosses `FinalizeNonce + groupSize` is composed. Catch-up attached to a round after that diff is composed cannot carry those txs into settlement.

Until the pull exists, a resume with a lagging executor can settle that executor's live inferences at reserved cost.

</div>

---

> 🔄 **Auto-synced** from [Issue #2079](https://github.com/gonka-ai/gonka/issues/2079) every hour.
