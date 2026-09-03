---
title: "#1542 — devshardctl: ParseProtocolVersion rejects route v4 (noisy rotation fallback log)"
source: https://github.com/gonka-ai/gonka/issues/1542
issue_number: 1542
synced_at: 2026-09-03T21:45:24Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    devshardctl: ParseProtocolVersion rejects route v4 (noisy rotation fallback log)
    <span class="issues-number">#1542</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/maria-mitina">@maria-mitina</a> opened 2026-08-04 15:58 UTC</span>
    <span class="issues-meta-item">5 comments</span>
    <span class="issues-meta-item">Updated 2026-08-30 19:17 UTC</span>
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

## 💬 Comments (5)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/w3lld1">@w3lld1</a></span>
    <span class="issues-meta-item">commented 2026-08-05 17:32 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>I'd like to take this. I plan to add <code>v4</code> support to <code>ParseProtocolVersion</code>, extend the focused unit coverage, and verify the escrow rotation parsing path. I can submit the PR within a day. Could you confirm that adding <code>ProtocolV4</code> is preferred over keeping route majors decoupled, and assign me?</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/bonujel">@bonujel</a></span>
    <span class="issues-meta-item">commented 2026-08-20 01:50 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p><code>ParseProtocolVersion</code> has one caller — <code>escrow_rotator.go:408</code>, the path in the report. Grepping for anything that reads the result turns up nothing:</p>
<pre><code>ParseProtocolVersion    -&gt; devshard/cmd/devshardctl/escrow_rotator.go:408  (only non-test caller)
ProtocolV1/V2/V3        -&gt; no readers outside devshard/types/domain.go and its tests
types.ProtocolVersion   -&gt; no consumers
</code></pre>
<p>So the parsed value gets stamped into the gateway DB and is never read back for a decision, which matches the note in the description that settlement goes through <code>StateRootAndProtocolVersion</code> from the session SM.</p>
<p>That points at option 2. Nothing downstream needs the value to be a known enum member, so an unknown route major isn't really an error condition — it's a name the enum hasn't been told about.</p>
<p>Option 1 also has a shelf life: v5 is already in flight (#1584, #1615). Adding <code>ProtocolV4</code> brings the same log back the day the route prefix moves to <code>/devshard/v5</code>.</p>
<p>@w3lld1 asked the same question on Aug 5 and hasn't had an answer — this is the evidence for it either way. If option 2 is the call, I can put up the patch.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/a-kuprin">@a-kuprin</a></span>
    <span class="issues-meta-item">commented 2026-08-28 14:08 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>I think we can close it with:
<a href="https://github.com/gonka-ai/gonka/pull/1662">[ak/fix-1542-parse-protocol-autoparse](https://github.com/gonka-ai/gonka/tree/ak/fix-1542-parse-protocol-autoparse)</a></p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/wrvnnull">@wrvnnull</a></span>
    <span class="issues-meta-item">commented 2026-08-28 17:19 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>I'd like to take this.\n\nPlan:\n- add ProtocolV4 to ParseProtocolVersion\n- extend unit test to cover v4\n- keep current v1/v2/v3 behavior unchanged\n\nETA: immediate PR.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/wrvnnull">@wrvnnull</a></span>
    <span class="issues-meta-item">commented 2026-08-30 10:43 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Tracked in #1630 (gateway v4). #1670 was a duplicate and is closed. PR #1678 covers the API-side malformed JSON fix for <code>/v1/participants</code>.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1542](https://github.com/gonka-ai/gonka/issues/1542) every hour.
