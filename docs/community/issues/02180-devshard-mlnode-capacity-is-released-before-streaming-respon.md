---
title: "#2180 — devshard: MLNode capacity is released before streaming response consumption"
source: https://github.com/gonka-ai/gonka/issues/2180
issue_number: 2180
synced_at: 2026-11-07T00:58:38Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    devshard: MLNode capacity is released before streaming response consumption
    <span class="issues-number">#2180</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/ilyar">@ilyar</a> opened 2026-10-30 07:01 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-11-06 18:12 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #F9EDEA; color: #24292f; border-color: #F9EDEA;">Bug</span></div>
</div>

<div class="issues-content" markdown="1">
The standalone inference engine releases the NodeManager slot before the caller consumes the MLNode response body, so a streaming response can still be generating after its slot becomes available again

## Source evidence

The affected deployment uses `ghcr.io/gonka-ai/versiond:0.2.16-devshard-v6-rc1`, an image listed in the official [devshard/v6.0.0-rc1 release](https://github.com/gonka-ai/gonka/releases/tag/devshard/v6.0.0-rc1), with the DevShard runtime reporting `v6.0.0-rc1`

The lifecycle finding below comes from inspection of [engine.go at the release commit](https://github.com/gonka-ai/gonka/blob/6a41bc3429d1029dc787a3bc04f1a14f201be006/devshard/cmd/devshardd/inference/engine.go), rather than an isolated reproduction inside the image

`versiond` is the container image, while `devshardd` is the versioned binary it launches

- `executeMLRequest` passes `httpClient.Do` as the callback to `doWithLockedNode`
- `doWithLockedNode` calls `releaseNode` after that callback returns, then returns the response to its caller
- Streaming response processing happens afterwards in [execute.go](https://github.com/gonka-ai/gonka/blob/6a41bc3429d1029dc787a3bc04f1a14f201be006/devshard/cmd/devshardd/inference/execute.go)
- The passive fallback path also releases its local capacity reservation before returning the response

For a streaming response, receiving HTTP headers is not the end of generation, so this lifecycle does not bound active streaming work by `max_concurrent`

## Expected behaviour

Keep the execution reservation until the response body reaches its terminal state or is closed, release exactly once on success, cancellation and failure, and define how upstream work that continues after client cancellation is accounted for

## Reproduction to add

Use an ML endpoint that flushes response headers and one SSE chunk, then waits before completing the body, configure one available NodeManager slot and start a second inference while the first body is still open

Check the ordering of acquire, response headers, release and body completion, the second request must not acquire the same capacity before the first execution releases it

Repeat for the passive fallback path and for response-body read failures

## Verification boundary

This report is based on source inspection, the isolated reproduction above has not been executed and the contribution to any particular deployment's overload has not been quantified

The finding is separate from [gateway quarantine recovery](https://github.com/gonka-ai/gonka/issues/1506) and [speed-up hedging amplification](https://github.com/gonka-ai/gonka/issues/2105)


</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Ryanchen911">@Ryanchen911</a></span>
    <span class="issues-meta-item">commented 2026-11-04 06:16 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>This still reproduces on devshard/v7 (860cd69d5): the test from #2183 fails there with releases=1, and engine.go is the same as on v6.
Planned fix:
-doWithLockedNode keeps the slot after a 2xx/4xx response and wraps resp.Body. The wrapper releases the slot once, when the body -is closed. Both callers already close it after reading the stream.
-Transport errors and 5xx still release right away.
-A read error before EOF releases with TRANSPORT_ERROR instead of SUCCESS.
-The release runs even if the request context was cancelled.
-The fallback path (doWithFallbackNodes) frees its local capacity slot the same way.
-The test from #2183 is the regression test, with extra cases for a stream that breaks mid-way, a cancelled request and the fallback path.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/startupcompliancekit">@startupcompliancekit</a></span>
    <span class="issues-meta-item">commented 2026-11-06 18:12 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Is any unclaimed, separately rewarded work still available on #2180 now that #2213 includes the lifecycle fix and the follow-up from Ryanchen911/gonka#5?</p>
<p>If maintainers need independent integration/regression validation, I can take a bounded task covering delayed streams, capacity-one concurrent admission, completion/read-error/cancellation cleanup, and known/unknown passive fallback against the current fix. This is an offer to cover an agreed remaining task, not a claim that those tests are missing from #2213.</p>
<p>Before I start, please confirm the remaining deliverable and acceptance criteria, target branch, and stablecoin reward amount with its review and Host-approval conditions. If the existing PR covers all available work and no additional paid scope remains, please confirm that so duplicate work can be avoided.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2180](https://github.com/gonka-ai/gonka/issues/2180) every hour.
