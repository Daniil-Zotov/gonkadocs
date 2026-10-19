---
title: "#1722 — Incomplete HTTP 200 streams are cached and replayed as successful responses"
source: https://github.com/gonka-ai/gonka/issues/1722
issue_number: 1722
synced_at: 2026-10-19T20:00:19Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Incomplete HTTP 200 streams are cached and replayed as successful responses
    <span class="issues-number">#1722</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/aleksandr-cstl">@aleksandr-cstl</a> opened 2026-09-07 11:57 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-10-12 20:10 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Problem

The devshard gateway can store an incomplete streamed chat response in the one-hour response cache. Identical requests then receive the same partial body immediately instead of starting a new inference.

## Observed behavior

A production DeepSeek streaming request returned partial reasoning for 1,205.663 seconds and then closed without `finish_reason` or usage. Eight identical retries returned the same 1,369,407-byte body in 0.871–2.758 seconds. The response fingerprint was identical through two broker endpoints.

A second response included `data: [DONE]` but had no `finish_reason`, usage, or final answer. The DONE marker made the response appear complete to clients even though generation did not finish.

No request prompts or credentials are included in this report.

## Cause

`gatewayChatCacheCapture.cacheEntry` calls `cacheableResponse`, which accepts any non-empty HTTP 2xx body unless it contains a recognized error. It does not validate semantic SSE completion.

This combines badly with streaming paths that can append `[DONE]` after `RunInference` returns without a terminal model chunk. A partial response can therefore become a deterministic cached result for one hour.

## Expected behavior

A successful streaming response must be cached only when:

- every observed choice has a non-empty `finish_reason`;
- `[DONE]` occurs after those terminal choice events;
- the body has no OpenAI-style error event.

Previously cached incomplete stream entries should also be rejected on lookup.

## Reproduction

Pass this HTTP 200 body to `gatewayChatCacheCapture.cacheEntry` with `stream=true`:

```text
data: {"choices":[{"index":0,"delta":{"reasoning":"still working"},"finish_reason":null}]}

data: [DONE]
```

Current result: the entry is cacheable.

Expected result: the entry is rejected because `[DONE]` is framing, not semantic completion.

## Proposed fix

Validate semantic stream completion in the shared cache eligibility path used by capture, Set, and Get. A focused PR with regression tests will follow.

As a separate operational escape hatch, the gateway could honor request `Cache-Control: no-cache, no-store`. This header must not replace completion validation.
</div>

---

> 🔄 **Auto-synced** from [Issue #1722](https://github.com/gonka-ai/gonka/issues/1722) every hour.
