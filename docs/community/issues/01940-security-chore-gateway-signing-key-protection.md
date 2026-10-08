---
title: "#1940 — [Security Chore]: Gateway signing-key protection"
source: https://github.com/gonka-ai/gonka/issues/1940
issue_number: 1940
synced_at: 2026-10-08T09:08:07Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    [Security Chore]: Gateway signing-key protection
    <span class="issues-number">#1940</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/a-kuprin">@a-kuprin</a> opened 2026-10-07 15:26 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-10-07 15:26 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #a2eeef; color: #24292f; border-color: #a2eeef;">enhancement</span></div>
</div>

<div class="issues-content" markdown="1">
# Chore: Gateway signing-key protection

**Status:** Deferred. Not part of PR #1568.  
**Related:** [PR #1568 review](https://github.com/gonka-ai/gonka/pull/1568#discussion_r4189385988) on `gateway_devshards.private_key_hex`. Earlier SQLite note: [escrow-keys-at-rest.md](./escrow-keys-at-rest.md).

This is an issue description. It does not change the Postgres gateway store.

## Decision for PR #1568

Storing `private_key_hex` in Postgres is acceptable for this PR. The database is the operator's, and protecting it is the operator's responsibility: who can read it, backups, replicas, and the path between the gateway process and Postgres. That matches the previous SQLite gateway store.

`private_key_env` stays as the alternative. When the hex column is empty and the env name is set, the gateway reads the key from the process environment and the database holds only the variable name.

Forcing TLS, or refusing to persist hex, is a deployment policy. It is out of scope for the Postgres backend change.

## What the review asked

`gateway_devshards` keeps the devshard signing key in `private_key_hex` and the optional env name in `private_key_env`. In a multi-instance deployment every gateway that shares the database can read the key, as can backups, replicas, and any role with `SELECT` on that table.

The pool is opened with `pgxpool.ParseConfig("")` in `gateway_store_postgres.go` and `accounting/store_postgres.go`. That uses libpq defaults, including `sslmode=prefer`. `prefer` uses TLS when the server offers it, and otherwise connects in the clear. It does not check the server certificate. A `SELECT` of `private_key_hex` can therefore cross the network unencrypted, or toward a host that is only pretending to be Postgres, unless the operator sets `PGSSLMODE=require` or `verify-full`. `ParseConfig` already honors `PGSSLMODE`; the client does not require it.

On a Postgres that stays on the operator's own machine, that traffic does not leave the host.

## Current behavior

- Create and import accept either an inline `private_key` or `private_key_env`. An inline key is stored as hex. An env-only request stores the variable name.
- Rotation commitments store `private_key_env` only.
- `GET /v1/admin/state` clears `private_key` before writing the response. The env name is still returned.
- Runtime startup uses the stored hex when it is set, and otherwise reads `os.Getenv(private_key_env)`.

## Follow-up

Decide, as its own chore, whether gateway key handling should get stricter than "the operator protects the database":

1. Document `private_key_env` as the production path, and treat a populated `private_key_hex` as an operator choice rather than the default for new escrows.
2. Document `PGSSLMODE` for any Postgres that is not on the gateway host. `require` encrypts. `verify-full` also checks the server certificate and hostname. Apply the same note to the other pools that use `ParseConfig("")` (session, payload, accounting, inference stats).
3. Optionally stop persisting hex once env or secret-store references cover create, import, and rotation. Encryption at rest (`DEVSHARD_GATEWAY_SECRETS_KEY` or equivalent) remains the later option already sketched in [escrow-keys-at-rest.md](./escrow-keys-at-rest.md).

## Out of scope

- Blocking PR #1568 on this.
- Per-escrow HSM or remote signing.
- Changing the pool size cap (`PG_POOL_MAX_CONNS`). That is a separate connection-count limit and does not encrypt the session.

</div>

---

> 🔄 **Auto-synced** from [Issue #1940](https://github.com/gonka-ai/gonka/issues/1940) every hour.
