---
title: "#1671 — chore(deps): rebase forked cosmos-sdk onto v0.53.8 (base is v0.53.3, ~5 patch releases behind)"
source: https://github.com/gonka-ai/gonka/issues/1671
issue_number: 1671
synced_at: 2026-08-29T14:33:31Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    chore(deps): rebase forked cosmos-sdk onto v0.53.8 (base is v0.53.3, ~5 patch releases behind)
    <span class="issues-number">#1671</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/kAIPraxisBot">@kAIPraxisBot</a> opened 2026-08-28 20:22 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-08-28 20:22 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

Our forked cosmos-sdk (`github.com/gonka-ai/cosmos-sdk`, currently `v0.53.3-ps19-observability`, referenced by both `inference-chain` and `decentralized-api` via `go.mod` replace) is based on upstream **v0.53.3** (2025-07-08). The latest upstream release in the v0.53.x line is **v0.53.8** (2026-07-27), which upstream marks **state-breaking** and describes as containing "important security fixes" with a recommendation to upgrade via a coordinated upgrade. We are ~5 patch releases / ~13 months behind.

## Current state

- Fork base: `v0.53.3` → `v0.53.3-ps19-observability`
- `cosmossdk.io/store`: base `v1.1.2` → `v1.1.2-ps1`
- Latest upstream v0.53.x: **v0.53.8**
- Intermediate releases we skipped: v0.53.4 (2025-07-25), v0.53.5 (2025-12-12), v0.53.6 (2026-02-10), v0.53.7 (2026-04-14)

## Why upgrade — what landed in v0.53.4 → v0.53.8

Everything through the last **formal** advisory is already in our v0.53.3 base — ISA-2025-005 (`GHSA-p22h-3m2v-cmgh`, distribution integer-overflow chain-halt) was fixed in v0.53.3. The gap is the *post-v0.53.3* patch releases, whose fixes touch modules we run:

- **auth** — nil-pointer panic guards in `GetSigningTxData` (including multisig with nil `Multi`/`BitArray`); reject transactions carrying extra `SignerInfo`s in `SetPubKeyDecorator`
- **crypto** — validate the secp256k1 pubkey SEC1 tag byte
- **tx / signing** — bound multisig signature & pubkey indexing by slice length; reject transactions with mismatched signer-info / signature counts; bound compact-bit-array index by element length
- **staking** — handle redelegation when the unbonded source has been removed
- **distribution** — strict + fallback behavior when withdrawing delegator rewards
- **store** — isolate the `traceContext` map across branched stores

Several of these are panic / availability-class (a malformed transaction reaching a nil-pointer path can halt a node) and signature-validation hardening. There is no known exploitation of our deployment, but running ~13 months behind on a security-patched consensus dependency is a standing risk we should close proactively.

## Proposed action

- [ ] Rebase our `psNN` patch set onto upstream `v0.53.8` (or cherry-pick the v0.53.4–v0.53.8 fixes if a full rebase is disruptive)
- [ ] Apply the same review to the `cosmossdk.io/store` fork (`v1.1.2-ps1` → latest `v1.1.x`)
- [ ] Re-run the fork test suite and prepare a coordinated (state-breaking) upgrade plan
- [ ] Add a lightweight process to watch upstream cosmos-sdk patch releases so the fork does not drift again

## References

- Upstream v0.53.8 release: https://github.com/cosmos/cosmos-sdk/releases/tag/v0.53.8
- Upstream v0.53.x releases: https://github.com/cosmos/cosmos-sdk/releases
- Cosmos SDK security advisories: https://github.com/cosmos/cosmos-sdk/security/advisories

</div>

---

> 🔄 **Auto-synced** from [Issue #1671](https://github.com/gonka-ai/gonka/issues/1671) every hour.
