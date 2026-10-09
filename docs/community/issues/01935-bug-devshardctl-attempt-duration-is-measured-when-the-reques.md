---
title: "#1935 — [BUG] devshardctl: attempt duration is measured when the request settles, not when the attempt ends"
source: https://github.com/gonka-ai/gonka/issues/1935
issue_number: 1935
synced_at: 2026-10-09T02:16:54Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    [BUG] devshardctl: attempt duration is measured when the request settles, not when the attempt ends
    <span class="issues-number">#1935</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/vitaly-andr">@vitaly-andr</a> opened 2026-10-07 11:46 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-10-07 11:46 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
# Title
devshardctl: attempt duration is measured when the request settles, not when the attempt ends

## Summary

`buildInvolvement` in `devshard/cmd/devshardctl/redundancy.go` sets `TotalTimeMs = time.Since(inf.sendTime)`, and the two performance samples set `sample.TotalTime` the same way. The records are built when the request settles, normally after all attempts have completed. So the value is the time since send at that moment, not the time until the attempt ended. When the collection times are close, the pairwise comparison leans toward later-started attempts and can reverse the real order of two durations: an attempt that started earlier and finished earlier can be recorded as the slower one.

`devshard/docs/host-health.md` defines `TotalTime` as "Wall clock from send to stream completion", and `devshard/docs/speculative-proxy.md` says the pairwise signal is the time from sending the attempt until it is finalized. Both mean the attempt's own duration.

## Motivation

These values feed `RatioAToB`, the ratio estimates, the speedup cutoff and the winner hold (`HoldEligible`), as well as the duration averages and `devshard_gateway_participant_total_attempt_seconds`. If they do not reflect host speed, the gateway can start or hold speculative attempts on a wrong signal, and the participant timing metrics are off.

## Impact

- Who is affected: gateway operators.
- Network-wide or limited: limited to how an operator's own gateway chooses and holds attempts. Chain, host and protocol code are not involved.
- Likelihood: common. Every request in which two attempts both complete is affected. I have not measured how large the effect is on a live fleet.
- Severity (impact x likelihood): low. It is a correctness defect in the routing signal and the timing metrics, not a security issue.
- Affected components: `devshard/cmd/devshardctl/redundancy.go` (`buildInvolvement`, `recordSample`, `recordPostContentWinnerFailureOnce`), read in `devshard/cmd/devshardctl/pairwise.go`.

## Detailed description

On `devshard/gateway/v5.1.0` (4a8d5c749):

- `redundancy.go:4453`: `hi.TotalTimeMs = float64(time.Since(inf.sendTime).Milliseconds())` in `buildInvolvement`, called at `:4213` for every attempt when the race finishes.
- `redundancy.go:4495` and `:4033`: `sample.TotalTime = time.Since(inf.sendTime)` in `recordSample` and `recordPostContentWinnerFailureOnce`.
- `pairwise.go:138`: `RatioAToB` is built from these values. `scoreablePairwiseHost` (`pairwise.go:153`) keeps finished, responsive attempts with a positive `TotalTimeMs`. None of these conditions looks at when the attempt ended.

Reproduction: two attempts with real durations of 100 ms (A, sent first) and 400 ms (B, sent 50 ms later). Both finish, then `buildInvolvement` is called for each.

```go
func TestAttemptDurationIsMeasuredAtSettlement(t *testing.T) {
	e := &Redundancy{}
	t0 := time.Now()
	a := &inflight{hostIdx: 0, nonce: 1, sendTime: t0, done: make(chan struct{})}
	b := &inflight{hostIdx: 1, nonce: 2, sendTime: t0.Add(50 * time.Millisecond), done: make(chan struct{})}
	time.AfterFunc(100*time.Millisecond, func() { close(a.done) })
	time.AfterFunc(450*time.Millisecond, func() { close(b.done) })
	<-a.done
	<-b.done

	ha := e.buildInvolvement(a, 1, user.InferenceParams{})
	hb := e.buildInvolvement(b, 1, user.InferenceParams{})
	if ha.TotalTimeMs >= 300 {
		t.Errorf("attempt A took 100 ms but is recorded as %.0f ms", ha.TotalTimeMs)
	}
	if ha.TotalTimeMs > hb.TotalTimeMs {
		t.Errorf("A is 4x faster than B but is recorded as slower (%.0f vs %.0f ms)", ha.TotalTimeMs, hb.TotalTimeMs)
	}
}
```

Output on `devshard/gateway/v5.1.0` (three runs, same result): real duration A=100 ms, B=400 ms; recorded A=450 ms, B=400 ms.

The snippet calls `buildInvolvement` directly, so it only shows how the value is computed. It does not go through the attempt goroutine and stays red after the fix. The fix comes with a test that runs a request through the real race.

## Proposed approach

- Record each attempt's duration when its send call returns, before `done` is closed, and use it in `buildInvolvement`, both performance samples and the `attempt_ms` field of the `race_completed` log line. An attempt with no recorded end falls back to the current behaviour. I found no completion time on the gateway's own clock in `inflight` or `HostResponse`: `HostResponse.ConfirmedAt` is the executor's clock, and `lastChunkAt` is updated on every stream write, not at the end of the attempt.
- Durations in the averages and the participant total-attempt metric decrease or stay the same. Persisted request records keep their old values.
- I have a fix ready against `devshard/gateway/v5.1.0`, where #1923 was merged and then carried into `devshard/gateway/v4.1.3`. It only touches `devshardctl`, so it can be retargeted. Which branch do you want it on?

</div>

---

> 🔄 **Auto-synced** from [Issue #1935](https://github.com/gonka-ai/gonka/issues/1935) every hour.
