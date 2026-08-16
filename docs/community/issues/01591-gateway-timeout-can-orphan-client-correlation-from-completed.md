---
title: "#1591 — Gateway timeout can orphan client correlation from completed request accounting"
source: https://github.com/gonka-ai/gonka/issues/1591
issue_number: 1591
synced_at: 2026-08-16T15:40:24Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Gateway timeout can orphan client correlation from completed request accounting
    <span class="issues-number">#1591</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/safal207">@safal207</a> opened 2026-08-13 13:17 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-08-13 13:17 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

I’ve been independently testing Gonka’s gateway/request-accounting flow in the local devshard test environment and found a reproducible causal-addressability edge case around client timeouts.

This is **not** being reported as a security vulnerability or a mainnet financial issue. The finding is currently scoped to the pinned local test environment.

## What happens

A request can intentionally continue executing after the client disconnects or times out. That behavior itself appears intentional and useful.

The problem is correlation/addressability:

1. the caller sends a request and may provide a caller-known request/correlation ID;
2. Gonka creates its own internal request ID for execution/accounting;
3. the client times out before receiving that generated internal ID;
4. the inference continues and completes;
5. request accounting exists under the internal request ID;
6. the timed-out client no longer has a reliable key that resolves the completed accounting record.

In short:

```text
caller-known correlation
        ↓
client timeout
        ↓
execution continues
        ↓
completed internal request/accounting
        ↓
internal request ID was never received by caller
```

## Local reproduction

Pinned Gonka revision:

`f040d0a5b5ef207a0c431894c9f9e2608f9d3073`

Control parameters:

- deterministic downstream latency: `1800ms`
- client timeout: `350ms`
- caller supplies a known `X-Request-Id`
- a completed post-timeout request witness is required before classification

Observed in the local testenv:

- client timeout: `true`
- execution completion after timeout: `true`
- caller-known request ID resolves request accounting: `false`

Evidence run:

https://github.com/safal207/ContractGraph-QA/actions/runs/31662057767

## Important: the obvious fix is unsafe

I also tested the tempting remediation: use the caller-provided request ID directly as the canonical `request_accounting.request_id`.

That fixes addressability, but creates a different integrity problem if two independent operations reuse the same caller-controlled value.

In a storage guard test, two independent logical operations using the same caller ID collapsed into one canonical accounting row:

- logical operations: `2`
- canonical accounting rows: `1`
- attempt nonces retained together: `[101, 202]`
- resulting remediation classification: `REJECTED_AS_PRODUCTION_FIX`

Evidence run:

https://github.com/safal207/ContractGraph-QA/actions/runs/31664550699

## Safer correlation shape

The safer model appears to be:

```text
client_correlation_id          # caller-controlled, may repeat
        ↓ one-to-many
internal_request_id            # gateway-generated, unique canonical ID
        ↓
execution attempt nonce(s) / accounting
```

That keeps Gonka’s internal request identity canonical while giving a timed-out caller a recoverable correlation path.

A lookup by caller correlation should be allowed to return multiple internal request IDs rather than silently selecting or overwriting one. Reusing a correlation ID should not imply idempotency.

## Current work

I’m currently validating a non-collapsing correlation implementation against:

- repeated caller correlation IDs;
- timeout followed by retry;
- independent internal request identities;
- request-accounting lineage preservation.

I’m deliberately gating broader financial reconciliation work until this identity/correlation layer is proven.

Related independent work/evidence is tracked here:

https://github.com/safal207/ContractGraph-QA/pull/33

## Related upstream observation

This is adjacent to, but different from, #1387. That issue is about client-visible success diverging from gateway request outcome. This issue is specifically about whether a caller can reliably recover the internal request/accounting lineage after a timeout.

Happy to share the minimal harness/evidence details if useful.
</div>

---

> 🔄 **Auto-synced** from [Issue #1591](https://github.com/gonka-ai/gonka/issues/1591) every hour.
