---
title: "#1914 — pplying a diff copies the whole escrow state, and the copy grows for the life of the escrow"
source: https://github.com/gonka-ai/gonka/issues/1914
issue_number: 1914
synced_at: 2026-10-04T13:17:26Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    pplying a diff copies the whole escrow state, and the copy grows for the life of the escrow
    <span class="issues-number">#1914</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/a-kuprin">@a-kuprin</a> opened 2026-10-04 13:06 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-10-04 13:06 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #a2eeef; color: #24292f; border-color: #a2eeef;">enhancement</span></div>
</div>

<div class="issues-content" markdown="1">
# Applying a diff copies the whole escrow state, and the copy grows for the life of the escrow

## Summary

Every diff on a host with storage, and every diff the gateway composes, deep-copies the mutable escrow state twice. Most of that state stays small. Two maps do not: `sealedNonces` keeps one entry per sealed inference and is never trimmed, and `TurnTracker.heartbeatAt` keeps one entry per heartbeat nonce for the whole session. Both are copied on every diff.

The cost of applying a diff therefore grows with the escrow's history, not with the diff. Over the life of an escrow the total copy work grows roughly with the square of the number of sealed inferences. The discarded copies are also the main source of allocation and GC on this path.

This needs measurements before a fix. The fix changes how state is snapshotted and rolled back, and post-state roots have to stay byte-identical, so it should be its own change.

## What the apply path does

A host with a store applies a diff in `Host.applyAndPersist`:

1. `StateMachine.ValidateDiff` copies the mutable state (`pre`), applies the diff to the live maps, copies the result (`post`), then puts `pre` back.
2. The diff is persisted.
3. `StateMachine.CommitValidated` installs `post` by assigning the copied maps. It does not copy them again.

The gateway does the same thing in `StateMachine.PreviewLocalBestEffort` when it composes a diff, and `CommitValidated` installs that copy too.

`snapshotMutable` (`devshard/state/machine.go`) is the copy. It deep-copies:

| Copied | Bound |
| --- | --- |
| Live `Inferences`, including `PromptHash` and `ResponseHash` | In-flight and in-grace records only |
| `committedEntries` | Same window. Sealing deletes the entry (`seal.go`, auto-seal, `SealInference`, and the settlement drain). The field comment that says it keeps every inference ever created is out of date |
| `HostStats`, `WarmKeys` | One entry per slot |
| `sealedNonces` | One `uint64` to `uint64` per sealed inference. Nothing deletes these entries |
| `TurnTracker` (`turns`, `heartbeatAt`) | `turns` keeps the newest 64. `heartbeatAt` keeps one entry per heartbeat nonce for the session (`heightsync/turn.go`) |
| `FloorIndex.entries` | Capped at `DefaultFloorWindow` (4096) |

On a successful diff both copies are allocated. `post` becomes the live state and stays until the next diff replaces it. `pre`, and the previous live maps, become garbage immediately. Hosts without a store take one rollback snapshot inside `ApplyDiff` instead of this pair.

Go's heap profile reports in-use memory by the allocating stack, so the surviving copy shows up under `snapshotMutable`, `copyInferences`, and `cloneCommittedInferenceEntries`. That is the live escrow state. `cmd/devshardd/memwatch.go` notes this next to `topHeapInUse`.

## Why this is the next cost

A diff's CPU and allocation are proportional to `len(sealedNonces)` plus `len(heartbeatAt)`, on top of the live inference set. Those two maps only grow.

If an escrow seals on the order of its diff count, each new diff copies a larger map than the last, so the copies across the escrow add up quadratically. The garbage is the same size, so GC CPU and peak heap rise with it. `FloorIndex.Clone` already calls this out: it runs several times per diff on the apply hot path.

The live inference copy is real too, but it tracks concurrency, not history.

## Measure before changing it

The size of the problem depends on production numbers we do not have:

- `len(sealedNonces)` and `len(heartbeatAt)` on busy escrows, and how fast they grow.
- The live inference count per escrow.
- The diff rate.
- The share of CPU and allocations in `snapshotMutable` during `ValidateDiff` and `CommitValidated`.

A benchmark of `ValidateDiff` plus `CommitValidated` at about 1k, 10k, and 100k sealed inferences, read against a production heap and CPU profile, is enough to decide whether this is worth a release of its own.

`/stats/memory` already reports live and sealed inference counts per process, and the fattest escrow. It does not report `sealedNonces` or `heartbeatAt` sizes. Those two lengths are the missing series.

## Directions, once there is a number

Any of these keeps the trial apply off the live maps and has to leave `post_state_root` unchanged:

- An undo log for maps that only gain entries (`sealedNonces`, `heartbeatAt`), so a rollback deletes the keys added during the trial instead of cloning the whole map.
- Copy-on-write for those maps.
- Leaving `sealedNonces` out of the full snapshot if its only mutation on apply is insertion.

`Inferences` is still mutated in place and still needs a real copy or a copy-on-write map. That part stays proportional to the live set.
</div>

---

> 🔄 **Auto-synced** from [Issue #1914](https://github.com/gonka-ai/gonka/issues/1914) every hour.
