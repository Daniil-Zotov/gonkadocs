---
title: "#632 — State sync snapshots corrupted - all snapshots fail on last 2 chunks (826-827/827)"
source: https://github.com/gonka-ai/gonka/issues/632
issue_number: 632
synced_at: 2026-07-06T09:52:08Z
template: issues-main.html
---

> 🔄 **Auto-synced:** from [Issue #632](https://github.com/gonka-ai/gonka/issues/632) every 6 hours. 

# 🟢 State sync snapshots corrupted - all snapshots fail on last 2 chunks (826-827/827)

**Author:** [@baranskyi](https://github.com/baranskyi) · **State:** Open · **Created:** 2026-01-24 15:11 UTC · **Updated:** 2026-04-29 01:16 UTC

---

## 📝 Описание

## Summary

State sync fails for all available snapshots (2309000, 2310000) - the last 2 chunks (826-827 out of 827) are either corrupted or unavailable, causing nodes to crash with IAVL store panic.

## Environment

- **Node Version:** inferenced:0.2.7-post1
- **OS:** Arch Linux (Docker)
- **Participant Address:** gonka18xk4m8t0zj9vpse5c2dem8uxhqw0egtjuafy77

## Error Details

### Panic Message
```
panic: failed to load latest version: failed to load store: version does not exist [/go/pkg/mod/cosmossdk.io/store@v1.1.2/rootmulti/store.go:264]
```

### Behavior
1. State sync discovers snapshots (2309000, 2310000, etc.)
2. Node selects the latest snapshot
3. Downloads chunks successfully up to ~825/827
4. Last 2 chunks (826, 827) either timeout or are corrupted
5. Node attempts to apply incomplete snapshot
6. IAVL store fails to load, node panics
7. Node restarts and repeats the cycle

### Logs showing the issue
```
INF Applied snapshot chunk to ABCI app chunk=825 format=3 height=2309000 module=statesync total=827
INF Fetching snapshot chunk chunk=826 format=3 height=2309000 module=statesync total=827
INF Saving AddrBook to file...
INF Ensure peers module=pex numDialing=0 numInPeers=0 numOutPeers=10 numToDial=0
[No more chunks applied - node eventually crashes]

panic: failed to load latest version: failed to load store: version does not exist
```

## Affected Snapshots

Tested snapshots - ALL fail with same issue:
- **2310000** - fails on chunks 826-827
- **2309000** - fails on chunks 826-827
- **2308000** - same issue
- **2305000** - same issue

## Attempted Workarounds

1. ❌ Changed RPC servers (node1, node2, node3.gonka.ai) - same result
2. ❌ Reduced discovery_time to pick different snapshot - still selects problematic ones
3. ❌ Set trust_height to older blocks - node still picks latest snapshot from peers
4. ❌ Disabled state sync (block sync from genesis) - impractical for 2.3M blocks
5. ❌ Waited for new snapshot (2310000) - same corruption pattern

## Impact

- **Severity:** Critical - Unable to sync new nodes
- **Scope:** Affects all new node operators attempting state sync
- **Duration:** Issue observed for multiple hours across different snapshot heights

## Suspected Cause

The issue appears to be network-wide - all peers offer the same corrupted snapshots. Possible causes:
1. Snapshot creation nodes have disk/memory issues affecting last chunks
2. P2P propagation issue for final chunks
3. Bug in snapshot chunking algorithm

## Request

1. Investigate snapshot creation on validator nodes
2. Consider creating fresh snapshots with verified integrity
3. Add chunk verification/retry mechanism for failed chunks

## Reproduction Steps

```bash
# 1. Clean node data
docker stop node
rm -rf .inference/data/* .inference/wasm/*

# 2. Ensure state sync is enabled in config.toml
# enable = true

# 3. Start node
docker start node

# 4. Observe logs - sync will fail on chunks 826-827
docker logs -f node
```

## Additional Context

- Node was previously synced and working until container crashed
- Multiple restart attempts over several hours all fail identically
- Network is currently at height ~2,310,000+
- 10 peers connected during sync attempts

---

## 💬 Comments (5)

### Комментарий 1 — [@AlexeySamosadov](https://github.com/AlexeySamosadov)

*2026-01-24 21:47 UTC*

## Analysis of State Sync Snapshot Corruption

I investigated this issue and found the following:

### Root Cause Location

The snapshot chunking and restoration logic is **not** in the `inference-chain` repository. It's in the custom Cosmos SDK fork:

```
github.com/gonka-ai/cosmos-sdk v0.53.3-ps15
```

The `inference-chain` only registers the WASM snapshotter in `app/app.go`, all chunking logic is delegated to the SDK.

### Why Last Chunks Fail

The failure on the last 2 chunks (826-827/827) suggests the chunks haven't fully propagated across the network yet after snapshot creation. Possible causes:

- Chunk boundary handling in the custom SDK fork
- IAVL export finalization timing
- Network propagation delay for newest chunks

### Solution

The issue resolves itself by **waiting approximately 1 hour**. After that, the chunks synchronize automatically and state sync completes successfully.

This is likely a propagation timing issue rather than data corruption - the snapshot needs time to fully distribute across the network before all chunks become consistently available.

### Комментарий 2 — [@gmorgachev](https://github.com/gmorgachev)

*2026-01-27 06:53 UTC*

When some existing node providing snapshot to another node, it already has full snapshot, all chunks. It's not really propagated more then to this P2P request. Snapshots are downloaded directly.

### Комментарий 3 — [@AlexeySamosadov](https://github.com/AlexeySamosadov)

*2026-02-04 11:46 UTC*

## Root Cause Found

The issue is a race condition between snapshot pruning and chunk serving during state sync.

### What happens

1. Snapshot at height H is complete (all 827 chunks on disk, metadata in DB)
2. Peer starts downloading chunks: 0, 1, 2, ... 825
3. New snapshot at H+1000 finishes creating in a background goroutine
4. `Prune(keepRecent)` runs immediately after, calling `os.RemoveAll` on snapshot H directory
5. Peer requests chunks 826-827 → files already deleted → `LoadChunk` returns nil
6. CometBFT sends `Missing: true`, peer times out after 2 minutes
7. After ~1 hour the new snapshot is available and sync succeeds

### Why it's always the last chunks

Chunks are downloaded sequentially (0→N). The peer manages to download most chunks before pruning kicks in, but the tail end gets deleted mid-transfer.

### Why `LoadChunk` doesn't protect against this

- `LoadChunk` runs lock-free, does not check if pruning is in progress
- `Delete`/`Prune` only check if a snapshot is being *saved*, not if it's being *served*
- No read-side reference counting exists

### Fix

PR with the fix: https://github.com/gonka-ai/cosmos-sdk/pull/10

Adds read-side reference counting to the snapshot `Store`: `Delete` now waits for active `LoadChunk` readers to finish before removing files from disk.

### Комментарий 4 — [@AlexeySamosadov](https://github.com/AlexeySamosadov)

*2026-02-09 18:00 UTC*

@gmorgachev The fix is ready and waiting for review: https://github.com/gonka-ai/cosmos-sdk/pull/10

Adds read-side reference counting to the snapshot Store so that Prune/Delete waits for active LoadChunk readers to finish before removing files from disk. This prevents the race condition that causes the last chunks to disappear mid-download.

### Комментарий 5 — [@AlexeySamosadov](https://github.com/AlexeySamosadov)

*2026-02-09 18:00 UTC*

Also — is the reference counting approach the right direction here, or would you prefer a different strategy (e.g. copy-on-write, or delaying prune until no active sync sessions)?
