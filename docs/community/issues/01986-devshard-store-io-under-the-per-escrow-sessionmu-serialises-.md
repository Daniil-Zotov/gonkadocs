---
title: "#1986 — devshard: store I/O under the per-escrow Session.mu serialises all requests of an escrow under load"
source: https://github.com/gonka-ai/gonka/issues/1986
issue_number: 1986
synced_at: 2026-10-23T13:34:55Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    devshard: store I/O under the per-escrow Session.mu serialises all requests of an escrow under load
    <span class="issues-number">#1986</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/kaileido">@kaileido</a> opened 2026-10-12 22:21 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-10-12 22:22 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
`Session.mu` (`devshard/user/session.go:240`) is one lock per escrow session, and the gateway runs one session per escrow, so it serialises every request on that escrow. Durable store I/O runs while it is held:

- `ProcessResponse` writes `store.AddSignature` once per validator slot (`session.go:964-968`).
- `PrepareInferenceFn` persists the diff through `persistDiffRetryLocked` → `storage.AppendDiffWithRetry`, with backoff retries, under the lock (`session.go:1319-1332`). This one is deliberate: releasing the lock during backoff would let a concurrent compose sign the same next nonce.
- For a host that lags more than the in-memory diff suffix, `diffRangeLocked` (`:685`) and `postStateRootForNonce` (`:870`) read diffs from the store under the lock.

Under load every lock hold carries a store round trip, so lock wait grows with request rate and with each speculative secondary attempt, which adds another `PrepareInferenceFn`. It shows up as growing session-mutex wait in the long-escrow 32 rps load scenario.

Proposal: keep `AppendDiff` under the lock, since it guards against a diff fork. Move `AddSignature` out of it: update `s.signatures` under the lock and persist the signature after unlock or through an ordered background writer. A failed signature write is already only logged (`failed to persist signature`), so durability semantics do not change. Optionally, read the lagging-host diff range outside the lock and re-check the cursor under it.

To verify: compare gateway mutex profiles from `devshard/testenv/loadtest` `long-escrow-32rps-8m` before and after.

</div>

---

> 🔄 **Auto-synced** from [Issue #1986](https://github.com/gonka-ai/gonka/issues/1986) every hour.
