---
title: "#819 — `application.db` growth / pruning"
source: https://github.com/gonka-ai/gonka/issues/819
issue_number: 819
synced_at: 2026-07-06T21:53:21Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    `application.db` growth / pruning
    <span class="issues-number">#819</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item">[@tcharchian](https://github.com/tcharchian) opened 2026-02-27 21:08 UTC</span>
    <span class="issues-meta-item">10 comments</span>
    <span class="issues-meta-item">Updated 2026-03-12 19:08 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span> <span class="issues-label" style="background-color: #008672; color: #ffffff; border-color: #008672;">help wanted</span> <span class="issues-label" style="background-color: #f86c7a; color: #24292f; border-color: #f86c7a;">Priority: High</span></div>
</div>

<div class="issues-content">

### Discussed in https://github.com/gonka-ai/gonka/discussions/817

<div type='discussions-op-text'>

<sup>Originally posted by **tcharchian** February 27, 2026</sup>

Task: `application.db` is growing unexpectedly; pruning does not appear to be effective. This impacts storage and performance.

Reports from multiple node operators indicate that block pruning is not reclaiming space as expected, which can result in continued growth of `application.db` and increased storage pressure. This issue tracks investigation, evidence gathering, and community-proposed mitigations. 

Sustained `application.db` growth can lead to:

- disk exhaustion and downtime
- performance degradation 
- more operational overhead during maintenance and upgrades

**Observations**
- Pruning may be configured, yet `application.db` continues to grow on some setups.
- Similar symptoms have been reported by multiple independent hosts
- The current state suggests a need to confirm whether this is:
    - a configuration issue,
    - expected retention behavior,
    - or a bug / unintended interaction 
    
**Goals**
- Identify the most likely cause(s) and validate them with reproducible evidence.
- Produce a short guide with:
    - recommended pruning settings (where applicable),
    - safe maintenance steps (e.g., compaction guidance),
    - monitoring suggestions (growth rate, alert thresholds).
- If a code-level change is justified, track it via linked PRs and governance-appropriate process.
</div>

---

## 💬 Comments (10)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@Mayveskii](https://github.com/Mayveskii)</span>
    <span class="issues-meta-item">commented 2026-03-03 07:58 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    I’d like to work on this issue, will start by reproducing application.db growth and investigating pruning behavior
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@AlexeySamosadov](https://github.com/AlexeySamosadov)</span>
    <span class="issues-meta-item">commented 2026-03-03 11:13 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    PR: https://github.com/gonka-ai/gonka/pull/846
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@Mayveskii](https://github.com/Mayveskii)</span>
    <span class="issues-meta-item">commented 2026-03-03 11:36 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    Root cause: application.db growth — code review + live data
TL;DR: Not a config problem. The pruning system silently deletes nothing on nodes that missed upgrade v0.2.4 (InferencePruningMax = 0 in DefaultEpochParams), and 9+ large collections were never pruned at all.
Live data (epochs 158–188, gonka.gg):
2.3M inferences over 31 epochs, peak 241K/epoch
Estimated application.db growth: ~7 GB (with payloads) / ~1.2 GB (metadata only)
Root causes in code:
InferencePruningMax = 0 by default (inference-chain/x/inference/types/params.go, DefaultEpochParams). On nodes without upgrade v0.2.4, pruning deletes zero records per block. The upgrade handler (app/upgrades/v0_2_4/upgrades.go) sets it to 5000 — but only for nodes that actually ran it.
Deprecated payload fields still stored on-chain. inference.proto still carries prompt_payload, response_payload, original_prompt inside every Inference written to application.db via SetInference.
9 large epoch-keyed collections never pruned. EpochPerformanceSummaries, ConfirmationPoCEvents, PoCValidationsV2, MLNodeWeightDistributions and others in keeper.go have zero pruning logic and grow unboundedly regardless of config.
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@Mayveskii](https://github.com/Mayveskii)</span>
    <span class="issues-meta-item">commented 2026-03-03 11:36 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    > PR: [#846](https://github.com/gonka-ai/gonka/pull/846)

were exactly working on it....

  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@AlexeySamosadov](https://github.com/AlexeySamosadov)</span>
    <span class="issues-meta-item">commented 2026-03-03 12:00 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    Summary of what was done in PR #846:

Root cause identified: **9 epoch-keyed collections were never pruned**, only 3 were cleaned up (Inferences, PoCBatches, PoCValidations v1). The unpruned collections:

1. PoCValidationsV2
2. PoCV2StoreCommits
3. MLNodeWeightDistributions
4. EpochGroupData
5. EpochGroupValidations
6. EpochPerformanceSummaries
7. ConfirmationPoCEvents
8. RandomSeeds
9. PoCValidationSnapshots

Additionally, `InferencePruningMax` and `PocPruningMax` defaulted to 0 in the proto definition, meaning pruning was **silently disabled** on any node that didn't receive the v0.2.4 upgrade handler.

Fix: extended `Prune()` to clean all 9 collections, added fallback default (5000) when configured max is zero, set sane defaults in `DefaultEpochParams()`. Tests added and passing.
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@sysmanalex](https://github.com/sysmanalex)</span>
    <span class="issues-meta-item">commented 2026-03-03 18:14 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    [!NOTE]
-  purning problem is part of IAVL bugs (will be fixed/can be - by migration to IAVLX v0.54) 100% 
Pruning isn't explicitly configured in app/app.go -> the Cosmos SDK default is used.

-  main reason for the growth of application.db - using one store for different tasks, creating a lot of cross locks and slowdown.

there stored: 
all epochs + task history
claims, rewards, top-miner calculations, PoC & account settlements.

The pruning mechanism is partially present (PruningEpochThreshold in types/params.go + Simple Pruning PR #226), but it's not fully implemented in EndBlocker and doesn't clean up old versions in IAVL. 
Therefore, pruning in app.toml "doesn't work," even though the config is valid.

Another reason - Pruning isn't explicitly configured in app/app.go -> the Cosmos SDK default is used 
btw default -> stores last 1 year (issue here, config and sets may fail).

[!TIP]
1. possible solutions, try to lower 
toml, [pruning] keep-recent = 50
db_backend = rocksdb !! or I suggest to try pebbleDB ! 
  - GoLevelDB very bad on compacting records/pruning ! 
check https://github.com/cosmos/cosmos-sdk/blob/main/docs/architecture/adr-065-store-v2.md
>Physical DB Backends
>This ADR proposes usage of RocksDB to utilize user-defined timestamps as a versioning mechanism. However, other >physical DB backends are available that may offer alternative ways to implement versioning while also providing >performance improvements over RocksDB. E.g. PebbleDB supports MVCC timestamps as well, but we'll need to explore >how PebbleDB handles compaction and state growth over time.

[!TIP]
2. better solution - Split Application.db for LOGICAL parts - that's has even more meaning.

InferenceKeeper, CollateralKeeper, and Training/Calculations modules are the main culprits of this growth.

Option1: // separate inference IAVL Store - even on separate disk/path.
```
inferenceStoreKey := storetypes.NewKVStoreKey("inference")
app.CommitMultiStore().MountStoreWithDB(inferenceStoreKey, storetypes.StoreTypeDB, pebbleDB)

pebbleDB, _ := dbm.NewDB("inference-data", dbm.PebbleDB, appOpts.Get("data-dir")+"/inference")
```
or similar options 
// 1. Separate StoreKey + DB
```
inferenceStoreKey := sdk.NewKVStoreKey(inferencetypes.StoreKey)
```
// 2. Mount with separate backend (Pebble/RocksDB)
```
app.MountStoreWithDB(inferenceStoreKey, sdk.StoreTypeIAVL, pebbleDB)
```
// 3. Store v2 (SDK ≥0.50) separate SS/SC
```
app.SetStoreLoader(store.NewCommitKVStoreLoader(inferenceStoreKey, customPruningOptions))
```
[!TIP]
Result: separate file, for heavy inference.db - easy to prun, less locks, more performance.
application.db will become 3-5x smaller and will be more properly used.

[!IMPORTANT]
best in class solution -  IAVLX (SDK v0.54+) commit 20ms vs 150++ms.
iavl-cache-size = 5000000 в app.toml // more RAM better.
inter-block-cache = true


p.s. I can make sample code for inference/end_blocker/keeper.go if needed. but upper should work fine and fix problem asap. 

  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@gmorgachev](https://github.com/gmorgachev)</span>
    <span class="issues-meta-item">commented 2026-03-04 00:00 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    > Root cause: application.db growth — code review + live data TL;DR: Not a config problem. The pruning system silently deletes nothing on nodes that missed upgrade v0.2.4 (InferencePruningMax = 0 in DefaultEpochParams), and 9+ large collections were never pruned at all. Live data (epochs 158–188, gonka.gg): 2.3M inferences over 31 epochs, peak 241K/epoch Estimated application.db growth: ~7 GB (with payloads) / ~1.2 GB (metadata only) Root causes in code: InferencePruningMax = 0 by default (inference-chain/x/inference/types/params.go, DefaultEpochParams). On nodes without upgrade v0.2.4, pruning deletes zero records per block. The upgrade handler (app/upgrades/v0_2_4/upgrades.go) sets it to 5000 — but only for nodes that actually ran it. Deprecated payload fields still stored on-chain. inference.proto still carries prompt_payload, response_payload, original_prompt inside every Inference written to application.db via SetInference. 9 large epoch-keyed collections never pruned. EpochPerformanceSummaries, ConfirmationPoCEvents, PoCValidationsV2, MLNodeWeightDistributions and others in keeper.go have zero pruning logic and grow unboundedly regardless of config.


> n nodes that missed upgrade v0.2.4

This parameter stored on chain => all nodes who in sync with chain will use the one from 0.2.4 upgrade handler 




  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@Lelouch33](https://github.com/Lelouch33)</span>
    <span class="issues-meta-item">commented 2026-03-04 09:32 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    ## Fix: pruning freeze caused by gaps in `pruneSnapshotHeights`

### Summary

When a snapshot creation is missed (network failure, disk full, timeout, node restart), a gap appears in the `pruneSnapshotHeights` array. The existing chain-trimming logic in `HandleSnapshotHeight` stops at the first gap, so `pruneSnapshotHeights[0]` never advances — permanently freezing pruning and causing unbounded DB growth.

This fix adds a `for` loop that removes any stale leading height where the gap to the next element exceeds `snapshotInterval`. It handles all known failure scenarios: fresh state-sync (`[0]=0`), missed snapshots at any position, and multiple consecutive gaps.

---

### Root Cause

`GetPruningHeight` uses `pruneSnapshotHeights[0]` to cap the maximum height IAVL will prune to:

```go
snHeight := pruneSnapshotHeights[0] + snapshotInterval - 1
```

`HandleSnapshotHeight` maintains the array: it appends the new height, sorts, and trims a contiguous chain from the start. The chain-trimming logic walks from `[0]` and removes elements as long as `[k+1] == [k] + snapshotInterval`. It breaks at the first gap.

**The problem:** when a snapshot is missed, a gap appears. Chain trimming stops at that gap — `[0]` never advances past it. All subsequent heights accumulate, but `GetPruningHeight` remains capped at the stale `[0] + snapshotInterval - 1`. IAVL versions pile up, DB grows without bound.

This affects two scenarios:
1. **Fresh state-sync:** `NewManager` initializes the array with `[0]`. The first real snapshot (e.g., height 2900000) creates a massive gap `[0, 2900000]` — chain trimming never removes `0`.
2. **Missed snapshots during operation:** if snapshot creation takes longer than the snapshot interval (common when snapshot creation overlaps with the next interval), a height is skipped, creating a gap mid-array that permanently stalls pruning.

### Production data (read from `application.db`, key `s/prunesnapshotheights`)

```
104 heights, 4 gaps:
[0]  = 2809000  → [1]  = 2811000  (missing 2810000)
[13] = 2823000  → [14] = 2825000  (missing 2824000)
[22] = 2833000  → [23] = 2835000  (missing 2834000)
[86] = 2898000  → [87] = 2900000  (missing 2899000)

GetPruningHeight capped at: 2809000 + 1000 - 1 = 2809999
Current height: ~2918000 → ~108,000 unpruned versions
DB growth: 420 GB → 611 GB (and rising)
```

Gaps are caused by snapshot creation conflicts — creation takes 1.5–2.5h while `snapshot-interval=1000` blocks is ~1.4h, so roughly every other snapshot fails to complete before the next one starts.

---

### The Fix

Add a `for` loop at the beginning of `HandleSnapshotHeight` (after sort, before chain trimming) that evicts stale leading heights:

```go
// Remove stale leading heights where the gap to the next element
// exceeds snapshotInterval — indicating missed intermediate snapshots
// (network failure, disk full, node restart, fresh state-sync, etc.).
// Without this, pruneSnapshotHeights[0] permanently caps
// GetPruningHeight at [0] + snapshotInterval - 1.
for len(m.pruneSnapshotHeights) > 1 &&
    m.pruneSnapshotHeights[1]-m.pruneSnapshotHeights[0] > int64(m.snapshotInterval) {
    m.pruneSnapshotHeights = m.pruneSnapshotHeights[1:]
}
```

The rest of `HandleSnapshotHeight` (chain trimming) is unchanged.

**How it works:**
- The loop checks if the gap between `[0]` and `[1]` is larger than `snapshotInterval`
- If yes, `[0]` is stale (intermediate snapshots were missed) — remove it
- Repeat until the leading pair is contiguous or only one element remains
- Then the existing chain-trimming logic runs normally

**What it covers:**

```
┌─────────────────────────────┬──────────────────────────────────────────────────────────────┬─────────┐
│ Scenario                    │ Example                                                      │ Handled │
├─────────────────────────────┼──────────────────────────────────────────────────────────────┼─────────┤
│ Fresh state-sync ([0]=0)    │ [0, 2900000] → gap 2900000 > 1000 → remove 0                 │ Yes     │
│ Single missed snapshot      │ [2809000, 2811000, ...] → gap 2000 > 1000 → remove 2809000   │ Yes     │
│ Multiple consecutive gaps   │ Gaps at positions 0, 13, 22, 86 → resolved progressively     │ Yes     │
│ Normal operation (no gaps)  │ [2900000, 2901000] → gap 1000, not > 1000 → no-op            │ Yes     │
└─────────────────────────────┴──────────────────────────────────────────────────────────────┴─────────┘
```

**Mid-array gaps** are handled progressively: each `HandleSnapshotHeight` call resolves the leading gap, then chain trimming runs until the next gap. On the next call, that gap becomes the new leading gap and gets resolved. With `snapshotInterval=1000`, all gaps are cleared within a few snapshots.

---

### How it's applied

The fix patches `cosmossdk.io/store@v1.1.2` via Go `replace` directive:

```go
// inference-chain/go.mod
replace cosmossdk.io/store v1.1.2 => ./store-patched
```

`store-patched/` is a copy of the upstream module with only `pruning/manager.go` modified.

---

### Test Results

**Test server** — 3 nodes running in parallel, all state-synced, GoLevelDB, `pruning=custom`, `keep-recent=1000`, `interval=100`. Measured at height ~2927190:

```
┌────────┬─────────────────────────────────┬────────────────┐
│ Node   │ Version                         │ application.db │
├────────┼─────────────────────────────────┼────────────────┤
│ node-d │ Stock (no fix)                  │ 87 GB (growing)│
│ node-c │ Fix applied                     │ 24 GB (stable) │
│ node-e │ Fix applied (fresh state-sync)  │ 33 GB (stable) │
└────────┴─────────────────────────────────┴────────────────┘
```

Node-e was deployed as a fresh state-sync from height 2919000 — synced successfully, blocks processing, pruning active. The 33 GB size (vs node-c's 24 GB) is due to GoLevelDB compaction lag after recent state-sync restore.

**Production** (height 2927195) — deployed via cosmovisor binary replacement. `application.db` = 37 GB, stable.

Production DB recovery after fix:
```
611 GB → 498 GB → 425 GB → 430 GB → 37 GB (stable after full compaction)
```

---

### Traces

<details>
<summary>Trace: production data (104 heights, 4 gaps)</summary>

```
Input: [2809000, 2811000, 2812000, ..., 2898000, 2900000, ..., 2916000]

Gap removal (for loop):
  Iter 1: 2811000-2809000=2000 > 1000 → remove 2809000
  Iter 2: 2812000-2811000=1000, not > 1000 → stop
  Result: [2811000, 2812000, ..., 2916000]

Chain trimming:
  k=1:  2812000 == 2811000+1000 OK
  ...
  k=12: 2823000 == 2822000+1000 OK
  k=13: 2825000 != 2823000+1000 → break
  Result: [2823000, 2825000, ..., 2916000]

After first HandleSnapshotHeight: [0]=2823000
GetPruningHeight: 2823000+999 = 2823999 (was 2809999)

Next call removes gap at 2823000→2825000:
GetPruningHeight: 2833999

After 4 snapshots (~4000 blocks, ~20 min): fully caught up.
```

</details>

<details>
<summary>Trace: fresh state-sync ([0]=0)</summary>

```
NewManager → [0]

HandleSnapshotHeight(2900000):
  sort → [0, 2900000]
  Gap: 2900000-0=2900000 > 1000 → remove 0 → [2900000]
  Result: [2900000]

HandleSnapshotHeight(2901000):
  sort → [2900000, 2901000]
  Gap: 1000, not > 1000 → skip
  Chain: contiguous → [2901000]
```

</details>

<details>
<summary>Trace: normal operation (no gaps)</summary>

```
[2900000] → HandleSnapshotHeight(2901000):
  sort → [2900000, 2901000]
  Gap: 1000, not > 1000 → skip
  Chain: contiguous → [2901000]

Steady state: array has 1 element, advances with each snapshot.
```

</details>

  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@gmorgachev](https://github.com/gmorgachev)</span>
    <span class="issues-meta-item">commented 2026-03-05 06:23 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    @Lelouch33 seems like that really solves problem, let's finalize details and make compartible release
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@Lelouch33](https://github.com/Lelouch33)</span>
    <span class="issues-meta-item">commented 2026-03-05 23:22 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    https://github.com/gonka-ai/gonka/pull/867
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #819](https://github.com/gonka-ai/gonka/issues/819) every hour.
