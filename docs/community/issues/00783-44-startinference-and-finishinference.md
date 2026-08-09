---
title: "#783 — [4/4] `StartInference` and `FinishInference`"
source: https://github.com/gonka-ai/gonka/issues/783
issue_number: 783
synced_at: 2026-08-09T06:03:58Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    [4/4] `StartInference` and `FinishInference`
    <span class="issues-number">#783</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-02-20 22:40 UTC</span>
    <span class="issues-meta-item">22 comments</span>
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
`SetParticipant` is executed twice in `ProcessInferencePayment` and `HandleInferenceComplete` for the second Start/Finish transaction, when it could be executed just once.

Most of the time spent in `SetParticipant` is consumed by `ComputeStatus` and `GetParams` (except for Logging, which takes 50%, which we discussed separately in https://github.com/gonka-ai/gonka/issues/780). `Decimal.Ln` in `ComputeStatus` can be optimized significantly. Regarding `GetParams`, we read it for each transaction in any case, so we can pass it to `SetParticipant` and reuse what we already have.

# Important
This issue is one of five issues in the [0/4] StartInference and FinishInference series (and correspondingly [1/4], [2/4], [3/4], [4/4]).
These tasks can be completed independently of each other by different contributors.
This specific task does not require maintaining and operating a node on mainnet in order to test and validate the result.

All five issues [0/4], [1/4], [2/4], [3/4], [4/4] in this series must be completed as part of the v0.2.11 upgrade, which is scheduled for the week of February 23. After the v0.2.11 upgrade, these tasks will no longer be relevant, because a different solution can/will be proposed.
</div>

---

## 💬 Comments (22)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-02-20 22:40 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>If you’re ready to take this task on, please leave a comment here so other community members can see it’s already being worked on.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/akup">@akup</a></span>
    <span class="issues-meta-item">commented 2026-02-21 04:32 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>According to GetParams. If we read it for each transaction, it could be read once per block, to also optimize reads on each transaction.</p>
<p>We change params not so often and only by authority or proposals, so we can afford per block cache for params.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/libermans">@libermans</a></span>
    <span class="issues-meta-item">commented 2026-02-21 05:23 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>The challenge that params can be changed through a transaction, so we can't use per block cache. But can use per transaction cache for Start, Finish, Validate.</p>
<p>I would add additional functions to Keeper with GetParam, to store cache and clean it, and run store cache in the begging of the transactions and defer clean.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/akup">@akup</a></span>
    <span class="issues-meta-item">commented 2026-02-21 05:23 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>According the ComputeStatus it seams we can completely skip it on HandleInferenceComplete and ProcessInferencePayment.</p>
<p>Calculations there are:
probabilityOfConsecutiveFailures (don't change on inference completion and will not throw error)
getInvalidationStatus (isn't related to inference completion and should be skipped)
getInactiveStatus (can not fail if we completed inference and could be skipped)
getConfirmationPoCStatus (isn't related to inference completion)</p>
<p>So we can skip ComputeStatus for inference complete?</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/libermans">@libermans</a></span>
    <span class="issues-meta-item">commented 2026-02-21 05:27 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>You actually right, so we may add parameter for the function to skip compute status and use it in the Start/Finish. </p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/akup">@akup</a></span>
    <span class="issues-meta-item">commented 2026-02-21 05:27 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>According to GetParams. Yes they can change through the transaction. but only if we set them (via authority or proposal).</p>
<p>And I think that it is absolutely affordable to ignore this change till the block ends, and use the change only on the next blocks</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/libermans">@libermans</a></span>
    <span class="issues-meta-item">commented 2026-02-21 05:31 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>You may be right here, that we can wait for the next block. I'm thinking about corner cases, like can we do multiple changes within one block, which require us to read parameters, but likely you right. It just usually not recommended to have any cache per block, to insure determinism. But you may be right that there is no case for non-determinism here. </p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/akup">@akup</a></span>
    <span class="issues-meta-item">commented 2026-02-21 05:34 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Even if we do multiple changes per one block, I think it is something very strange if the change is reading previous state...</p>
<p>Anyway we control this by proposals and can manage to be in separate blocks</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/x0152">@x0152</a></span>
    <span class="issues-meta-item">commented 2026-02-21 11:20 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>I'd like to help with this issue if no one is working on it yet</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/x0152">@x0152</a></span>
    <span class="issues-meta-item">commented 2026-02-21 12:02 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <blockquote>
<p>Even if we do multiple changes per one block, I think it is something very strange if the change is reading previous state...</p>
<p>Anyway we control this by proposals and can manage to be in separate blocks</p>
</blockquote>
<p>I agree block height caching can help, and it may improve consistency when workers run in parallel. But we still need more testing to prove it is safe and useful in multi-node setups</p>
<p>In PR #542, using 'x-cosmos-block-height' looks good, but we should measure cache hit rate first, because if misses are frequent the real speedup may be small</p>
<p>Since v0.2.11 is close, I suggest we keep quick safe fixes now (including local memoization) and move block-height caching to the next update</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/x0152">@x0152</a></span>
    <span class="issues-meta-item">commented 2026-02-21 12:15 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <blockquote>
<p>According the ComputeStatus it seams we can completely skip it on HandleInferenceComplete and ProcessInferencePayment.</p>
<p>Calculations there are: probabilityOfConsecutiveFailures (don't change on inference completion and will not throw error) getInvalidationStatus (isn't related to inference completion and should be skipped) getInactiveStatus (can not fail if we completed inference and could be skipped) getConfirmationPoCStatus (isn't related to inference completion)</p>
<p>So we can skip ComputeStatus for inference complete?</p>
</blockquote>
<p>If we skip ComputeStatus on HandleInferenceComplete, then InactiveLLR won't be updated with the successful inference result. What do you think?</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/akup">@akup</a></span>
    <span class="issues-meta-item">commented 2026-02-21 15:25 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <blockquote>
<p>If we skip ComputeStatus on HandleInferenceComplete, then InactiveLLR won't be updated with the successful inference result. What do you think?</p>
</blockquote>
<p>InactiveLLR is used only here when we compute the status and it has effect on logic only if it fails. When Participant became inactive it can become active again only on next epoch. Serving inference will not change it's status to inactive from active. So inactiveLLR can be just for information for get queries.
But I don't think we should store and calculate something on chain that is just for information, all of this could be caluclated offchain.</p>
<p>So for performance it is better to skip it here.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/akup">@akup</a></span>
    <span class="issues-meta-item">commented 2026-02-21 15:27 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <blockquote>
<p>I'd like to help with this issue if no one is working on it yet</p>
</blockquote>
<p>@x0152 I've already started it with <a href="https://github.com/gonka-ai/gonka/issues/782">782</a></p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/akup">@akup</a></span>
    <span class="issues-meta-item">commented 2026-02-21 15:44 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <blockquote>
<p>I agree block height caching can help, and it may improve consistency when workers run in parallel. But we still need more testing to prove it is safe and useful in multi-node setups</p>
</blockquote>
<p>It's onchain logic, it's hard to compare with the case of  'x-cosmos-block-height' when there is offchain communication with multiple chain nodes that can have different height.</p>
<p>Here we are determenistic every node on height X has the same state and input, and they all can have the logic that if params are adjusted by proposal this params are not used before next block (it's determenistic). </p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/x0152">@x0152</a></span>
    <span class="issues-meta-item">commented 2026-02-21 19:27 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <blockquote>
<p>InactiveLLR is used only here when we compute the status and it has effect on logic only if it fails. When Participant became inactive it can become active again only on next epoch. Serving inference will not change it's status to inactive from active. So inactiveLLR can be just for information for get queries. But I don't think we should store and calculate something on chain that is just for information, all of this could be caluclated offchain.</p>
<p>So for performance it is better to skip it here.</p>
</blockquote>
<p>InactiveLLR tracks both passes and misses. If we skip ComputeStatus on completion, pass updates are not applied, while misses are still applied. As a result, getInactiveStatus can move a participant to 'inactive' earlier than intended
Moving this offchain is not trivial task, since InactiveLLR is consensus state used by on-chain status logic</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/x0152">@x0152</a></span>
    <span class="issues-meta-item">commented 2026-02-21 19:34 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <blockquote>
<blockquote>
<p>I agree block height caching can help, and it may improve consistency when workers run in parallel. But we still need more testing to prove it is safe and useful in multi-node setups</p>
</blockquote>
<p>It's onchain logic, it's hard to compare with the case of 'x-cosmos-block-height' when there is offchain communication with multiple chain nodes that can have different height.</p>
<p>Here we are determenistic every node on height X has the same state and input, and they all can have the logic that if params are adjusted by proposal this params are not used before next block (it's determenistic).</p>
</blockquote>
<p>my bad, mixed up dapi and on-chain context here, sorry</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/akup">@akup</a></span>
    <span class="issues-meta-item">commented 2026-02-23 09:35 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <blockquote>
<p>InactiveLLR tracks both passes and misses.</p>
</blockquote>
<p>It doesn't track them, it is used for status computations. <code>InferenceCount</code> and <code>MissedRequests</code> are tracked at <code>Participant. CurrentEpochStats</code> and we don't miss this tracking by skipping status recomputation. The logic is that first we change this InferenceCount and MissedRequests, and then we set the Participant, it calls setting Participant status, that is calculated from this parameters. But if we serve the inference successfully participant can't change it's status and we don't need to compute it.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/x0152">@x0152</a></span>
    <span class="issues-meta-item">commented 2026-02-23 12:46 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Sorry for pushing on this, I just want to understand where I'm wrong</p>
<p>I wrote a quick test to check this (50 completions + 6 misses):</p>
<pre><code class="language-go">func TestSkipComputeStatusOnCompletionBreaksLLR(t *testing.T) {
    params := types.DefaultValidationParams()
    completions := 50
    misses := 6

    emptyStats := func() types.CurrentEpochStats {
        return types.CurrentEpochStats{InactiveLLR: types.DecimalFromFloat(0), InvalidLLR: types.DecimalFromFloat(0)}
    }

    // A: simulate 50 successful inferences + 6 misses (calling ComputeStatus every time)
    stored := emptyStats()
    for i := 0; i &lt; completions; i++ {
        _, _, stored = ComputeStatus(params, nil, types.Participant{CurrentEpochStats: &amp;types.CurrentEpochStats{
            InferenceCount: stored.InferenceCount + 1, MissedRequests: stored.MissedRequests,
            InactiveLLR: stored.InactiveLLR, InvalidLLR: stored.InvalidLLR}}, stored)
    }
    var st types.ParticipantStatus
    for i := 0; i &lt; misses; i++ {
        st, _, stored = ComputeStatus(params, nil, types.Participant{CurrentEpochStats: &amp;types.CurrentEpochStats{
            InferenceCount: stored.InferenceCount, MissedRequests: stored.MissedRequests + 1,
            InactiveLLR: stored.InactiveLLR, InvalidLLR: stored.InvalidLLR}}, stored)
    }
    t.Logf(&quot;always compute: LLR=%s status=%s&quot;, stored.InactiveLLR.ToDecimal(), st)
    require.Equal(t, types.ParticipantStatus_ACTIVE, st)

    // B: now same thing but skip ComputeStatus on completions (bump counter and don't call ComputeStatus)
    skipped := emptyStats()
    skipped.InferenceCount = uint64(completions)
    var st2 types.ParticipantStatus
    for i := 0; i &lt; misses; i++ {
        st2, _, skipped = ComputeStatus(params, nil, types.Participant{CurrentEpochStats: &amp;types.CurrentEpochStats{
            InferenceCount: uint64(completions), MissedRequests: skipped.MissedRequests + 1,
            InactiveLLR: skipped.InactiveLLR, InvalidLLR: skipped.InvalidLLR}}, skipped)
    }
    t.Logf(&quot;skip completions: LLR=%s status=%s&quot;, skipped.InactiveLLR.ToDecimal(), st2)

    // same participant, same event sequence, but marked 'inactive'
    require.Equal(t, types.ParticipantStatus_INACTIVE, st2)
}
</code></pre>
<pre><code>A: result: LLR=-1.73, status=ACTIVE
B: result: LLR=+4.16, status=INACTIVE
</code></pre>
<p>'getInactiveStatus' updates InactiveLLR from deltas. If we skip ComputeStatus on successful completions, positive newInferences updates are never applied to InactiveLLR</p>
<p>Did I misunderstand anything in this reasoning?</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/akup">@akup</a></span>
    <span class="issues-meta-item">commented 2026-02-23 16:46 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@x0152 you are correct. And it is really nice to pushing on this.</p>
<p>The point is that <code>ComputeStatus</code> is using <code>Participant.CurrentEpochStats.InactiveLLR</code> for next delta calculation.</p>
<p>The test could pass if we first apply ComputeStatus(50, 0, oldStatus), and then ComputeStatus(50, 6, oldStatus), but if we skip computations InactiveLLR will not be updated.</p>
<p>And even if we can optimize it (for example apply all passed inferences on first met missedInference) it's need additional tracking of changing trend from passed inference to missed inference. So optimizing Ln math (caching it) is good enough to keep the flow. Skipping compute status while possible needs additional tracking and it needs to measure does it provide real performance win.</p>
<p>Actually I've finished by selectable skipping of probabilityOfConsecutiveFailures, getInvalidationStatus, getInactiveStatus, getConfirmationPoCStatus dependant of source of SetParticipant call.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/akup">@akup</a></span>
    <span class="issues-meta-item">commented 2026-02-23 17:00 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@x0152 so to extend your test:</p>
<pre><code class="language-go">// C: batch 50 completions (one ComputeStatus with delta (50,0)), then apply 6 misses.
// Same net deltas as A, so InactiveLLR and status must match A.
skipped2 := emptyStats()
var st3 types.ParticipantStatus
st3, _, skipped2 = ComputeStatus(params, nil, types.Participant{
    CurrentEpochStats: &amp;types.CurrentEpochStats{
        InferenceCount: uint64(completions),
        MissedRequests: 0,
        InactiveLLR:    skipped2.InactiveLLR,
        InvalidLLR:     skipped2.InvalidLLR,
    },
}, skipped2, scope)
for i := 0; i &lt; misses; i++ {
    st3, _, skipped2 = ComputeStatus(params, nil, types.Participant{
        CurrentEpochStats: &amp;types.CurrentEpochStats{
            InferenceCount: skipped2.InferenceCount,
            MissedRequests: skipped2.MissedRequests + 1,
            InactiveLLR:    skipped2.InactiveLLR,
            InvalidLLR:     skipped2.InvalidLLR,
        },
    }, skipped2, scope)
}
t.Logf(&quot;batch completions then misses: LLR=%s status=%s&quot;, skipped2.InactiveLLR.ToDecimal(), st3)
require.Equal(t, types.ParticipantStatus_ACTIVE, st3, &quot;same event sequence as A should stay ACTIVE&quot;)
require.Equal(t, stored.InactiveLLR.ToDecimal().String(), skipped2.InactiveLLR.ToDecimal().String(),
    &quot;InactiveLLR should equal case A when we batch completions then apply misses&quot;)
</code></pre>
<p>In this case InactiveLLR will be same with case A, when you Compute on every passed inference</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/x0152">@x0152</a></span>
    <span class="issues-meta-item">commented 2026-02-23 21:27 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Got you. Thanks for detailed explanation</p>
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

> 🔄 **Auto-synced** from [Issue #783](https://github.com/gonka-ai/gonka/issues/783) every hour.
