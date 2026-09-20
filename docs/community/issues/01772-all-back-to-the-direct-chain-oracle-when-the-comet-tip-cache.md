---
title: "#1772 — all back to the direct chain oracle when the Comet tip cache becomes stale"
source: https://github.com/gonka-ai/gonka/issues/1772
issue_number: 1772
synced_at: 2026-09-20T18:53:13Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    all back to the direct chain oracle when the Comet tip cache becomes stale
    <span class="issues-number">#1772</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/anatoly-kuz-mntn">@anatoly-kuz-mntn</a> opened 2026-09-15 02:01 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-09-15 02:01 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Description

After the Comet tip cache receives its first header, `Cache.Latest()` continues returning that header regardless of its age.

The outer failover oracle treats this as a successful fresh read, does not query the direct chain oracle, and updates `lastOK = true`. As a result, `Stale()` reports false even though the cached tip has stopped advancing.

Hosts can therefore continue reporting a frozen height as `SYNCED` during a Comet WebSocket outage.

## Affected code

- [`Latest` accepts any cached header and skips the direct fallback](https://github.com/gonka-ai/gonka/blob/dfa3d30b44da938135f23d82b8d4a8291b2df7ca/devshard/chainoracle/blocks/failover/failover.go#L42-L66)
- [`Oracle.Stale` uses the successful frozen read as `lastOK`](https://github.com/gonka-ai/gonka/blob/dfa3d30b44da938135f23d82b8d4a8291b2df7ca/devshard/chainoracle/blocks/failover/failover.go#L157-L172)
- [`Cache.Latest` has no freshness check](https://github.com/gonka-ai/gonka/blob/dfa3d30b44da938135f23d82b8d4a8291b2df7ca/devshard/chainoracle/blocks/tipcache/cache.go#L99-L110)
- [`Cache.Stale` already knows when the last observation is too old](https://github.com/gonka-ai/gonka/blob/dfa3d30b44da938135f23d82b8d4a8291b2df7ca/devshard/chainoracle/blocks/tipcache/cache.go#L163-L174)

## Expected behavior

Once the cached tip exceeds its staleness threshold, `Latest()` should query the configured direct chain oracle. A frozen cached header must not reset the outer oracle’s stale state.

## Acceptance criteria

- A fresh cached tip remains preferred.
- A stale cached tip triggers a direct-chain lookup.
- The fresher direct-chain header is returned when available.
- `Stale()` remains true when neither source provides a fresh header.
- Add a regression test using a populated cache that stops receiving new blocks.
</div>

---

> 🔄 **Auto-synced** from [Issue #1772](https://github.com/gonka-ai/gonka/issues/1772) every hour.
