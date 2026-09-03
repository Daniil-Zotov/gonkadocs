---
title: "#1696 — devshard: bridge.ClassifyQueryError has no production callers, so transient chain-query failures return 500 instead of the intended retryable 503"
source: https://github.com/gonka-ai/gonka/issues/1696
issue_number: 1696
synced_at: 2026-09-03T00:21:06Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    devshard: bridge.ClassifyQueryError has no production callers, so transient chain-query failures return 500 instead of the intended retryable 503
    <span class="issues-number">#1696</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/Ryanchen911">@Ryanchen911</a> opened 2026-09-01 08:25 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-09-01 08:25 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

`bridge.ClassifyQueryError` — the function whose job is to mark transient chain
query failures as `ErrChainUnavailable` so they can be retried — has **zero
non-test callers**. As a result `bridge.ErrChainUnavailable` is never produced in
production, the two branches that consume it in `devshard/server/routes.go` are
unreachable, and a temporarily throttled or unreachable chain endpoint is
reported to clients as `500 Internal Server Error` instead of the intended
retryable `503`.

## Evidence

`ClassifyQueryError` is defined and tested, but never called:

```
$ git grep -n "ClassifyQueryError" upstream/main -- '*.go' | grep -v _test.go
upstream/main:devshard/bridge/errors.go:20:// ClassifyQueryError wraps transient query/transport failures as ErrChainUnavailable.
upstream/main:devshard/bridge/errors.go:22:func ClassifyQueryError(err error) error {
```

Its stated contract (`devshard/bridge/errors.go:15-17`):

```go
// ErrChainUnavailable means the chain/query path is temporarily unreachable.
// Lazy session create should map this to HTTP 503 so clients can retry.
ErrChainUnavailable = errors.New("chain unavailable")
```

Both bridges wrap query errors with `fmt.Errorf` and skip classification:

```
$ git show upstream/main:devshard/bridge/grpc.go | grep -n "%s: %w"
69:  return nil, fmt.Errorf("DevshardEscrow %s: %w", escrowID, err)
110: return nil, fmt.Errorf("Participant %s: %w", address, err)

$ git show upstream/main:devshard/cmd/devshardd/bridge/chain.go | grep -n "%s: %w"
103: return nil, fmt.Errorf("DevshardEscrow %s: %w", escrowID, err)
141: return nil, fmt.Errorf("Participant %s: %w", address, err)
```

So the consumers in `devshard/server/routes.go` cannot fire:

```go
// line 203, sessionHTTPError
if errors.Is(err, bridge.ErrChainUnavailable) {
    return transport.HTTPError(c, http.StatusServiceUnavailable,
        transport.DevshardErrorChainUnavailable, err.Error())
}
// ... falls through to:
return echo.NewHTTPError(http.StatusInternalServerError, err.Error())
```

```go
// line 142, sessionResolutionStatus
if errors.Is(err, bridge.ErrChainUnavailable) {
    return observability.MetricStatusError, observability.ReasonGetEscrowErr
}
```

The metric case is partly rescued further down by a string match on
`"get escrow"`, so `GetEscrow` failures still land on `ReasonGetEscrowErr`. But
`GetHostInfo` failures are wrapped as `"get host info for %s"` and fall through
to the default `ReasonSessionResolveErr`, and the HTTP status is wrong in both
cases.

## Impact

`ClassifyQueryError` maps `codes.ResourceExhausted`, `codes.Unavailable`,
`codes.DeadlineExceeded` and bare transport errors to `ErrChainUnavailable`.
These are exactly the codes a rate-limited or briefly unreachable chain endpoint
produces. With classification missing:

- Clients get `500` for a condition that is retryable, and a well-behaved client
  correctly does not retry a `500`.
- `transport.DevshardErrorChainUnavailable` never appears in any response, so it
  cannot be used to distinguish infrastructure trouble from a real fault.
- The `ReasonGetEscrowErr` / `ReasonSessionResolveErr` split does not reliably
  separate "chain is throttling us" from "something is actually broken".

We hit this from the operator side. A network node's nginx was rate-limiting our
gateway's chain queries at 0.33 req/s for weeks (filed separately as a proxy
configuration issue, 8,000+ rejections in 24h). Nothing in the devshard-side
output identified the failures as transient/upstream, which is a large part of
why it took so long to attribute. The proxy misconfiguration is the root cause of
that incident; this issue is about the devshard side not being able to say what
was happening.

## Suggested fix

Call `ClassifyQueryError` at the bridge query boundaries — `GetEscrow` and
`GetHostInfo` in both `devshard/bridge/grpc.go` and
`devshard/cmd/devshardd/bridge/chain.go`:

```go
resp, err := b.client.InferenceQueryClient().DevshardEscrow(ctx, req)
if err != nil {
    return nil, ClassifyQueryError(fmt.Errorf("DevshardEscrow %s: %w", escrowID, err))
}
```

`ClassifyQueryError` already passes its sentinels through unchanged and returns
`nil` for `nil`, so this is additive: `NotFound` still becomes
`ErrEscrowNotFound`, application errors still pass through, and only the
transient classes gain the `ErrChainUnavailable` wrapper that the existing 503
branch is waiting for.

Two things worth deciding alongside it:

- Whether the escrow-existence check in `devshard/cmd/devshardctl/escrow_checker.go`
  should also branch on `ErrChainUnavailable`. It currently deactivates only on
  `ErrEscrowNotFound` and logs "keeping active" otherwise, which is the correct
  behaviour, but it would become explicit rather than incidental.
- Whether a log line or metric should mark sustained `ErrChainUnavailable` rates,
  so an operator sees "chain path is degraded" rather than inferring it from
  request failures.

Happy to open a PR for the bridge-boundary change if that direction is agreeable.

## Environment

- Verified on `upstream/main`. `devshard/bridge/errors.go` was added in
  `d8b8e9073` (v0.2.12, 2026-04-29); the 503 consumer in `server/routes.go`
  arrived in `ee730031d` (v0.2.14, 2026-07-23). The classifier appears to have
  been written ahead of its call sites and then never wired in.

</div>

---

> 🔄 **Auto-synced** from [Issue #1696](https://github.com/gonka-ai/gonka/issues/1696) every hour.
