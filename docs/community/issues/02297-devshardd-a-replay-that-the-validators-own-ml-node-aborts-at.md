---
title: "#2297 — devshardd: a replay that the validator's own ML node aborts at PoC start is voted invalid against the executor"
source: https://github.com/gonka-ai/gonka/issues/2297
issue_number: 2297
synced_at: 2026-11-27T20:02:33Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    devshardd: a replay that the validator's own ML node aborts at PoC start is voted invalid against the executor
    <span class="issues-number">#2297</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/kaileido">@kaileido</a> opened 2026-11-19 21:46 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-11-21 05:18 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
### What happens

When the validator's ML node starts PoC generation, every replay still running on it ends early. If the replay comes back as a complete stream (usage chunk and `[DONE]`) with fewer output tokens than the executor's enforced tokens, devshardd scores it like any other replay: "Inflated token counts." for a short replay, "Executor returned error but prompt is servable." for an empty-sentinel one. Both are a `Valid: false` vote against an executor that did nothing wrong.

Seen on a validator running devshardd v6.0.0 at a confirmation PoC on 2026-11-18, generation start 12:29:13 UTC. `common/validation/validation.go` is the same blob (`5b74c871`) in `v6.0.0` and on the current `devshard/v7` tip `34ddd777`, so v7 behaves the same.

- 384 `validation failed: inflated token counts` warnings between 12:29:14.024 and 12:29:25.346 (373 distinct inference ids), none in the 9 minutes of log before. 579 in total by 12:35.
- In all 384 the input matched (`validationInput == claimedInput`); only the output was short. Mean claimed output 10,752 tokens, mean replayed 2,436; 42 replays returned 0 output tokens.
- No `validator replay stream failed on ML node` line in the whole log, so every one of these replays was a complete stream and none was rotated to another node.
- Of the 579 warnings, 234 were followed within 10 s by `validation tx published ... result_valid=false` for the same inference id and 167 by a later invalid vote; 6 were later voted valid and 172 had no vote in the log window. Example: escrow 175729, inference 710, claimed output 402, replayed 0, warning at 12:29:14.024, invalid vote at 12:29:14.026.
- Invalid votes per minute: 10 to 41 (about 22 on average) from 12:20 to 12:28, then 135 invalid and 5 valid at 12:29. Not every invalid in that minute comes from a cut replay, but the 234 above follow an inflated-token warning for the same id.

The log does not record the replay's `finish_reason`, so that these replays ended with `"abort"` is not observed here. It is what the plugin's `abort_all_requests` path produces according to #2146 and gonka-ai/gonka-vllm-plugins#34, and the timing matches.

### Where

- `NormalizeReplayStream` fails a replay only on an `error` event or a missing `[DONE]`; a stream with an `"abort"` choice passes as complete: [validation.go#L213-L266](https://github.com/gonka-ai/gonka/blob/34ddd777475be05f583945add3c275b490f3cf39/common/validation/validation.go#L213-L266)
- `ExecuteValidationWithPolicy` parses the replay and goes straight to the empty-sentinel and token-count checks, with no look at `finish_reason`: [validation.go#L551-L579](https://github.com/gonka-ai/gonka/blob/34ddd777475be05f583945add3c275b490f3cf39/common/validation/validation.go#L551-L579)
- `InvalidInferenceResult` becomes `false`: [validator.go#L393-L396](https://github.com/gonka-ai/gonka/blob/34ddd777475be05f583945add3c275b490f3cf39/devshard/cmd/devshardd/inference/validator.go#L393-L396), published as `MsgValidation{Valid: result.Valid}`: [host.go#L1732-L1736](https://github.com/gonka-ai/gonka/blob/34ddd777475be05f583945add3c275b490f3cf39/devshard/host/host.go#L1732-L1736)
- The path that should apply instead already exists: `ErrValidationDeferred` keeps the obligation and retries after the 30 s cooldown: [validate.go#L613-L614](https://github.com/gonka-ai/gonka/blob/34ddd777475be05f583945add3c275b490f3cf39/devshard/cmd/devshardd/inference/validate.go#L613-L614), [host.go#L1677-L1681](https://github.com/gonka-ai/gonka/blob/34ddd777475be05f583945add3c275b490f3cf39/devshard/host/host.go#L1677-L1681), [host.go#L117](https://github.com/gonka-ai/gonka/blob/34ddd777475be05f583945add3c275b490f3cf39/devshard/host/host.go#L117)

### Why it is wrong

`finish_reason: "abort"` is set by the validator's own vLLM when it drops the request. It says the replay was not finished, not that the executor's tokens are wrong, so it cannot be the basis of a vote. Today the executor takes the invalid for the validator's PoC pause, and invalid votes feed the consecutive-invalid counter and the invalidation-rate test.

### Proposed fix

In `ExecuteValidationWithPolicy`, right after the replay is parsed and before the empty-sentinel and token-count checks, return a new `ErrReplayAborted` if any choice of the replay has `finish_reason == "abort"`. `classifyExecuteValidationErr` wraps it in `ErrValidationDeferred`, so the host retries after the existing cooldown and no vote is cast. The deferral keys only on that node-set reason: a short replay that ends with `"stop"` or `"length"` is still voted invalid, as today. Also add the replay's finish reasons and the enforced token count to the `inflated token counts` warning, so the next PoC shows which reason the short replays carried.

gonka-ai/gonka-vllm-plugins#34 fixes this at the source by turning an aborted request into a 503 error event. This check covers validators whose ML node does not run that plugin version yet, and defers at once instead of rotating through other nodes that may be in PoC too. Not covered: an aborted replay is an HTTP 200, so the validation credit for that attempt is still spent.

Related: #2146 (executor side of the same abort), gonka-ai/gonka-vllm-plugins#34, #1805.

</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/gafrustam">@gafrustam</a></span>
    <span class="issues-meta-item">commented 2026-11-21 05:18 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Starting work, PR in a day or two</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2297](https://github.com/gonka-ai/gonka/issues/2297) every hour.
