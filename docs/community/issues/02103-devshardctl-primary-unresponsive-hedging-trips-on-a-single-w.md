---
title: "#2103 — devshardctl: primary_unresponsive hedging trips on a single winner_served_without_finish sample (threshold 1.0, no min-sample guard, 1 h tumbling window)"
source: https://github.com/gonka-ai/gonka/issues/2103
issue_number: 2103
synced_at: 2026-10-30T16:00:54Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    devshardctl: primary_unresponsive hedging trips on a single winner_served_without_finish sample (threshold 1.0, no min-sample guard, 1 h tumbling window)
    <span class="issues-number">#2103</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/maria-mitina">@maria-mitina</a> opened 2026-10-23 12:17 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-10-23 20:03 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

`Decide()` Rule 1 (`primary_unresponsive`) starts an immediate parallel attempt on another host whenever `perf.IsUnresponsiveParticipant(primary)` is true. With the default `UnresponsiveThreshold = 1.0`, no minimum-sample guard, and a 1-hour tumbling perf window, **a single failed sample flips a healthy host to "unresponsive" for up to an hour**. In the runs below the single failed sample came from a premature `winner_served_without_finish` strike (tracked separately in #2104), but the classifier is wrong for any single legitimate failure too. The cost of the resulting hedge on a mixed-latency group is tracked in #2105.

## Environment (testnet1, `gonka-testnet`)

- Gateway: one instance, image `devshard-gateway:testnet-v6-f5ad27a`, locally built 2026-10-14 from commit `f5ad27a47` (branch `devshard-0.2.x-v6`). The relevant code (`hostperf.go`, `Decide()` Rule 1, the `winner_served_without_finish` branch) is unchanged at the current branch head `6a41bc342`.
- Devshard hosts: 7 participants, identical stack — `versiond` image `ghcr.io/product-science/versiond:0.2.15` running devshard binary `0.2.16-v6` (self-reported `binary_version=0.2.16-v6`, chain-approved version), `proxy` `ghcr.io/product-science/proxy:0.2.15`, `api 0.2.15-post3`, `inferenced 0.2.15`, `mlnode 3.0.12-post4`.
- Topology: 2 hosts co-located with the gateway (host-ping RTT ≈ 1 ms, receipt ≈ 10 ms), 5 hosts in a remote DC (RTT ≈ 310–370 ms, receipt 0.7–1.4 s).
- Live gateway settings: `unresponsive_threshold: 1`, `receipt_timeout_ms: 5000`, `speed_policy: hybrid`, `pairwise_max_proactive_attempts: 3`.
- Load: 10-minute runs, concurrency 2, real captured prompts, via the `remote-long-load` scenario (#2009).

## Code path

```go
// redundancy.go — Decide()
// Rule 1: primary is known unresponsive → immediate parallel
if e.perf.IsUnresponsiveParticipant(primaryParticipant) {
    return Decision{RunSecondary: true, Delay: 0, Reason: "primary_unresponsive", ImmediateAttempts: 1}
}
```

```go
// hostperf.go
func statsUnresponsive(st HostPerfStats) bool {
    if st.TotalSamples == 0 {
        return false
    }
    return st.ResponsiveRate < UnresponsiveThreshold   // default 1.0
}
```

- `ResponsiveRate` is computed over the participant's samples in the current window. The window is a tumbling 1 h (`PerfSettings{SampleSize: 256, WindowMS: 1h}`, `participantPerfWindowStart` with a per-participant hashed offset), so a strike persists until that participant's next hourly boundary.
- `MinSamplesForDecision = 3` exists but is not consulted by Rule 1; `TotalSamples == 1, failures == 1` is enough.
- A sample is "responsive" only if `attemptCountsAsSuccessfulForPerf` → `session.IsNonceFinished(nonce)` at the time the sample is taken.

## Evidence (run 2026-10-23 11:35–11:45 UTC, escrow 758)

Perf snapshot before the run (`/v1/debug/perf`): both co-located hosts had `n=0` in their current window.

Source of the single failing sample on each co-located host (details and fix proposal in #2104):

```
11:38:08.942 nonce=264 host=q9u4txhy stage=started
11:38:09.202 nonce=264 stage=receipt_received elapsed_ms=259
11:38:20.385 nonce=264 stage=send_completed output_chunks=517 output_bytes=99188
11:38:20.387 nonce=264 stage=winner_served_without_finish          <-- strike recorded here
11:38:33.096 nonce=264 stage=race_completed winner=true finished=true responsive=true has_receipt=true
```

```
11:38:26.969 nonce=266 host=jg2f3a2y stage=started
11:38:31.488 nonce=266 stage=send_completed output_bytes=61963
11:38:31.490 nonce=266 stage=winner_served_without_finish          <-- strike recorded here
11:38:31.490 nonce=266 stage=race_completed winner=true finished=true responsive=true
11:38:37.721 nonce=266 stage=timeout_skipped reason=nonce_already_finished
```

Both nonces finished (13 s and <1 s later), both answers were delivered intact, yet each host now carries `fail=1`:

```
/v1/debug/perf after the run
q9u4txhy  responsive_rate=0.973 total=37 failures=1 avg_receipt_ms=16    window_start=11:31:47
jg2f3a2y  responsive_rate=0.941 total=17 failures=1 avg_receipt_ms=10    window_start=11:26:57
p232vrcn  responsive_rate=1.000 total=49 failures=0 avg_receipt_ms=1410  (remote DC)
```

Consequence in the same run — every subsequent request whose primary was one of the two fast hosts was hedged immediately onto a remote host:

```
decision=primary_unresponsive  host=q9u4txhy  13×  11:38:39 → 11:45:05
decision=primary_unresponsive  host=jg2f3a2y   8×  11:38:47 → 11:43:41
```

Metrics delta: `devshard_speculative_attempt_starts_total{reason="primary_unresponsive"} +21`, `user_requests_with_hidden_failure_total{reason="not_finished",severity="protected"} +1`. The secondaries ran on hosts with 0.7–1.4 s receipt and 1.1–1.8 s first-token vs 10 ms / 0.15 s on the "unresponsive" primaries, so the hedge never won; it only consumed a second GPU slot per request.

The same pattern appeared the day before (run 2026-10-22 10:48–10:58): 46 `primary_unresponsive` decisions, one remote host flagged by a single failure (`rate=0.917, n=12, fail=1`) from ~10:49 until its window boundary at 11:40:05, another host's decisions stopping exactly at its window boundary (10:54:12) — the hour-long stickiness is visible as a hard edge in the logs.

## Why this matters

- A healthy host is penalised for an ordering artefact (stream end vs. finish marker) that resolves within seconds and is already handled by the execution-timeout machinery.
- Rule 1 fires with `Delay: 0`, so the hedge costs a full second inference every time; across the run, 21 of 83 races (25 %) were caused by it.
- On a mixed-latency fleet the hedge is directed to hosts that are structurally slower than the "unresponsive" primary, so it cannot improve latency and only burns capacity.
- The hour-long tumbling window makes the penalty disproportionate to a single event and makes behaviour change abruptly at per-host boundaries, which is hard to reason about operationally.

## Suggested fixes

1. **Guard Rule 1**: require `TotalSamples >= MinSamplesForDecision` (already defined) and ship a default `UnresponsiveThreshold < 1.0` (e.g. 0.8), or require at least two failures.
2. **Sliding or decaying window** instead of a 1-hour tumbling window, so one event ages out gradually rather than at a hashed hourly boundary.
3. **RTT-aware hedging** when Rule 1 does fire (see #2105 for the broader hedging cost): prefer a secondary whose expected receipt/first-token is not worse than the primary's, or use a delay proportional to the secondary's RTT instead of `Delay: 0`.

## Workaround

Operators can raise the bar at runtime via the admin API (persisted in the gateway settings store):

```
PUT /v1/admin/settings  {"redundancy":{"unresponsive_threshold":0.8}}
```

With `n=37` one strike gives 0.973 and no longer trips Rule 1. Trade-off: a host that genuinely fails ~15 % of requests is no longer hedged pre-emptively (it is still covered by `receipt_timeout` at 5 s and by the pairwise policies).


</div>

---

> 🔄 **Auto-synced** from [Issue #2103](https://github.com/gonka-ai/gonka/issues/2103) every hour.
