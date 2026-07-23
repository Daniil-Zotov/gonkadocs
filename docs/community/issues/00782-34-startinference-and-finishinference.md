---
title: "#782 — [3/4] `StartInference` and `FinishInference`"
source: https://github.com/gonka-ai/gonka/issues/782
issue_number: 782
synced_at: 2026-07-23T22:19:31Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    [3/4] `StartInference` and `FinishInference`
    <span class="issues-number">#782</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-02-20 22:37 UTC</span>
    <span class="issues-meta-item">5 comments</span>
    <span class="issues-meta-item">Updated 2026-03-11 20:01 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #f86c7a; color: #24292f; border-color: #f86c7a;">Priority: High</span> <span class="issues-label" style="background-color: #9214a6; color: #ffffff; border-color: #9214a6;">requires own mainnet node</span></div>
</div>

<div class="issues-content" markdown="1">
# Background

`MsgStartInference` and `MsgFinishInference` are too slow in production. Blocks should be processed by nodes within 1-2 seconds, so that block time stays below 6 seconds. This means that to process 1000 inferences in a block, we need to record 1000 `MsgStartInference`, 1000 `MsgFinishInference`, and 100-200 `MsgValidation` transactions. This means that these transactions should be processed faster than 1ms. Even though they are quite fast in tests, in production with a large state they require 10-20ms, and on some nodes 50ms or more.

There are 2 main areas identified that contribute most of the time to transactions:
- Signatures validation (57% of `FinishInference` and 63% of `StartInference`)
- Stats query and recording (40% of `FinishInference` and 30% of `StartInference`)

Download profiling file:
https://drive.google.com/file/d/1yxY91lzMHxv_MeloAxW1zczcpbkBjZ0t/
And use command:
```
go tool pprof -http=:8080 /Users/davidliberman/Downloads/pprof.inferenced.samples.cpu.001.pb.gz
```

And choose flame graph to explore

Screen recoding: https://drive.google.com/file/d/1yxDaJllxCQ-l3ZO6ZuBb5bTEUgZ5t7Yu/view?usp=sharing

_**Signature validation**_ can be significantly optimized, reducing the number of signatures to be validated in most scenarios by 5x (from 5 signatures to just 1).

https://github.com/gonka-ai/gonka/issues/608 - which is now implemented by @DimaOrekhovPS

https://github.com/gonka-ai/gonka/pull/779 

**_Stats query and recording_** is designed to make it easier to query usage statistics for inference operations by storing this data on a chain. However, it is too heavy for on-chain operations and should be removed. In the end, we shouldn't read and write any large state record in `MsgStartInference`, `MsgFinishInference`, or `MsgValidation`.

`SetInference` (including the second time it is executed in `HandleInferenceComplete`): 
- 10% of `FinishInference`, 
- 12% of `StartInference`, 
- 4% of Validation
- 33% is Logging, 
- 38% `SetOrUpdateInferenceStatsByEpoch`, 
- 22% `SetOrUpdateInferenceStatusByTime` w/o logging

`HandleInferenceComplete`, excluding `SetInference`, accounts for 16% of `FinishInference` and 4% of `StartInference` (as it is rare for `StartInference` to come second).
- 20% is Logging
- 45% is 2xGetEpochGroupData
- 5% GetEpochIndex
- 10% SetEpochGroupData, 
- 20% SetParticipant/GetParticipants w/o logging

`ProcessInferencePayment`: 14% of `FinishInference` and 12% of `StartInference` 
- 63% is Logging
- 18% `SetParticipant`/2x`GetParticipant` w/o logging
- 9% Add/GetTokenomicsData

# Tasks:
In `HandleInferenceComplete`, we also read `GetEpochGroupData` to add `ExecutorReputation`, `ExecutorPower`, and `TotalPower` (of the model group) to `InferenceValidationDetails`, which is then saved for future validation. We also increment `NumberOfRequests` of the epoch group and save it. This operation should also be moved to the `EndBlocker`. Execute `GetEpochGroup` (main and for each required models) and `SetEpochGroup` only once per block.

We should add a key Block+InferenceId in `HandleInferenceComplete` then iterate through  the keys to get Inferences by id during `EndBlocker` to store `InferenceValidationDetails` (clean keys immediately in the `EndBlocker` after the iteration).

After moving those operations to the `EndBlocker`, we need to validate if the endblocker time won't be increased significantly by the action (though adding `GetInference` iterations to `EndBlock` without changing state during transactions) - it should take not more than 50-100ms for 1000 inferences in a mainnet node. The test can be done by adding the read operations to `EndBlocker` mainnet node but without set operation, so that state of the node will stay the same.

# Important
This issue is one of five issues in the [0/4] StartInference and FinishInference series (and correspondingly [1/4], [2/4], [3/4], [4/4]).
These tasks can be completed independently of each other by different contributors.
However, this specific task requires maintaining and operating a node on mainnet in order to test and validate the result.

All five issues [0/4], [1/4], [2/4], [3/4], [4/4] in this series must be completed as part of the v0.2.11 upgrade, which is scheduled for the week of February 23. After the v0.2.11 upgrade, these tasks will no longer be relevant, because a different solution can/will be proposed.
</div>

---

## 💬 Comments (5)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-02-20 22:41 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>If you’re ready to take this task on, please leave a comment here so other community members can see it’s already being worked on.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/akup">@akup</a></span>
    <span class="issues-meta-item">commented 2026-02-21 15:27 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>I will take it</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/akup">@akup</a></span>
    <span class="issues-meta-item">commented 2026-02-24 05:29 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@libermans I've found that EpochGroupData should be read/write once in a lot of places. It is a relatively large structure and we should optimize on its decoding/encoding on read/write to store.</p>
<p>Moreover there are places where we do not read EpochGroupData but should to. Every operation that is intended to be called by active participant should be checked for was the message came from real active participant. For example StartInference message could be runned by any developer account (currently there is a TA whitelist that blocks this vulnarability, but after removing this whitelist it will be reopened). So any account can start inferences that will not be finished and any honest participant could be slashed. Same thing for validation/invalidation/revalidation.
But the main point that we very often need to read EpochGroupData to check if message came from active participant (ConfirmationWeight &gt; 0)</p>
<p>So I've implemented a more generic approach using EpochGroupData 2level caches: per-tx cache + per-block cache. We read/write EpochGroupData once to store. Tx-draft-cache is needed because tx can be reverted so we first store in context-binded memory all changes and commit them to per-block cache when tx succeeds. Finally we write the per-block cache at EndBlocker and clear it on block start.</p>
<p>More detailed description is attached to PR, also there is explanation on cosmos SDK optimistic mode, to run txs in parallel on multicore CPUs.</p>
<p>Added PR here: https://github.com/gonka-ai/gonka/pull/793
Currently i'm taking it to tests on running node</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/akup">@akup</a></span>
    <span class="issues-meta-item">commented 2026-02-24 06:12 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@libermans
Do we really need to move InferenceValidationDetails to EndBlocker?
If the only purpose is to have precise value at
<code>TrafficBasis:         uint64(math.Max(currentEpochGroup.GroupData.NumberOfRequests, currentEpochGroup.GroupData.PreviousEpochRequests))</code></p>
<p>it seams to be not a lot of meaning, as this value changes every block and it could be ok to use previous block value.</p>
<p>I understand that the idea was to move reading and writing currentEpochGroup.GroupData to endBlocker to make it once in one place, but if using caches that are aimed to solve same problem more generically, maybe we could keep updating <code>InferenceValidationDetails</code> in message handling without moving to EndBlocker?</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/gmorgachev">@gmorgachev</a></span>
    <span class="issues-meta-item">commented 2026-03-11 20:01 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>The big part of inference flow optimization is merged in https://github.com/gonka-ai/gonka/pull/812
I'm closing all <code>[*/4] StartInference and FinishInference: optimiziation</code> tasks to finalize this work in milestone 0.2.11. I think it'd be better to re-open in case of additinal optimizations required</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #782](https://github.com/gonka-ai/gonka/issues/782) every hour.
