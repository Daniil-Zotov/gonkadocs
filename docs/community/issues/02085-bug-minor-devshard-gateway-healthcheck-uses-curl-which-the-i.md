---
title: "#2085 — [BUG: minor] devshard-gateway healthcheck uses curl, which the image does not contain → container permanently unhealthy"
source: https://github.com/gonka-ai/gonka/issues/2085
issue_number: 2085
synced_at: 2026-10-30T02:00:46Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    [BUG: minor] devshard-gateway healthcheck uses curl, which the image does not contain → container permanently unhealthy
    <span class="issues-number">#2085</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/maria-mitina">@maria-mitina</a> opened 2026-10-22 11:17 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-10-22 11:18 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
**Summary**

`deploy/join/docker-compose.devshard-gateway.yml` defines the gateway healthcheck as

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8080/v1/status"]
```

but the image it runs (`devshardctl-runtime` stage in `devshard/Dockerfile`) is `alpine:3.23` with only `ca-certificates wget` installed — no `curl`. Every gateway started from the stock compose therefore reports `unhealthy` forever.

**Observed**

- testnet1 gateway (`devshard-gateway:testnet-v6-f5ad27a`): `docker ps` → `Up 8 days (unhealthy)`, `FailingStreak=23034`, health log: `OCI runtime exec failed: exec: "curl": executable file not found in $PATH`. The service itself answers `/v1/status` with 200.
- Same for `ghcr.io/gonka-ai/devshard-gateway:mainnet-v0.2.15-v4.1` and `mainnet-v0.2.15-v4-latest` (the compose default tag).
- Present on every branch checked (`main`, `devshard-0.2.x-v6`, `devshard/v7`, `upgrade-v0.2.17`). Reported internally on 2026-09-16; since then `cbb20c196` (Oct 7) and `e2e7873a6` (Oct 12) re-added the same `curl` line.

**Impact**

Container health is always `unhealthy`, so `depends_on: condition: service_healthy`, orchestration restarts and health-based alerting are misled; operators cannot tell a broken gateway from a healthy one via `docker ps`.

**Fix (either)**

- compose: `test: ["CMD", "wget", "-q", "-O", "/dev/null", "http://localhost:8080/v1/status"]`
- or Dockerfile: `RUN apk add --no-cache ca-certificates curl` in the `devshardctl-runtime` stage.

The same check should be applied to any other compose file that healthchecks a `devshardctl`-based container.

</div>

---

> 🔄 **Auto-synced** from [Issue #2085](https://github.com/gonka-ai/gonka/issues/2085) every hour.
