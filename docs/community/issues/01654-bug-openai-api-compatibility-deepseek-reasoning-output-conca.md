---
title: "#1654 — ⁠[Bug] OpenAI API compatibility: DeepSeek reasoning output concatenated into content & invalid reasoning_effort validation⁠"
source: https://github.com/gonka-ai/gonka/issues/1654
issue_number: 1654
synced_at: 2026-08-29T09:08:53Z
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
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-08-28 23:25 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span></div>
</div>

<div class="issues-content" markdown="1">
### Summary
When using `deepseek-ai/DeepSeek-V4-Flash-0731` via Open Broker (`api.openbroker.gonka.gg`), the gateway fails to parse reasoning tokens into `message.reasoning_content`.

Instead, the model's scratchpad/CoT is merged into `message.content` as plain text without any `<think>` tags. This breaks downstream agent UI systems (e.g., Nous Hermes, LangChain) because agents ingest their own scratchpad as part of the assistant's final response, polluting dialogue context.

---

### Comparison Logs (Captured on Aug 26)

**Prompt:**
`n2m-probe-1979. What is 23 multiplied by 17? Think step by step, then reply with only the integer.`

#### 1. Official DeepSeek API (Expected Behavior)
- Reasoning process is isolated in `reasoning_content`.
- `content` contains strictly the final response.
- `usage` properly reflects `reasoning_tokens`.

```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "391",
        "reasoning_content": "We need answer only integer. Need compute 23*17=391..."
      }
    }
  ],
  "usage": {
    "completion_tokens_details": {
      "reasoning_tokens": 34
    }
  }
}

2. Open Broker Direct Call (Observed Behavior)
⚬ Host/Node: devshard-63078-9577 (vllm-0.25.1)
⚬ CoT and final answer are merged into content.
⚬ No <think> tags are provided to filter output on the client side.
⚬ reasoning_content is null.
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "23 × 17 = 23 × (10 + 7) = 230 + 161 = 391. \n\n391",
        "reasoning": null,
        "reasoning_content": null
      }
    }
  ],
  "usage": {
    "completion_tokens": 27,
    "prompt_tokens": 34,
    "total_tokens": 61
  }
}


</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-08-28 23:21 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <ul>
<li><code>reasoning_effort</code> will be available in the new gateway.</li>
<li>The "reply with only the integer" shape is in tension with the inference-validation floor (<code>min_tokens</code> is currently 64). Dropping that to 1 would make a short numeric answer possible, but it is a protocol tradeoff (validation / accounting) </li>
<li>Forcing reasoning into a separate field is not something that can be assumed across hosts today (uneven <code>--reasoning-parser</code> / vLLM V2 support).</li>
</ul>
<p>There is no broker-side workaround that looks safe to ship. The remaining question is a design one — whether to keep the validation floor or treat <code>min_tokens: 1</code> as an explicit tradeoff. That needs a discussion before anyone can promise the official DeepSeek <code>reasoning_content</code> split. Happy to have community input on that tradeoff; @qdanik please correct if anything is wrong </p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1654](https://github.com/gonka-ai/gonka/issues/1654) every hour.
