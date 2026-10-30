---
title: "#2049 — Important! ChallengeReceipt memory overflows"
source: https://github.com/gonka-ai/gonka/issues/2049
issue_number: 2049
synced_at: 2026-10-30T20:53:45Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Important! ChallengeReceipt memory overflows
    <span class="issues-number">#2049</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/a-kuprin">@a-kuprin</a> opened 2026-10-16 12:08 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-10-16 21:29 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #a2eeef; color: #24292f; border-color: #a2eeef;">enhancement</span></div>
</div>

<div class="issues-content" markdown="1">
# ChallengeReceipt memory: problem statement

A refused-timeout check sends the executor the diffs it may have missed, in one `ChallengeReceipt`. Today the verifier loads that range into one decoded slice, re-encodes it three times, and sends it in one message. When the executor tip cannot be anchored, or is ahead of the verifier, the range is the whole journal from nonce 1. Several checks run at once and none share work.

In the 2-hour soak this took versiond-0 to 17.86 GiB of Go `sys`. The executor rejects any such message over 10 MiB, so past roughly 20,000 diffs the memory is spent on a challenge that can never be delivered. The verifier then accepts the timeout as if the executor had not answered.

The fix plan is [challenge-receipt-memory-plan.md](challenge-receipt-memory-plan.md).

## Soak evidence

`soak2h-host-memory-snapshots.log`, binary `0.2.13-v2-r2`, about 16 rps for two hours. Fields are described in [memory-snapshot.md](memory-snapshot.md).

| Time (UTC) | versiond-0 live heap | versiond-0 `sys` | Objects |
| --- | --- | --- | --- |
| 21:33 | 0.19 GiB | 0.37 GiB | steady |
| 21:43 | 0.45 GiB | 8.28 GiB | spike already collected |
| 21:53 | 2.79 GiB | 8.28 GiB | 12.0M |
| 22:23 | 3.98 GiB | 15.93 GiB | 53.8M |
| 22:33 | 0.26 GiB | 15.93 GiB | collected |
| 22:53 | 7.52 GiB | 17.86 GiB | 101.0M |

versiond-2 and versiond-3 step the same way (peak `sys` 14.77 and 14.55 GiB). At 22:53 all three hold the same escrow, 111,932 live and 35,612 sealed inferences, about 148,000 diffs. The retained cost of the live map is about 3 KB per inference. The spikes are not that map.

The named heap stacks at every spike are `refusalJournal.Diffs` and `proto.Marshal` under `RPCClient.ChallengeReceipt`, called from `VerifyRefusedProgress`. At 22:53:

- `refusalJournal.Diffs` holds 346 MiB in 30 objects. A `types.Diff` is 80 bytes, so one 148,000-entry slice is 11.8 MiB. That is about 30 full-journal loads live together.
- Two 147 MiB `ChallengeReceipt` marshal lines are about 74 MiB per body, written twice. 74 MiB / 148,000 is about 500 bytes of wire form per diff.
- 101M objects / 30 loads / 148,000 diffs is about 23 heap objects per decoded diff.

The heap lines keep 12 stacks and sample once per 512 KiB. The large buffers show up in them. The roughly 80-byte protobuf objects mostly do not, and those make up most of the 7.52 GiB.

The 21:53 sample is the same shape with less overlap: nine marshal buffers of about 46 MiB (412 MiB total), and 12.0M decoded objects.

After each wave GC brings `heap_alloc` back under 0.5 GiB, and `heap_released` returns the pages to the OS. `sys` is the arena high-water mark and never shrinks. The 17.86 GiB is the largest wave, not a leak.

## When the verifier sends the whole journal

`VerifyRefusedProgress` (`devshard/host/refusal_progress.go`) first runs the local checks. If they all pass, it asks the executor for its tip with `SessionHead`.

- If the tip is `0 < nonce <= LatestNonce` and `Anchor(nonce, root)` matches the stored root, it calls `Diffs(nonce+1, LatestNonce)`. This is the suffix, usually small. Each retry in `refusalAfterProgress` loads a new suffix.
- Otherwise it calls `Diffs(1, LatestNonce)` and then challenges once. That covers:
  - `SessionHead` answered with an error (not unreachable), such as a session the executor has not bound.
  - The executor reports nonce 0.
  - The executor reports a nonce **above** the verifier's `LatestNonce`. Under load the executor is often a few nonces ahead of the verifier's snapshot.
  - The root does not match.

The executor's `applyDiffsLocked` drops every diff with `nonce <= latest` before verifying anything. A bound executor at tip `T` uses only `T+1..LatestNonce` from the full journal. When `T >= LatestNonce` it uses none of it. So the nonce-1 fallback sends 148,000 diffs to a host that will apply a handful, or zero.

The only case that needs nonce 1 is an executor that has never bound the session. `bindStartProof` then needs the diff that holds the first `MsgStartInference`.

## Paging does not bound it

`refusalJournal.Diffs` (`devshard/transport/refusal.go`) reads 64-nonce pages but appends every page to one slice:

```go
diffs := make([]types.Diff, 0, to-from+1)
for start := from; start <= to; {
	recs, err := j.store.GetDiffs(j.escrowID, start, end)
	// ...
	diffs = append(diffs, rec.Diff)
}
return diffs, nil
```

The 64-nonce window limits one `GetDiffs` call, not what stays live. The 8 MiB byte budget of `ReadDiffPages` is not applied. The result goes into one `ChallengeReceipt`.

[diff-catchup-memory-plan.md](diff-catchup-memory-plan.md) step 7 describes "one page per `ChallengeReceipt`, in order from nonce 1". That was dbc3245d3. f6bca169f removed the journal from the refused path. 9c620cadc brought it back as the accumulating `Diffs` above. Step 7 no longer describes the code.

## Where the copies appear

One check, with the range of `N` diffs, holds these at the same time.

### Verifier (gateway-facing host)

**A. Decoded journal.** `GetDiffs` reads each `txs_proto` and `proto.Unmarshal`s it into `[]*DevshardTx` (`diffRecordFromStored`). `Diffs` keeps `rec.Diff` for every nonce in one `[]types.Diff`. That is 80 bytes per diff plus about 23 small objects for the transactions, their oneof messages, and their byte fields. This is the bulk of the 7.52 GiB.

**B. Re-encoded transactions.** `RPCClient.ChallengeReceipt` (`devshard/transport/rpcclient.go`) calls `DiffToJSON` per diff. `marshalDiffWireTxs` runs `proto.Marshal(DiffContent{Nonce, Txs})` and stores a new `[]byte`. That is a second copy of every transaction. It is byte-for-byte the stored `txs_proto` with a nonce field in front. `UserSig` and `PostStateRoot` are shared with A.

**C. Proto wrappers.** `ChallengeReceiptRequestToProto` → `diffsJSONToProto` allocates one `*rpcpb.Diff` per diff. They share B's bytes, so this copy is pointers only.

**D. Request body.** `proto.Marshal(inner)` writes the whole request into one buffer, about 74 MiB at 148,000 diffs. A, B, and C are still in scope and stay live.

**E. Envelope.** `signEnvelope(raw)` puts D in `SignedEnvelope.Payload`. Connect `MarshalAppend`s the envelope into its own buffer, which is a second copy of D. These are the two 147 MiB lines.

**F. Gzip.** `WithSendGzip` compresses E into another buffer while the request is written.

A through E stay reachable until `ChallengeReceipt` returns. That call is bounded by the 3-minute verify budget (a quarter of it on the tip path) and the client's `VerifyTimeout`, not by the size of the body.

The HTTP fallback (`HTTPClient.ChallengeReceipt` in `devshard/transport/client.go`) has the same A and B. It then `json.Marshal`s the request, which base64-encodes every byte field into one body about 4/3 the size of D.

### Executor

The executor allocates nothing for the oversized messages, because the Connect read cap rejects them first (see below). For a challenge under 10 MiB it holds:

**G0. Wire buffers.** The decompressed body, then `SignedEnvelope.Payload`, then the inner `rpcpb.ChallengeReceiptRequest`. Go protobuf copies `bytes` fields on unmarshal, so each is a separate copy.

**G1. First decode.** `SessionHandler.ChallengeReceipt` (`devshard/transport/rpcserver/session.go`) calls `transport.DiffsFromJSON` to get `[]types.Diff` for `bindStartProof`. On a cold host `GatewayStartVersion` verifies the user signature of every diff in the request.

**G2. Second decode.** It then passes the `DiffJSON` request to `Server.ServeChallengeReceipt` (`devshard/transport/server.go`), which calls `decodeDiffsJSON` and unmarshals every diff again. `Host.ChallengeReceipt` → `applyDiffsLocked` then drops the diffs at or below its tip and verifies the user signature of the rest a second time.

G1 is still referenced when G2 is built. Both are the full request.

### Per check, not per escrow

`ServeVerifyTimeout` runs one independent check per gateway vote request. The gateway posts up to 64 timeout votes at once (`maxConcurrentTimeoutVotePosts` in `devshard/cmd/devshardctl/timeout_vote_posts.go`). Checks against the same executor load the same range and build the same body, A through F each time. The soak caught about 30 at once.

Each check also starts with `SnapshotState`, a deep copy of the escrow state with all live inference records (`cloneEscrowState`). It is small next to A–F, but it is another per-check copy of something every check shares.

## The memory buys nothing past 10 MiB

The executor serves `ChallengeReceipt` with `connect.WithReadMaxBytes(transport.DefaultRPCLargeReadMaxBytes)`, 10 MiB (`devshard/transport/rpcserver/mux.go`), and that cap also limits decompression. The HTTP route has `DefaultMaxBodySize`, also 10 MiB. The client has no send cap. It builds and sends the whole body anyway.

At about 500 bytes per diff, any range above roughly 20,000 diffs is rejected with `ResourceExhausted` before `ServeChallengeReceipt` runs. `TestRPCClient_ChallengeReceiptReadMaxBytes` in `devshard/transport/peerconn_attach_test.go` covers this: a request over 10 MiB is `ResourceExhausted` and does not reach `ServeChallengeReceipt`.

On the verifier, `executorUnreachable` treats message-too-large as an answer, not as unreachable. The fallback path's `finishRefusedChallenge` accepts on any call error. The tip path goes to `refusalAfterProgress`, sees the same nonce, and accepts. Either way the check:

- spends A–F for a message that cannot be delivered,
- never lets the executor catch up, so the next check for the same executor starts from the same tip and does it again,
- accepts the timeout without the executor having been asked about the inference. A behind or cold executor can no longer prove it holds the start, which is what the challenge exists for.

## What the executor actually needs

The diffs after its tip, once, as nonce plus transactions plus user signature plus post-state root, in pieces that fit the read cap. On a cold host, the first piece must contain the start proof. The verifier already stores exactly those bytes as `txs_proto`. It does not need to decode them to forward them, it does not need the range in one message, and concurrent checks against one executor do not each need to send it.

</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/a-kuprin">@a-kuprin</a></span>
    <span class="issues-meta-item">commented 2026-10-16 21:29 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>merged</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2049](https://github.com/gonka-ai/gonka/issues/2049) every hour.
