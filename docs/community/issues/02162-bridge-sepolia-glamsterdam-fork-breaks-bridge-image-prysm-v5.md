---
title: "#2162 — Bridge: Sepolia Glamsterdam fork breaks bridge image (Prysm v5 / geth 1.16.7) — testnet-4 bridge down"
source: https://github.com/gonka-ai/gonka/issues/2162
issue_number: 2162
synced_at: 2026-10-30T08:45:36Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Bridge: Sepolia Glamsterdam fork breaks bridge image (Prysm v5 / geth 1.16.7) — testnet-4 bridge down
    <span class="issues-number">#2162</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/maria-mitina">@maria-mitina</a> opened 2026-10-28 17:24 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-10-28 17:28 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span></div>
</div>

<div class="issues-content" markdown="1">
## Summary

The Ethereum bridge is non-functional on testnet-4 (all 4 validators): Prysm inside `ghcr.io/product-science/bridge:0.2.15` crash-loops on checkpoint sync because Sepolia activated **Glamsterdam** (CL fork Gloas `0x90000076`, epoch 353024, 2026-10-06 13:53 UTC) and the bundled clients predate that fork. The same applies to `bridge:0.2.16` — every published bridge tag pins the same Prysm/Geth base images, so redeploying does not help.

Related: #2153 (mainnet bridge update, projected activation 2026-11-18) — the fix below is the same image that mainnet will need before Ethereum mainnet Glamsterdam.

## Symptoms

`docker logs bridge` on any testnet-4 host (18221/18223/18226/18214), repeating every ~8 s:

```
PRSM: INFO  Checkpoint sync - Downloading origin state and block
PRSM: FATAL unable to start beacon node: could not start modules: could not start DB:
      Error retrieving checkpoint origin state and block: error detecting chain config for
      finalized state: version=0x90000076 not found in any known fork choice schedule:
      unable to find requested BeaconChainConfig
Prysm failed to stay alive after start ... Prysm-only restart failed; will retry in monitor loop
GETH: WARN Beacon client online, but no consensus updates received in a while.
```

API handshake returns no block:

```
$ curl -s http://127.0.0.1:8000/v1/bridge/block/latest?chain=sepolia
{"chainId":"sepolia"}
```

## Root cause

| Component | In `bridge:0.2.13 … 0.2.16` | Problem |
|---|---|---|
| Prysm — `ghcr.io/product-science/bridge-prysm:0.2.12` | Prysm **v5.x** (`gonka-ai/bridge-prysm`; only a Dockerfile on top of upstream) | Knows forks up to Fulu (`0x90000075`); Sepolia finalized state is now Gloas (`0x90000076`) |
| Geth — `ghcr.io/product-science/bridge-geth:0.2.14-post3` | patched **v1.16.7** (`gonka-ai/bridge-geth` branch `bridge-rebase-1.16.7`) | Sepolia config has Osaka/BPO1/BPO2 but no `amsterdamTime`; cannot follow the EL side of Glamsterdam |

Sepolia fork schedule (from `https://sepolia.checkpoint-sync.ethpandaops.io/eth/v1/config/fork_schedule`): `222464 0x90000074` (Electra), `272640 0x90000075` (Fulu), `353024 0x90000076` (Gloas). Any checkpoint provider now serves a Gloas finalized state, so changing `BEACON_STATE_URL` does not help; the force-clear of the Prysm datadir on restart rules out stale DB state.

Upstream support: Prysm `v7.3.1` — `config/params/testnet_sepolia_config.go`: `GloasForkEpoch = 353024`, `GloasForkVersion = 0x90000076`. go-ethereum `v1.17.10` — `params/chainspecs/sepolia.json`: `"amsterdamTime": 1791294816`.

Ethereum mainnet is still on Fusaka (`0x06000000`), so the mainnet bridge is unaffected until mainnet Glamsterdam.

## Proposed fix

1. **`gonka-ai/bridge-prysm`**: branch from upstream `v7.3.1`, cherry-pick the Dockerfile commits (`c8c0b6568`, `35f8630de`), build and push `ghcr.io/product-science/bridge-prysm:0.2.18`.
2. **`gonka-ai/bridge-geth`**: branch from upstream `v1.17.10`, cherry-pick the bridge commits `8c9f51e66^..06055a1ac` (`bridge changes for initial release`, `explicit urls fix request`, `docker alpine version up`, `withdrawal support`, `update classify bridge log`, `when ReceiptSync is active skip blockchain header check`, `previous uncommitted changes`, `bridge sync - self heal`), resolve conflicts, run tests for touched packages, build and push `ghcr.io/product-science/bridge-geth:0.2.18`.
3. **`gonka`**: update the two `FROM` lines in `bridge/Dockerfile` (pin by digest), `make -C bridge build-docker docker-push VERSION=0.2.18`; bump the `bridge` image in `deploy/join/docker-compose.yml`.
4. **Verify locally** with `ETHEREUM_NETWORK=sepolia`: Prysm completes checkpoint sync, Geth imports Sepolia blocks, `--bridge.postblock` posts reach the API.
5. **Roll out on testnet-4** (4 hosts, `docker compose ... pull bridge && up -d --no-deps --force-recreate bridge`), confirm `/v1/bridge/block/latest?chain=sepolia` returns a block, re-run a bridge scenario (`docs/bridge-upgrade-scenario-a-runbook.md`).
6. Ship the same image to mainnet ahead of mainnet Glamsterdam (#2153).

## Environment

- testnet-4, chain `gonka-testnet-4`, binary `v0.2.17-testnet-2`
- `bridge` service from `deploy/join/docker-compose.yml`, `ETHEREUM_NETWORK=sepolia`, `BEACON_STATE_URL=https://sepolia.checkpoint-sync.ethpandaops.io`
- `docker exec bridge beacon-chain --version` → `Prysm/Unknown/Local build` (prysm/v5 symbols); `geth version` → `1.16.7-stable`

</div>

---

> 🔄 **Auto-synced** from [Issue #2162](https://github.com/gonka-ai/gonka/issues/2162) every hour.
