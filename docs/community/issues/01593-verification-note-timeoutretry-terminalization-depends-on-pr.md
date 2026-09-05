---
title: "#1593 — Verification note: timeout/retry terminalization depends on protocol-time, not wall-clock time"
source: https://github.com/gonka-ai/gonka/issues/1593
issue_number: 1593
synced_at: 2026-09-05T01:04:28Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Verification note: timeout/retry terminalization depends on protocol-time, not wall-clock time
    <span class="issues-number">#1593</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/safal207">@safal207</a> opened 2026-08-14 03:59 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-08-14 03:59 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Hi Gonka team — we’ve been independently pressure-testing the timeout/retry + accounting path against a pinned local devshard revision (`f040d0a5b5ef207a0c431894c9f9e2608f9d3073`) and found a verification boundary that may be useful upstream.

This is **not a vulnerability claim** and we are deliberately not labeling it as an upstream bug yet.

## What the first probe observed

Our initial G-004P probe reproduced this sequence:

```text
client request
→ client-side timeout
→ retry
→ retry returns HTTP 2xx
→ request accounting reports success
→ retry winner remains protocol `pending`
```

In the recorded run, the retry winner stayed `pending` for the full 120-second observation window. Its `ReservedCost` remained reserved and `ActualCost` was still zero during that window.

At first glance this looked like a possible post-success terminalization/accounting liveness issue.

## Why we are not claiming that

A deeper causal pass over the pinned Gonka state flow showed that our first interpretation was too strong.

The relevant path is closer to:

```text
host execution completes
→ MsgFinishInference is signed/published to host mempool
→ user Session queues host mempool Finish txs in pendingTxs for a subsequent diff
→ next eligible diff applies Finish
→ inference becomes StatusFinished
→ ReservedCost - ActualCost is released
```

So our original oracle:

```text
HTTP success
→ wait N seconds
→ inference must be terminal
```

was using **wall-clock time as a proxy for protocol/nonce time**. That is not a valid causal boundary for this implementation.

We therefore changed the verifier rather than treating the first result as an upstream defect.

## Corrected experiment

The new G-004Q proof now requires the following chain:

```text
retry HTTP 2xx
→ retry winner observed pending
→ exact MsgFinishInference(retry_nonce) witnessed in Session.pendingTxs
→ only then drive a separate eligible state-advancing request/diff
→ prove protocol state advanced
→ retry winner must become finished
→ reconcile ReservedCost / ActualCost / balance / fees / HostStats
```

To avoid racing the protocol, our proof build exposes a **read-only, test-only** view of `Session.PendingTxs()` and refuses to advance unless the exact retry nonce is already present in the pending Finish set.

The financial oracle also avoids attributing raw balance movement to one request, because the advancing request can itself reserve funds and create fees. Instead it verifies the whole-state identities:

```text
Balance_after
  = Balance_before
  - (InferenceLiability_after - InferenceLiability_before)
  - (Fees_after - Fees_before)

HostStatsCost_delta
  = InferenceActualCost_delta
```

where pending/started inference liability is represented by `ReservedCost`, and terminal no-dispute liability by `ActualCost`.

## Interpretation boundary

If G-004Q converges after Finish-readiness + a proven protocol advance, we will classify the earlier G-004/G-004P discrepancy as a **non-terminal protocol-time snapshot**, not a durable financial defect.

If it remains pending **after** the exact Finish is already eligible and a real state-advance opportunity occurred, that would be a materially stronger sequencing/state-application candidate worth narrowing further.

The executable proof and causal trace are in:

https://github.com/safal207/ContractGraph-QA/pull/50

The corrected runtime proof is still running, so we are intentionally sharing the verification boundary before making any defect conclusion.

Happy to share the evidence bundle or adjust the probe if there is a more canonical Gonka state-advance/terminalization boundary you would prefer us to test.
</div>

---

> 🔄 **Auto-synced** from [Issue #1593](https://github.com/gonka-ai/gonka/issues/1593) every hour.
