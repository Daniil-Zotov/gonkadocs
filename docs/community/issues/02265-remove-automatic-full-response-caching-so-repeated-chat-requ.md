---
title: "#2265 — Remove automatic full-response caching so repeated chat requests start a new inference"
source: https://github.com/gonka-ai/gonka/issues/2265
issue_number: 2265
synced_at: 2026-11-13T16:32:15Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Remove automatic full-response caching so repeated chat requests start a new inference
    <span class="issues-number">#2265</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/hertznsk">@hertznsk</a> opened 2026-11-13 11:45 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-11-13 11:46 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Proposal

Permanently remove automatic full-response caching for chat completions based on matching model and normalized request body. A new client POST should start a new inference attempt even when its body matches a previous request.

This concerns the gateway chat response cache, not vLLM prefix/KV caching or replay of the result of an existing protocol operation.

## Related issues and pull requests

- #1722 reported incomplete HTTP 200 SSE responses being cached.
- #1723 was superseded by #1827. #1827 has been merged into devshard-0.2.x-v6 and checks response completion before caching.
- #1864 proposed caller-scoped cache entries, but preserved retry deduplication and was closed without merging.

This proposal changes the API contract rather than duplicating the completion-validation fix. A correctly terminated response can still be unusable to the application.

## Problem

An agent client may repeat a request because the model failed to call the output tool, returned an unusable answer, or did not follow the task. That retry needs a fresh generation attempt. An identical request body does not establish that the client wants the previous result.

The current cache conflates two different intentions:

1. Retrieve the result of an already executed operation.
2. Start another attempt with the same inputs.

The Response cache and request accounting section of devshard/docs/proxy-architecture.md explicitly describes serving equivalent requests without consuming another devshard nonce. In the inspected main checkout (8af3f3f692c2809f7c61f4f20cb4fa22d6ec9eee), response_cache.go defines a one-hour TTL and keys entries by model, response-format intent, and normalized request body.

Checking finish_reason, JSON, and SSE structure can reject protocol failures, but cannot generally determine whether an answer is useful or correct for the application. A response with finish_reason: stop may still require another attempt. Caching it makes a retry reproduce the failure instead of allowing recovery.

The project's own tests already account for this: WaitGatewayChatExpectFailure in devshard/testenv/citest/harness/adversarial.go changes the request body on each attempt so an early HTTP 200 cannot freeze subsequent checks on cache hits. Ordinary clients should not need to add random prompt text or change semantic parameters to obtain a new execution.

## Motivating observations

Agent requests to DeepSeek-V4-Flash-0731 returned no tool calls despite an outgoing tool_choice: required and a token budget of 16384. Responses reported usage of 512 input / 128 output tokens. Two consecutive attempts for the same agent returned identical unfinished reasoning. The saved response summaries contained finish_reason: stop.

These observations do not prove a cache hit or identify the component responsible for the original bad response. Broker and host logs would be needed to establish that. They illustrate why clients need a fresh attempt even after a formally successful response. Underlying host execution failures should be investigated separately.

## Expected behavior

- Permanently remove automatic replay of a full response based on the body of a new chat-completions request, rather than merely shortening the TTL or temporarily disabling the cache.
- Two separate identical client POSTs should start two separate inference attempts. Their generated text need not differ; the requirement is fresh execution rather than cache replay.
- Preserve prefix/KV caching to accelerate prompt processing.
- Preserve replay of the same protocol operation where needed for reconnection and response-hash consistency. That is not a new inference and is outside this proposal.
- If the API needs client-operation deduplication, define an explicit operation-identifier contract separately instead of inferring identity from request contents.

## Verification

A regression test should send two identical client POSTs and assert two fresh runtime executions. Re-delivery of a single existing protocol operation must still avoid re-running the model.

The trade-off is additional compute for requests that would previously have been cache hits. For agent recovery, this is the intended cost of another attempt. Normal conversation turns change the history, while repeated prefixes can still benefit from KV caching.

</div>

---

> 🔄 **Auto-synced** from [Issue #2265](https://github.com/gonka-ai/gonka/issues/2265) every hour.
