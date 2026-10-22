---
title: "#2034 — [BUG] devshardctl: one escrow's runtime build error at startup stops the whole gateway"
source: https://github.com/gonka-ai/gonka/issues/2034
issue_number: 2034
synced_at: 2026-10-22T10:18:20Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    [BUG] devshardctl: one escrow's runtime build error at startup stops the whole gateway
    <span class="issues-number">#2034</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/snevolin">@snevolin</a> opened 2026-10-15 20:27 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-10-16 08:28 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span></div>
</div>

<div class="issues-content" markdown="1">
## Summary
At startup `buildGatewayRuntimes` builds a runtime for every active escrow and classifies a build error by name. Four errors deactivate the escrow and let the gateway start; `ErrParticipantNotFound` skips it. Every other error is fatal for the process: `log.Fatalf("create runtimes")`.

The effect is not limited to the escrow with the error. A transient chain call, a damaged SQLite file, or a recovery error of one escrow stops the process, and with it all of its escrows at once, including the healthy ones that have nothing to do with the error: their clients get no answers, their Finishes are not delivered, their settlements do not run. With `restart: unless-stopped` the container loops, and the healthy escrows stay unavailable for as long as the one broken escrow keeps the gateway from starting.

The settlement of an escrow that the gateway cannot serve is a separate issue: #2039.

## Motivation
Pre-existing on `main` (`main.go:560-593` at fd99f88d). v6 (#1792) raises the exposure: shared Postgres, many escrows per gateway, 16 `GetHostInfo` calls per escrow over peer RPC, and new recovery steps (validation-obs and sealed-index rebuild). The allow-list grows by incident: #1988 item 9 added `ErrParticipantNotFound` after one missing participant record disabled a funded escrow.

## Impact
- Who is affected: gateway operators and their clients; hosts in the affected escrows.
- Scope: one gateway, but total for it. The gateway is the only sequencer of its escrows: no requests, no Finish delivery, no finalize, no settlement while it is down.
- Likelihood: intermittent. One timeout in N × 16 chain calls at boot is enough. With `restart: unless-stopped` the container loops and repeats the calls on each restart.
- Money: an escrow that is not settled in its epoch or the next cannot be settled at all; two epochs later the chain splits the full deposit equally per slot (`devshard_pruning.go`, `distributeUnsettledEscrow`). The owner gets no remainder back, hosts are paid as if the escrow was fully used, and no host stats reach the epoch record.
- Affected components: `devshard/cmd/devshardctl/main.go` (`buildGatewayRuntimes`), `devshard/user/httpsession.go`, `devshard/user/recover.go`.

## Detailed description
Code at v6 head 8f9279f1 (same structure on `main`):
- `main.go:591-634`: classification; `main.go:478`: `log.Fatalf`. No retry, no backoff.
- Per-escrow errors that reach the fatal branch: a transient chain error in `GetEscrow` (`httpsession.go:64-66`) or in any `GetHostInfo` of the 16 slots (`:118-122`); `open storage` for that escrow's SQLite (`:88-90`); every error of `RecoverSession` (`recover.go`: group mismatch :153, version mismatch :161, snapshot restore :212, backfill diffs :294, sealed-index rebuild :390, validation-obs rebuild :420).
- These errors have different scopes: some are process-wide (chain or store unavailable, no key), some are permanent for one escrow (damaged journal, group or version mismatch), some are transient for one escrow (one slow chain call, SQLite busy). The classification does not distinguish them.

Reproduce:
1. Run a gateway with two active escrows.
2. During startup make one `GetHostInfo` fail (block the chain gRPC for a few seconds) or damage the SQLite file of one escrow.
3. The gateway exits with `create runtimes: ...` and never serves the healthy escrow; the container loops.

Expected: the healthy escrow serves; the failed one is reported.

</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/snevolin">@snevolin</a></span>
    <span class="issues-meta-item">commented 2026-10-15 21:13 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>I solved these problems from this issue in #2035:</p>
<ul>
<li>The gateway starts although one escrow's runtime build fails for a reason that is not final. The healthy escrows serve, and the container does not loop on <code>restart: unless-stopped</code>.</li>
<li>The failed escrow is reported (<code>devshard_gateway_startup_skipped_escrow</code> with reason <code>runtime_build_failed</code>, plus a log line) and is retried in the background every 30 s until it starts or a final reason deactivates it. No restart is needed.</li>
<li>A process-wide environment error stops the start with its own reason. A per-escrow error with no final meaning skips that escrow only. An unknown error keeps the gateway up without a new allow-list entry.</li>
<li>The reproduction above ends with the healthy escrow serving and the other one skipped and retried, or deactivated when the damage is proven unrecoverable.</li>
</ul>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2034](https://github.com/gonka-ai/gonka/issues/2034) every hour.
