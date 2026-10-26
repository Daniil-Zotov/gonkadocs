---
title: "#2104 — devshardctl: winner_served_without_finish records a not_finished host strike at stream end although the nonce finishes seconds later"
source: https://github.com/gonka-ai/gonka/issues/2104
issue_number: 2104
synced_at: 2026-10-26T23:11:33Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    devshardctl: winner_served_without_finish records a not_finished host strike at stream end although the nonce finishes seconds later
    <span class="issues-number">#2104</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/maria-mitina">@maria-mitina</a> opened 2026-10-23 12:28 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-10-23 20:04 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

When a winning attempt's stream ends before the gateway has seen the nonce's finish marker, the race-settlement path takes the `errWinnerIncomplete && deliveredWholeAnswer` branch: the caller keeps the answer, but `recordWinnerTerminalFailureOnce` immediately records a **terminal failure / `not_finished` perf sample against the host**, and logs `winner_served_without_finish`. The strike is taken at stream end, not when the finish actually fails to arrive. In the observed cases the nonce finished 0.002–13 s later — well inside the execution timeout — yet the host keeps a permanent `not_finished` strike in its perf window, in `attempts_terminal_total`, and in `user_requests_with_hidden_failure_total`.

This is the sample that trips the `primary_unresponsive` classifier in #2103, but it is a separate defect: it mislabels a successful inference as a host failure regardless of what consumes the sample.

## Environment (testnet1, `gonka-testnet`)

- Gateway: one instance, image `devshard-gateway:testnet-v6-f5ad27a`, locally built 2026-10-14 from commit `f5ad27a47` (branch `devshard-0.2.x-v6`). The branch at current head `6a41bc342` has the same branch in `redundancy.go` (comment: "Settled as the failure it is: the caller keeps the answer, the host keeps the strike").
- Devshard hosts: 7 participants, identical stack — `versiond` image `ghcr.io/product-science/versiond:0.2.15` running devshard binary `0.2.16-v6` (self-reported `binary_version=0.2.16-v6`, chain-approved version), `proxy` `ghcr.io/product-science/proxy:0.2.15`, `api 0.2.15-post3`, `inferenced 0.2.15`, `mlnode 3.0.12-post4`.
- Hosts' `versiond`/`api`/mlnode logs for the window contain no WARN/ERROR; the host side completed both inferences normally.

## Code path (`devshard/cmd/devshardctl/redundancy.go`, v6 head)

```go
w := race.winnerNonce()
if w != 0 && inf != nil && inf.nonce == w {
    failed, err := e.winningInflightTerminalFailure(inf)
    // An unclosed nonce is a protocol fact for the timeout vote and the host's record, not a
    // reason to take back an answer the caller already has.
    if failed && errors.Is(err, errWinnerIncomplete) && deliveredWholeAnswer(inf) {
        ...
        e.recordWinnerTerminalFailureOnce(inf, params, w)
        // Settled as the failure it is: the caller keeps the answer, the host keeps the strike.
        e.goTrackedRaceCleanup(settleCtx, func(ctx context.Context) {
            e.finishRaceWhenPendingDone(ctx, attempts, params, decision, w, ...)
        })
        logInferenceStage(settleCtx, inf.escrowID, inf.nonce, "winner_served_without_finish", "host", inf.hostID)
        return nil
    }
```

`attemptCountsAsSuccessfulForPerf` requires `session.IsNonceFinished(nonce)` *at sampling time*; the sample is taken here, before `finishRaceWhenPendingDone` has waited for the finish.

## Evidence (run 2026-10-23 11:35–11:45 UTC, escrow 758)

Both cases are the first inference a co-located host served after returning from a confirmation PoC (`chain phase gate: phase inactive previous_reason=confirmation_poc` at 11:38:08).

```
11:38:08.942 nonce=264 host=q9u4txhy stage=started
11:38:09.202 nonce=264 stage=receipt_received elapsed_ms=259
11:38:10.875 nonce=264 stage=first_token
11:38:20.385 nonce=264 stage=send_completed output_chunks=517 content_chunks=507 output_bytes=99188 max_gap_ms=154
11:38:20.387 nonce=264 stage=winner_served_without_finish        <-- strike recorded
11:38:23–30     sse_devshard_receipt ×4 for nonce 264
11:38:33.096 nonce=264 stage=race_completed winner=true finished=true responsive=true has_receipt=true attempt_ms=24153
11:38:33.097 nonce=264 stage=request_succeeded / request_fully_settled outcome=success
```

```
11:38:26.969 nonce=266 host=jg2f3a2y stage=started
11:38:26.982 nonce=266 stage=receipt_received elapsed_ms=12
11:38:31.488 nonce=266 stage=send_completed output_bytes=61963
11:38:31.490 nonce=266 stage=winner_served_without_finish        <-- strike recorded
11:38:31.490 nonce=266 stage=race_completed winner=true finished=true responsive=true
11:38:31.490 nonce=266 stage=timeout_scheduled reason=execution remaining_ms=1919509
11:38:37.721 nonce=266 stage=timeout_skipped reason=nonce_already_finished
```

Note that for nonce 266 the `race_completed` line in the **same millisecond** already reports `finished=true responsive=true` — the strike and the "responsive" verdict are both recorded for the same attempt.

Effect on host records (`/v1/debug/perf`, hosts had `n=0` in their window before the run):

```
q9u4txhy  responsive_rate=0.973 total=37 failures=1 avg_receipt_ms=16
jg2f3a2y  responsive_rate=0.941 total=17 failures=1 avg_receipt_ms=10
```

Metric deltas over the run: `user_requests_with_hidden_failure_total{reason="not_finished",severity="protected"} +1`, `timeout_actions_total{action="scheduled",kind="execution",reason="deadline_not_due"} +1` and `{action="skipped",reason="nonce_already_finished"} +1` for the .79 host. Downstream: 21 `primary_unresponsive` hedges in the following 7 minutes (#2103).

The same `winner_served_without_finish` → single-strike pattern was seen on 2026-10-22 on two remote hosts (`rate=0.917 n=12 fail=1`).

## Why this is wrong

- The host did nothing wrong: the stream was complete, the receipt was present, and the finish arrived within seconds. The only thing "incomplete" was the gateway's view at the instant the stream closed.
- The strike is permanent for the perf window and feeds every consumer of host health: `IsUnresponsiveParticipant`, `ParticipantFailureThresholdExceeded`, `pairwiseParticipantAvailable`, the hidden-failure metric, and operator dashboards.
- The execution-timeout machinery already exists to decide whether a nonce truly failed to finish (`timeout_scheduled reason=execution`); recording the failure before that decision duplicates it with a stricter, premature answer.

## Suggested fix

1. Defer the perf/accounting sample for a `deliveredWholeAnswer` winner until `finishRaceWhenPendingDone` / `race_completed`, which already knows `finished=true|false`; count `not_finished` only if the nonce is still unfinished then (or at the execution deadline).
2. Alternatively, keep an immediate *protocol* record ("delivered, finish pending") separate from the *host-health* strike, and convert it to a strike only when the execution timeout actually fires (`timeout_vote_*` with `reason=execution`).
3. Log the eventual outcome (`winner_finish_arrived_late elapsed_ms=…`) so operators can tell a late finish from a real loss.

</div>

---

> 🔄 **Auto-synced** from [Issue #2104](https://github.com/gonka-ai/gonka/issues/2104) every hour.
