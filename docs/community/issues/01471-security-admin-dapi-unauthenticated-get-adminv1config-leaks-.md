---
title: "#1471 — Security: Admin DAPI unauthenticated — GET /admin/v1/config leaks worker_private key"
source: https://github.com/gonka-ai/gonka/issues/1471
issue_number: 1471
synced_at: 2026-08-08T08:04:44Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Security: Admin DAPI unauthenticated — GET /admin/v1/config leaks worker_private key
    <span class="issues-number">#1471</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/Aphelios01-sdk">@Aphelios01-sdk</a> opened 2026-07-18 03:05 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-07-18 03:07 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

The decentralized-api **admin** server (`/admin/v1/*`) registers routes with **only** logging middleware — no authentication.  
`GET /admin/v1/config` returns the **unsanitized** live config as JSON, including `ml_node_key_config.worker_private`.

Other unauthenticated endpoints include `POST /admin/v1/tx/send`, claim recovery, bridge block inject, node enable/disable.

## Affected components

| Path | Role |
|------|------|
| `decentralized-api/internal/server/admin/server.go` | Routes + `getConfig` |
| `decentralized-api/apiconfig/config.go` | `WorkerPrivateKey` `json:"worker_private"` |
| `decentralized-api/main.go` | Listens `:%port` (all interfaces) |
| `deploy/join/docker-compose.yml` | Maps `127.0.0.1:9200:9200` (mitigation only at compose layer) |

## Source

```go
// getConfig returns the current configuration as JSON (unsanitized)
func (s *Server) getConfig(c echo.Context) error {
	cfg := s.configManager.GetConfig()
	return c.JSONPretty(200, cfg, "  ")
}
```

```go
type MLNodeKeyConfig struct {
	WorkerPublicKey  string `json:"worker_public"`
	WorkerPrivateKey string `json:"worker_private"` // leaked via JSON
}
```

Note: `KeyringPassword` correctly uses `json:"-"`; worker private key does not.

## Reproduce (if admin port reachable)

```bash
curl -sS "http://HOST:9200/admin/v1/config" | jq '.ml_node_key_config'
# No Authorization header required
```

## Impact

If admin port is exposed (misconfigured publish / proxy / SG):

- Theft of worker private key
- Abuse of `tx/send` to broadcast host-signed txs
- Operational control of nodes / bridge / claim recovery

Default compose binds loopback only, but the app does not fail-closed to localhost.

## Suggested remediation

1. Require auth on all `/admin/v1/*` (mTLS, bearer, or Unix socket only)
2. Sanitize secrets from any config export API
3. Bind admin to `127.0.0.1` in application code
4. Message-type allowlist + auth on `tx/send`

## Disclosure

No production hosts attacked. Happy to move this to HackerOne if preferred over public issues.
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Aphelios01-sdk">@Aphelios01-sdk</a></span>
    <span class="issues-meta-item">commented 2026-07-18 03:07 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Closing to focus disclosure on the highest-priority finding: https://github.com/gonka-ai/gonka/issues/1470 (SSRF via InferenceUrl). Other items can be re-opened or filed via HackerOne if needed.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1471](https://github.com/gonka-ai/gonka/issues/1471) every hour.
