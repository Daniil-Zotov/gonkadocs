---
title: "#1529 — devshard v4: epoch prune leaves zombie in-memory Hosts → AppendDiff session not found"
source: https://github.com/gonka-ai/gonka/issues/1529
issue_number: 1529
synced_at: 2026-08-08T06:00:10Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    devshard v4: epoch prune leaves zombie in-memory Hosts → AppendDiff session not found
    <span class="issues-number">#1529</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/maria-mitina">@maria-mitina</a> opened 2026-07-31 11:00 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-08-01 06:33 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

On testnet (`gonka-testnet`, participant `versiond` / `devshardd` `0.2.14-v4-r4`), gateway chat fails with:

```text
persist diff nonce N: diff persist retries exhausted: session not found: <escrow_id>
```

logged as `HandleInference` / `where=host.apply_diff`.

**Root cause:** epoch retention prune deletes durable session state (Postgres partitions + `escrowIdx`) while the in-memory `Host` for that escrow stays registered in `HostManager.sessions`. The next gateway `/sessions/<id>/chat/completions` reuses that zombie Host; `AppendDiff` → `lookupEpoch` → `ErrSessionNotFound`.

`HostManager.EvictBefore(cutoff)` already exists but is **never called** on the v4 standalone path (`upgrade-v0.2.15` / `main` after #1482).

## Impact

- Gateway sees participant `send_failed` / HTTP 500 / 0-byte upstream.
- Hosts get marked suspicious → `picker_exhausted` cascades.
- Especially hits **long-lived gateway escrows** that span more epochs than `sessionEpochRetain` (3).

## Observed on testnet (seed `89.169.111.79`)

Timeline for escrow `47` (representative):

1. `NewStateMachine` / Host created for escrow `47`
2. Later: `devshard pruned epochs before=349 … retain=3` and/or `cleared .pg-bound; postgres has no remaining sessions`
3. Still later: `where=host.apply_diff` … `session not found: 47`
4. `devshard_sessions` / `devshard_session_index` no longer contain that escrow

Repro / evidence command on seed:

```bash
ssh ubuntu@89.169.111.79 'bash -s' <<'EOF'
docker logs versiond --since 24h 2>&1 | grep -E \
  "pruned epochs|cleared \.pg-bound|where=host\.apply_diff.*session not found|NewStateMachine.*escrow_id=47" | tail -40
docker exec -e PGPASSWORD=devshardd devshard-postgres \
  psql -U devshardd -d devshardd -c \
  "SELECT escrow_id, epoch_id, status FROM devshard_sessions
   WHERE escrow_id IN ('30','32','44','47') ORDER BY 1;"
EOF
```

## What we prune

Local **devshard session storage** keyed by **chain epoch** (not on-chain escrow state):

- With `sessionEpochRetain = 3`, prune drops everything with `epoch_id < cutoff`
- Postgres: epoch partitions for sessions, diffs, signatures, snapshots, sealed inferences, validation obs/leases, plus `devshard_session_index` / `escrow_cache` and in-memory `escrowIdx`
- Trigger: `ManagedStorage.PruneOnce` via `PruneOnceAsync` on epoch change (`devshard/cmd/devshardd/app.go`)

On-chain escrow remains; only the node’s durable session copy is removed.

## Regression history

| When | What |
|------|------|
| #1417 / fix “stop leaking hosts…” | Wired `RegisterEpochPrune(store, func(cutoff) { manager.EvictBefore(cutoff) })` in `decentralized-api/cmd/devshardd/main.go` |
| #1267 Upgrade v0.2.14 on `main` | Call still present on dapi `devshardd` path |
| #1482 Devshard v4 | Session manager moved to `devshard/cmd/devshardd/`; **`EvictBefore` kept as method, prune→evict wiring dropped** |
| `main` / `upgrade-v0.2.15` today | Definition only — **no call sites** |

Show in repo:

```bash
git fetch origin
git grep -n 'EvictBefore(' origin/upgrade-v0.2.15 -- '*.go'
# only the definition

git grep -n 'manager.EvictBefore' origin/upgrade-v0.2.14 -- '*.go'
# old wiring in decentralized-api/cmd/devshardd/main.go
```

## Expected fix

1. **Restore prune → evict wiring** on standalone v4 `devshardd`: before durable wipe, call `HostManager.EvictBefore(cutoff)` (e.g. `ManagedStorage.SetOnPrune` from `app.go`, same intent as pre-v4 `RegisterEpochPrune(..., evict)`).
2. **Prefer also:** do not prune epochs that still have `status='active'` sessions (`ListActiveSessions` clamp), so long-lived gateway escrows keep durable state until settled.
3. **Safety net:** on persist `errors.Is(err, storage.ErrSessionNotFound)`, `Evict(escrowID)` so the next bind recreates instead of looping on a zombie Host.

## Out of scope (related but separate)

- Filfox clock skew / `maxTimestampDrift=30` timeout-vote failures
- Gateway client timeouts while racing after host marked suspicious

## References

- `devshard/storage/managed.go` — `PruneOnce` / retain=3
- `devshard/storage/postgres.go` — `pruneBefore` / `lookupEpoch` → `ErrSessionNotFound`
- `devshard/cmd/devshardd/session/manager.go` — `EvictBefore` (unused)
- `devshard/cmd/devshardd/app.go` — `PruneOnceAsync` on new epoch
- Related PRs: https://github.com/gonka-ai/gonka/pull/1417 https://github.com/gonka-ai/gonka/pull/1482

</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/maria-mitina">@maria-mitina</a></span>
    <span class="issues-meta-item">commented 2026-07-31 13:02 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>fix in https://github.com/gonka-ai/gonka/pull/1530</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1529](https://github.com/gonka-ai/gonka/issues/1529) every hour.
