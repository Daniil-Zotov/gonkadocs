---
title: "#1955 — [BUG] `min_tokens` floor (MinTokensFloor=64) breaks tool calling: runaway garbage, fabricated tool results, up to max_tokens billed per turn"
source: https://github.com/gonka-ai/gonka/issues/1955
issue_number: 1955
synced_at: 2026-10-09T20:59:51Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    [BUG] `min_tokens` floor (MinTokensFloor=64) breaks tool calling: runaway garbage, fabricated tool results, up to max_tokens billed per turn
    <span class="issues-number">#1955</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/KTibow">@KTibow</a> opened 2026-10-08 23:48 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-10-08 23:50 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span></div>
</div>

<div class="issues-content" markdown="1">
## Summary
Every inference request runs with `min_tokens >= 64` (`EnforceTokenBudgetFloor`, #1391), and `stop_token_ids` are stripped. This masks every stop token, including end-of-turn and tool-call terminators, until 64 tokens have been generated. A tool-call turn naturally ends after a few dozen tokens, so the model is forced to keep generating past its own end. On the public broker this turns a correct tool call into one of three things: 2,000 tokens of degenerate garbage (GLM-5.3-Flash, running to `max_tokens`), a fabricated tool result with a fake success message (GLM-5.3-Flash), or a premature "Done." (DeepSeek-V4-Flash). In each case the tool call itself is valid and `finish_reason` is `tool_calls`, so agent frameworks accept the turn and write the junk into conversation history. Output is deterministic, so retries reproduce it exactly. Short answers (yes/no, labels, routing) get padded the same way.

## Motivation
- Tool-calling agents are the main thing people point at the public brokers; most of the FAQ's Inference section is about agent clients (Hermes, OpenClaw, Kilo Code, OpenCode). Nearly every tool-call turn is shorter than 64 tokens.
- The failure is silent. The tool call parses, `finish_reason` looks right, and the garbage or fabricated result lands in the agent's history, where it poisons later turns.
- Validation work is now being layered on top of the floor (#1873), so it gets harder to change the longer it stays.

## Impact
- Who is affected (hosts, developers, validators): Developers and agents using tool calling through any broker, plus anyone making short-answer calls. Brokers absorb billing disputes and support load. Hosts burn GPU on runaway output (up to `max_tokens` per turn). Validators are not functionally affected.
- Is the effect network-wide or limited: Network-wide. The floor lives in `common/completionapi` and is enforced on executor, validator, and gateway, so no broker can opt out.
- Likelihood (common, intermittent, or edge case): Common and deterministic for any turn whose natural output is under 64 tokens. The GLM case below reproduced in 4 of 4 attempts.
- Affected components: `common/completionapi` (`MinTokensFloor`, `EnforceTokenBudgetFloor`, `ModifyRequestBodyWithLogprobsMode`), `common/validation` (`ExecuteValidation`), `devshard/cmd/devshardctl` (`applyTokenBudgetFloor`), the devshardd executor path, and the FAQ.

## Detailed description
### Observed (api.openbroker.gonka.gg, 2026-10-08, one `bash` tool, `max_tokens: 2000`)

| Case | finish_reason | completion_tokens | content |
|---|---|---|---|
| GLM-5.3-Flash, system prompt | `tool_calls` | **2000** (= max_tokens) | 11,728 chars of `ynamoDbContext.json $ DynamoDbContext.json � DynamoDbContext.json& …` |
| GLM-5.3-Flash, no system prompt | `tool_calls` | 169 | Fabricated tool output and success message ("The command output `hi` as expected…"), then starts narrating its reasoning |
| DeepSeek-V4-Flash-0731, system prompt | `tool_calls` | 66 | `Done.` (claims completion before the tool has run) |
| DeepSeek-V4-Flash-0731, no system prompt | `tool_calls` | 82 | empty |

- In the GLM system-prompt case, the tool call itself is correct (`{"command": "echo hi"}`). The damage is everything generated after it.
- All 4 attempts of that case were byte-identical: same `tool_call` id (`chatcmpl-tool-ad01c018ae3f2499`), same 11,728 chars. Client retries don't recover.
- That case bills 2,000 completion tokens for a tool call that needs a few dozen, at about 26 s per call.

### Reproduce
```python
import json, os, urllib.request

BROKER = os.environ.get("GONKA_BROKER", "https://api.openbroker.gonka.gg/v1")
KEY = os.environ["GONKA_KEY"]

def call(payload):
    req = urllib.request.Request(f"{BROKER}/chat/completions",
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=180))

tools = [{"type": "function", "function": {"name": "bash", "description": "Run a shell command",
    "parameters": {"type": "object", "properties": {"command": {"type": "string"}}, "required": ["command"]}}}]
sysmsg = {"role": "system", "content": "You are a coding agent. Use tools to run commands."}

cases = [
    ("GLM  +sys ", "zai-org/GLM-5.3-Flash", [sysmsg, {"role": "user", "content": "run echo hi"}]),
    ("GLM  nosys", "zai-org/GLM-5.3-Flash", [{"role": "user", "content": "run echo hi using the tool"}]),
    ("DpSk +sys ", "deepseek-ai/DeepSeek-V4-Flash-0731", [sysmsg, {"role": "user", "content": "run echo hi"}]),
    ("DpSk nosys", "deepseek-ai/DeepSeek-V4-Flash-0731", [{"role": "user", "content": "run echo hi using the tool"}]),
]
for label, model, msgs in cases:
    d = call({"model": model, "messages": msgs, "tools": tools, "max_tokens": 2000})
    ch = d["choices"][0]; msg = ch["message"]; ct = msg.get("content") or ""
    print(f"{label}: finish={ch.get('finish_reason')} completion_tokens={d['usage']['completion_tokens']} content_chars={len(ct)}")
    print(f"   tool_calls: {json.dumps(msg.get('tool_calls'))[:160]}")
    print(f"   content:    {ct[:150]!r}")
```

### Mechanism
- **Stop tokens are masked.** `min_tokens` suppresses every stop token (EOS, generation-config EOS ids, `stop_token_ids`) until it is reached. A tool-call turn ends with an end-of-turn token after a few dozen tokens. Masking that token forces the model off-distribution, and what happens next depends on the model:
  - it hallucinates the tool result and writes a final answer (GLM, no system prompt);
  - it writes a premature "Done." and stops right after the floor (DeepSeek, 66 tokens);
  - it degenerates into a loop that never produces a stop token and runs to `max_tokens` (GLM, system prompt).
- **Output is deterministic.** This is likely due to the seed `ModifyRequestBodyWithLogprobsMode` injects, so the same bad continuation comes back every time.
- **Control to confirm the cause.** Send the same GLM system-prompt request with a command long enough that the tool call alone exceeds 64 tokens.
  - If it comes back clean, the floor is the cause.
  - If it still produces garbage, the stripped `stop_token_ids` are. Both changes come from #1391.

### The concern the floor addresses
H1 #3833622 is a real gap. With only a few output positions, the logprob-distance check can't distinguish the real model from a substitute. Long-prompt, short-output requests are exactly where substitution pays, because the executor is paid for a big-model prefill it may not have run. The floor closes the gap by lengthening the user's output. The fixes below close it on the verification side instead.

### Proposed fixes
1. **Stop delivering the padding (short-term, validation unchanged).** Keep generating 64 positions for validation, but have the vLLM fork record the first position where a masked stop token would have been selected. If that position comes before 64:
   - end generation at exactly 64 tokens, so there is no runaway;
   - deliver only the tokens up to the natural stop, with its natural `finish_reason`;
   - bill the natural token count, or a fixed floor fee, but never return the padding to the user.

   Validators replay all 64 positions as they do today and can check the claimed cutoff. A dishonest cutoff only shortens the executor's own answer.
2. **Use `prompt_logprobs` instead of `min_tokens`.** Logprobs at the last N prompt positions have three useful properties:
   - they are already computed during prefill;
   - they can't be reproduced without running the real model over the whole prompt;
   - they are typically much higher-entropy than a one-word answer.

   Validating N prompt-tail positions plus the output positions gives at least 64 positions of signal without forcing generation. It also verifies the prefill, which is what long-prompt requests actually pay for.
3. **Restore `stop_token_ids`.** They were stripped because an out-of-vocab stop id CUDA-asserts the node. The `VocabularyResolver` from #1873 can reject those ids at the gateway instead.
4. **Fix the docs.** The FAQ still says the floor is 16.

### Acceptance criteria
- The GLM-5.3-Flash system-prompt case above returns one tool call, empty or short content, and `completion_tokens` well under 100.
- "Is 7 prime? Answer with only yes or no." returns `yes` with no trailing text.
- The model-substitution case from H1 #3833622 is still rejected (add a test if none exists).

### Links
- #1391 introduces the floor (H1 #3833622).
- #1873 builds on the floor and adds `VocabularyResolver`.
- FAQ: https://gonka.ai/docs/FAQ/
</div>

---

> 🔄 **Auto-synced** from [Issue #1955](https://github.com/gonka-ai/gonka/issues/1955) every hour.
