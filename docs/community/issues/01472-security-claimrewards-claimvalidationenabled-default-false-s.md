---
title: "#1472 — Security: ClaimRewards — ClaimValidationEnabled default false; sample RNG uses claim-time block hash"
source: https://github.com/gonka-ai/gonka/issues/1472
issue_number: 1472
synced_at: 2026-07-22T16:52:38Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Security: ClaimRewards — ClaimValidationEnabled default false; sample RNG uses claim-time block hash
    <span class="issues-number">#1472</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/Aphelios01-sdk">@Aphelios01-sdk</a> opened 2026-07-18 03:05 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-07-18 03:08 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

Two related issues in `MsgClaimRewards` integrity:

### A) `ClaimValidationEnabled` defaults to `false` (also forced false in upgrade v0.2.11)

When false, `validateClaim` (seed check + missed-validation statistical test) is skipped; handler goes straight to `payoutClaim` after basic settle checks.

### B) When validation is enabled, must-validate membership uses reservoir sampling (max 10000) seeded by **claim-time** `ctx.HeaderInfo().Hash`

`ShouldValidate(msg.Seed, …)` is deterministic from the settled seed (good), but **which inferences are checked** can be influenced by when the claimant submits (grind block hashes) if `filteredCount > 10000`.

## Affected

- `inference-chain/x/inference/keeper/msg_server_claim_rewards.go`
- `inference-chain/x/inference/types/params.go` (`ClaimValidationEnabled: false`)
- `inference-chain/app/upgrades/v0_2_11/upgrades.go`
- `const maxInferenceSampleSize = 10000`

## Relevant source

```go
if params.ValidationParams != nil && params.ValidationParams.ClaimValidationEnabled {
    // validateClaim ...
}
// else: skip duty enforcement
payoutClaim(...)
```

```go
blockHash := ctx.HeaderInfo().Hash
blockHashSeed := int64(binary.BigEndian.Uint64(blockHash[:8]))
rng := rand.New(rand.NewSource(blockHashSeed))
// reservoir sample then ShouldValidate(msg.Seed, ...)
```

## Impact

- Flag off: hosts can claim work/reward coins without on-chain validation-duty enforcement
- Flag on + high volume: sample grinding may reduce detected misses

## Suggested remediation

1. Re-enable claim validation only after fixing sample entropy
2. Seed sampling with epoch-fixed material (e.g. settle seed / epoch hash), not claim-time header hash
3. Or fix must-set at end-of-epoch before claim
4. Tests: claim block hash must not change must-validate set for same settle state

## Disclosure

Static analysis + local logic proofs only. Prefer HackerOne if public issues are out of process.
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Aphelios01-sdk">@Aphelios01-sdk</a></span>
    <span class="issues-meta-item">commented 2026-07-18 03:07 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Closing to focus disclosure on the highest-priority finding: https://github.com/gonka-ai/gonka/issues/1470 (SSRF via InferenceUrl). Other items can be re-opened or filed via HackerOne if needed.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1472](https://github.com/gonka-ai/gonka/issues/1472) every hour.
