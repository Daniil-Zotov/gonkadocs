---
title: "#1733 — Extend e2e for HA devshard config with multiple routers and multiple versiond"
source: https://github.com/gonka-ai/gonka/issues/1733
issue_number: 1733
synced_at: 2026-09-12T04:44:23Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Extend e2e for HA devshard config with multiple routers and multiple versiond
    <span class="issues-number">#1733</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/a-kuprin">@a-kuprin</a> opened 2026-09-08 16:31 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-09-08 16:31 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #a2eeef; color: #24292f; border-color: #a2eeef;">enhancement</span></div>
</div>

<div class="issues-content" markdown="1">
# Proposal: Unjoined-network citest for multiple versiond-routers

**Status:** Draft  
**Related:** [PR #1610](https://github.com/gonka-ai/gonka/pull/1610) (`VERSIOND_POOL_ENDPOINTS_FILE`), existing `TestRouterStickiness` / `TestVersiondStickySessionFailover`  
**Scope:** One new testenv citest. Not a second `citest-stack`, not multi-host public ingress.

## Gap

Join HA after #1610 can run **several** `versiond-router` processes against versionds that **do not share a Docker network** with the routers (other machines, listed by address).

CI today covers the pieces separately:

| Coverage | Routers | Versionds | Network |
|---|---|---|---|
| testenv citest | 1 | 2 (real, Postgres HA) | one shared compose network, DNS `versiond-pool` |
| `test-fleet` / `test-routing` | 2–3 | fake / one stub | shared test networks |
| `endpoints-render_test.sh` | render only | n/a | n/a |

Nothing boots **two real routers + two real versionds with no shared Docker network** and checks that the same escrow still hashes to the same versiond.

That is the `#1610` other-host path: `VERSIOND_POOL_ENDPOINTS_FILE` replaces DNS.

## Topology

Two Compose projects on one CI Docker daemon. **No common network.**

```text
Compose A  (network: testenv-versiond)          Compose B  (network: testenv-routers)
  mock-chain, mock-dapi, mock-openai              versiond-router-0
  postgres, versiond-0, versiond-1               versiond-router-1
  publish each versiond :8080 → host            no versiond-pool DNS
                                                 VERSIOND_POOL_ENDPOINTS_FILE =
                                                   [{id, host, port}, …]
  test client (harness) ──HTTP──▶ both routers' published :8080
```

Reachability A→B is only **host-published ports**. Inside router containers, `localhost` is the router, so the endpoint list must use one canonical host both slots can dial, e.g. `host.docker.internal` (`extra_hosts: host-gateway`) plus the port from `docker compose port`. **The same `host:port` string must appear in every slot’s list** — the ring is `hash-key addr`. Different literals for the same versiond (`127.0.0.1` vs `172.17.0.1`) are a failed test, not a flake to paper over.

Compose A is today’s HA pair (shared Postgres, `GONKA_HA`). Compose B is two slot-shaped routers, not the public `proxy-router` and not `versiond-router-fleet.sh`. Gateway, height-sync, and host-ping stay off this job.

Negative: `getent hosts versiond-pool` (or equivalent) from a router container must fail. Membership is the file only.

## Scenario

**Name:** Unjoined routers agree on sticky HA versiond.

1. Boot Compose A; wait until both versionds serve `/readyz` and `/<version>/healthz`.
2. Discover published `host:port` for `versiond-0` and `versiond-1`. Write `versiond-endpoints.json` with two `{id, host, port}` entries. Boot Compose B with that file in both routers (`VERSIOND_ROUTING_ACTIVATION_MIN_READY=2`).
3. Wait until both routers’ `/healthz` and per-version readiness succeed.
4. **Stickiness per router.** For session `S`, `GET /<v>/sessions/S/healthz` eight times on router-0 and eight times on router-1. `X-Upstream-Addr` is stable on each router.
5. **Agreement across routers.** For `S`, router-0 and router-1 return the **same** upstream address (the canonical `host:port` from the file, not a Docker DNS name).
6. **Two-member pool.** Probe other session ids until one lands on the other versiond; both routers agree on that second mapping too.
7. **Failover.** Stop `versiond-0`. Session `S` (was on 0) reaches `versiond-1` on **both** routers within the existing sticky-failover window. A session already on 1 stays on 1.

**Pass:** DNS pool unused; explicit list is the only membership; independent routers compute the same ring; failover is consistent.

## How to add it

1. **Harness** — `BootUnjoinedRouterFleet(t)`:
   - Compose A: reuse `WriteStackConfig` + `gencompose`, then **drop** the generated `versiond-router` service (or a small overlay that removes it) so versionds do not share a network with routers.
   - Publish versiond 8080; record `docker compose port`.
   - Write the endpoint JSON; start Compose B from a checked-in `docker-compose.unjoined-routers.yml` (two `versiond-router` builds, distinct published ports, `host-gateway`).
   - Return two router HTTP bases plus the canonical endpoint list.
2. **Test** — `citest/unjoined_router_fleet_test.go` (`//go:build testenvci`), reuse `RouterSessionURL`, `StickyUpstreamHeader`, `WaitStickyFailoverToSurvivor`. Compare addresses after normalising to the JSON `host:port`, not container IPs.
3. **Makefile** — `citest-unjoined-router-fleet` next to the other `citest-*` targets so `list-citest-targets` puts it on its own `devshard-testenv` runner (isolated subnet, no shared 20m stack).
4. **Docs** — one section in `testenv/docs/scenarios.md` pointing here.

Keep the job on `/healthz` only. No chat, no fleet CLI, no public proxy.

## Out of scope

- Two full joins / two public proxies (not a #1610 invariant; two edges are two rings).
- Same-network two-router stickiness (default join DNS `versiond-pool`). Useful, cheaper, and a **separate** test — do not fold it into this job or the unjoined topology will not be what failed.
- `versiond-router-fleet.sh` drain/commit (already `test-fleet` + `--gate`).
- Live two-machine CI.

## Cost

One extra matrix runner: two versionds + two routers + mocks + Postgres. No gateway. Failures dump Compose A and B logs.

</div>

---

> 🔄 **Auto-synced** from [Issue #1733](https://github.com/gonka-ai/gonka/issues/1733) every hour.
