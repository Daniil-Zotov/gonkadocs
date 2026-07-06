---
title: "#412 — [P2] MLNode Token-Based Authentication and FQDN Support"
source: https://github.com/gonka-ai/gonka/issues/412
issue_number: 412
synced_at: 2026-07-06T09:51:43Z
template: issues-main.html
---

> 🔄 **Авто-синхронизация:** из [Issue #412](https://github.com/gonka-ai/gonka/issues/412) каждые 6 часов. 

# 🟢 [P2] MLNode Token-Based Authentication and FQDN Support

**Автор:** [@gmorgachev](https://github.com/gmorgachev) · **Состояние:** Open · **Создано:** 2025-10-31 07:50 UTC · **Обновлено:** 2026-06-27 20:42 UTC

**Метки:** `Priority: Low`

**Веха:** v0.2.15

---

## 📝 Описание

## Goal / Problem

Current MLNode registration in the API service requires three static parameters:
- Static IP address
- PoC port (management API, default 8080)
- Inference port (vLLM inference API, default 5000)

Both ports serve the same MLNode container through nginx proxy for version management (see `deploy/join/docker-compose.mlnode.yml` and `deploy/join/nginx.conf`).

Problems:
- Some cloud providers (e.g., Aliyun EAS) assign new IPs on container recreation, making static IP registration impractical
- Managing two ports adds operational complexity
- Cloud providers often assign stable FQDNs with token-based authentication (e.g., `http://<some-id>.ap-southeast-1.pai-eas.aliyuncs.com/api/predict/eas02/`) that remain consistent across deployments
- Current registration doesn't support using authentication tokens that managed services provide for access control

**Note:** Segment fields (InferenceSegment, PoCSegment) are legacy parameters that are always empty in current deployments.

## Proposal

Support additional registration method using full URLs:

1. Use single port (8080) since both endpoints proxy to the same container   
2. Allow registration using stable baseURLs with authentication tokens instead of IP/ports

The system will support both registration methods, allowing users to choose between IP/port configuration or baseURL-based registration

## Implementation

### Single-Port Operation

Current state (see `deploy/join/nginx.conf` for nginx setup and `mlnode/packages/api/src/api/proxy.py` for internal routing logic):

Management API (port 8080) supports:
- `http://<host>:<poc_port>/api/v1/*` - management API endpoints
- `http://<host>:<poc_port>/v1/*` - proxies to vLLM endpoints
- `http://<host>:<poc_port>/readyz` - ready for inference
- `http://<host>:<poc_port>/health` - whole service health, *not only inference*

Inference API (port 5000, backward compatible) supports:
- `http://<host>:<inference_port>/v1/*` - proxies to vLLM endpoints  
- `http://<host>:<inference_port>/health` - vLLM health check (proxied from vLLM backend)

`<poc_port>/health` checks whole service health while `<inference_port>/health` checks only vLLM backend health. API node currently checks MLNode health via `client.InferenceHealth()` at `http://<host>:<inference_port>/health`. New API binary must support both old MLNodes (port 5000) and new single-port configuration.

### Solution
Use registration method to determine which health endpoint to check:
- Legacy registration (Host/Port/Segment): Check `http://<host>:<inference_port>/health`
- New registration (baseURL): Check `<baseURL>/readyz` (management API readiness endpoint on port 8080)

### FQDN and Token Authentication

Current structure (`decentralized-api/apiconfig/config.go`):
```go
type InferenceNodeConfig struct {
    Host             string
    InferenceSegment string
    InferencePort    int
    PoCSegment       string
    PoCPort          int
    // ... other fields
}
```

Proposed structure for `InferenceNodeConfig` and `broker.Node`:
```go
type InferenceNodeConfig struct {
    // Existing fields (preserved for backward compatibility)
    Host             string
    InferenceSegment string  // Legacy, always empty
    InferencePort    int
    PoCSegment       string  // Legacy, always empty
    PoCPort          int
    
    // New optional fields (SQLite only, not stored on-chain)
    BaseURL          string  // Optional: full URL to MLNode (e.g., "http://service.provider.com/path/")
    AuthToken        string  // Optional: bearer token for authentication
    
    // ... other fields
}

type Node struct {
    // Existing fields
    Host             string
    InferenceSegment string
    InferencePort    int
    PoCSegment       string
    PoCPort          int
    
    // New optional fields
    BaseURL          string
    AuthToken        string
    
    // ... other fields
}
```

URL construction uses baseURL when present, otherwise falls back to `http://<host>:<port>/<segment>`. Version insertion for rolling upgrades works identically for both approaches: `<baseURL>/<version>/<path>` or `http://<host>:<port>/<version>/<path>`.

baseURL and AuthToken are stored in local SQLite database only, not on-chain. This allows each API node to configure its own MLNode access methods independently.

Required changes:

1. Add `base_url` and `auth_token` columns to SQLite schema with empty defaults for automatic migration
2. Update URL construction methods:
   - `broker.Node.InferenceUrlWithVersion()` and `broker.Node.PoCUrlWithVersion()` in `broker/broker.go` (main methods used for all inference and management calls including `/v1/chat/completions`)
   - Helper functions in `mlnode_background_manager.go` 
   - Helper functions in `setup_report.go` for consistency
3. Add `Authorization: Bearer <token>` header to all MLNode requests when AuthToken is set
4. Validate registration: require either (Host+Ports) OR baseURL, not both. baseURL must be valid HTTP(S) URL. AuthToken is always optional.


### Testing

1. Covered by unit tests and they pass:
- local `make local-build`
- [CICD](https://github.com/gonka-ai/gonka/actions/workflows/verify.yml)
2. Existing testermint tests pass:
- local `make build-docker && ./local-test-net/stop.sh &&  make run-tests`
- [Recommended] [CICD](https://github.com/gonka-ai/gonka/actions/workflows/integration.yml)
3. New node joins testnet and works with new MLNode registration

### Backward Compatibility

- Existing nodes using Host/Port configuration are unaffected
- baseURL and AuthToken are local SQLite configuration, not stored on-chain
- No migration needed - old and new registration methods coexist



---

## 💬 Комментарии (6)

### Комментарий 1 — [@Pegasus-starry](https://github.com/Pegasus-starry)

*2025-11-06 04:12 UTC*

Hi @gmorgachev , I have  two questions:
New registration (baseURL): Check <baseURL>/readyz (management API readiness endpoint on port 8080): 
Is it means in the new registration:  the /readyz interface will be used , not using http://<host>:<inference_port>/health any more?       
And the single-port operation only need to modify this place when checking MLNode health ? 

Validate registration: require either (Host+Ports) OR baseURL, not both. baseURL must be valid HTTP(S) URL. AuthToken is always optional.  :  
Where to do this and do we have a validate method already existed to validate the baseURL?

Thanks

### Комментарий 2 — [@tcharchian](https://github.com/tcharchian)

*2026-02-04 23:26 UTC*

@DimaOrekhovPS did the initial review, but now @DimaOrekhovPS  is waiting for @Pegasus-starry  to resolve conflicts with the current gonka version   

### Комментарий 3 — [@tcharchian](https://github.com/tcharchian)

*2026-03-21 00:56 UTC*

Hey @jacky6block @x0152 @akup! It would be great if you could sync on the next steps for this pull request and make the needed decisions together. If you are able to move it forward on your own, it could potentially be included in v0.2.12. But overall, this is a nice-to-have rather than something critical.

### Комментарий 4 — [@akup](https://github.com/akup)

*2026-03-23 06:15 UTC*

All this protections are nice to have. But I want it to be aligned with other features and moving PoC v2 APIs to the repo from vLLM repo.

Need some time to have a big picture in my head

### Комментарий 5 — [@bonujel](https://github.com/bonujel)

*2026-06-23 07:47 UTC*

Hi @tcharchian, I'm picking this up and continuing the issue, and currently working on it. (draft pr #1359, blocked by #1296 )
The new work centralizes MLNode addressing + auth in one place instead of spreading BaseURL/AuthToken across every call site (the #717 approach), and folds in the review feedback.

It's coupled with the Onboarding changes in #1296, so the new PR #1296 is draft and will be opened once 1296 is approved.
Thanks to everyone for the earlier work and review here.



### Комментарий 6 — [@tcharchian](https://github.com/tcharchian)

*2026-06-27 20:42 UTC*

Hi @bonujel, thanks, I see. @DimaOrekhovPS @x0152 are working on v0.2.14 and v0.2.15 and will review https://github.com/gonka-ai/gonka/pull/1296 shortly
