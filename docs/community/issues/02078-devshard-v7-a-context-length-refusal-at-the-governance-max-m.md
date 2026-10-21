---
title: "#2078 — devshard v7: a context-length refusal at the governance --max-model-len should never cost the host a miss or an invalidation"
source: https://github.com/gonka-ai/gonka/issues/2078
issue_number: 2078
synced_at: 2026-10-21T17:21:19Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    devshard v7: a context-length refusal at the governance --max-model-len should never cost the host a miss or an invalidation
    <span class="issues-number">#2078</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/cyberdelamain">@cyberdelamain</a> opened 2026-10-21 15:38 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-10-21 15:38 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
This is for v7, alongside #1903 (client-caused engine rejections, by @zpoken, moved to v7) and the v7 max-context-length item #1807. The code paths below are `devshard/v7` (67230e4dc) and #1903 at b20918017.

Case: a host runs exactly the governance `--max-model-len` (400000 for DeepSeek-V4-Flash and GLM-5.3, 180000 for MiniMax-M2.7), and a request's prompt plus `max_tokens` is above it. vLLM rejects it up front with a JSON 400 ("This model's maximum context length is 400000 tokens…"). The host neither lies nor is misconfigured. Other hosts may serve the same request if they raised their limit: a local `--max-model-len=600000` survives `MergeModelArgs`, which compares keys literally, and vLLM keeps the last value. That is #1911, fix open in #1912. Even after #1912 nothing checks the limit a host's vLLM actually runs.

On `devshard/v7` today, without #1903: the executor relays the 400 and signs no Finish. For the gateway the message is a retriable capability error (`isRetriableCapabilityErrorMessage`, `redundancy.go:4627`). When the request exceeds the table limit, `contextRefusalIsFinal` (`redundancy.go:4356`) ends the race, and `voteTimeoutsForFailedRequest` posts an execution timeout that verifiers accept because no Finish exists. The host ends `TimedOut` with `Missed=1` on every such request. I reproduced this with a gateway race test on d3d806a2c, which has the same code as `devshard/v7`. #1903 fixes this general case with the 0/0 client-fault Finish.

With #1903 one path remains: validation. `replayClientFault` (`common/validation/validation.go:555`) replays the prompt without enforced tokens. A validator with a raised limit serves it and votes `Valid:false` ("Executor reported a client fault but the prompt is servable"). In the challenge every host replays. With `vote_threshold_factor` 50, once more than half of the group's slots run a raised limit, `VotesInvalid > VoteThreshold` and the compliant host's inference is `Invalidated` (`Invalid++`), by my reading of `resolveChallengeTalliesLocked`. On #1903 I tested the steps up to the `Valid:false` vote, not a full challenge run.

A related hardening point: verifiers accept an error-miss on a client-fault Finish when `SiblingServedPrompt` (`devshard/host/timeout.go:490`) holds, i.e. a sibling with the same prompt hash finished with `OutputTokens > 0`. The rule doesn't check the error type, so it would accept such a miss for a context-length refusal if a gateway sent one. Today's gateway doesn't: it sends an error-miss only for `errorTerminal` attempts, and a context-length message is not one.

A gateway pre-check doesn't solve this. The gateway sets `max_tokens` itself (the default `request_max_tokens_cap` is 4096) but has no tokenizer. It knows only the body size in bytes (`gateway.go:2751`, "1 token ~= 4 bytes"), so it can't tell a 399k-token prompt from a 401k one. Only a real token count shows whether the request was over the limit.

Proposal: a context-length refusal counts against the host only if the request is shown to fit the governance limit.

- The fix for the validation path: in `replayClientFault`, a validator whose replay served doesn't vote `Valid:false` straight away. It first counts the prompt tokens itself (`/tokenize` on its ML node, or the replay's usage) and confirms the client fault when that count plus `rec.MaxTokens` exceeds the limit. A forged context-length 400 on a prompt that fits still fails validation, as asked in the earlier review of #1903 and fixed there in d5fbfa38c.
- Hardening: in `SiblingServedPrompt`, also require `sibling.InputTokens + rec.MaxTokens <= limit(rec.Model)`. Both values are signed (the sibling's Finish and the request) and checked against the verifier's own applied state, so nothing comes from the refusing host's error text. Actual output is not enough, because vLLM rejects on prompt plus requested `max_tokens` before generating: a 397k-token prompt with the default `max_tokens` 4096 is refused at 400k even if the sibling then produced 500 tokens.
- `limit(model)` comes from the governance model args, or `DevshardEscrow.max_model_len` after #1763, not from the gateway-only `modelContextLimits`, because verifiers and validators need it too.

Both checks are small on top of #1903. I can open them as a follow-up PR against the branch #1903 lands in, or add them to #1903 if @zpoken prefers.

</div>

---

> 🔄 **Auto-synced** from [Issue #2078](https://github.com/gonka-ai/gonka/issues/2078) every hour.
