---
title: "#1660 — Large per-host catch-up diff backlog can cause 413 on host transport"
source: https://github.com/gonka-ai/gonka/issues/1660
issue_number: 1660
synced_at: 2026-08-29T21:48:34Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Large per-host catch-up diff backlog can cause 413 on host transport
    <span class="issues-number">#1660</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/aikuznetsov">@aikuznetsov</a> opened 2026-08-27 13:24 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-08-27 13:31 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

A host can fall far behind the current session state and later receive an oversized catch-up request, causing `413 Payload Too Large` on host transport.

This is related to large payload handling, but the root cause is different from the raw client prompt size issue. In this case, the main factor is the accumulated per-host diff backlog.

## What happens

The session tracks a separate sync cursor for each host:

[`hostSyncNonce map[int]uint64`](https://github.com/gonka-ai/gonka/blob/5af3770b234548643ce65f826edbd17a6964ba48/devshard/user/session.go#L278)

This cursor represents the latest nonce that a specific host has successfully acknowledged.

When the gateway prepares a request for a host, it builds catch-up diffs using `diffsForHost`:

[`diffsForHost`](https://github.com/gonka-ai/gonka/blob/5af3770b234548643ce65f826edbd17a6964ba48/devshard/user/session.go#L532-L543)

That function returns all diffs with `Nonce > hostSyncNonce[hostIdx]`.

The cursor only advances after a successful host response is processed:

[`processResponse` updates `hostSyncNonce`](https://github.com/gonka-ai/gonka/blob/5af3770b234548643ce65f826edbd17a6964ba48/devshard/user/session.go#L680-L688)

So if a host is unavailable, times out, fails state verification, or repeatedly receives a transport-level error such as `413`, its sync cursor does not move forward while the session continues accumulating new diffs.

## Ordinary inference path

When that host is selected again for inference, the ordinary inference path builds the full catch-up backlog:

[`catchUp := s.diffsForHost(hostIdx)`](https://github.com/gonka-ai/gonka/blob/5af3770b234548643ce65f826edbd17a6964ba48/devshard/user/session.go#L1176-L1187)

Then it sends the catch-up diffs together with the current prompt in one host-bound request:

[`SendOnly` sends `Diffs: p.catchUp` and `Payload.Prompt`](https://github.com/gonka-ai/gonka/blob/5af3770b234548643ce65f826edbd17a6964ba48/devshard/user/session.go#L1203-L1217)

So the host-bound body size includes the catch-up diffs, prompt payload, height-sync / envelope fields, signatures, metadata, and JSON/base64 overhead.

## Why this can produce 413

Each diff is represented in the JSON transport as `DiffJSON`:

[`DiffJSON`](https://github.com/gonka-ai/gonka/blob/5af3770b234548643ce65f826edbd17a6964ba48/devshard/transport/types.go#L12-L19)

`DiffJSON` contains several `[]byte` fields:

- `Txs`
- `UserSig`
- `PostStateRoot`

In Go JSON serialization, these byte slices are encoded as base64, which adds overhead to every diff.

So a large backlog, for example thousands of diffs, can become large enough to exceed the host transport body limit even before considering the prompt.

The host transport currently enforces a `10 MiB` default body cap:

[`DefaultMaxBodySize = 10 * 1024 * 1024`](https://github.com/gonka-ai/gonka/blob/5af3770b234548643ce65f826edbd17a6964ba48/devshard/transport/server.go#L32-L39)

[`VerifyPOSTAuth` wraps the request body with `http.MaxBytesReader`](https://github.com/gonka-ai/gonka/blob/5af3770b234548643ce65f826edbd17a6964ba48/devshard/transport/server.go#L223-L260)

## Validation and vote diff size

Validation and voting traffic can make the backlog heavier.

For example, these tx types include signatures, escrow IDs, hashes, and other metadata:

[`MsgFinishInference`](https://github.com/gonka-ai/gonka/blob/5af3770b234548643ce65f826edbd17a6964ba48/devshard/types/tx.pb.go#L249-L259)

[`MsgValidation`](https://github.com/gonka-ai/gonka/blob/5af3770b234548643ce65f826edbd17a6964ba48/devshard/types/tx.pb.go#L594-L600)

[`MsgValidationVote`](https://github.com/gonka-ai/gonka/blob/5af3770b234548643ce65f826edbd17a6964ba48/devshard/types/tx.pb.go#L670-L676)

So the issue is not only the number of diffs, but also the average serialized size of each diff.

## Failure loop

This can create a self-reinforcing failure loop:

1. Host falls behind.
2. Gateway builds a large catch-up for that host.
3. Catch-up plus prompt exceeds the host transport body limit.
4. Host returns `413` before applying the diffs.
5. Gateway does not advance `hostSyncNonce`.
6. The next attempt sends the same or even larger backlog.

At that point the host may be unable to catch up through the ordinary inference path.

## Existing partial mitigation

There is already chunked catch-up logic:

[`catchUpChunkSize = 200`](https://github.com/gonka-ai/gonka/blob/5af3770b234548643ce65f826edbd17a6964ba48/devshard/user/session.go#L1307-L1316)

[`sendCatchUpWith` sends catch-up diffs in chunks](https://github.com/gonka-ai/gonka/blob/5af3770b234548643ce65f826edbd17a6964ba48/devshard/user/session.go#L1318-L1370)

The comment explicitly mentions that large sessions can accumulate many diffs and that sending them all at once risks timeouts and oversized request bodies.

However, this chunking is not used in the ordinary inference path. Ordinary inference currently sends `catchUp + prompt` in a single POST.

## Related path

A similar risk exists in heartbeat / height-sync flow, where `diffsForHost` is also sent as one request:

[`heartbeat sendComposedDiff` uses `s.diffsForHost`](https://github.com/gonka-ai/gonka/blob/5af3770b234548643ce65f826edbd17a6964ba48/devshard/user/heartbeat.go#L374-L383)

This request does not include the prompt, but a sufficiently large diff backlog can still exceed the same transport body limit.

## Expected behavior

If a host is too far behind to receive its catch-up in a single host-bound request, the gateway should avoid sending an oversized ordinary inference request.

The system should not treat this as an ordinary host failure, because the request is deterministically too large for the current host transport format.

This would avoid:

- repeated `413` failures
- stale `hostSyncNonce` cursors
- self-reinforcing catch-up backlog growth
- misleading host failure / voting signals
- unnecessary fanout of requests that cannot fit into host transport limits
</div>

---

> 🔄 **Auto-synced** from [Issue #1660](https://github.com/gonka-ai/gonka/issues/1660) every hour.
