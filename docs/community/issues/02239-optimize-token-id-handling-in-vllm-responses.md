---
title: "#2239 — Optimize token ID handling in vLLM responses"
source: https://github.com/gonka-ai/gonka/issues/2239
issue_number: 2239
synced_at: 2026-11-06T20:56:47Z
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
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-11-06 19:10 UTC</span>
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

> 🔄 **Auto-synced** from [Issue #2239](https://github.com/gonka-ai/gonka/issues/2239) every hour.
