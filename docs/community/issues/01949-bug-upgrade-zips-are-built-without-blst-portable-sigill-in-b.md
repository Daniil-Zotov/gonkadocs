---
title: "#1949 — [BUG] Upgrade zips are built without BLST_PORTABLE: SIGILL in blst_cgo_init on x86-64 CPUs without ADX"
source: https://github.com/gonka-ai/gonka/issues/1949
issue_number: 1949
synced_at: 2026-10-09T02:16:51Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    [BUG] Upgrade zips are built without BLST_PORTABLE: SIGILL in blst_cgo_init on x86-64 CPUs without ADX
    <span class="issues-number">#1949</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/unameisfine">@unameisfine</a> opened 2026-10-08 17:28 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-10-08 17:28 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

The amd64 upgrade binaries published for `release/v0.2.16-post1` (`inferenced-amd64.zip`, `decentralized-api-amd64.zip`, `edge-api-amd64.zip`) are built with blst in its default, non-portable mode. On x86-64 CPUs without the ADX extension they exit at startup:

```
Caught SIGILL in blst_cgo_init, consult <blst>/bindings/go/README.md.
```

Our full node runs on an Intel Xeon E5-1650 (Sandy Bridge). Before the upgrade it ran the `inferenced` from the `ghcr.io/product-science/inferenced:0.2.15` image, which is built with `-D__BLST_PORTABLE__`. At the v0.2.16 upgrade height (proposal #112, block 6,449,400) cosmovisor switched to the binary from the upgrade zip, and that binary crashed in a restart loop. The node was down for ~7 hours, until we rebuilt the same tag with `BLST_PORTABLE=1`.

## Motivation

Every upgrade zip goes through the same build path, so affected nodes will go down the same way at every future upgrade. Nothing fails before the upgrade height, so operators find out only after the node is down. The fix is a few lines in the build files.

## Impact

- Who is affected: node operators (hosts/validators as well as full, RPC and sentry nodes) that get upgrade binaries through cosmovisor auto-download (the image sets `DAEMON_ALLOW_DOWNLOAD_BINARIES=true`) on x86-64 CPUs without ADX:
  - Intel before Broadwell, e.g. Xeon E3/E5 v1–v3, which are common on budget dedicated servers;
  - AMD before Zen;
  - VMs whose CPU model hides ADX, e.g. `qemu64` or `kvm64`.
- Is effect network-wide or limited: limited. Each affected participant loses availability at every upgrade.
- Likelihood: organic. The crash is deterministic on every affected machine at every chain upgrade.
- Severity: Medium (Medium impact × Medium likelihood).
- Affected components: `inference-chain/Makefile`, `decentralized-api/Makefile`, `.github/workflows/publish_upgrade_binaries.yml`, and the amd64 upgrade zips of every release.

## Detailed description

### Root cause

- On amd64 the blst Go binding is compiled with `-D__ADX__` (`#cgo amd64 CFLAGS: -D__ADX__ -mno-avx`). Its README says: *"If the test or target application crashes with an "illegal instruction" exception [after copying to an older system], rebuild with `CGO_CFLAGS` environment variable set to `-O2 -D__BLST_PORTABLE__`."*
- The Dockerfiles add `-D__BLST_PORTABLE__` only when `BLST_PORTABLE=1`, and the default is `ARG BLST_PORTABLE=0`. `scripts/blst-portable.mk` sets it to `1` only on Apple Silicon hosts; this mechanism came from #697 for macOS builds.
- `DOCKER_BUILD` (images) forwards `--build-arg BLST_PORTABLE`, but `DOCKER_BUILD_UPGRADE` in `inference-chain/Makefile` and `decentralized-api/Makefile` does not. So `make build-for-upgrade BLST_PORTABLE=1` prints `BLST_PORTABLE: 1` and still produces a non-portable binary. `edge-api/Makefile` does forward the flag.
- `publish_upgrade_binaries.yml` runs `make … build-for-upgrade` on `ubuntu-latest` without `BLST_PORTABLE`, so every published upgrade binary is non-portable.

https://github.com/gonka-ai/gonka/blob/136041c81ea8ff38e7620d76af66a7c7fe7eec50/inference-chain/Makefile#L115-L141

https://github.com/gonka-ai/gonka/blob/136041c81ea8ff38e7620d76af66a7c7fe7eec50/decentralized-api/Makefile#L55-L70

https://github.com/gonka-ai/gonka/blob/136041c81ea8ff38e7620d76af66a7c7fe7eec50/.github/workflows/publish_upgrade_binaries.yml#L147-L158

### Reproduction (any x86-64 machine with Docker)

```bash
mkdir v0216 && cd v0216
curl -fsSLO 'https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.16-post1/inferenced-amd64.zip'
unzip -q inferenced-amd64.zip && chmod +x inferenced
docker run --rm -v "$PWD:/x:ro" alpine:3.21 sh -c \
  'apk add -q qemu-x86_64 && qemu-x86_64 -cpu SandyBridge /x/inferenced version'
# Caught SIGILL in blst_cgo_init, consult <blst>/bindings/go/README.md.   (exit code 132)
```

With `-cpu Broadwell-noTSX` (has ADX) the same binary prints `v0.2.16-post1`.

### Evidence

`CGO_CFLAGS` recorded in the build info (`go version -m`):

| Binary | `CGO_CFLAGS` |
|---|---|
| `inferenced` in `inferenced-amd64.zip` | `-I/lib -O2` |
| `decentralized-api` and `inferenced` in `decentralized-api-amd64.zip` | `-I/lib -O2` |
| `edge-api` in `edge-api-amd64.zip` | `-I/lib -O2` |
| `/usr/bin/inferenced` in `ghcr.io/product-science/inferenced:0.2.15` | `-I/lib -O2 -D__BLST_PORTABLE__` |

Startup under `qemu-x86_64 -cpu <model>`:

| CPU model | binaries from the three v0.2.16-post1 zips | `inferenced` rebuilt with `BLST_PORTABLE=1` |
|---|---|---|
| `SandyBridge` | SIGILL | OK |
| `Haswell-noTSX` | SIGILL | OK |
| `qemu64` | SIGILL | OK |
| `Broadwell-noTSX` | OK | OK |

The rebuilt `inferenced` comes from the same tag through the same Dockerfile and LDFLAGS. Its build info differs from the official binary only in `CGO_CFLAGS` (`-D__BLST_PORTABLE__`), and two independent rebuilds produced the same sha256. Our node has been running v0.2.16 on it since.

### Proposed fix

1. Add `--build-arg BLST_PORTABLE=$(BLST_PORTABLE)` to `DOCKER_BUILD_UPGRADE` in `inference-chain/Makefile` and `decentralized-api/Makefile`, the same way `DOCKER_BUILD` and `edge-api/Makefile` already do.
2. Pass `BLST_PORTABLE=1` to the three `make … build-for-upgrade` calls in `publish_upgrade_binaries.yml`, or make portable the default for linux/amd64 release builds.
3. Optionally, add a release check: fail if `go version -m` lacks `-D__BLST_PORTABLE__`, or smoke-run the binary under `qemu-x86_64 -cpu SandyBridge … version`.

The cost on modern CPUs should be negligible. In portable mode blst detects ADX once at startup (`__blst_platform_cap`), and each generic routine starts with `testl $1,__blst_platform_cap(%rip); jnz <mulx/adx variant>`, so CPUs with ADX keep the fast path.

A PR with (1) and (2) follows.

### Workaround for affected operators

Before the upgrade height, build the release tag with `BLST_PORTABLE=1` and put the binary at `$DAEMON_HOME/cosmovisor/upgrades/<plan name>/bin/inferenced`. If an executable is already there, cosmovisor switches to it and downloads nothing.

</div>

---

> 🔄 **Auto-synced** from [Issue #1949](https://github.com/gonka-ai/gonka/issues/1949) every hour.
