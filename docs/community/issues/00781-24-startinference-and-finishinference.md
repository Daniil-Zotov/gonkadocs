---
title: "#781 — [2/4] `StartInference` and `FinishInference`"
source: https://github.com/gonka-ai/gonka/issues/781
issue_number: 781
synced_at: 2026-07-06T09:52:43Z
---

> 🔄 **Авто-синхронизация:** из [Issue #781](https://github.com/gonka-ai/gonka/issues/781) каждые 6 часов. 

# 🔴 [2/4] `StartInference` and `FinishInference`

**Автор:** [@tcharchian](https://github.com/tcharchian) · **Состояние:** Closed · **Создано:** 2026-02-20 22:26 UTC · **Обновлено:** 2026-03-11 20:01 UTC

**Метки:** `Priority: High`

**Веха:** v0.2.11

---

## 📝 Описание

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

---

## 💬 Комментарии (13)

### Комментарий 1 — [@tcharchian](https://github.com/tcharchian)

*2026-02-20 22:41 UTC*

If you’re ready to take this task on, please leave a comment here so other community members can see it’s already being worked on.

### Комментарий 2 — [@akup](https://github.com/akup)

*2026-02-21 04:08 UTC*

It is important to mention, that SetInference -> SetDeveloperStats are also called at validation, revalidation, invalidation.
There we only change the status of the existing inference.
So when we move DevelopersStats off-chain, we also should handle validation events (and emit new events if needed).

### Комментарий 3 — [@libermans](https://github.com/libermans)

*2026-02-21 05:20 UTC*

Yes, correct. 

Also DeveloperStats are used for DynamicPricing and MaximumInvalidationsReached, we should use some optimal storage for that values but likely should be implemented after both this task and https://github.com/gonka-ai/gonka/issues/782 finished.

### Комментарий 4 — [@x0152](https://github.com/x0152)

*2026-02-22 12:02 UTC*

I'd like to take this on and start with draft #788. I'm ready to pass ownership If someone has a stronger approach

### Комментарий 5 — [@x0152](https://github.com/x0152)

*2026-02-23 21:14 UTC*

With stats computation moved off-chain, StatsByTimePeriodByDeveloper and StatsByDeveloperAndEpochsBackwards will only return legacy data no longer updated after cutover (kept for compatibility). Do we need new dapi endpoints for per-developer stats from the local store, or is that out of scope now?


StatsByTimePeriodByDeveloper and StatsByDeveloperAndEpochsBackwards are not called internally (only InferencesAndTokensStatsByModels is used by pricing)


### Комментарий 6 — [@libermans](https://github.com/libermans)

*2026-02-24 00:53 UTC*

Per-developer. I don't think we use it now anywhere, so out of scope likely

For DynamicPricing and MaximumInvalidationsReached we need an on-chain storage, I would say with rolling sum for X blocks (the amount of blocks we get from params for DynamicPricing and MaximumInvalidationsReached). Which I would prefer to be in EndBlocker.

How would you implement it?

@akup have you moved the iterating though inferences to EndBlocker for InferenceValidationDetails in 782?

### Комментарий 7 — [@libermans](https://github.com/libermans)

*2026-02-24 01:27 UTC*

@x0152 I see that you actually store the values directly in HandleComplete. Do you think that it will be faster that way? Should we clean the old keys to not store them for entire history on chain for every block?

Have you implemented it only for DynamicPricing or for MaximumInvalidationsReached as well? 

### Комментарий 8 — [@akup](https://github.com/akup)

*2026-02-24 05:50 UTC*

> [@akup](https://github.com/akup) have you moved the iterating though inferences to EndBlocker for InferenceValidationDetails in 782?

I've implemented another approach it is described (with motivation) in details at https://github.com/gonka-ai/gonka/pull/793
Need to discuss it. 

### Комментарий 9 — [@x0152](https://github.com/x0152)

*2026-02-24 07:24 UTC*

I added lightweight on-chain storage for both DynamicPricing and MaximumInvalidationsReached (via GetSummaryByModelAndTime). To keep business logic working after removing DeveloperStats from the hot path, we now write only a fixed 24-byte aggregate per (model, second), which should stay fast under load. This is a temporary compromise (a better long-term option is rolling sums in EndBlocker after current tasks), but local benchmarks already show ~20x faster execution and ~30x lower memory usage.

Pruning is definitely needed, and if this approach is accepted, I will add it next

### Комментарий 10 — [@x0152](https://github.com/x0152)

*2026-02-24 14:21 UTC*

Added description to PR #788 with "Out of scope" section (from my point of view). Let me know if any of those items are critical for this PR and I should include them

### Комментарий 11 — [@akup](https://github.com/akup)

*2026-03-04 16:00 UTC*

@x0152 are you going to implement rolling sums for X blocks at this commit?

### Комментарий 12 — [@x0152](https://github.com/x0152)

*2026-03-04 16:09 UTC*

@akup This issue is already closed by PR #812, so there's no point in implementing and maintaining rolling sums here

### Комментарий 13 — [@gmorgachev](https://github.com/gmorgachev)

*2026-03-11 20:01 UTC*

The big part of inference flow optimization is merged in https://github.com/gonka-ai/gonka/pull/812
I'm closing all `[*/4] StartInference and FinishInference: optimiziation` tasks to finalize this work in milestone 0.2.11. I think it'd be better to re-open in case of additinal optimizations required
