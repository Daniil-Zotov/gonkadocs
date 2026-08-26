---
title: "#1654 — ⁠[Bug] OpenAI API compatibility: DeepSeek reasoning output concatenated into content & invalid reasoning_effort validation⁠"
source: https://github.com/gonka-ai/gonka/issues/1654
issue_number: 1654
synced_at: 2026-08-26T15:55:24Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    ⁠[Bug] OpenAI API compatibility: DeepSeek reasoning output concatenated into content & invalid reasoning_effort validation⁠
    <span class="issues-number">#1654</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/dmrtest">@dmrtest</a> opened 2026-08-26 15:07 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-08-26 15:07 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span></div>
</div>

<div class="issues-content" markdown="1">
### Summary
When querying `deepseek-ai/DeepSeek-V4-Flash-0731` via Open Broker, the OpenAI-compatible response parser concatenates the model's reasoning process (chain-of-thought) directly into `message.content` instead of outputting it to `message.reasoning_content` (or `delta.reasoning` / `delta.reasoning_content` in streaming mode).

This breaks downstream AI agent frameworks (e.g., Nous Hermes, LangChain, Cursor) because the agent ingests its own scratchpad as part of the assistant's final output, causing context pollution and loop failures.

Additionally, there are issues with the `reasoning_effort` parameter validation and execution speed.

---

### Observed Behavior
1. **Empty Reasoning Field:** `message.reasoning_content` is almost always `null` or empty.
2. **Polluted Content:** `<think>` tokens and internal scratchpad text are prefixed into `message.content`.
3. **Param Validation Issue:** `reasoning_effort=max` is rejected by the OpenAI-compat schema validator (returns 400/422).
4. **Performance:** `reasoning_effort=xhigh` takes ~6 minutes per completion, resulting in agent timeouts.

---

### Expected Behavior (Alignment with Official DeepSeek & OpenAI Specification)
1. **Thinking Output Split:**
   - Scratchpad/CoT output must be routed to `message.reasoning_content` (or `delta.reasoning_content` in SSE streams).
   - `message.content` should contain **only** the final user-facing response.
2. **Parameter Validation:** Support standard OpenAI parameters (`max` should be accepted, or mapped correctly without throwing validation errors).


Impact
High. Affects all agentic workflows using Open Broker endpoint for DeepSeek V4. Willing to assist with testing or providing more trace logs if needed.

</div>

---

> 🔄 **Auto-synced** from [Issue #1654](https://github.com/gonka-ai/gonka/issues/1654) every hour.
