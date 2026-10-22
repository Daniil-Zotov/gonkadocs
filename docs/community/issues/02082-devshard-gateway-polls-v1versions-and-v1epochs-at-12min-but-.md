---
title: "#2082 — devshard gateway polls /v1/versions and /v1/epochs/* at 12/min, but default proxy api_zone allows 10/min → permanent 503s after ~5 h"
source: https://github.com/gonka-ai/gonka/issues/2082
issue_number: 2082
synced_at: 2026-10-22T19:16:44Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    devshard gateway polls /v1/versions and /v1/epochs/* at 12/min, but default proxy api_zone allows 10/min → permanent 503s after ~5 h
    <span class="issues-number">#2082</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/maria-mitina">@maria-mitina</a> opened 2026-10-22 07:31 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-10-22 08:02 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
**Summary**

`devshardctl gateway` polls public API endpoints on a hardcoded 5 s ticker. The default nginx proxy puts those endpoints in `api_zone` (10 r/min per client IP, burst 600, `nodelay`). 12 req/min > 10 req/min, so the burst bucket drains in ~5 h and from then on roughly 1 in 6 polls is rejected with 503 — indefinitely. Every gateway in the network does this to every miner it considers a candidate, and the gateway's own `PublicAPI` node takes the heaviest load.

**Where the 5 s comes from**

- `devshard/cmd/devshardctl/phase_gate.go`: `defaultChainPhasePollInterval = 5 * time.Second`. `ChainPhaseGate.run()` polls `PublicAPI + /v1/epochs/latest` and `/v1/epochs/current/participants` on that interval.
- The same interval is reused for `VersionsCache` (`g.versions.Run(ctx, g.pollInterval)`), which fetches `inference_url + /v1/versions` from **every candidate miner** every 5 s, TTL = 3 × interval (fail-closed: a stale/failed fetch marks all of that miner's nodes as not validation-capable).
- `gateway.go` always calls `NewChainPhaseGate(settings.PublicAPI, 0)`, so there is no config or env override.

**Where the 10/min comes from**

- `proxy/entrypoint.sh`: `GONKA_API_RATE_LIMIT_RPS` default 10, `GONKA_API_RATE_UNIT` default `m`, `GONKA_API_BURST` 600 → `limit_req_zone … zone=api_zone rate=10r/m`, applied by the catch-all `location /v1/` and `location /api/v1/`.
- `GONKA_API_EXEMPT_ROUTES` default is `chat inference poc/proofs subnet devshard`; `versions` and `epochs` are not in it, so they fall into `api_zone`.

**Observed (testnet1, 15-min window on one node)**

- 1489 requests, 342 × 503, all from devshard gateways:
  - gateway using this node as `PublicAPI`: `/v1/versions` 12/min + `/v1/epochs/latest` 12/min + participants ~5/min → 282 × 503 (65% of its requests)
  - two other gateways: `/v1/versions` 12/min each → ~30 × 503 each
- Error log: `limiting requests, excess: … by zone "api_zone"`.
- Consequences: `VersionsCache` entries expire (TTL 15 s) → nodes intermittently treated as not validation-capable; `ChainPhaseGate` misses phase polls; the same per-IP bucket is shared with any other client behind that IP (e.g. explorer/dashboard), which then also sees 503s.

**Workaround applied on testnet1**

`GONKA_API_EXEMPT_ROUTES=chat inference poc/proofs subnet devshard versions epochs` on the proxy → 0 × 503 afterwards. Requires every operator to know about it.

**Proposed fix**

**Gateway**: make the poll interval configurable (`DEVSHARD_GATEWAY_CHAIN_PHASE_POLL_INTERVAL`, same pattern as `DEVSHARD_GATEWAY_HOST_PING_INTERVAL` in `hostping.go`) and give `/v1/versions` its own, slower interval — the `poc_validation_inference` flag only changes on upgrades, so 30–60 s is plenty. Default must land under 10/min (≥ 6 s), ideally well under.


</div>

---

> 🔄 **Auto-synced** from [Issue #2082](https://github.com/gonka-ai/gonka/issues/2082) every hour.
