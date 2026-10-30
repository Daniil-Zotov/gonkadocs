---
title: "#2105 — devshardctl: speed-up hedging on a mixed-latency escrow group doubles GPU work — remote primaries lose 67–82 % of races and finish as suppressed losers"
source: https://github.com/gonka-ai/gonka/issues/2105
issue_number: 2105
synced_at: 2026-10-30T20:53:36Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    devshardctl: speed-up hedging on a mixed-latency escrow group doubles GPU work — remote primaries lose 67–82 % of races and finish as suppressed losers
    <span class="issues-number">#2105</span>
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

On an escrow group whose hosts have very different network distance to the gateway, the primary host for a request is fixed by the nonce stream (nonce → slot → host), not by expected speed. The speed-up policies (`pairwise_budgeted_speedup`, `pairwise_ab_sample`, legacy `secondary_faster`) then correctly predict that a nearer host will be faster and start it in parallel with `Delay: 0`. The near host wins almost every time, and the far primary runs its full generation to completion as a `suppressed_loser`. Net effect across two 10-minute runs: **remote-host primaries lose 67–82 % of their races, 1.8 attempts per user request, and roughly half of all GPU time on the remote hosts produces output that is discarded.** Latency does not improve either, because the winner was reachable from the start — the hedge only recovers from the primary assignment.

This is distinct from #2103 (`primary_unresponsive` false positives): here every host is healthy and the perf model is right; the waste comes from choosing a primary the model already knows is slower and from losers running to completion.

## Environment (testnet1, `gonka-testnet`)

- Gateway: one instance, image `devshard-gateway:testnet-v6-f5ad27a`, locally built 2026-10-14 from commit `f5ad27a47` (branch `devshard-0.2.x-v6`); `Decide()` / `decidePairwiseSpeedup` / `decideLegacySecondaryFaster` are unchanged at branch head `6a41bc342`. Live settings: `speed_policy: hybrid`, `pairwise_max_proactive_attempts: 3`, `receipt_timeout_ms: 5000`.
- Devshard hosts: 7 participants, identical stack — `versiond` image `ghcr.io/product-science/versiond:0.2.15` running devshard binary `0.2.16-v6` (self-reported `binary_version=0.2.16-v6`, chain-approved version), `proxy` `ghcr.io/product-science/proxy:0.2.15`, `api 0.2.15-post3`, `inferenced 0.2.15`, `mlnode 3.0.12-post4`. All L40S-class, same model (`Qwen/Qwen3-4B-Instruct-2507`).
- Topology: 2 hosts in the gateway's DC (host-ping RTT ≈ 1 ms; receipt median 9 ms; started→first_token median 0.13–0.15 s), 5 hosts in a remote DC (RTT ≈ 310–370 ms; receipt median 0.7–1.35 s; first token 1.05–1.8 s). Escrow group of 16 slots over 6 hosts.
- Load: `remote-long-load` scenario (#2009), 10 min, concurrency 2, real captured prompts, 105–124 requests per run, all HTTP 200.

## Evidence

**Run 2026-10-23 11:35–11:45 UTC (escrow 758), after the PoC window:**

Decisions: `pairwise_ab_sample` 26, `primary_unresponsive` 21 (#2103), `secondary_faster` 15, `receipt_timeout` 11, `pairwise_budgeted_speedup` 10 → 83 races, 151 attempts for 105 user requests (22 served from cache).

Remote host `p232vrcn` as primary: **45 races, won 15, lost 30**. Who beat it and why:

```
decision=pairwise_ab_sample        winner=q9u4txhy (local)   13
decision=secondary_faster          winner=q9u4txhy (local)   11
decision=pairwise_budgeted_speedup winner=kepcgs0y (remote)   4
decision=pairwise_ab_sample        winner=kepcgs0y (remote)   2
```

`attempts_terminal_total{p=p232vrcn,role=primary,visibility=suppressed_loser} +29` — 29 of the 30 lost races finished the whole generation anyway. The local host `q9u4txhy` won 24 of 24 secondary attempts. Remote `kepcgs0y` as secondary: 26 attempts, 20 suppressed.

Example of the cost (`request=req-1792755329123448414-1547`, 16 k-token prompt):

```
11:35:29.131 nonce=54 host=p232vrcn started                 (primary, remote)
11:35:29.335 nonce=64 host=kepcgs0y started                 (secondary, remote, pairwise_ab_sample)
11:35:32.436 nonce=64 first_token → winner_selected
11:35:36.170 nonce=54 first_token route=loser → stream_suppressed
11:36:49.461 nonce=54 send_completed output_chunks=2962 output_bytes=624017   <-- 80 s of discarded generation
11:36:52.090 nonce=64 send_completed output_chunks=3511 output_bytes=666230
```

**Run 2026-10-22 10:48–10:58 UTC (escrow 672):** `p232vrcn` primary 51 races, won 9, `suppressed_loser` 42 (82 % lost); local hosts won 69 of their secondary attempts; 165 attempts for 91 inferences.

Across both runs the perf model's own numbers show the outcome was predictable before dispatch: receipt 9 ms vs 1.1–1.4 s and first token 0.15 s vs 1.4–1.8 s are stable per host for the whole hour.

## Why this matters

- GPU work: on the remote hosts roughly every second completed generation is thrown away. For a 7-host group this is ~45 % extra inference load at concurrency 2; it scales with request rate.
- Latency: the hedge cannot beat "dispatch to the fast host in the first place". p50 user latency was 3.9–6.3 s with first tokens at ~1.5 s from the remote primaries before the local secondary took over.
- Accounting/validation: every suppressed loser is still a started+finished nonce that has to be receipted, settled and (potentially) validated, which multiplies the `rejected executor receipt` duplicates and timeout-vote traffic seen on the same runs.
- Fairness: remote hosts carry primaries they rarely get credit for as `user_visible_wins`.

## Suggested directions

1. **Speed-aware primary assignment.** When a nonce binds to a host whose estimated time (`EstimatedTimeMsForParticipant` / pairwise ratio) is clearly worse than another available host's, let the picker hold the nonce as a ghost (as it already does for PoC/throttled/excluded hosts) and dispatch the request on the next nonce that binds to a faster host, instead of dispatching and then hedging.
2. **Replace instead of add.** When `decidePairwiseSpeedup` accepts a candidate with a large predicted ratio (e.g. `candidateCost < 0.5`), run only the candidate rather than primary + candidate; keep the parallel race for marginal ratios where it genuinely reduces tail latency.
3. **Stop or shorten suppressed losers.** Where the protocol allows, cancel the loser's generation once the winner is streaming (or cap its `max_tokens`) instead of letting it run 60–80 s to completion; if a finished nonce is required for settlement, finish it with the minimum work.
4. **Bound A/B sampling by cost.** `pairwise_ab_sample` fired 26× in 10 minutes on pairs whose ratio was already well established; sampling should back off once the estimate's confidence is high, and should not sample on very long prompts/outputs.
5. Expose the predicted ratio and confidence in `decision_made` so operators can see why a parallel attempt was started.

</div>

---

> 🔄 **Auto-synced** from [Issue #2105](https://github.com/gonka-ai/gonka/issues/2105) every hour.
