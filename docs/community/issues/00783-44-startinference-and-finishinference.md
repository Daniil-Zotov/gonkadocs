---
title: "#783 — [4/4] `StartInference` and `FinishInference`"
source: https://github.com/gonka-ai/gonka/issues/783
issue_number: 783
synced_at: 2026-07-06T09:52:42Z
template: issues-main.html
---

> 🔄 **Auto-synced:** from [Issue #783](https://github.com/gonka-ai/gonka/issues/783) every 6 hours. 

# 🔴 [4/4] `StartInference` and `FinishInference`

**Author:** [@tcharchian](https://github.com/tcharchian) · **State:** Closed · **Created:** 2026-02-20 22:40 UTC · **Updated:** 2026-03-11 20:01 UTC

**Labels:** `Priority: High`

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
`SetParticipant` is executed twice in `ProcessInferencePayment` and `HandleInferenceComplete` for the second Start/Finish transaction, when it could be executed just once.

Most of the time spent in `SetParticipant` is consumed by `ComputeStatus` and `GetParams` (except for Logging, which takes 50%, which we discussed separately in https://github.com/gonka-ai/gonka/issues/780). `Decimal.Ln` in `ComputeStatus` can be optimized significantly. Regarding `GetParams`, we read it for each transaction in any case, so we can pass it to `SetParticipant` and reuse what we already have.

# Important
This issue is one of five issues in the [0/4] StartInference and FinishInference series (and correspondingly [1/4], [2/4], [3/4], [4/4]).
These tasks can be completed independently of each other by different contributors.
This specific task does not require maintaining and operating a node on mainnet in order to test and validate the result.

All five issues [0/4], [1/4], [2/4], [3/4], [4/4] in this series must be completed as part of the v0.2.11 upgrade, which is scheduled for the week of February 23. After the v0.2.11 upgrade, these tasks will no longer be relevant, because a different solution can/will be proposed.

---

## 💬 Comments (22)

### Комментарий 1 — [@tcharchian](https://github.com/tcharchian)

*2026-02-20 22:40 UTC*

If you’re ready to take this task on, please leave a comment here so other community members can see it’s already being worked on.

### Комментарий 2 — [@akup](https://github.com/akup)

*2026-02-21 04:32 UTC*

According to GetParams. If we read it for each transaction, it could be read once per block, to also optimize reads on each transaction.

We change params not so often and only by authority or proposals, so we can afford per block cache for params.

### Комментарий 3 — [@libermans](https://github.com/libermans)

*2026-02-21 05:23 UTC*

The challenge that params can be changed through a transaction, so we can't use per block cache. But can use per transaction cache for Start, Finish, Validate.

I would add additional functions to Keeper with GetParam, to store cache and clean it, and run store cache in the begging of the transactions and defer clean.

### Комментарий 4 — [@akup](https://github.com/akup)

*2026-02-21 05:23 UTC*

According the ComputeStatus it seams we can completely skip it on HandleInferenceComplete and ProcessInferencePayment.

Calculations there are:
probabilityOfConsecutiveFailures (don't change on inference completion and will not throw error)
getInvalidationStatus (isn't related to inference completion and should be skipped)
getInactiveStatus (can not fail if we completed inference and could be skipped)
getConfirmationPoCStatus (isn't related to inference completion)

So we can skip ComputeStatus for inference complete?


### Комментарий 5 — [@libermans](https://github.com/libermans)

*2026-02-21 05:27 UTC*

You actually right, so we may add parameter for the function to skip compute status and use it in the Start/Finish. 

### Комментарий 6 — [@akup](https://github.com/akup)

*2026-02-21 05:27 UTC*

According to GetParams. Yes they can change through the transaction. but only if we set them (via authority or proposal).

And I think that it is absolutely affordable to ignore this change till the block ends, and use the change only on the next blocks

### Комментарий 7 — [@libermans](https://github.com/libermans)

*2026-02-21 05:31 UTC*

You may be right here, that we can wait for the next block. I'm thinking about corner cases, like can we do multiple changes within one block, which require us to read parameters, but likely you right. It just usually not recommended to have any cache per block, to insure determinism. But you may be right that there is no case for non-determinism here. 

### Комментарий 8 — [@akup](https://github.com/akup)

*2026-02-21 05:34 UTC*

Even if we do multiple changes per one block, I think it is something very strange if the change is reading previous state...

Anyway we control this by proposals and can manage to be in separate blocks

### Комментарий 9 — [@x0152](https://github.com/x0152)

*2026-02-21 11:20 UTC*

I'd like to help with this issue if no one is working on it yet

### Комментарий 10 — [@x0152](https://github.com/x0152)

*2026-02-21 12:02 UTC*

> Even if we do multiple changes per one block, I think it is something very strange if the change is reading previous state...
> 
> Anyway we control this by proposals and can manage to be in separate blocks

I agree block height caching can help, and it may improve consistency when workers run in parallel. But we still need more testing to prove it is safe and useful in multi-node setups

In PR #542, using 'x-cosmos-block-height' looks good, but we should measure cache hit rate first, because if misses are frequent the real speedup may be small

Since v0.2.11 is close, I suggest we keep quick safe fixes now (including local memoization) and move block-height caching to the next update






### Комментарий 11 — [@x0152](https://github.com/x0152)

*2026-02-21 12:15 UTC*

> According the ComputeStatus it seams we can completely skip it on HandleInferenceComplete and ProcessInferencePayment.
> 
> Calculations there are: probabilityOfConsecutiveFailures (don't change on inference completion and will not throw error) getInvalidationStatus (isn't related to inference completion and should be skipped) getInactiveStatus (can not fail if we completed inference and could be skipped) getConfirmationPoCStatus (isn't related to inference completion)
> 
> So we can skip ComputeStatus for inference complete?

If we skip ComputeStatus on HandleInferenceComplete, then InactiveLLR won't be updated with the successful inference result. What do you think?

### Комментарий 12 — [@akup](https://github.com/akup)

*2026-02-21 15:25 UTC*

> If we skip ComputeStatus on HandleInferenceComplete, then InactiveLLR won't be updated with the successful inference result. What do you think?

InactiveLLR is used only here when we compute the status and it has effect on logic only if it fails. When Participant became inactive it can become active again only on next epoch. Serving inference will not change it's status to inactive from active. So inactiveLLR can be just for information for get queries.
But I don't think we should store and calculate something on chain that is just for information, all of this could be caluclated offchain.

So for performance it is better to skip it here.

### Комментарий 13 — [@akup](https://github.com/akup)

*2026-02-21 15:27 UTC*

> I'd like to help with this issue if no one is working on it yet

@x0152 I've already started it with [782](https://github.com/gonka-ai/gonka/issues/782)


### Комментарий 14 — [@akup](https://github.com/akup)

*2026-02-21 15:44 UTC*

> I agree block height caching can help, and it may improve consistency when workers run in parallel. But we still need more testing to prove it is safe and useful in multi-node setups

It's onchain logic, it's hard to compare with the case of  'x-cosmos-block-height' when there is offchain communication with multiple chain nodes that can have different height.

Here we are determenistic every node on height X has the same state and input, and they all can have the logic that if params are adjusted by proposal this params are not used before next block (it's determenistic). 

### Комментарий 15 — [@x0152](https://github.com/x0152)

*2026-02-21 19:27 UTC*

> InactiveLLR is used only here when we compute the status and it has effect on logic only if it fails. When Participant became inactive it can become active again only on next epoch. Serving inference will not change it's status to inactive from active. So inactiveLLR can be just for information for get queries. But I don't think we should store and calculate something on chain that is just for information, all of this could be caluclated offchain.
> 
> So for performance it is better to skip it here.

InactiveLLR tracks both passes and misses. If we skip ComputeStatus on completion, pass updates are not applied, while misses are still applied. As a result, getInactiveStatus can move a participant to 'inactive' earlier than intended
Moving this offchain is not trivial task, since InactiveLLR is consensus state used by on-chain status logic




### Комментарий 16 — [@x0152](https://github.com/x0152)

*2026-02-21 19:34 UTC*

> > I agree block height caching can help, and it may improve consistency when workers run in parallel. But we still need more testing to prove it is safe and useful in multi-node setups
> 
> It's onchain logic, it's hard to compare with the case of 'x-cosmos-block-height' when there is offchain communication with multiple chain nodes that can have different height.
> 
> Here we are determenistic every node on height X has the same state and input, and they all can have the logic that if params are adjusted by proposal this params are not used before next block (it's determenistic).

my bad, mixed up dapi and on-chain context here, sorry

### Комментарий 17 — [@akup](https://github.com/akup)

*2026-02-23 09:35 UTC*

> InactiveLLR tracks both passes and misses.

It doesn't track them, it is used for status computations. `InferenceCount` and `MissedRequests` are tracked at `Participant. CurrentEpochStats` and we don't miss this tracking by skipping status recomputation. The logic is that first we change this InferenceCount and MissedRequests, and then we set the Participant, it calls setting Participant status, that is calculated from this parameters. But if we serve the inference successfully participant can't change it's status and we don't need to compute it.

### Комментарий 18 — [@x0152](https://github.com/x0152)

*2026-02-23 12:46 UTC*

Sorry for pushing on this, I just want to understand where I'm wrong

I wrote a quick test to check this (50 completions + 6 misses):
```go
func TestSkipComputeStatusOnCompletionBreaksLLR(t *testing.T) {
	params := types.DefaultValidationParams()
	completions := 50
	misses := 6

	emptyStats := func() types.CurrentEpochStats {
		return types.CurrentEpochStats{InactiveLLR: types.DecimalFromFloat(0), InvalidLLR: types.DecimalFromFloat(0)}
	}

	// A: simulate 50 successful inferences + 6 misses (calling ComputeStatus every time)
	stored := emptyStats()
	for i := 0; i < completions; i++ {
		_, _, stored = ComputeStatus(params, nil, types.Participant{CurrentEpochStats: &types.CurrentEpochStats{
			InferenceCount: stored.InferenceCount + 1, MissedRequests: stored.MissedRequests,
			InactiveLLR: stored.InactiveLLR, InvalidLLR: stored.InvalidLLR}}, stored)
	}
	var st types.ParticipantStatus
	for i := 0; i < misses; i++ {
		st, _, stored = ComputeStatus(params, nil, types.Participant{CurrentEpochStats: &types.CurrentEpochStats{
			InferenceCount: stored.InferenceCount, MissedRequests: stored.MissedRequests + 1,
			InactiveLLR: stored.InactiveLLR, InvalidLLR: stored.InvalidLLR}}, stored)
	}
	t.Logf("always compute: LLR=%s status=%s", stored.InactiveLLR.ToDecimal(), st)
	require.Equal(t, types.ParticipantStatus_ACTIVE, st)

	// B: now same thing but skip ComputeStatus on completions (bump counter and don't call ComputeStatus)
	skipped := emptyStats()
	skipped.InferenceCount = uint64(completions)
	var st2 types.ParticipantStatus
	for i := 0; i < misses; i++ {
		st2, _, skipped = ComputeStatus(params, nil, types.Participant{CurrentEpochStats: &types.CurrentEpochStats{
			InferenceCount: uint64(completions), MissedRequests: skipped.MissedRequests + 1,
			InactiveLLR: skipped.InactiveLLR, InvalidLLR: skipped.InvalidLLR}}, skipped)
	}
	t.Logf("skip completions: LLR=%s status=%s", skipped.InactiveLLR.ToDecimal(), st2)

	// same participant, same event sequence, but marked 'inactive'
	require.Equal(t, types.ParticipantStatus_INACTIVE, st2)
}
```
```
A: result: LLR=-1.73, status=ACTIVE
B: result: LLR=+4.16, status=INACTIVE
```

'getInactiveStatus' updates InactiveLLR from deltas. If we skip ComputeStatus on successful completions, positive newInferences updates are never applied to InactiveLLR

Did I misunderstand anything in this reasoning?

### Комментарий 19 — [@akup](https://github.com/akup)

*2026-02-23 16:46 UTC*

@x0152 you are correct. And it is really nice to pushing on this.

The point is that `ComputeStatus` is using `Participant.CurrentEpochStats.InactiveLLR` for next delta calculation.

The test could pass if we first apply ComputeStatus(50, 0, oldStatus), and then ComputeStatus(50, 6, oldStatus), but if we skip computations InactiveLLR will not be updated.

And even if we can optimize it (for example apply all passed inferences on first met missedInference) it's need additional tracking of changing trend from passed inference to missed inference. So optimizing Ln math (caching it) is good enough to keep the flow. Skipping compute status while possible needs additional tracking and it needs to measure does it provide real performance win.

Actually I've finished by selectable skipping of probabilityOfConsecutiveFailures, getInvalidationStatus, getInactiveStatus, getConfirmationPoCStatus dependant of source of SetParticipant call.



### Комментарий 20 — [@akup](https://github.com/akup)

*2026-02-23 17:00 UTC*

@x0152 so to extend your test:

```go
// C: batch 50 completions (one ComputeStatus with delta (50,0)), then apply 6 misses.
// Same net deltas as A, so InactiveLLR and status must match A.
skipped2 := emptyStats()
var st3 types.ParticipantStatus
st3, _, skipped2 = ComputeStatus(params, nil, types.Participant{
	CurrentEpochStats: &types.CurrentEpochStats{
		InferenceCount: uint64(completions),
		MissedRequests: 0,
		InactiveLLR:    skipped2.InactiveLLR,
		InvalidLLR:     skipped2.InvalidLLR,
	},
}, skipped2, scope)
for i := 0; i < misses; i++ {
	st3, _, skipped2 = ComputeStatus(params, nil, types.Participant{
		CurrentEpochStats: &types.CurrentEpochStats{
			InferenceCount: skipped2.InferenceCount,
			MissedRequests: skipped2.MissedRequests + 1,
			InactiveLLR:    skipped2.InactiveLLR,
			InvalidLLR:     skipped2.InvalidLLR,
		},
	}, skipped2, scope)
}
t.Logf("batch completions then misses: LLR=%s status=%s", skipped2.InactiveLLR.ToDecimal(), st3)
require.Equal(t, types.ParticipantStatus_ACTIVE, st3, "same event sequence as A should stay ACTIVE")
require.Equal(t, stored.InactiveLLR.ToDecimal().String(), skipped2.InactiveLLR.ToDecimal().String(),
	"InactiveLLR should equal case A when we batch completions then apply misses")
```
In this case InactiveLLR will be same with case A, when you Compute on every passed inference

### Комментарий 21 — [@x0152](https://github.com/x0152)

*2026-02-23 21:27 UTC*

Got you. Thanks for detailed explanation

### Комментарий 22 — [@gmorgachev](https://github.com/gmorgachev)

*2026-03-11 20:01 UTC*

The big part of inference flow optimization is merged in https://github.com/gonka-ai/gonka/pull/812
I'm closing all `[*/4] StartInference and FinishInference: optimiziation` tasks to finalize this work in milestone 0.2.11. I think it'd be better to re-open in case of additinal optimizations required
