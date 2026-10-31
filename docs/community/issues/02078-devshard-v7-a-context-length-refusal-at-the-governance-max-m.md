---
title: "#2078 — devshard v7: a context-length refusal at the governance --max-model-len should never cost the host a miss or an invalidation"
source: https://github.com/gonka-ai/gonka/issues/2078
issue_number: 2078
synced_at: 2026-10-31T00:52:29Z
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
    <span class="issues-meta-item">9 comments</span>
    <span class="issues-meta-item">Updated 2026-10-27 19:40 UTC</span>
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

## 💬 Comments (9)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/a-kuprin">@a-kuprin</a></span>
    <span class="issues-meta-item">commented 2026-10-24 06:49 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>What else I think on this point.</p>
<p>executor that responds with max-context-length error, anyway, should provide logits for generated output tokens.
max-context-length &gt;= input_tokens + output_tokens</p>
<p>When we are validating we anyway need logits for output tokens</p>
<p>Overall it looks like fixes need changes to MLNode</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/cyberdelamain">@cyberdelamain</a></span>
    <span class="issues-meta-item">commented 2026-10-24 07:25 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@a-kuprin agreed: input + actual output is what has to fit, and validation needs the output logits anyway, so the better fix is that the executor generates instead of refusing.</p>
<p>Today vLLM refuses before generating because it checks prompt + requested <code>max_tokens</code> at tokenization (<code>TokenizeParams</code>, "This model's maximum context length is N tokens. However, you requested M output tokens and your prompt contains K input tokens…"). Later <code>get_max_tokens</code> would already clamp <code>max_tokens</code> to <code>max_model_len - prompt_len</code>, but the request never gets that far. If the ML node checks only the prompt against <code>--max-model-len</code> and lets <code>max_tokens</code> be clamped, a request whose prompt fits returns tokens and logits with <code>finish_reason: length</code>, and validators replay those enforced tokens as usual. No client-fault path is needed for it.</p>
<p>What stays is a prompt that alone is at or above the limit: nothing can be generated, so there are no logits. For that case my #2093 only needs to check <code>prompt_tokens &gt;= limit</code> instead of <code>prompt_tokens + max_tokens &gt; limit</code>. I'll narrow it once the ML node change exists.</p>
<p>I can take the ML node change too (the vLLM fork / plugin side), unless you or @zpoken already have it planned.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/a-kuprin">@a-kuprin</a></span>
    <span class="issues-meta-item">commented 2026-10-24 07:33 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <blockquote>
<p>Today vLLM refuses before generating because it checks prompt + requested max_tokens at tokenization</p>
</blockquote>
<p>I think it's a good way to refuse before generation (we shouldn't spend resources if we are pretty sure it will not fit the context).</p>
<p>So validation part is better to fix: we should have special context length validation path where vllm just tokenizes and checks  <code>prompt + requested max_tokens &lt; max_model_len</code></p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/cyberdelamain">@cyberdelamain</a></span>
    <span class="issues-meta-item">commented 2026-10-24 08:42 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@a-kuprin #2093 is that path. On a client-fault Finish the validator counts the prompt on its own ML node and confirms the fault only if <code>prompt_tokens + max_tokens</code> exceeds <code>--max-model-len</code> from the epoch's model snapshot. vLLM accepts equality, so the check is <code>&gt;</code>. A prompt that fits keeps <code>Valid:false</code>.</p>
<p>Two differences from "just tokenize":</p>
<ul>
<li>The count is the same request with <code>stream:false, max_tokens:1</code>, so it costs one prefill. vLLM's <code>/tokenize</code> takes chat messages and returns <code>count</code> without a prefill. The validator can reach it today through the ML node's port 5000 compatibility server (<code>proxy.py</code>, which forwards any path), though that block is marked temporary and the main port forwards only <code>/v1/*</code>. I haven't checked that <code>/tokenize</code> renders exactly the prompt chat/completions serves for these models; the 1-token request goes through the same path.</li>
<li>The count runs after a replay that served. I can move it in front: over the limit, confirm without a replay; otherwise, or if the count fails or the limit is unknown, replay as now, which covers other client faults and a forged refusal.</li>
</ul>
<p>I'll make the reorder in #2093 if that matches what you meant, and switch the count to <code>/tokenize</code> if you prefer it over the 1-token request.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/a-kuprin">@a-kuprin</a></span>
    <span class="issues-meta-item">commented 2026-10-24 08:54 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>I think we can skip prefill phase here and make cheaper validation</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/cyberdelamain">@cyberdelamain</a></span>
    <span class="issues-meta-item">commented 2026-10-24 10:41 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@a-kuprin Done in #2093: the count is vLLM <code>/tokenize</code> on the validator's ML node, so there is no prefill and no <code>max_tokens:1</code> request. Following your note on #1903, #2093 is now standalone on <code>devshard/v7</code> (the check, the governance-limit resolver and the <code>/tokenize</code> call), so it can land first; #1903 then calls it before the replay.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/redstartechno">@redstartechno</a></span>
    <span class="issues-meta-item">commented 2026-10-26 21:00 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Field data from one DeepSeek-V4-Flash host, in case it helps size this.</p>
<p>Epoch 432 (2026-10-21, 10:30-13:30 UTC): one client sent about 9,300 requests with <code>input_length</code> 590,231 characters and <code>max_tokens</code> 64 (5,874 distinct prompt hashes, a new escrow every few minutes). Every executor returned 400 at once (1,003 on our host, 0 before and 0 after the window), each nonce sealed as TIMEOUT with <code>Missed++</code>, and the client got the reserved cost back. The DeepSeek group's miss share went from 1-3 % per hour to 89-100 % for three hours (33.6 % for the epoch at the time, 9,902 of 29,497 sealed).</p>
<p>Epoch 437 (2026-10-26): 5 more of the same shape on our slot. One prompt of 1,551,611 characters was served by slot 12 at 392,499 input tokens and refused by us with <code>max_tokens</code> 8,192 (392,499 + 8,192 &gt; 400,000), so it is the prompt-plus-max_tokens rule, not the prompt alone. Another request in the same escrow finished elsewhere with 401,929 input tokens, which confirms a host running above the governance limit (#1911).</p>
<p>Two notes on the mechanics:</p>
<ul>
<li><code>/tokenize</code> cost: 0.5 s CPU for a 1.57M-character chat request on our node, so the count in #2093 is cheap even at the limit.</li>
<li>With #1903 plus #2093 the executor no longer takes the miss, but the client still pays nothing for a request no host can serve (the 0/0 Finish refunds the reservation). The 432 flood cost the sender only escrow fees. Is a fee for a confirmed client fault something you want on v7, or is that out of scope?</li>
</ul>
<p>Per-inference extract for the 432 window (escrow, inference id, input_length, max_tokens, status, timestamps) is available on request.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/cyberdelamain">@cyberdelamain</a></span>
    <span class="issues-meta-item">commented 2026-10-27 01:52 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@redstartechno on the epoch 432 window: <code>input_length</code> is the request body in bytes (<code>len(body)</code> in <code>devshardctl/proxy.go</code>), and your epoch 437 prompt came to about 3.95 bytes per token, so 590,231 bytes would be around 150k tokens, well under 400,000 even with <code>max_tokens</code> 64. Was the 400 there vLLM's "maximum context length" message or another rejection? If another, #1903's 400/422 client-fault Finish covers it and #2093's count is not involved.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/redstartechno">@redstartechno</a></span>
    <span class="issues-meta-item">commented 2026-10-27 19:40 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@cyberdelamain you're right about the unit: <code>input_length</code> is <code>len(body)</code> (<code>devshardctl/proxy.go:257</code>), so the "characters" figures in my comment are request-body bytes.</p>
<p>We don't have the error text for the 432 window. vLLM doesn't log the 400 reason at INFO, our devshard log has only <code>get usage: JsonCompletionResponse: no usage found</code> for each of the 1,003, and payloads of failed executions aren't stored. At the ~3.95 bytes per token of the 437 prompt, 590,231 bytes is about 150k tokens, so it was most likely another rejection: that window belongs with #1903's client-fault Finish, not with the count in #2093. Please read the 432 numbers as a 400 flood of unknown cause, not as a context-limit case.</p>
<p>The 437 case (392,499 prompt tokens, counted by the host that served it, plus 8,192 <code>max_tokens</code> &gt; 400,000) is unaffected.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2078](https://github.com/gonka-ai/gonka/issues/2078) every hour.
