---
title: "#2173 — Gateway admin API silently ignores EOF failure threshold updates"
source: https://github.com/gonka-ai/gonka/issues/2173
issue_number: 2173
synced_at: 2026-11-27T10:59:54Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Gateway admin API silently ignores EOF failure threshold updates
    <span class="issues-number">#2173</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/ilyar">@ilyar</a> opened 2026-10-29 16:14 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-11-27 07:36 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Gateway settings expose `participant_throttle.eof_transport_failure_threshold` on GET, but POST silently leaves it unchanged

Observed with `ghcr.io/gonka-ai/devshard-gateway:mainnet-v0.2.16-v6.0.0-rc1`, inspected against [source revision](https://github.com/gonka-ai/gonka/tree/6a41bc3429d1029dc787a3bc04f1a14f201be006)

## Reproduction

1. Read `/v1/admin/settings` using an admin key and preserve the original settings
2. POST settings with `participant_throttle.empty_stream_threshold=2147483647` and `participant_throttle.eof_transport_failure_threshold=2147483647`
3. Read settings again

The first field becomes `2147483647`, the EOF field remains `3`, while the other requested quarantine durations are applied

## Impact and source

[The limiter](https://github.com/gonka-ai/gonka/blob/6a41bc3429d1029dc787a3bc04f1a14f201be006/devshard/cmd/devshardctl/participant_limiter.go) takes the smaller of these two thresholds, so increasing the exposed empty-stream threshold alone still leaves the effective failure threshold at `3`

[The settings handler](https://github.com/gonka-ai/gonka/blob/6a41bc3429d1029dc787a3bc04f1a14f201be006/devshard/cmd/devshardctl/gateway.go) omits the EOF field from `adminParticipantThrottleRequest` and its update path, although the stored settings include it

Expected: accept and validate this field with persistence and effective runtime readback, or explicitly reject the unsupported update rather than silently accepting a partial change

Acceptance should cover POST and GET round-trip, persistence, effective limiter threshold, invalid values and preservation of unrelated settings

[Issue 1506](https://github.com/gonka-ai/gonka/issues/1506) discusses quarantine recovery behaviour, this report concerns the separate admin settings update contract

</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/qdanik">@qdanik</a></span>
    <span class="issues-meta-item">commented 2026-11-27 07:36 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@ilyar devshardctl (removed in #2339) only issue.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2173](https://github.com/gonka-ai/gonka/issues/2173) every hour.
