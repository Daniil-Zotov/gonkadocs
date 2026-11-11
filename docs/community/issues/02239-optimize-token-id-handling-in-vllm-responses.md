---
title: "#2239 — Optimize token ID handling in vLLM responses"
source: https://github.com/gonka-ai/gonka/issues/2239
issue_number: 2239
synced_at: 2026-11-11T06:43:48Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Optimize token ID handling in vLLM responses
    <span class="issues-number">#2239</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-11-06 19:10 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-11-07 11:26 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
There is one part of the current implementation that works without any changes to vLLM itself, but could likely be improved.

Currently, we enable the `return_token_ids` parameter so that all token IDs are available when processing logprobs.

The downside is that vLLM also returns the full list of generated token IDs as a separate field in the response. We do not actually need this additional data, so it creates unnecessary response overhead.

We also currently have some workaround logic around trimming / slicing the returned data.

## Goal

Investigate whether we can get the token information required for logprobs **without returning the redundant full token ID list**, or otherwise simplify this flow.

Ideally, we should:

* avoid unnecessary data in the vLLM response;
* remove or simplify the current trimming workaround;
* reduce serialization / response processing overhead;
* potentially save a small amount of latency, likely on the order of a few milliseconds.

## Expected outcome

Find and implement a cleaner approach to token ID handling, if one exists, and measure whether it provides a meaningful latency improvement.

Changes to vLLM itself are acceptable to investigate if that turns out to be the cleanest solution, but they are not necessarily required.
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/cyberdelamain">@cyberdelamain</a></span>
    <span class="issues-meta-item">commented 2026-11-07 11:26 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>I looked at where <code>return_token_ids</code> costs time on devshard v7 (860cd69d5) and the vLLM forks (release/v0.25.1, v0.28.0-glm53, v0.30.0-decode-int).</p>
<p><strong>Why it can't simply be turned off.</strong> In <code>serving_chat.py</code> the flag does two things: it attaches ids, and it keeps chunks whose <code>delta_message</code> is <code>None</code> (reasoning <code>&lt;think&gt;</code>/<code>&lt;/think&gt;</code>, tool-call control tokens) — <code>if output.finish_reason is None and (not request.return_token_ids or hide_stream_metadata): continue</code>. Without it those tokens and their logprobs vanish from the stream while still counted in <code>usage.completion_tokens</code>, so enforced-token reconstruction breaks. Nothing in validation reads <code>token_ids</code>/<code>prompt_token_ids</code> (<code>fieldsNoValidatorReads</code>); per-chunk <code>token_ids</code> is small, ~20 B.</p>
<p><strong>Where the cost is.</strong> The first chunk carries the whole <code>prompt_token_ids</code> (~6.3 B per prompt token). Measured on M1, per request on the TTFT path:</p>
<table>
<thead>
<tr>
<th>prompt tokens</th>
<th>first chunk</th>
<th>vLLM build+serialize (pydantic)</th>
<th>host <code>ProcessStreamedResponse</code></th>
</tr>
</thead>
<tbody>
<tr>
<td>2k</td>
<td>13 KB</td>
<td>0.06 ms</td>
<td>0.12 ms</td>
</tr>
<tr>
<td>32k</td>
<td>200 KB</td>
<td>0.8 ms</td>
<td>1.5 ms</td>
</tr>
<tr>
<td>100k</td>
<td>626 KB</td>
<td>2.6 ms</td>
<td>4.4 ms</td>
</tr>
</tbody>
</table>
<p>The vLLM part runs in the API server event loop, and validators pay it again on replay. The host part is the trimming workaround (<code>decodeDocumentWithoutUnreadFields</code> still scans the array into <code>json.RawMessage</code>).</p>
<p><strong>Suggested fix.</strong> In the gonka vLLM fork, split the flag: keep <code>None</code>-delta chunks under <code>return_token_ids</code> but emit <code>prompt_token_ids</code> (and per-chunk <code>token_ids</code>) only when a new <code>return_prompt_token_ids</code> / <code>include_token_ids</code> is set; devshard then stops asking for them and the trimming path becomes dead code for new engines. Older engines ignore the unknown field, so the host keeps the current strip until they are gone. I can take this if it helps.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2239](https://github.com/gonka-ai/gonka/issues/2239) every hour.
