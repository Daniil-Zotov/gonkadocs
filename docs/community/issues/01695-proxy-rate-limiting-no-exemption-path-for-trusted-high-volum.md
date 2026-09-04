---
title: "#1695 — Proxy rate limiting: no exemption path for trusted high-volume clients, and the tuning variables are not passed through in compose"
source: https://github.com/gonka-ai/gonka/issues/1695
issue_number: 1695
synced_at: 2026-09-04T09:43:38Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Proxy rate limiting: no exemption path for trusted high-volume clients, and the tuning variables are not passed through in compose
    <span class="issues-number">#1695</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/Ryanchen911">@Ryanchen911</a> opened 2026-09-01 08:25 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-09-03 18:49 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

A devshard gateway run by our team was rate-limited by a network node's nginx
for weeks without either side realising it: **8,000+ rejected requests in 24
hours** across three zones. The limits themselves are a deliberate design
("Punisher" low-rate/high-burst, documented in `proxy/README.md`). The problems
are that (a) there is no supported way to exempt a known-good high-volume
client, and (b) the variables that would let an operator tune the limits are not
passed through in `deploy/join/docker-compose.yml`, so setting them in
`config.env` silently does nothing.

## Observed

Node running `proxy:0.2.12-post5`. Single client IP = our devshard gateway, 24h:

```
$ docker logs proxy --since 24h 2>&1 | grep 'client: <gateway-ip>' \
    | grep 'limiting ' | awk -F'zone "' '{print $2}' | cut -d'"' -f1 \
    | sort | uniq -c | sort -nr
   4452 api_zone
   3478 rpc_zone
     61 chain_api_zone
```

`grpc_zone` does not appear, consistent with chain queries taking the CometBFT
RPC fallback path rather than gRPC.

For a sustained client, `burst` only absorbs transients — the steady-state
ceiling is the refill rate:

| zone | default | steady-state |
| --- | --- | --- |
| `api_zone` | `10r/m` burst 600 | 0.167 req/s |
| `rpc_zone` | `20r/m` burst 200 | 0.33 req/s |
| `chain_api_zone` | `20r/m` burst 200 | 0.33 req/s |

Binding a devshard session issues one `Participant` query per host slot, so
chain-query volume scales with the number of active escrows rather than with
request volume. Crossing 0.33 req/s takes very little.

## 1. No way to exempt a trusted client that is not a participant

`whitelist_ips.conf` is only ever populated from active participants'
`InferenceUrl` (`proxy/sidecar/main.go`, `syncWhitelist`). A devshard gateway, an
internal monitor, or any trusted client whose address is not itself a
participant endpoint can never appear there.

There is also no volume mount for `/etc/nginx/conf.d/`, and the sidecar rewrites
the file atomically when whitelist sync is enabled, so hand-editing is not
durable either. Operators are left with no supported mechanism, even though the
config already has the right shape for it: `$whitelist_limit_key` is shared by
every zone, so a single entry mapped to `""` exempts a client from all of them
at once.

**Suggested fix:** an `EXTRA_WHITELIST_IPS` variable (space/comma-separated IPs
and CIDRs) merged into `whitelist_ips.conf` and into the fail2ban whitelist,
independently of participant sync.

## 2. The rate-limit variables are not passed through in compose

The `proxy` service's `environment:` block in `deploy/join/docker-compose.yml`
(`upstream/main`) contains **none** of `GONKA_API_RATE_LIMIT_RPS`,
`GONKA_API_RATE_UNIT`, `GONKA_API_BURST`, `CHAIN_API_RATE_*`, `CHAIN_RPC_RATE_*`,
or `CHAIN_GRPC_RATE_*`:

```
$ git show upstream/main:deploy/join/docker-compose.yml \
    | grep -cE "CHAIN_(RPC|GRPC|API)_RATE|GONKA_API_RATE"
0
```

Compose only forwards variables listed in a service's `environment:`. An
operator who reads `proxy/README.md`, correctly concludes the limit is too tight
for their traffic, and sets `CHAIN_RPC_RATE_UNIT=s` in `config.env` gets **no
effect and no warning** — the value never reaches the container. This is the
most costly part in practice, because the configuration appears to have been
applied.

**Suggested fix:** add the documented rate-limit variables to the `proxy`
service's `environment:` block, in the same `${VAR:-default}` style already used
for `CHAIN_RPC_PORT` etc.

## 3. Naming: `*_RATE_LIMIT_RPS` variables whose unit is per-minute

`proxy/entrypoint.sh` on `upstream/main`:

```sh
493: GLOBAL_RATE_UNIT=${GLOBAL_RATE_UNIT:-s}
502: METRICS_RATE_LIMIT_VAL=${METRICS_RATE_LIMIT_RPM:-6}   # named RPM, unit m
506: GONKA_API_RATE_UNIT=${GONKA_API_RATE_UNIT:-m}          # named RPS, unit m
512: EXEMPT_RATE_UNIT=${EXEMPT_RATE_UNIT:-s}
523: DEVSHARD_OBS_RATE_UNIT=${DEVSHARD_OBS_RATE_UNIT:-s}
528: CHAIN_API_RATE_UNIT=${CHAIN_API_RATE_UNIT:-m}           # named RPS, unit m
533: CHAIN_RPC_RATE_UNIT=${CHAIN_RPC_RATE_UNIT:-m}           # named RPS, unit m
538: CHAIN_GRPC_RATE_UNIT=${CHAIN_GRPC_RATE_UNIT:-m}         # named RPS, unit m
```

`METRICS_RATE_LIMIT_RPM` shows the intended convention: a per-minute knob is
named `RPM`. Every zone in the file either uses `s` or is named `RPM` — except
these four, which are named `RPS` and default to `m`. `proxy/README.md` does
state the unit ("Default `m` for slow recovery"), so this is a naming
inconsistency rather than a hidden default, but it is the reason an operator
reading `CHAIN_RPC_RATE_LIMIT_RPS=20` mentally budgets 20 req/s and plans
capacity against a number that is 60x off.

**Suggested fix:** rename to `*_RATE_LIMIT_RPM` (keeping the old names as
accepted aliases), or state the effective req/s in the README table.

## Why this took a long time to find

Nothing on either side reports throttling. The node's rejections are only in the
proxy container log; the gateway sees generic query failures. Filing a companion
issue for the devshard side, where transient chain-query failures are not
classified as retryable and so are indistinguishable from real errors.

## Environment

- Node: `proxy:0.2.12-post5`. Defaults verified unchanged on `upstream/main`.
- Rate-limit defaults predate devshard v4 (`f038d9840`, v0.2.8), so this is not
  version-specific; devshard v4 raised the query volume enough to cross the line.
- Note for the `rc/token-auth` branch: `GONKA_API_EXEMPT_ROUTES` there is
  `chat inference poc/proofs`, dropping the `subnet devshard` present on
  `upstream/main` and in 0.2.12/0.2.15. Since exemption is implemented as a
  path-prefix `location` block, that would move all devshard API traffic into
  `api_zone` at 10r/m. Possibly unintentional.

I have a working patch for items 1-3 and am glad to open a PR. The whitelist
change keeps the generated `whitelist_ips.conf` byte-identical when
`EXTRA_WHITELIST_IPS` is unset, so it is a no-op for existing deployments.

</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/a-kuprin">@a-kuprin</a></span>
    <span class="issues-meta-item">commented 2026-09-03 18:49 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Next devshard release (v6) is planning to switch networking to gRPC, so rate limiting problem should go away mostly</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1695](https://github.com/gonka-ai/gonka/issues/1695) every hour.
