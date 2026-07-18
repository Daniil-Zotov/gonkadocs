---
title: "#1079 — Deep Security Audit: BLS/DKG protocol, state machine consistency, and economic logic vulnerabilities"
source: https://github.com/gonka-ai/gonka/issues/1079
issue_number: 1079
synced_at: 2026-07-18T09:50:24Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Deep Security Audit: BLS/DKG protocol, state machine consistency, and economic logic vulnerabilities
    <span class="issues-number">#1079</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/Doog-bot534">@Doog-bot534</a> opened 2026-04-16 03:20 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-04-28 16:59 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

Follow-up deep audit to #1053, focusing on **logic bugs, economic attacks, and protocol-level vulnerabilities** that require understanding business logic — not surface-level input validation.

## Fix PRs Submitted

| PR | Severity | Issue |
|----|----------|-------|
| #1077 | **Critical** | BLS SetParams skips Validate() — governance can manipulate signing threshold |
| #1078 | **High** | Zero-request participants bypass downtime punishment — free-riding economic attack |

## Additional Findings (No PR Yet)

### BLS/DKG Protocol

**1. [HIGH] Self-validation fallback when previous epoch missing**
- `x/bls/keeper/msg_server_group_validation.go:68-74`
- When previous epoch BLS data is not found, falls back to `previousEpochBLSData = newEpochBLSData`. New epoch participants validate their own key — circular trust violation.
- **Impact**: Defeats cross-epoch key validation security model.

**2. [MEDIUM] No on-chain commitment verification in DKG dealing phase**
- `x/bls/keeper/msg_server_dealer.go:49-73`
- `SubmitDealerPart` accepts commitments with only structural validation. No verification that commitments are valid G2 points.

**3. [MEDIUM] Verification votes are unproven boolean assertions**
- `x/bls/keeper/msg_server_verifier.go:58-65`
- `SubmitVerificationVector` accepts boolean array with no proof verifier actually checked shares. 51% collusion can exclude honest dealers.

### State Machine Consistency

**4. [HIGH] failedFinish returns response not error — double payment vulnerability**
- `x/inference/keeper/msg_server_finish_inference.go:150-156`
- If `SetParticipant` succeeds but `SetInference` fails, `failedFinish` returns `(response, nil)`. Cosmos SDK commits the cache context (participant paid), but inference isn't marked finished. A second `FinishInference` can pay the executor again.
- **Impact**: Direct double payment for the same inference.

**5. [HIGH] Pruning deletes inferences with active validation/invalidation**
- `x/inference/keeper/pruning.go:78-83`
- Pruning removes inferences by epoch threshold without checking if invalidation proposals are still pending. If invalidated after pruning, `GetInference` fails and the executor keeps ill-gotten earnings permanently.
- **Impact**: No recourse for invalidated inferences — executor retains payment.

**6. [MEDIUM] No status guard on InvalidateInference — can invalidate EXPIRED inferences**
- `x/inference/keeper/msg_server_invalidate_inference.go:12-62`
- Does not check inference is in FINISHED/COMPLETED status. An EXPIRED inference (already refunded) can be invalidated, potentially triggering a second refund.

### Economic Logic

**7. [MEDIUM] Epoch underflow in bitcoin_rewards — governance griefing**
- `x/inference/keeper/bitcoin_rewards.go:585`
- `epochsSinceGenesis := currentEpoch - bitcoinParams.GenesisEpoch` — unsigned subtraction with no underflow guard. Governance can set `GenesisEpoch > currentEpoch`, wrapping to ~2^64 and killing all reward emissions.

**8. [MEDIUM] CollateralPerWeightUnit=0 silently disables collateral model**
- `x/inference/keeper/collateral.go:102-104`
- Zero value is warned but not rejected. Any non-zero collateral deposit activates 100% weight. Slashing computes zero required collateral. Governance can silently disable the entire collateral security model.

## Methodology

- Manual deep-dive into business logic, reward calculations, cryptographic protocols, and state machine transitions
- Focus on exploitable logic rather than input validation
- Cross-referenced with existing fixes (PR #948 CacheContext, #1013 escrow fund loss)

Payout address: `gonka10zaal553duxp05nvfpqtsqrm2g0j6j34r8nan7`
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/x0152">@x0152</a></span>
    <span class="issues-meta-item">commented 2026-04-28 16:59 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi,
Thanks for the deep audit!</p>
<p>I am closing this issue for now because several findings are based on incorrect assumptions about how the code currently works, and some points are already addressed in recent changes. </p>
<p>If you believe a specific issue is still valid, please open a separate issue with a clear reproduction case, and I will review it again</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1079](https://github.com/gonka-ai/gonka/issues/1079) every hour.
