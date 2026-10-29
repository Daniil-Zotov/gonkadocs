---
title: "#1658 — 413 on large chat payload due to gateway/host request size mismatch"
source: https://github.com/gonka-ai/gonka/issues/1658
issue_number: 1658
synced_at: 2026-10-29T16:59:13Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    413 on large chat payload due to gateway/host request size mismatch
    <span class="issues-number">#1658</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/aikuznetsov">@aikuznetsov</a> opened 2026-08-27 13:02 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-10-15 00:51 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
### Summary

Large `/v1/chat/completions` requests can pass the gateway-side body limit but fail later with `413 Payload Too Large` on host transport.

The issue appears to be a mismatch between:

- what the gateway accepts from the client
- what the gateway later sends to hosts

### Current behavior

The gateway limits the client request body as raw JSON. The current cap is `10 MiB`:

- [`MaxChatRequestBodySize = 10 * 1024 * 1024`](https://github.com/gonka-ai/gonka/blob/5af3770b234548643ce65f826edbd17a6964ba48/devshard/cmd/devshardctl/request_filters_config.go#L3-L6)
- client body read/reject path: [`readLimitedChatRequestBody`](https://github.com/gonka-ai/gonka/blob/5af3770b234548643ce65f826edbd17a6964ba48/devshard/cmd/devshardctl/request_filters.go#L163-L176)

However, after the request is accepted, the normalized request body is stored in:

```go
host.InferencePayload.Prompt []byte
```

The host-bound transport request then exposes this prompt as a JSON-facing `[]byte` field:

- [`PayloadJSON.Prompt []byte`](https://github.com/gonka-ai/gonka/blob/5af3770b234548643ce65f826edbd17a6964ba48/devshard/transport/types.go#L21-L28)
- [`InferenceRequest.Payload *PayloadJSON`](https://github.com/gonka-ai/gonka/blob/5af3770b234548643ce65f826edbd17a6964ba48/devshard/transport/types.go#L30-L38)
- conversion from `host.HostRequest` to the transport JSON shape: [`HostRequestToJSON`](https://github.com/gonka-ai/gonka/blob/5af3770b234548643ce65f826edbd17a6964ba48/devshard/transport/types.go#L146-L164)

In Go JSON serialization, `[]byte` is encoded as base64, which adds roughly 33% overhead.

As a result, a client payload of about `8 MiB` can pass the gateway-side limit, but becomes approximately `10.7 MiB` when sent to a host as base64-encoded JSON. On top of that, the host-bound request also includes:

- `diffs`
- signatures
- envelope / height-sync fields
- other metadata

The host then enforces the actual inbound request body size with the same `10 MiB` default cap:

- host transport default cap: [`DefaultMaxBodySize = 10 * 1024 * 1024`](https://github.com/gonka-ai/gonka/blob/5af3770b234548643ce65f826edbd17a6964ba48/devshard/transport/server.go#L32-L39)
- host signed POST body is wrapped with `http.MaxBytesReader`: [`VerifyPOSTAuth`](https://github.com/gonka-ai/gonka/blob/5af3770b234548643ce65f826edbd17a6964ba48/devshard/transport/server.go#L223-L260)

This causes the request to fail with `413` on the host side.

### Why this is problematic

This is not really a host failure. The request is deterministically too large for the current host transport format.

If the gateway sends the same oversized request to multiple hosts, several hosts may fail in the same way. Redundancy may then treat this as host failure, even though the real issue is that the request cannot fit into the host transport limit after internal serialization overhead.

### Related edge case: large catch-up diffs

There is a similar potential issue when a host is far behind and needs a large diff catch-up.

The ordinary inference path sends `diffsForHost` together with the prompt payload:

- [`diffsForHost` returns all diffs since the host sync nonce](https://github.com/gonka-ai/gonka/blob/5af3770b234548643ce65f826edbd17a6964ba48/devshard/user/session.go#L532-L543)
- ordinary inference path builds `catchUp := s.diffsForHost(hostIdx)`: [`PrepareInferenceFn`](https://github.com/gonka-ai/gonka/blob/5af3770b234548643ce65f826edbd17a6964ba48/devshard/user/session.go#L1178-L1187)
- `SendOnly` sends that catch-up together with `Payload.Prompt`: [`SendOnly`](https://github.com/gonka-ai/gonka/blob/5af3770b234548643ce65f826edbd17a6964ba48/devshard/user/session.go#L1203-L1217)

So if a host has accumulated a large backlog of diffs, the host-bound request can exceed the same body cap even when the prompt itself is not huge.

Finalize catch-up already chunks diffs, which may be a useful pattern to reuse:

- [`catchUpChunkSize = 200`](https://github.com/gonka-ai/gonka/blob/5af3770b234548643ce65f826edbd17a6964ba48/devshard/user/session.go#L1307-L1316)
- chunked finalize catch-up loop: [`sendCatchUpWith`](https://github.com/gonka-ai/gonka/blob/5af3770b234548643ce65f826edbd17a6964ba48/devshard/user/session.go#L1318-L1370)

### Expected behavior

If a request cannot fit into the host-bound wire format, the gateway should reject it before fanout, ideally with `413 Payload Too Large`.

This would avoid:

- unnecessary host requests
- false host failure signals
- noisy redundancy behavior
- misleading voting / observability data

</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/qdanik">@qdanik</a></span>
    <span class="issues-meta-item">commented 2026-09-27 14:42 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>after the discussion with @akup the solution delivered in https://github.com/gonka-ai/gonka/pull/1732 is declined.
https://github.com/gonka-ai/gonka/pull/1832 - gRPC should cover this case.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/a-kuprin">@a-kuprin</a></span>
    <span class="issues-meta-item">commented 2026-10-15 00:51 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Closed in v6</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1658](https://github.com/gonka-ai/gonka/issues/1658) every hour.
