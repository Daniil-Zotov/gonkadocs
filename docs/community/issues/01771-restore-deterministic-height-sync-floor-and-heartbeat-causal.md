---
title: "#1771 — Restore deterministic height-sync floor and heartbeat causality state from snapshots"
source: https://github.com/gonka-ai/gonka/issues/1771
issue_number: 1771
synced_at: 2026-09-16T23:01:15Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Restore deterministic height-sync floor and heartbeat causality state from snapshots
    <span class="issues-number">#1771</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/anatoly-kuz-mntn">@anatoly-kuz-mntn</a> opened 2026-09-15 02:00 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-09-15 02:00 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Description

Snapshot recovery does not always reconstruct the same derived height-sync state as live application of the diff journal.

## Problem 1: sealed confirms are omitted during floor rebuild

During live application, a `MsgConfirmStart` is attributed while its inference record exists. During recovery, journal entries are processed against the final snapshot state. If the inference has been sealed, its record is absent and the confirm claim is skipped.

Affected code:

- [Journal-based height-sync rebuild](https://github.com/gonka-ai/gonka/blob/dfa3d30b44da938135f23d82b8d4a8291b2df7ca/devshard/state/heightsync.go#L259-L274)
- [Confirm attribution depends on a live inference record](https://github.com/gonka-ai/gonka/blob/dfa3d30b44da938135f23d82b8d4a8291b2df7ca/devshard/state/heightsync.go#L306-L328)

The executor can instead be derived from the deterministic group assignment using the inference ID.

## Problem 2: snapshot fallback loses heartbeat causality

When `GetDiffs` fails, recovery installs the saved floor and calls `SeedCompleted`. This restores summary counters but not the tracker’s `heartbeatAt` mapping.

L3 subsequently rejects valid acknowledgements whose `ref_nonce` points to a heartbeat created before the snapshot.

Affected code:

- [Snapshot-floor fallback](https://github.com/gonka-ai/gonka/blob/dfa3d30b44da938135f23d82b8d4a8291b2df7ca/devshard/state/heightsync.go#L276-L294)
- [`SeedCompleted` restores only summary state](https://github.com/gonka-ai/gonka/blob/dfa3d30b44da938135f23d82b8d4a8291b2df7ca/devshard/heightsync/turn.go#L496-L509)
- [L3 requires the heartbeat-to-turn mapping](https://github.com/gonka-ai/gonka/blob/dfa3d30b44da938135f23d82b8d4a8291b2df7ca/devshard/heightsync/logplane.go#L259-L281)

## Expected behavior

A replica restored from a snapshot must produce the same floor and acknowledgement-causality decisions as a replica that applied the complete journal live.

## Acceptance criteria

- Confirms belonging to sealed inferences are attributed during rebuild.
- `HeightSyncFloorAsOf` produces identical results before and after recovery.
- Snapshot data contains enough tracker state to validate retained pre-snapshot acknowledgements.
- Valid acknowledgements referencing pre-snapshot heartbeats pass L3.
- Recovery fails closed when neither the journal nor snapshot can reconstruct the required state.
</div>

---

> 🔄 **Auto-synced** from [Issue #1771](https://github.com/gonka-ai/gonka/issues/1771) every hour.
