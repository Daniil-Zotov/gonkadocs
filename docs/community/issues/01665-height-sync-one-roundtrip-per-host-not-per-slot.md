---
title: "#1665 — Height-sync: one roundtrip per host, not per slot"
source: https://github.com/gonka-ai/gonka/issues/1665
issue_number: 1665
synced_at: 2026-09-02T04:44:15Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Height-sync: one roundtrip per host, not per slot
    <span class="issues-number">#1665</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/a-kuprin">@a-kuprin</a> opened 2026-08-28 12:01 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-08-28 12:01 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #a2eeef; color: #24292f; border-color: #a2eeef;">enhancement</span></div>
</div>

<div class="issues-content" markdown="1">
# Height-sync: one roundtrip per host, not per slot

**Labels:** `enhancement`, `devshard`, `height-sync`

## Summary

Idle height-sync still fans out **one signed `/chat/completions` roundtrip per escrow slot**. A host that holds several slots in the same escrow is therefore pinged once per slot, even though those slots share one process, one oracle, and one signer.

That extra traffic does not add independent height evidence. Floor raises already require **distinct signers**; echoing the same host across its slots is the case the floor was written to ignore.

Heartbeats and height-sync should be scheduled and transported as **one roundtrip per unique host**, not as a `slots_num`-wide height-sync span.

## Motivation

On `devshard-0.2.15-v5` (and current gateway):

1. `Heartbeat.SpanTxs` emits one `MsgHeartbeat` per slot.
2. `Session.dispatchHeartbeatSpan` unicasts each composed diff with `HostClient.Send` — a full signed POST to `/sessions/{escrow}/chat/completions`, then an SSE receipt.
3. `NewHTTPSession` already caches one `HTTPClient` per `ValidatorAddress`, so the logical client is per host, but the **span still sends once per slot**.
4. Ack flush is another round of slot-indexed `Send`s (`flushHeartbeatAckRounds`).
5. Cadence is `DefaultHeartbeatInterval` (3s) per idle escrow. Busy escrows skip heartbeats because inference stamps discharge the turn.

Same-host multi-slot is the normal weighted-participant case, not an edge case. Each extra slot today buys another HTTP RTT and another Diff nonce, not another independent height claim.

A later idle gRPC connection (one conn per host, reconnect on drop) makes this worse to leave unfixed: the expensive part would no longer be dialing, it would be **N application RPCs and N log applies** for one physical peer.

## Impact

- **Affected:** `devshard/heightsync` (span, turn, quorum), `devshard/user` (heartbeat dispatch / ack flush), `devshard/transport` (one RPC per host), gateway session wiring, host admission of coalesced payloads.
- **Who:** gateway operators (idle-escrow chatter), hosts (duplicate apply + 100 RPS/sender bucket), protocol reviewers (quorum vs slot count).
- **Metrics expected to improve:**
  - Heartbeat POSTs / RPCs per idle escrow: `O(slots_num)` → `O(unique_hosts)`.
  - Time to one honest host ack: one host RTT, not “span dispatch + ack flush” scaled by slots on that host.
  - Honest-ack lateness: today’s span is dispatched slot-by-slot while `HReq` stays at the span start (`height-sync-review-findings.md`); collapsing same-host work into one RTT shortens that tail.
  - Pressure on host `DefaultRateLimitConfig` (100 RPS/sender, burst 200), which currently counts heartbeats as ordinary chat POSTs.

Example (one idle escrow, interval 3s):

| Host slots in escrow | Heartbeat + ack RPCs to that host / turn today | After per-host roundtrip |
|---|---|---|
| 1 | ~2 | ~2 |
| 4 | ~5–8 | **1** (+ acks for its slots in the same RPC) |
| 8 | ~9–16 | **1** |

Across `E` idle escrows that all include the same heavy host, waste is `E × (slots_on_host − 1)` RPCs every 3s.

## Detailed description

### What a “height-sync roundtrip” is today

A turnover is “Q distinct slot claims landed within `Interval`” (`Heartbeat`, `TurnTracker.countingAcks`, `QuorumForRoster(slots_num)`). To produce those claims the user:

1. Opens a turn and composes a **span of `slots_num` diffs**, consecutive nonces, one heartbeat per slot.
2. Sends them concurrently, **one `Send` per `hostIdx`**.
3. Flushes ack-carrying diffs until the turn is no longer open or the round bound (`len(group)+1`) is hit.

That whole construction is the height-sync roundtrip. Its width is **roster slots**, not unique peers. Two slots on one validator are two roundtrips and two (or more) log entries signed by the same key.

### Why same-host slot heartbeats are not useful

- **Same signer.** Floor already treats “raise by more than `W_conf`” as needing `Q` **distinct signers** (`heightsync/floor.go` / review D2). Slot-id is not a second identity.
- **Same oracle / same process.** N acks from one `devshardd` are N copies of one tip, not N independent observations.
- **Liveness.** `T_idle` and close-ready care that *the host* is silent, not that slot 3 of 8 on that host missed a ping.
- **Transport.** Client cache is already per validator. The extra `Send`s only multiply HTTP (or future gRPC) calls and SM apply.

Inference, accounting, and validation **remain per slot**. This issue is only the height-sync / heartbeat control plane.

### How to confirm

- Idle escrow, group with repeated `ValidatorAddress`: count `POST .../chat/completions` (or `heartbeat span send failed` / `heartbeat span dispatched` with `span=N`) vs unique hosts.
- Metrics: `devshard_gateway_heightsync_cadence_events_total{event="heartbeat_opened"}` vs actual outbound RPCs per `baseURL`.
- Compare turn time-to-quorum when the Q-th independent signer is one host with many slots vs many hosts with one slot. Today the former still pays the span.

## Expected outcome

- **One host RTT** is enough to deliver that host’s height-sync work for the turn (heartbeat + that host’s acks / slot-local txs).
- Cadence and turnover **count unique hosts (signers)**, not extra slots of the same host.
- Log may still be slot-addressed (nonces, `slot_id`, accounting) if that stays simpler; the **wire and the wait** must not be.
- Idle chatter scales with unique hosts in the escrow, independent of weight-as-slots.
- Backward compatible on the log if coalescing is transport-only (same txs, one RPC). Protocol change (one claim per signer) is a versioned follow-up if we drop redundant Diff entries.

Not in scope for the first cut: migrating gateway↔host from HTTP to gRPC. Per-host coalescing is valuable on HTTP and is the right RPC shape if/when there is one idle gRPC connection per host.

## Proposed approach

### Phase 1 — Transport coalescing (no log-plane change)

Keep `MsgHeartbeat` / `MsgHeightAck` per slot in Diff so L0–L4, `sync_vector`, and `peer_seen` stay as they are.

Change dispatch:

- Group `composedDiff`s by unique host (`ValidatorAddress` / `baseURL`).
- One `Send` (or future gRPC RPC) per host per turn, body carrying **all diffs for that host’s slots** (already the catch-up list in `HostRequest.Diffs`; stop splitting them into N POSTs).
- Ack flush: same grouping — do not walk the roster slot-by-slot when several `hostIdx` share a client.
- Heartbeat `Send` already uses query timeout when `Payload == nil`; coalesced path should keep that.

This alone cuts wire RTTs to `O(unique_hosts)` without a spec bump.

### Phase 2 — Cadence keyed by host, not slot span

- `SpanTxs` / turn width: emit **one heartbeat per unique signer**, or one heartbeat that the host applies to all of its slots locally.
- `countingAcks` / `Heartbeat` quorum: `QuorumForRoster(unique_hosts)` (or equivalent distinct-signer set), not `QuorumForRoster(slots_num)` when those counts differ.
- Align with floor: extra slots of one signer never inflate Q and never shorten the wait for “enough independent tips”.
- Schedule wait: **host RTT + ack**, not `slots_num` sequential/parallel slot RTTs. `D_ack` / `TurnTimeout` stay schedule-derived; they should not have to cover a same-host slot fan-out.

Phase 2 needs an explicit log-plane / version note if wire messages or nonce span shape change.

### Alternatives

| Alternative | Why not (as the whole fix) |
|---|---|
| Keep per-slot unicasts; only switch to idle gRPC | Multiplexed conn makes each RPC cheaper; still N applies, N receipts, N-wide span for one peer. |
| Raise host 100 RPS cap | Masks waste; does not fix latency or false independence. |
| Heartbeat only slot 0 of each host | Underspecified for `sync_vector` / `peer_seen` / per-slot ack L3 unless hosts expand the claim locally. Phase 1 coalescing is safer first. |

### Rollout

- Feature-flag or protocol version if Phase 2 changes Diff shape.
- Phase 1 can ship behind a gateway/host flag (`HEIGHT_SYNC_COALESCE_PER_HOST`) and be the default once citest covers repeated-validator groups.
- Hosts must accept a catch-up batch that advances several of their slots in one request (likely already true via `ApplyCatchUpDiffs`); pin that with a test.

## Test plan

- [ ] Unit: `SpanTxs` / dispatch grouping — two slots, one `ValidatorAddress` → one outbound `Send` (Phase 1).
- [ ] Unit: turn quorum — four slots, two signers → Q from 2 signers, not 4 slots (Phase 2).
- [ ] Unit: floor unchanged — one host acking all its slots still counts as one signer.
- [ ] `user/heightsync_test.go`: existing `slots_num` span tests updated or split (log still has per-slot txs if Phase 1 only).
- [ ] Citest: weighted group (repeat host URL) idle for `> 2 * Interval`; assert outbound chat POSTs to that URL ≈ 1 per interval, not `slots_on_host`.
- [ ] Mixed group: unique hosts still get one RPC each; a dead unique host still fails turnover the same way.
- [ ] Inference path unchanged: per-slot assignment, validation, accounting.

## External feedback

- (fill in Discord / reviewers)

</div>

---

> 🔄 **Auto-synced** from [Issue #1665](https://github.com/gonka-ai/gonka/issues/1665) every hour.
