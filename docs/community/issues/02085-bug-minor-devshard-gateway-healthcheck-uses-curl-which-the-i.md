---
title: "#2085 — [BUG: minor] devshard-gateway healthcheck uses curl, which the image does not contain → container permanently unhealthy"
source: https://github.com/gonka-ai/gonka/issues/2085
issue_number: 2085
synced_at: 2026-11-27T10:59:59Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    [BUG: minor] devshard-gateway healthcheck uses curl, which the image does not contain → container permanently unhealthy
    <span class="issues-number">#2085</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/maria-mitina">@maria-mitina</a> opened 2026-10-22 11:17 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-11-27 01:50 UTC</span>
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

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/qdanik">@qdanik</a></span>
    <span class="issues-meta-item">commented 2026-11-27 01:49 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>fixed by PR: https://github.com/gonka-ai/gonka/pull/2166</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2085](https://github.com/gonka-ai/gonka/issues/2085) every hour.
