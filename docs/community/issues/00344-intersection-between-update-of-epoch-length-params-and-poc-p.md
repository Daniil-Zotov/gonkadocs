---
title: "#344 — Intersection between update of `epoch_length` params and PoC procedure can lead to consensus failure"
source: https://github.com/gonka-ai/gonka/issues/344
issue_number: 344
synced_at: 2026-07-06T09:52:47Z
template: issues-main.html
---

> 🔄 **Auto-synced:** from [Issue #344](https://github.com/gonka-ai/gonka/issues/344) every 6 hours. 

# 🟢 Intersection between update of `epoch_length` params and PoC procedure can lead to consensus failure

**Author:** [@tcharchian](https://github.com/tcharchian) · **State:** Open · **Created:** 2025-09-05 17:52 UTC · **Updated:** 2026-02-28 00:31 UTC

---

## 📝 Описание

- [consensus-failure-epoch-length.log](https://github.com/user-attachments/files/22176980/consensus-failure-epoch-length.log)
- https://github.com/gonka-ai/gonka/blob/f0a36298bddf8ba7f924b30ac289ad7f50a7a8d8/inference-chain/x/inference/keeper/power.go#L53
```
node      | 1:53AM INF NewPocStart blockHeight=446 module=x/inference subsystem=Stages
node      | 1:53AM ERR CreateEpochGroup: Root epoch group data already exists epochIndex=3 module=x/inference subsystem=EpochGroup
node      | 1:53AM ERR Unable to create epoch group error="epoch group data already exists for the given poc start block height and model id" module=x/inference subsystem=EpochGroup
node      | 1:53AM ERR error in proxyAppConn.FinalizeBlock err="epoch group data already exists for the given poc start block height and model id" module=state
node      | 1:53AM ERR CONSENSUS FAILURE!!! err="failed to apply block; error epoch group data already exists for the given poc start block height and model id" module=consensus stack="goroutine 49 [running]:\nruntime/debug.Stack()\n\t/usr/local/go/src/runtime/debug/stack.go:26 +0x5e\ngithub.com/cometbft/cometbft/consensus.(*State).receiveRoutine.func2()\n\t/go/pkg/mod/github.com/cometbft/cometbft@v0.38.17/consensus/state.go:801 +0x46\npanic({0x4a030e0?, 0xc00213e990?})\n\t/usr/local/go/src/runtime/panic.go:785 +0x132\ngithub.com/cometbft/cometbft/consensus.(*State).finalizeCommit(0xc002e39508, 0x1be)\n\t/go/pkg/mod/github.com/cometbft/cometbft@v0.38.17/consensus/state.go:1781 +0xde5\ngithub.com/cometbft/cometbft/consensus.(*State).tryFinalizeCommit(0xc002e39508, 0x1be)\n\t/go/pkg/mod/github.com/cometbft/cometbft@v0.38.17/consensus/state.go:1682 +0x2e8\ngithub.com/cometbft/cometbft/consensus.(*State).enterCommit.func1()\n\t/go/pkg/mod/github.com/cometbft/cometbft@v0.38.17/consensus/state.go:1617 +0x9c\ngithub.com/cometbft/cometbft/consensus.(*State).enterCommit(0xc002e39508, 0x1be, 0x0)\n\t/go/pkg/mod/github.com/cometbft/cometbft@v0.38.17/consensus/state.go:1655 +0xc2f\ngithub.com/cometbft/cometbft/consensus.(*State).addVote(0xc002e39508, 0xc002d001a0, {0xc0040a4060, 0x28})\n\t/go/pkg/mod/github.com/cometbft/cometbft@v0.38.17/consensus/state.go:2343 +0x1e8d\ngithub.com/cometbft/cometbft/consensus.(*State).tryAddVote(0xc002e39508, 0xc002d001a0, {0xc0040a4060?, 0x0?})\n\t/go/pkg/mod/github.com/cometbft/cometbft@v0.38.17/consensus/state.go:2067 +0x26\ngithub.com/cometbft/cometbft/consensus.(*State).handleMsg(0xc002e39508, {{0x620d620, 0xc003e34590}, {0xc0040a4060, 0x28}})\n\t/go/pkg/mod/github.com/cometbft/cometbft@v0.38.17/consensus/state.go:929 +0x38b\ngithub.com/cometbft/cometbft/consensus.(*State).receiveRoutine(0xc002e39508, 0x0)\n\t/go/pkg/mod/github.com/cometbft/cometbft@v0.38.17/consensus/state.go:836 +0x3f1\ncreated by github.com/cometbft/cometbft/consensus.(*State).OnStart in goroutine 1\n\t/go/pkg/mod/github.com/cometbft/cometbft@v0.38.17/consensus/state.go:398 +0x10c\n"
node      | 1:53AM INF service stop impl=baseWAL module=consensus msg="Stopping baseWAL service" wal=/root/.inference/data/cs.wal/wal
```

---

## 💬 Comments (2)

### Комментарий 1 — [@tcharchian](https://github.com/tcharchian)

*2026-01-28 22:26 UTC*

@DimaOrekhovPS or @patimen please give more details for this task

### Комментарий 2 — [@tcharchian](https://github.com/tcharchian)

*2026-02-28 00:31 UTC*

@patimen please give more details for this task


