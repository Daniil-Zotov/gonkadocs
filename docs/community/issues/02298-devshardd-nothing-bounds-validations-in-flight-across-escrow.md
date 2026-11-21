---
title: "#2298 — devshardd: nothing bounds validations in flight across escrows, so a PoC start makes hundreds of them parse replays at once"
source: https://github.com/gonka-ai/gonka/issues/2298
issue_number: 2298
synced_at: 2026-11-21T23:27:38Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    devshardd: nothing bounds validations in flight across escrows, so a PoC start makes hundreds of them parse replays at once
    <span class="issues-number">#2298</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/kaileido">@kaileido</a> opened 2026-11-19 21:47 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-11-21 17:17 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
### What happens

Every escrow host in a devshardd process runs its own 20 validation workers, and they all share one `Validator` that has no process-wide limit. Each validation fetches both executor payloads, then holds them while it reads and parses the whole replay and scores it. When the ML nodes switch to PoC, all replays in flight end within seconds, so all of those validations parse at the same moment.

Seen on a validator running devshardd v6.0.0 (61 GB host, no swap) at a confirmation PoC on 2026-11-18, generation start 12:29:13 UTC. The code paths below are the same on the current `devshard/v7` tip `34ddd777`.

- The process's own memory snapshot at 12:23:05 logged `sessions=932 validating=766` (`validating` counts queued and in-flight validations), `heap_alloc` 30.4 GB.
- Between 12:29:14.024 and 12:29:25.346, 384 validations got their replay back (384 `inflated token counts` warnings), so at least 384 held their payloads at PoC start.
- Container RSS went from 37.76 GB at 12:29:30 to 51.24 GB at 12:30:00. The child exited at 12:32:20 (`child exited version=v6 error="exit status 1"`) and RSS fell to 6.3 GB.
- The bytes per validation were not measured on this host. #2293 measures about 20 MB allocated per validation for an 800-token replay with 5 top logprobs; these replays averaged 2,436 returned tokens against 10,752 claimed.

### Where

- One `Validator` per process: [app.go#L309-L321](https://github.com/gonka-ai/gonka/blob/34ddd777475be05f583945add3c275b490f3cf39/devshard/cmd/devshardd/app.go#L309-L321)
- One `Host` per escrow: [session/manager.go#L1008](https://github.com/gonka-ai/gonka/blob/34ddd777475be05f583945add3c275b490f3cf39/devshard/cmd/devshardd/session/manager.go#L1008), [session/manager.go#L1470](https://github.com/gonka-ai/gonka/blob/34ddd777475be05f583945add3c275b490f3cf39/devshard/cmd/devshardd/session/manager.go#L1470), each starting 20 workers: [host.go#L115-L116](https://github.com/gonka-ai/gonka/blob/34ddd777475be05f583945add3c275b490f3cf39/devshard/host/host.go#L115-L116), [host.go#L336-L338](https://github.com/gonka-ai/gonka/blob/34ddd777475be05f583945add3c275b490f3cf39/devshard/host/host.go#L336-L338)
- `CanValidate` checks only the model's credit: [validator.go#L109-L118](https://github.com/gonka-ai/gonka/blob/34ddd777475be05f583945add3c275b490f3cf39/devshard/cmd/devshardd/inference/validator.go#L109-L118)
- `Validate` fetches the payloads and keeps them through the replay and scoring: [validator.go#L122](https://github.com/gonka-ai/gonka/blob/34ddd777475be05f583945add3c275b490f3cf39/devshard/cmd/devshardd/inference/validator.go#L122), [validator.go#L157-L179](https://github.com/gonka-ai/gonka/blob/34ddd777475be05f583945add3c275b490f3cf39/devshard/cmd/devshardd/inference/validator.go#L157-L179)
- The replay body is read whole and parsed in `executeMLRequest` and again in `ExecuteValidationWithPolicy`: [validator.go#L423-L428](https://github.com/gonka-ai/gonka/blob/34ddd777475be05f583945add3c275b490f3cf39/devshard/cmd/devshardd/inference/validator.go#L423-L428), [validation.go#L519-L555](https://github.com/gonka-ai/gonka/blob/34ddd777475be05f583945add3c275b490f3cf39/common/validation/validation.go#L519-L555)

### Why it is wrong

The upper bound on validations holding payloads is 20 times the number of open escrows, which grows with the network and is in the thousands on a busy host. Peak memory then depends on how many replays finish together, and a PoC start makes them all finish together. The host has no way to trade validation throughput for a memory bound.

### Proposed fix

A process-wide, non-blocking slot cap on `Validator`. `Validate` takes a slot after the credit check and before the payload fetch, and releases it on return. When no slot is free it returns `ErrValidationDeferred`, so the host keeps the obligation and retries after the existing 30 s cooldown. `CanValidate` also reports false while the cap is full, so the collector and workers skip the job before taking a Postgres lease. The cap is set by `DEVSHARD_MAX_CONCURRENT_VALIDATIONS`; a value of 0 or less is rejected at startup.

The prepared change defaults to 192. On this host at least 384 validations were in flight under normal load, so 192 would also defer part of the normal work, not only the PoC burst. The right default depends on how many replays the ML nodes serve at once, and it may be better picked by maintainers from their own data.

Related: #2293 (fewer bytes per validation; it does not bound how many run at once), #2111 (payload client sweep), #2146.

</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/gafrustam">@gafrustam</a></span>
    <span class="issues-meta-item">commented 2026-11-21 17:17 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@kaileido you mention the change is already prepared. Are you opening the PR yourself? If not, I'm happy to take it.</p>
<p>@a-kuprin is #1449 still the plan for v7? It replaces the per-escrow workers and already has an in-flight cap, so if it lands, a slot cap here would only be a stopgap. If it's not coming soon, I'd do the cap as described in the issue: non-blocking, returns ErrValidationDeferred, set by an env var, with the default left to you.</p>
<p>Related: #2305 defers validations whose replay was aborted at PoC start, the same burst from the other side.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2298](https://github.com/gonka-ai/gonka/issues/2298) every hour.
