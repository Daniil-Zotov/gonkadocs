---
title: "#1671 — chore(deps): rebase forked cosmos-sdk onto v0.53.8 (base is v0.53.3, ~5 patch releases behind)"
source: https://github.com/gonka-ai/gonka/issues/1671
issue_number: 1671
synced_at: 2026-11-14T03:22:56Z
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
    <span class="issues-meta-item"><a href="https://github.com/kaileido">@kaileido</a> opened 2026-08-28 20:22 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-11-07 05:02 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #ebe335; color: #24292f; border-color: #ebe335;">release-candidate</span></div>
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

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/kaileido">@kaileido</a></span>
    <span class="issues-meta-item">commented 2026-11-07 05:02 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Status check against <code>v0.53.3-ps19-observability</code> (pinned by <code>main</code>, <code>upgrade-v0.2.16</code>, <code>upgrade-v0.2.17</code> and <code>upgrade-v0.2.18</code>): none of the 55 upstream commits between <code>v0.53.3</code> and <code>v0.53.8</code> is in the fork, either by SHA or as a cherry-pick (checked by upstream PR number, subject and patch lines). 15 of them are fixes in runtime code:</p>
<table>
<thead>
<tr>
<th>upstream commit</th>
<th>subject</th>
</tr>
</thead>
<tbody>
<tr>
<td><a href="https://github.com/cosmos/cosmos-sdk/commit/c49441c822c684ada79bef2522347f3c6837502e">c49441c822</a></td>
<td>fix(crypto): validate secp256k1 pubkey SEC1 tag byte (#26665)</td>
</tr>
<tr>
<td><a href="https://github.com/cosmos/cosmos-sdk/commit/b2b06d578717ee40d81bebc1e8ec14b09931d860">b2b06d5787</a></td>
<td>fix: bound compact bit array index by elems length (#26662)</td>
</tr>
<tr>
<td><a href="https://github.com/cosmos/cosmos-sdk/commit/a13c0f9fb987d8b3504bb5e044b5938e0716ccc6">a13c0f9fb9</a></td>
<td>fix(x/auth/ante): reject tx with extra SignerInfos in SetPubKeyDecorator (#26663)</td>
</tr>
<tr>
<td><a href="https://github.com/cosmos/cosmos-sdk/commit/e640d9b41b0ffb9c184953d2894223889eb7ad1f">e640d9b41b</a></td>
<td>fix: reject tx with mismatched signer info and signature counts (#26653)</td>
</tr>
<tr>
<td><a href="https://github.com/cosmos/cosmos-sdk/commit/a35744565a420527d84410db04028e1cbfa4ef6c">a35744565a</a></td>
<td>fix(x/auth/tx): avoid nil pointer panic in GetSigningTxData for multisig ModeInfo with a nil Multi or nil Bitarray</td>
</tr>
<tr>
<td><a href="https://github.com/cosmos/cosmos-sdk/commit/a91a822eb2339d563bbe8c7bc61d71fa6c6c60e2">a91a822eb2</a></td>
<td>fix(x/auth/tx): avoid nil pointer panic in GetSigningTxData (#26661)</td>
</tr>
<tr>
<td><a href="https://github.com/cosmos/cosmos-sdk/commit/45d48b3a1bad01483b169e10af6ff5f0a25df793">45d48b3a1b</a></td>
<td>fix: bound multisig signature and pubkey indexing by slice lengths (#26651)</td>
</tr>
<tr>
<td><a href="https://github.com/cosmos/cosmos-sdk/commit/d46c6303eef713ffc05017b66ed279db119af609">d46c6303ee</a></td>
<td>fix(x/distribution): return errors for missing historical rewards internally (#26655)</td>
</tr>
<tr>
<td><a href="https://github.com/cosmos/cosmos-sdk/commit/e1a737ffc2d6f6fff963f6fe0165ca7b0db1624f">e1a737ffc2</a></td>
<td>fix(distribution): add strict + fallback behavior when withdrawing delegator rewards (#26410)</td>
</tr>
<tr>
<td><a href="https://github.com/cosmos/cosmos-sdk/commit/91a3dd6a1c42a7a84aa4facafd1c378314140440">91a3dd6a1c</a></td>
<td>fix(x/staking): handle redelegation when unbonded source is removed (#26417)</td>
</tr>
<tr>
<td><a href="https://github.com/cosmos/cosmos-sdk/commit/3fcf23af3f3131df0ab33eb0bd67398ed1957584">3fcf23af3f</a></td>
<td>fix(store/cachemulti): isolate traceContext map across branched stores (#25841)</td>
</tr>
<tr>
<td><a href="https://github.com/cosmos/cosmos-sdk/commit/d9d77304fd3d08c98e55e083975b770b63625cf7">d9d77304fd</a></td>
<td>fix: limit pagination (#25871)</td>
</tr>
<tr>
<td><a href="https://github.com/cosmos/cosmos-sdk/commit/4379cc49ae65632614096e8e382bf620b1beae13">4379cc49ae</a></td>
<td>fix(baseapp): index pre-block events (#25643)</td>
</tr>
<tr>
<td><a href="https://github.com/cosmos/cosmos-sdk/commit/e1bc1f93f42f51d0275654ccd52fa267fff3e23d">e1bc1f93f4</a></td>
<td>fix: add missing close when graceful shutdown (#25634)</td>
</tr>
<tr>
<td><a href="https://github.com/cosmos/cosmos-sdk/commit/d9e50213610c9f22a192415d563cf9b6cdfe11cd">d9e5021361</a></td>
<td>fix(cli): failed to convert address field in withdraw-validator-commission (#25489)</td>
</tr>
</tbody>
</table>
<p>The x/distribution and x/staking files touched by e1a737ff, 91a3dd6a and d46c6303 are patched in the fork, so those three need a manual merge; the other twelve touch files unchanged in the fork since <code>v0.53.3</code>.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1671](https://github.com/gonka-ai/gonka/issues/1671) every hour.
