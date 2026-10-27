---
title: "#2146 — devshard: requests in flight or queued when a PoC / cPoC starts on a non-preserved host become invalids and misses for a pause the protocol orders"
source: https://github.com/gonka-ai/gonka/issues/2146
issue_number: 2146
synced_at: 2026-10-27T02:09:18Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    devshard: requests in flight or queued when a PoC / cPoC starts on a non-preserved host become invalids and misses for a pause the protocol orders
    <span class="issues-number">#2146</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/redstartechno">@redstartechno</a> opened 2026-10-26 21:00 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-10-26 21:00 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
### Summary

When a confirmation PoC (or the start PoC, same code path) begins generation on a host that is not preserved for it, the host must stop inference at once. Everything it had already accepted is cut, and each cut request is charged to the host: a request mid-generation comes back as an empty or truncated answer that the executor signs and validators invalidate; a request still queued, or arriving during the round, ends as a miss. The cPoC trigger gives about 14 s of notice before generation, too short to drain minutes of accepted work. A host cannot opt out, and nothing in settlement recognises the pause.

Related: #2107 / #2108 (the preserved host's side of the same event), #1805 (protocol-aware PoC / cPoC, v8).

### Mechanism (gonka-vllm-plugins `decode/vlm030` @ 02558e9, vllm `release/v0.30-decode-int`, gonka `devshard/v7`, same on `devshard-0.2.x-v6`)

1. `src/gonka_poc/poc/routes.py:565-577`: `/init/generate` activates `PoCGate`, then `abort_all_requests(engine_client)` aborts every in-flight request ("PoC init: aborted N in-flight requests before generation"). `src/gonka_poc/poc/reservation.py:181` escalates a failed KV lease to the same abort.
2. vLLM finishes an aborted request normally: `vllm/v1/engine/output_processor.py:558` sets `finish_reason` "abort"; `_raise_if_error` (`vllm/entrypoints/generate/base/serving.py:204-211`) raises only for "error". The client gets HTTP 200 with the tokens generated so far (none, if the abort came during prefill) and `finish_reason: "abort"`; a stream gets a final chunk with that reason and `[DONE]`.
3. The executor has no `finish_reason` check (`devshard/cmd/devshardd/inference/execute.go:49-61`). Usage is present (prompt tokens > 0), so it signs a `MsgFinishInference` over the empty answer (`devshard/host/host.go:1319-1327`). The consensus error predicate (`common/completionapi/terminal_error.go:37-53`) accepts only an error envelope or unparseable `data:` lines, so the Finish stands and the invalid comes from the challenge replay.
4. New requests during the round get 503 `poc_generation_active` from `src/gonka_poc/entrypoint/gating.py:111-127`; the API refuses with "not intended for INFERENCE: POC" (`decentralized-api/broker/broker.go:611`). Either way the executor sends no Finish and the nonce times out as a miss.
5. Settlement has no PoC-aware path: `devshard/state/machine.go` `applyTimeout` / `applyErrorMiss` and `devshard/host/timeout.go` contain no PoC or preserved-set reference. The gateway's `poc_unavailable_host` ghost (`devshard/cmd/devshardctl/session_picker.go:114-115`, keyed on the chain phase snapshot in `poc_mode.go:42-47`) stops new dispatch to non-preserved hosts, but work already dispatched is not taken back.

### What we saw (one DeepSeek-V4-Flash host, not preserved)

- Epoch 435 (2026-10-24): cPoC `/init/generate` at 09:42:50Z "aborted 21 in-flight requests", at 13:37:39Z "aborted 33"; vLLM went from 16 running to 0 in 10 s. The executor logged `finish_published reason=ok` with 0 output tokens for 137635/1805 (09:42:50Z), 137571/5440 and 137831/2178 (13:37:40Z); validators voted each invalid (9-10 votes). They were 3 of the host's 4 invalids after the morning.
- Epoch 436 (2026-10-25): cPoC at 14:27:40Z "aborted 34 in-flight requests"; the API refused 20 requests during the round's POC status.
- The start PoC uses the same gate and abort; not measured on this host yet.

### Proposals

1. **Plugin, small (PR follows):** a request aborted by the PoC gate must end as an error envelope (`{"error": {"type": "poc_preempted", "code": 503, ...}}`, as a 503 body or as the terminal SSE event), never as a 200 completion with `finish_reason: "abort"`. The executor then publishes no Finish; the host takes a miss instead of an invalid. Invalids are the worse outcome (they feed the consecutive-invalid counter and the invalidation-rate test), so this is the safe first step and needs no protocol change.
2. **Verifiable "interrupted by PoC" record (devshard + settlement):** the executor signs a `poc_interrupted` terminal for a request that was in flight or queued when a PoC / cPoC generation started for which it was not preserved. Validators check it against chain data (phase start height, preserved snapshot, the request's sealed start). Settlement: no `Missed++`, no invalid vote, client refunded as now. This extends the existing `poc_unavailable_host` ghost to work the host had already taken.
3. **Hand the queue back at the trigger (gateway + host):** at the trigger the host returns its not-yet-started requests with that refusal and the gateway re-dispatches them to preserved hosts at once, instead of after the 1,200 s first-byte timeout. Clients lose seconds, not 20 minutes.
4. **Fallback at settlement only:** leave out of the miss test the nonces whose execution window overlaps the host's mandatory PoC pause (from chain heights and sealed start times). Cruder than 2, no new message type.

A drain window before cPoC generation would also help, but it weakens the short-notice property cPoC relies on; 2 + 3 keep the notice short and still do not charge the host. If #1805 is the place for 2-4, happy to move them there.

</div>

---

> 🔄 **Auto-synced** from [Issue #2146](https://github.com/gonka-ai/gonka/issues/2146) every hour.
