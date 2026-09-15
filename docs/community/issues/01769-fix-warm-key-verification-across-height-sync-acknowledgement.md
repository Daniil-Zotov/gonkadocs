---
title: "#1769 — Fix warm-key verification across height-sync acknowledgement and repair paths"
source: https://github.com/gonka-ai/gonka/issues/1769
issue_number: 1769
synced_at: 2026-09-15T21:28:33Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Fix warm-key verification across height-sync acknowledgement and repair paths
    <span class="issues-number">#1769</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/anatoly-kuz-mntn">@anatoly-kuz-mntn</a> opened 2026-09-15 01:58 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-09-15 01:58 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Description

Height-sync messages are signed with the host process signer, which is normally a warm key for joined participants. Several verification paths compare the recovered signer only with the cold validator address.

Consequently, valid height-sync acknowledgements and repair messages from joined hosts are rejected. Genesis hosts are unaffected because their process signer and validator account use the same key.

This issue covers `heightsync-correctness-1`.

## Affected code

- [`checkL2` verifies acknowledgements against `SlotKeys`](https://github.com/gonka-ai/gonka/blob/dfa3d30b44da938135f23d82b8d4a8291b2df7ca/devshard/heightsync/logplane.go#L240-L257)
- [`SlotKeys` contains validator addresses](https://github.com/gonka-ai/gonka/blob/dfa3d30b44da938135f23d82b8d4a8291b2df7ca/devshard/state/heightsync.go#L162-L171)
- [Hosts sign acknowledgements with the process signer](https://github.com/gonka-ai/gonka/blob/dfa3d30b44da938135f23d82b8d4a8291b2df7ca/devshard/host/heightsync.go#L58-L68)
- [Repair requests are verified against the cold validator address](https://github.com/gonka-ai/gonka/blob/dfa3d30b44da938135f23d82b8d4a8291b2df7ca/devshard/transport/server_repair.go#L48-L57)
- [Repair responses are verified against the cold validator address](https://github.com/gonka-ai/gonka/blob/dfa3d30b44da938135f23d82b8d4a8291b2df7ca/devshard/transport/server_repair.go#L107-L115)
- [Courtesy acknowledgements have the same cold-key-only check](https://github.com/gonka-ai/gonka/blob/dfa3d30b44da938135f23d82b8d4a8291b2df7ca/devshard/host/repair.go#L186-L207)

## Expected behavior

Height-sync signatures should be accepted when they belong either to the validator’s cold key or to an authorized warm key for the corresponding slot.

## Acceptance criteria

- Warm-key-signed `MsgHeightAck` passes L2 validation.
- Warm-key-signed repair requests and responses are accepted.
- Courtesy acknowledgements support authorized warm keys.
- Unauthorized warm keys remain rejected.
- Cold-key signing remains supported.
</div>

---

> 🔄 **Auto-synced** from [Issue #1769](https://github.com/gonka-ai/gonka/issues/1769) every hour.
