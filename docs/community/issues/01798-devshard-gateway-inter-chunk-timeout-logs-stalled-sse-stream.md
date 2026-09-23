---
title: "#1798 — devshard gateway: inter-chunk timeout logs stalled SSE streams but does not cancel them"
source: https://github.com/gonka-ai/gonka/issues/1798
issue_number: 1798
synced_at: 2026-09-23T17:12:58Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    devshard gateway: inter-chunk timeout logs stalled SSE streams but does not cancel them
    <span class="issues-number">#1798</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/aikuznetsov">@aikuznetsov</a> opened 2026-09-18 02:37 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-09-18 21:23 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
A successful HTTP status only means that the response headers were received. The request can still hang indefinitely while reading the SSE body if the upstream keeps the connection open without sending another event.

This can happen here:

https://github.com/gonka-ai/gonka/blob/87940400cd633e514349580185ebce8cfd23502d/devshard/transport/client.go#L333-L349

After detecting `text/event-stream`, the client enters `parseSSEResponse()`, which blocks while waiting for the next SSE line:

https://github.com/gonka-ai/gonka/blob/87940400cd633e514349580185ebce8cfd23502d/devshard/transport/client.go#L381-L420

If the connection remains open but no additional bytes, EOF, or socket error arrive, `readBoundedSSELine()` does not return. As a result, no error reaches the retry logic, so no retry is started.

## Existing timeout behavior

The gateway defines an inter-chunk timeout and describes it as the limit after which a stalled winner should be aborted:

https://github.com/gonka-ai/gonka/blob/87940400cd633e514349580185ebce8cfd23502d/devshard/cmd/devshardctl/redundancy.go#L341-L354

However, the configured `InterChunkStallTimeout` is currently not used when calculating the stall deadline. The code uses the separate `InterChunkStallLogThreshold` instead:

https://github.com/gonka-ai/gonka/blob/87940400cd633e514349580185ebce8cfd23502d/devshard/cmd/devshardctl/redundancy.go#L2114-L2132

When that timer fires, the gateway only records `winner_stalled_after_content`. It does not cancel the request:

https://github.com/gonka-ai/gonka/blob/87940400cd633e514349580185ebce8cfd23502d/devshard/cmd/devshardctl/redundancy.go#L2430-L2463

The request is actually cancelled only when `StreamingAttemptHardTimeout` fires:

https://github.com/gonka-ai/gonka/blob/87940400cd633e514349580185ebce8cfd23502d/devshard/cmd/devshardctl/redundancy.go#L2464-L2483

That timeout defaults to 30 minutes:

https://github.com/gonka-ai/gonka/blob/87940400cd633e514349580185ebce8cfd23502d/devshard/cmd/devshardctl/redundancy.go#L38-L41

## Expected behavior

Once the winning stream has produced content, receiving no meaningful SSE events for `InterChunkStallTimeout` should:

1. Cancel the upstream request.
2. Close the response body.
3. Return a typed retryable error.
4. Retry against another eligible host, if possible.

The timeout should track meaningful `data:` events rather than arbitrary network activity. SSE comments such as `: keepalive` should not keep a generation alive indefinitely.

## Suggested change

Use `InterChunkStallTimeout` as a sliding deadline based on the timestamp of the last meaningful SSE event. When the deadline expires, call the attempt's cancellation function and classify the result as a retryable stalled-stream failure.

The existing 30-minute `StreamingAttemptHardTimeout` should remain as an absolute safety limit, independent of stream activity.
</div>

---

> 🔄 **Auto-synced** from [Issue #1798](https://github.com/gonka-ai/gonka/issues/1798) every hour.
