---
title: "#344 — Intersection between update of `epoch_length` params and PoC procedure can lead to consensus failure"
source: https://github.com/gonka-ai/gonka/issues/344
issue_number: 344
synced_at: 2026-08-11T06:09:22Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Intersection between update of `epoch_length` params and PoC procedure can lead to consensus failure
    <span class="issues-number">#344</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2025-09-05 17:52 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-02-28 00:31 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
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
</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-01-28 22:26 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@DimaOrekhovPS or @patimen please give more details for this task</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-02-28 00:31 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@patimen please give more details for this task</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #344](https://github.com/gonka-ai/gonka/issues/344) every hour.
