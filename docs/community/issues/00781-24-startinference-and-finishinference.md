---
title: "#781 — [2/4] `StartInference` and `FinishInference`"
source: https://github.com/gonka-ai/gonka/issues/781
issue_number: 781
synced_at: 2026-07-22T03:52:49Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    [2/4] `StartInference` and `FinishInference`
    <span class="issues-number">#781</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-02-20 22:26 UTC</span>
    <span class="issues-meta-item">13 comments</span>
    <span class="issues-meta-item">Updated 2026-03-11 20:01 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #f86c7a; color: #24292f; border-color: #f86c7a;">Priority: High</span></div>
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
- 14% of Validation
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
We do `SetInference` twice in the main function of the `StartInference` and `FinishInference` messages, as well as in `HandleInferenceComplete` for the second Start/Finish. We can execute it once.

We should move `SetDeveloperStats` with `SetOrUpdateInferenceStatsByEpoch` and `SetOrUpdateInferenceStatusByTime` from `SetInference` to off-chain (store the data on api node). The stored structures are quite big for the on-chain storage.

Add the required data to the emitted event in `HandleInferenceComplete` (inference_finished event), and adjust the event listener on api nodes to collect this data and store it independently (look for storage we use for payload storage on api node). Check which endpoints are used by the dashboard, and see if we need to store the per-inference stats (like we do now), or only per block/model cumulative stats.

# Important
This issue is one of five issues in the [0/4] StartInference and FinishInference series (and correspondingly [1/4], [2/4], [3/4], [4/4]).
These tasks can be completed independently of each other by different contributors.
This specific task does not requires maintaining and operating a node on mainnet in order to test and validate the result.

All five issues [0/4], [1/4], [2/4], [3/4], [4/4] in this series must be completed as part of the v0.2.11 upgrade, which is scheduled for the week of February 23. After the v0.2.11 upgrade, these tasks will no longer be relevant, because a different solution can/will be proposed.
</div>

---

## 💬 Comments (13)

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
    <span class="issues-meta-item">commented 2026-02-21 04:08 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>It is important to mention, that SetInference -&gt; SetDeveloperStats are also called at validation, revalidation, invalidation.
There we only change the status of the existing inference.
So when we move DevelopersStats off-chain, we also should handle validation events (and emit new events if needed).</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/libermans">@libermans</a></span>
    <span class="issues-meta-item">commented 2026-02-21 05:20 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Yes, correct. </p>
<p>Also DeveloperStats are used for DynamicPricing and MaximumInvalidationsReached, we should use some optimal storage for that values but likely should be implemented after both this task and https://github.com/gonka-ai/gonka/issues/782 finished.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/x0152">@x0152</a></span>
    <span class="issues-meta-item">commented 2026-02-22 12:02 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>I'd like to take this on and start with draft #788. I'm ready to pass ownership If someone has a stronger approach</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/x0152">@x0152</a></span>
    <span class="issues-meta-item">commented 2026-02-23 21:14 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>With stats computation moved off-chain, StatsByTimePeriodByDeveloper and StatsByDeveloperAndEpochsBackwards will only return legacy data no longer updated after cutover (kept for compatibility). Do we need new dapi endpoints for per-developer stats from the local store, or is that out of scope now?</p>
<p>StatsByTimePeriodByDeveloper and StatsByDeveloperAndEpochsBackwards are not called internally (only InferencesAndTokensStatsByModels is used by pricing)</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/libermans">@libermans</a></span>
    <span class="issues-meta-item">commented 2026-02-24 00:53 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Per-developer. I don't think we use it now anywhere, so out of scope likely</p>
<p>For DynamicPricing and MaximumInvalidationsReached we need an on-chain storage, I would say with rolling sum for X blocks (the amount of blocks we get from params for DynamicPricing and MaximumInvalidationsReached). Which I would prefer to be in EndBlocker.</p>
<p>How would you implement it?</p>
<p>@akup have you moved the iterating though inferences to EndBlocker for InferenceValidationDetails in 782?</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/libermans">@libermans</a></span>
    <span class="issues-meta-item">commented 2026-02-24 01:27 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@x0152 I see that you actually store the values directly in HandleComplete. Do you think that it will be faster that way? Should we clean the old keys to not store them for entire history on chain for every block?</p>
<p>Have you implemented it only for DynamicPricing or for MaximumInvalidationsReached as well? </p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/akup">@akup</a></span>
    <span class="issues-meta-item">commented 2026-02-24 05:50 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <blockquote>
<p><a href="https://github.com/akup">@akup</a> have you moved the iterating though inferences to EndBlocker for InferenceValidationDetails in 782?</p>
</blockquote>
<p>I've implemented another approach it is described (with motivation) in details at https://github.com/gonka-ai/gonka/pull/793
Need to discuss it. </p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/x0152">@x0152</a></span>
    <span class="issues-meta-item">commented 2026-02-24 07:24 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>I added lightweight on-chain storage for both DynamicPricing and MaximumInvalidationsReached (via GetSummaryByModelAndTime). To keep business logic working after removing DeveloperStats from the hot path, we now write only a fixed 24-byte aggregate per (model, second), which should stay fast under load. This is a temporary compromise (a better long-term option is rolling sums in EndBlocker after current tasks), but local benchmarks already show ~20x faster execution and ~30x lower memory usage.</p>
<p>Pruning is definitely needed, and if this approach is accepted, I will add it next</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/x0152">@x0152</a></span>
    <span class="issues-meta-item">commented 2026-02-24 14:21 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Added description to PR #788 with "Out of scope" section (from my point of view). Let me know if any of those items are critical for this PR and I should include them</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/akup">@akup</a></span>
    <span class="issues-meta-item">commented 2026-03-04 16:00 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@x0152 are you going to implement rolling sums for X blocks at this commit?</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/x0152">@x0152</a></span>
    <span class="issues-meta-item">commented 2026-03-04 16:09 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@akup This issue is already closed by PR #812, so there's no point in implementing and maintaining rolling sums here</p>
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

> 🔄 **Auto-synced** from [Issue #781](https://github.com/gonka-ai/gonka/issues/781) every hour.
