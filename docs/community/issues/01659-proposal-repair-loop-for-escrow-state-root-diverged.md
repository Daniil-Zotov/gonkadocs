---
title: "#1659 — Proposal: Repair loop for `escrow_state_root_diverged`"
source: https://github.com/gonka-ai/gonka/issues/1659
issue_number: 1659
synced_at: 2026-09-03T00:21:23Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Proposal: Repair loop for `escrow_state_root_diverged`
    <span class="issues-number">#1659</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/a-kuprin">@a-kuprin</a> opened 2026-08-27 13:23 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-08-27 13:23 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #a2eeef; color: #24292f; border-color: #a2eeef;">enhancement</span></div>
</div>

<div class="issues-content" markdown="1">
# Proposal: Repair loop for `escrow_state_root_diverged`

**Status:** Draft / proposal  
**Related:** [PR #1581 accounting review](../pr-1581-accounting-review.md) §1 (ghosts) and §3 (capability / state-root block)  
**Scope:** After the gateway withholds a participant for escrow state-root divergence, periodically try to restore that host onto the canonical diff chain and **clear the flag only when the host has proven it**.

This is a design note only; it does not change code by itself.

---

## Problem today

On a failed attempt, if the error looks like a post-state mismatch (`apply diff nonce` + `post_state_root does not match computed state root`, or gateway `ErrStateHashMismatch` wrapped the same way), `maybeRecordEscrowStateDivergence` writes:

```
stateBlockedHosts[participant] = "escrow_state_root_diverged"
```

That map is **append-only** for the escrow runtime. There is no TTL and no clear on later success.

While the flag is set:

1. **User traffic is withheld** — `capabilityBlocked` → picker skips `/chat/completions`. That part is correct: a forked SM must not apply the next signed nonce.
2. **The picker still consumes a nonce** — the skip is `ghostCapability`. With ghost accounting on, that becomes a refused-timeout round and possible `Missed`.
3. **The nonce that actually diverged may skip `HandleTimeout`** — the failed-inflight loop bails when the host is already state-blocked.
4. **Catch-up is never invoked for this reason** — `Session.sendCatchUp` / `SyncHosts` already exist (warmup and finalize use them). The block does not start them, and a later 200 on chat is not treated as recovery (see `TestRunInference_StateRootDivergenceBlocksParticipantForEscrow`).

So a one-shot mismatch, a catch-up race, a host restart that could be taught again, or a body that merely *contains* those substrings, blackholes the participant until the escrow process dies — and may bill them for being skipped.

Catch-up of “diffs we think you missed” is **not** enough by itself for a true fork. `diffsForHost` starts after `hostSyncNonce`. If the host already applied nonce *N* with a **different** root, sending *N+1* fails the same way. Healing a real fork needs empty local session + replay from genesis (host restart today; no `DeleteSession` RPC). Healing **lag / false trip / restart** only needs catch-up + a root check.

---

## Desired behavior

Keep the safety invariant:

- Do **not** send live `/chat/completions` to a participant while the flag is set.
- Do **not** clear the flag because the next chat returned 200.

Add a gateway-owned repair loop:

1. When the flag is first set, start periodic restore for **that host only**.
2. Each tick: teach canonical diffs (admission-bypassing catch-up, same as warmup/finalize), then **verify** the host signs the gateway’s post-state root at the current nonce.
3. On verify success: delete the map entry, log unblock, host re-enters the rota.
4. On verify failure: leave the flag, back off, retry until the escrow stops.
5. While repair is in progress: do not burn accountable ghosts for this participant (gateway chose to withhold; that is not a host 503).

---

## Proposed shape

### 1. Trigger

On the first insert in `maybeRecordEscrowStateDivergence` (today’s `!existed` log path), start one repair worker for `(escrow, participantKey, hostIdx)`.

Dedup: if the flag is already set, do not start a second worker. Bind the worker to `runtime.stopped` (same cancel as warmup).

### 2. Loop

Per blocked participant, not `SyncHosts` over the whole group (do not stall healthy hosts).

Suggested cadence:

- First attempt immediately (or after a short delay so the failed request’s catch-up/gossip can finish).
- Then interval with backoff, e.g. 15s → 30s → 1m → 5m, jittered.
- Stop on: flag cleared, escrow retiring/stopped, phase no longer active.

Use `getFinalizeClients()` so the participant limiter does not refuse catch-up (same reason warmup bypasses admission).

### 3. Each attempt

**A. Teach**

`sendCatchUpWith(ctx, hostIdx, finalizeClient)`.

- Host dead / timeout: log, retry later. Do not clear.
- Catch-up `processResponse` still reports state-hash / post-state mismatch: host is still forked. Do not clear. Optionally reset gateway `hostSyncNonce` for that index only if the host later reports `session not found` (empty SM after restart) so the next tick sends the full chain from 0.
- `session not found`: existing create/catch-up path should run; this is the cheap recovery for a restarted host.

**B. Verify (the only clear signal)**

Do not treat catch-up HTTP 200 as restored.

Require a signature over the **gateway** canonical root at `session.Nonce()` (or the nonce catch-up claimed to reach):

- `SignatureFetcher.GetSignatures(nonce)` (existing GET `/signatures?nonce=N` path), then `verifyStateSignature` against expected slot address and gateway `post_state_root`.
- If the client has no fetcher: a catch-up response whose `StateSig` verifies the same preimage is enough.

Host nonce behind the gateway → not restored. Host nonce equal with a sig over a **different** root → still forked.

**C. Clear**

If verify succeeds:

```
delete(stateBlockedHosts, participantKey)
log escrow_participant_state_unblocked
```

Next picker pass may send user traffic again. No special “first request after repair” nonce.

### 4. True fork (no wipe API today)

Phase 1 of this proposal does **not** add a host `reset-session` RPC. A host that applied a conflicting nonce cannot be healed by later diffs.

Until a wipe exists, the loop still helps:

- Host **restarts** (empty store) → `session not found` → full catch-up → verify → clear.
- Host was only **behind** or the trip was a **false string match** → catch-up + verify → clear.
- Host stays forked and alive → flag remains; user traffic stays off. That is intended.

Phase 2 (optional later): host-side drop of this escrow’s SM + `CreateSession`, then gateway catch-up from 0. Do not reset in place on a live SM.

### 5. Picker / ghosts while blocked

Today `capabilityBlocked` is only this flag, and it is `ghostCapability` (accountable).

Change:

| Window | User `/chat/completions` | Nonce consume | Ghost accounting |
| --- | --- | --- | --- |
| Repair in progress (flag set, worker alive) | no | **no** (treat like exclude / not in rota) | no |
| Repair gave up (optional deadline) **or** flag still set and worker stopped | no | yes, `ghostCapability` | yes (host never came back) |
| Flag cleared | yes | normal | n/a |

Rationale: charging `Missed` on every slot while the gateway is actively teaching the host is the same distortion ghosts were meant to fix, in reverse. After a bounded give-up, charging again is fair so a permanently forked host does not finish the epoch cleaner than one that served.

Companion (small, can ship with this): **do not skip `HandleTimeout` on the nonce that tripped the mismatch.** That failure is a real dispatch; skipping it hides the original fault. The skip can stay for *later* inflights once the flag is set, or go away entirely if those inflights are no longer created (no nonce consume during repair).

### 6. Observability

Log stages (mirror `escrow_participant_state_blocked`):

- `escrow_participant_state_repair_started`
- `escrow_participant_state_repair_attempt` (catch-up result, verify ok/fail)
- `escrow_participant_state_unblocked`
- `escrow_participant_state_repair_gave_up` (if a deadline exists)

Metrics (low cardinality): repair attempts, currently blocked participants, time-to-unblock, give-ups. Per `(escrow, participant)` is enough; do not add request_id.

---

## What this is not

- **Not** “retry the user request against the blocked host and clear on 200.” The existing test must keep failing that path until verify succeeds.
- **Not** re-introducing tool/context/version as routing vetoes.
- **Not** changing how `post_state_root` is computed or signed.
- **Not** (phase 1) a host wipe RPC. Call that out if catch-up+verify is insufficient in production.
- Follow-up, not required here: classify divergence with `errors.Is(types.ErrPostStateRootMismatch)` instead of two substrings, so a crafted body is harder to trip.

---

## Acceptance sketch

- After a recorded `escrow_state_root_diverged`, the gateway starts a per-host repair loop cancelled with the escrow runtime.
- A host that is only behind (or that restarted empty) is taught via finalize-client catch-up, verifies a signature over the gateway root, **loses the flag**, and is eligible for the next user send.
- A host that still computes a different root keeps the flag; no user `/chat/completions`; the existing “even if it would answer now, do not send” test still holds.
- A 200 on chat without a verified root does **not** clear the flag.
- While repair is running, that participant does not consume accountable ghost nonces.
- Repair does not `SyncHosts` the whole group; other participants keep serving.
- Stopping/retiring the escrow stops the worker; no leak of goroutines across rotation.

</div>

---

> 🔄 **Auto-synced** from [Issue #1659](https://github.com/gonka-ai/gonka/issues/1659) every hour.
