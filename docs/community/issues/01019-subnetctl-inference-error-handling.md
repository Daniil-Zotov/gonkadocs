---
title: "#1019 — subnetctl: inference error handling"
source: https://github.com/gonka-ai/gonka/issues/1019
issue_number: 1019
synced_at: 2026-08-04T10:02:50Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    subnetctl: inference error handling
    <span class="issues-number">#1019</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/akup">@akup</a> opened 2026-04-06 02:29 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-07-01 06:00 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #95b500; color: #24292f; border-color: #95b500;">Priority: Low</span></div>
</div>

<div class="issues-content" markdown="1">
## Summary

**Today `subnetctl` does not surface many host-side failures during inference.** When the HTTP call to the executor fails (for example **403 Forbidden** with `sender not in group`), the proxy treats that as “no response yet” and **waits through refusal / execution timeouts** before eventually failing with timeout-related errors (for example insufficient timeout votes). The original transport error is **not** returned to the API client immediately.

This behavior comes from `sendAndProcess` in:

- `subnet/cmd/subnetctl/proxy.go`

## What the code does today

Flow (simplified):

1. `SendOnly` → `transport.HTTPClient.Send` → on non-200 (including 403), the client returns **`(nil, error)`** (see `subnet/transport/client.go`).
2. `sendAndProcess` does:

   ```go
   resp, sendErr := p.session.SendOnly(ctx, prepared)
   if sendErr != nil && resp == nil {
       return false, 0, nil   // no error propagated to runInference
   }
   ```

3. `runInference` interprets that as “not finished, no receipt,” sleeps until **RefusalTimeout** or **ExecutionTimeout**, retries once, then may enter **timeout vote** collection.

So **403 / 401 / 5xx** from the host are **not** distinguished at the proxy layer today; send failures with `resp == nil` are **silent** until the timeout machinery runs.

## Why this is a problem

- **Misconfiguration** (wrong user key vs escrow `CreatorAddress`, wrong network, ACL bugs) surfaces as **minute-long waits** and confusing messages like “insufficient timeout votes,” instead of an immediate **4xx with a clear cause**.
- **Operators and clients** cannot distinguish “host is down” from “host rejected the request” without reading participant logs.

## Target behavior (to implement)

Errors from the executor (and related paths) should be split into two classes:

### 1. Non-retryable / fatal (interrupt the inference)

Fail **immediately** (or after a single idempotent sanity check) and return a clear error to the OpenAI-compatible client (e.g. HTTP 502/403 with message body).

Examples:

- **4xx from host** where retrying the same request will not help without changing client or chain state:
  - **403** — `sender not in group`, auth/signature mismatch, creator vs escrow mismatch.
  - **400** — malformed payload, validation errors.
- **401** if used for auth failures.

These should **not** block on RefusalTimeout / ExecutionTimeout.

### 2. Retryable (bounded retries, then fail)

Transient infrastructure or ordering issues:

- **Connection errors**, **timeouts**, **502/503/504** from a reverse proxy.
- **429** with backoff (if applicable).
- Brief **unavailability** where the same signed request might succeed shortly (optional: small retry budget with jitter).

Policy should be **explicit**: max attempts, backoff, and when to give up and return an error to the client.

#### After `MsgStartInference` succeeded, before `MsgFinishInference`

Once the session has **successfully advanced** so that **`MsgStartInference` is in effect** for this inference, but **`MsgFinishInference` has not yet appeared** in the mempool (executor still running or client is waiting on stream / follow-up sync):

- **5xx** and **network errors** on any later HTTP interaction with the same or peer hosts (status polls, catch-up, streaming chunk fetches, verifier traffic, etc.) should be treated as **retryable**, not as fatal client misconfiguration.
- Retries should stay within the existing **execution / refusal deadline** window where applicable, so the overall inference does not hang unbounded.

By contrast, a **403 / 401 / 400** on a request that clearly indicates **authorization or payload rejection** (e.g. first contact with wrong creator key) remains **non-retryable** unless the error semantics are known to be transient (rare).

### 3. Protocol continuation (keep current timeout path)

When the transport **succeeds** (HTTP 200) and the host returns a normal **`HostResponse`**, but the mempool still does not contain **`MsgFinishInference`** for this nonce, **`runInference`** should keep using **refusal / execution deadlines** and optional **timeout votes** as today.

That timeout path addresses **slow or stuck executors**, not **misclassified transport failures** — transport errors during this phase should still follow §2 (retryable 5xx / network) where possible before falling through to timeout.

## Implementation notes (for a future change)

- **Classify** `SendOnly` / `HTTPClient.Send` errors: parse status code when available (wrap errors with `errors.As` into a typed `HTTPStatusError` or similar).
- **In `sendAndProcess`**: on `sendErr != nil && resp == nil`, return **`(false, 0, sendErr)`** for fatal statuses, or implement a **retry loop** for retryable statuses before returning.
- **Phase-aware policy**: same status code may be **fatal** on the first “start inference” exchange and **retryable** once `MsgStartInference` is already committed for this nonce (see §2 above). Thread **inference phase** (pre-start vs post-start vs waiting-for-finish) into error handling.
- **Align** `subnet/cmd/subnetctl` and `subnet/testenv/cmd/subnetctl` (or share one `proxy` package to avoid drift).
- **Document** status mapping in this file once implemented.

## Related code

| Piece | Role |
|-------|------|
| `subnet/transport/client.go` | Returns error on `StatusCode != 200` |
| `subnet/cmd/subnetctl/proxy.go` → `sendAndProcess` | Swallows send failure when `resp == nil` |
| `subnet/user/user.go` → `SendOnly` | Thin wrapper over client `Send` |
| `subnet/testenv/cmd/subnetctl/proxy.go` | Same as production proxy |

</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/unameisfine">@unameisfine</a></span>
    <span class="issues-meta-item">commented 2026-04-08 21:06 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Taking this. Submitted a minimal fix that addresses the core symptom (fatal 4xx swallowed into timeouts) in PR to follow, leaving the broader phase-aware retry design (§2 and §3 in the issue) for a separate change.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1019](https://github.com/gonka-ai/gonka/issues/1019) every hour.
