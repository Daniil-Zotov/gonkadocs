---
title: "#1770 — Make height-sync heartbeat and cadence safe against DoS, partial persistence, and nonce exhaustion"
source: https://github.com/gonka-ai/gonka/issues/1770
issue_number: 1770
synced_at: 2026-09-15T07:51:46Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Make height-sync heartbeat and cadence safe against DoS, partial persistence, and nonce exhaustion
    <span class="issues-number">#1770</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/anatoly-kuz-mntn">@anatoly-kuz-mntn</a> opened 2026-09-15 01:58 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-09-15 01:59 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Description

The heartbeat/cadence implementation contains three related availability and resource-consumption problems.

## Problem 1: cadence arithmetic can loop forever

`ComputeCadenceSwallow` iterates through periodic windows using unsigned multiplication. With a sufficiently large `AnchorK`, `i * anchorK` wraps and the termination condition may never be reached.

Affected code:

- [`ComputeCadenceSwallow`](https://github.com/gonka-ai/gonka/blob/dfa3d30b44da938135f23d82b8d4a8291b2df7ca/devshard/heightsync/cadence.go#L6-L24)
- [State-machine call site](https://github.com/gonka-ai/gonka/blob/dfa3d30b44da938135f23d82b8d4a8291b2df7ca/devshard/state/heightsync.go#L65-L98)

The relevant window should be calculated directly using division and checked arithmetic.

## Problem 2: heartbeat spans can be partially persisted

A span reads the floor once and gives every heartbeat the same height. However, the first span diff may also drain pending host-signed transactions and raise the floor.

A later heartbeat can then fail L0 after the earlier diff has already been persisted and committed. `composeHeartbeatSpan` returns an error and does not dispatch the persisted prefix.

Affected code:

- [Single floor read and per-heartbeat composition loop](https://github.com/gonka-ai/gonka/blob/dfa3d30b44da938135f23d82b8d4a8291b2df7ca/devshard/user/heartbeat.go#L167-L238)
- [Pending transactions are included before heartbeat transactions](https://github.com/gonka-ai/gonka/blob/dfa3d30b44da938135f23d82b8d4a8291b2df7ca/devshard/user/session.go#L797-L808)
- [Each diff is persisted and committed immediately](https://github.com/gonka-ai/gonka/blob/dfa3d30b44da938135f23d82b8d4a8291b2df7ca/devshard/user/session.go#L810-L842)

## Problem 3: quiet escrows rapidly consume the nonce budget

For a group of 16 hosts, one quiet height-sync turn consumes approximately 17 nonces: 16 heartbeat diffs and at least one flush diff.

With the default configuration:

- Healthy acknowledgements: approximately 17 nonces every 6 seconds.
- Missing acknowledgements: approximately 17 nonces every 12 seconds.
- `max_nonce = 20,000` is exhausted in approximately 2–4 hours.
- `FeePerNonce` is charged for each applied nonce.

Affected code:

- [Quiet-session and timeout scheduling](https://github.com/gonka-ai/gonka/blob/dfa3d30b44da938135f23d82b8d4a8291b2df7ca/devshard/heightsync/heartbeat.go#L186-L195)
- [Heartbeat span and mandatory flush](https://github.com/gonka-ai/gonka/blob/dfa3d30b44da938135f23d82b8d4a8291b2df7ca/devshard/user/heartbeat.go#L206-L239)
- [Default six-second interval](https://github.com/gonka-ai/gonka/blob/dfa3d30b44da938135f23d82b8d4a8291b2df7ca/devshard/heightsync/params.go#L11-L24)
- [Default `max_nonce` and `FeePerNonce`](https://github.com/gonka-ai/gonka/blob/dfa3d30b44da938135f23d82b8d4a8291b2df7ca/inference-chain/x/inference/types/params.go#L99-L108)

## Acceptance criteria

- Cadence calculation terminates for every valid `uint64` input.
- Arithmetic overflow is explicitly prevented.
- Heartbeat composition cannot leave persisted but undispatched prefixes.
- Pending host raises cannot invalidate later heartbeats in the same span.
- Define an acceptable minimum lifetime for an idle escrow.
- Add a fake-clock test measuring nonce and fee consumption.
- Add a snapshot-based test starting near nonce `20,000` and verifying exhaustion behavior without waiting several hours.
</div>

---

> 🔄 **Auto-synced** from [Issue #1770](https://github.com/gonka-ai/gonka/issues/1770) every hour.
