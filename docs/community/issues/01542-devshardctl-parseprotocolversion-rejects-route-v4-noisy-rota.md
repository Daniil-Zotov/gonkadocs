---
title: "#1542 — devshardctl: ParseProtocolVersion rejects route v4 (noisy rotation fallback log)"
source: https://github.com/gonka-ai/gonka/issues/1542
issue_number: 1542
synced_at: 2026-08-05T16:55:15Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    devshardctl: ParseProtocolVersion rejects route v4 (noisy rotation fallback log)
    <span class="issues-number">#1542</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/maria-mitina">@maria-mitina</a> opened 2026-08-04 15:58 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-08-04 15:58 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #a2eeef; color: #24292f; border-color: #a2eeef;">enhancement</span> <span class="issues-label" style="background-color: #7057ff; color: #ffffff; border-color: #7057ff;">good first issue</span> <span class="issues-label" style="background-color: #95b500; color: #24292f; border-color: #95b500;">Priority: Low</span> <span class="issues-label" style="background-color: #aaaaaa; color: #24292f; border-color: #aaaaaa;">devshards</span></div>
</div>

<div class="issues-content" markdown="1">
## Summary

When the gateway serves `DEVSHARD_ROUTE_PREFIX=/devshard/v4`, escrow autorotation logs a fallback on every create:

```
escrow_rotation_protocol_version_fallback route_prefix="/devshard/v4" version="v4" reason=unparseable_protocol error=unknown protocol version "v4"
```

This is **cosmetic**: rotation create/settle still succeed. The empty local `protocol_version` stamp is not used for settlement (settlement uses `StateRootAndProtocolVersion` from the session SM, e.g. `v4`).

It clutters testnet/gateway logs and makes health checks harder to read.

## Root cause

- `rotationEscrowProtocolVersion()` in `devshard/cmd/devshardctl/escrow_rotator.go` derives a registry protocol stamp from the route version segment.
- `ParseProtocolVersion` in `devshard/types/domain.go` only accepts `v1` / `v2` / `v3`.
- `"v4"` hits the default branch → log + return `""`.

## Observed impact

- Does **not** fail escrow rotation (fallback log is followed by `escrow_rotation_created`).
- Does **not** affect settlement / state roots.
- Only leaves gateway DB `protocol_version` empty instead of a parsed enum.

## Suggested fix (small)

Either:

1. Add `ProtocolV4` / `"v4"` to `ParseProtocolVersion` (and tests), if v4 should be a real protocol stamp; or
2. Stop treating unknown route majors as an error-level fallback (silent empty stamp / explicit config), if route name and protocol enum are intentionally decoupled.

Also worth aligning compose healthcheck (`curl` vs image `wget`) separately — not required for this issue.

## Test plan

- [ ] Unit: `ParseProtocolVersion("v4")` (or chosen behavior) covered
- [ ] With `DEVSHARD_ROUTE_PREFIX=/devshard/v4`, autorotation creates escrows without `unparseable_protocol` spam
- [ ] Settlement still carries `state_root_and_protocol_version=v4` as today
</div>

---

> 🔄 **Auto-synced** from [Issue #1542](https://github.com/gonka-ai/gonka/issues/1542) every hour.
