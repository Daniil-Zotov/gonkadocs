---
title: "#1965 — [BUG] Incomplete JSON clock timestamps produce a false divergence sample"
source: https://github.com/gonka-ai/gonka/issues/1965
issue_number: 1965
synced_at: 2026-10-10T18:41:48Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    [BUG] Incomplete JSON clock timestamps produce a false divergence sample
    <span class="issues-number">#1965</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/EazyHood">@EazyHood</a> opened 2026-10-09 21:02 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-10-09 21:02 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

`common/probe` treats a JSON clock response with `send_unix_ns` but no usable `recv_unix_ns` as a valid four-timestamp sample. In a deterministic local reproduction, it reports a clock offset of **-895,773,600 seconds** with no error. A usable HTTP `Date` header does not prevent the false sample.

## Motivation and impact

This is an observability correctness issue for operators using the optional JSON clock-response format. An incomplete response can produce a misleading clock-divergence metric instead of falling back to `Date` or omitting the sample. It is an edge case, not a claim of a production incident or network-wide failure. The normative two-header response is not affected; probe results are observability-only, not routing or consensus inputs.

The [clock contract](https://github.com/gonka-ai/gonka/blob/fd99f88d1f5d51f498a7108a56c41a826aa0dbe9/devshard/docs/proposals/gateway-host-ping-observability.md#appendix-mlnode-handoff--how-dapi-connects-what-to-add) specifies both JSON timestamps, with no optional fields. The parser already rejects incomplete timestamp headers.

## Reproduction and cause

Checked on main `fd99f88d1f5d51f498a7108a56c41a826aa0dbe9`, using Go 1.25.9.

1. Set the injected probe clock to `2026-10-09T12:00:00Z`.
2. Return HTTP 200 with `Content-Type: application/json`, no timestamp headers, and body `{"send_unix_ns":1791547200000000000}`.
3. Call `ProbeOnce` with this endpoint as `ClockURL`.

Observed:

```text
up=true hasDivergence=true source=clock divergenceSeconds=-895773600.000 err=<nil>
```

The same happens with `"recv_unix_ns":null`. Adding `Date: Fri, 09 Oct 2026 12:00:00 GMT` still produces the false `clock` sample. Supplying both timestamps correctly produces zero offset.

In [parse.go](https://github.com/gonka-ai/gonka/blob/fd99f88d1f5d51f498a7108a56c41a826aa0dbe9/common/probe/parse.go), `pingJSON` has plain `int64` fields. An absent/null receive timestamp becomes zero. The `both == 0` check does not catch it, and `send >= recv` passes. The function returns both presence flags as true; `finishPing` then uses epoch zero as T2 and skips the Date fallback.

Minimal regression test, saved as `common/probe/partial_json_regression_test.go`:

```go
package probe_test

import (
    "common/probe"
    "context"
    "io"
    "net/http"
    "strings"
    "testing"
    "time"
)

type incompleteClockTransport struct{}
func (incompleteClockTransport) RoundTrip(req *http.Request) (*http.Response, error) {
    return &http.Response{
        StatusCode: 200, Header: http.Header{"Content-Type": {"application/json"}},
        Body: io.NopCloser(strings.NewReader(`{"send_unix_ns":1791547200000000000}`)),
        Request: req,
    }, nil
}

func TestIncompleteJSONClockDoesNotEmitDivergence(t *testing.T) {
    p, err := probe.New(probe.Config{
        Interval: time.Second, Timeout: 200*time.Millisecond,
        Clock: func() time.Time { return time.Date(2026,10,9,12,0,0,0,time.UTC) },
        Transport: incompleteClockTransport{},
    })
    if err != nil { t.Fatal(err) }
    r := p.ProbeOnce(context.Background(), probe.Target{
        Key: "fixture", ClockURL: "http://fixture.invalid/clock",
    })
    if r.HasDivergence {
        t.Fatalf("incomplete JSON became a clock sample: %+v", r)
    }
}
```

Run from `common`: `go test ./probe -run TestIncompleteJSONClockDoesNotEmitDivergence -v`. The transport is a local test double; it sends no network request.

## Proposed scope

Use presence-aware decoding for the JSON timestamp pair and reject incomplete pairs, preserving reachability and the existing Date fallback. Add regression cases for missing/null receive or send time, a complete pair, a usable Date fallback, and the existing explicit zero-pair behavior.

I tested a small pointer-field correction in an isolated module initialized with byte-identical copies of this package's source and existing tests. The regression suite fails on missing/null receive timestamps before the correction and passes afterward; complete-pair and missing-send controls already pass on the baseline. The correction preserves the existing explicit zero-pair fallback behavior, also covered by regression tests. All existing probe tests pass. I have not run the full repository/integration suite or changed a live node.

Could you confirm this scope is actionable and assign it to me if it is not already being handled? I would also like to know whether this bounded fix would be considered for contributor rewards; I understand a payout requires governance approval. No PR has been opened. This investigation used Codex assistance and executable regression checks.

</div>

---

> 🔄 **Auto-synced** from [Issue #1965](https://github.com/gonka-ai/gonka/issues/1965) every hour.
