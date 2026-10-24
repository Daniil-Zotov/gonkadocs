---
title: "#2107 — devshard: during confirmation PoC generation a session's whole stream lands on its preserved slots, whatever their size"
source: https://github.com/gonka-ai/gonka/issues/2107
issue_number: 2107
synced_at: 2026-10-24T23:21:59Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    devshard: during confirmation PoC generation a session's whole stream lands on its preserved slots, whatever their size
    <span class="issues-number">#2107</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/redstartechno">@redstartechno</a> opened 2026-10-23 13:03 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-10-23 13:03 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

During the generation phase of a confirmation PoC only preserved hosts serve inference. The gateway keeps routing
each session in nonce order, turns every non-preserved slot's turn into a ghost, and puts the real requests on the
preserved slots. When a session's only preserved slot is a small host, that host receives the traffic meant for all
16 slots, with no look at its weight. The requests fail after the receipt, count as misses, and the binomial miss
test can zero the host's epoch reward.

We propose two changes:
1. Gateway (PR linked below): during PoC generation, cap each host's in-flight requests at its weight share of the
   existing PoC concurrency budget. Excess requests are refused before any receipt, so nobody takes a miss.
2. Chain (design only, needs a param): plan the preserved capacity per model from the inference demand seen during
   PoC, instead of a fixed fraction of weight filled with the smallest nodes.

## What happened (epoch 433, DeepSeek-V4-Flash)

- Confirmation PoC event 0: trigger height 6679258, generation phase 12:04:28-12:07:28 (UTC+3), about 3 minutes.
- Escrow 134985 has 16 slots. Exactly one of them belonged to a preserved host (ours, weight 1,809 of 749,558 in
  the DeepSeek group, 0.24 %). The preserved snapshot at the trigger height lists three DeepSeek nodes.
- Gateway accounting for that escrow (tracker.gonka.pro, source openbroker2): the other 15 slots had 718-882 ghost
  nonces each (of 1,256-1,257), 11,114 of them `poc_unavailable_host` in dispatch phase `confirmation_poc`; our slot
  had 2 ghosts.
- Just before the event the whole session started 5-10 requests per minute (our slot 0-2). In the minutes
  12:04-12:07, which contain the generation phase, our proxy logged 731 requests for that escrow (about 240 per
  minute). During the generation phase the other 15 slots got 4 sealed starts, all in its first 4 seconds.
- Our host's admission limit was full: 581 requests in those minutes ended with `acquire_err` after the receipt,
  5 finished.
- Result for our slot in that escrow: 749 misses of 1,256 assigned nonces. On chain the epoch stats show 749 missed
  against 748 completed, a miss share of 50 % against a network miss share of about 1.7 %, so the miss test failed
  and the epoch reward was 0.

Nothing in the host's configuration could have avoided this: a host cannot opt out of preservation, and 53 of the
749 misses were refusals before any receipt (52 of them HTTP 503 from the host's proxy), which also count as misses.

## Mechanism (refs at upstream/devshard-0.2.x-v6 and upstream/upgrade-v0.2.18)

- Preserved set: `SamplePreservedForEpisode` -> `samplePreservedForModel`
  (`inference-chain/x/inference/module/model_assignment.go:873-924`). Target weight = `PocSlotAllocation` x the
  model's total weight (:881-882). The loop takes each eligible participant's smallest unallocated node
  (`getSmallestUnallocatedMLNode`, :935), in sorted address order, until the target is reached. There is no load or
  capacity input, so the preserved set is built from small nodes.
- Routing: a session's nonce picks the slot; during generation the picker ghosts non-preserved hosts
  (`devshard/cmd/devshardctl/session_picker.go`, branch 1a) and the real request waits for the next preserved slot.
- The PoC concurrency budget `PoCMaxConcurrentPer10000Weight` is gateway-wide per model (`gateway.go:1340-1368`,
  `gateway_limiter.go:296-362`, weight = all available hosts). Nothing limits what lands on one host.
- Escrow choice: the gateway picks the runtime with the lowest active requests per W(e); an escrow with one small
  preserved slot keeps W(e) > 0 and stays eligible.

## Proposal

### 1. Gateway: per-host cap during PoC generation (PR linked below)

- Each host gets at most max(1, floor(host weight x `PoCMaxConcurrentPer10000Weight` / 10000)) real requests in
  flight from this gateway, across all its escrows, while PoC generation is active. This is the ratio the gateway
  already uses for the whole model, applied per host.
- A host at its cap is treated like a throttled host: its turn is a ghost, and a queued request with no other
  available host gets `ErrNoAvailableHost` before any receipt. The client sees a refusal it can retry; no host takes
  a miss. Outside PoC generation nothing changes.
- The cap is computed by the gateway from chain weight, not declared by the host, so a host cannot use it to avoid
  work.

### 2. Chain: preserve enough capacity for the expected PoC-time demand

- Target per model: `max(PocSlotAllocation x W_m, D_m)`, where `D_m` is the weight needed to serve model m's
  expected inference demand during a PoC window, estimated from the previous epoch (for example, peak in-flight
  requests for m during its PoC windows, converted to weight with the same per-10000 ratio).
- Fill the target with nodes that can carry load (largest first, or by declared serving capacity), not the smallest.
- This needs a per-model demand record (state or param), so it is a design for the team, not part of the PR.
- Preserving more weight does not weaken PoC: a preserved node is still checked during the same window, through
  the inference it serves and the validation of that inference.

## Related

- #1805 "Protocol-aware PoC / cPoC (preserved nodes)" (Devshard v8): if the gateway part belongs there, we are happy
  to move the PR onto that line.
- Discussion #1384 (cPoC skip protocol), #1348 (serve inference during PoC validation).

</div>

---

> 🔄 **Auto-synced** from [Issue #2107](https://github.com/gonka-ai/gonka/issues/2107) every hour.
