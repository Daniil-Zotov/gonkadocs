---
title: "#1395 — fix(inference): power cap zeros network when zero-weight participants are in settlement"
source: https://github.com/gonka-ai/gonka/issues/1395
issue_number: 1395
synced_at: 2026-08-10T23:53:56Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    fix(inference): power cap zeros network when zero-weight participants are in settlement
    <span class="issues-number">#1395</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/maria-mitina">@maria-mitina</a> opened 2026-07-04 11:58 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-07-08 23:18 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Problem

On **gonka-testnet-4**, epoch 15 settlement zeroed all participant weights and cascaded into epochs 16–20 with `total_weight=0` and no active epoch members.

Chain logs at settlement (block ~5305):

```
weight_group model=Qwen/Qwen2.5-7B-Instruct raw_total=81702 scale=1.0
weight_pipeline addr=gonka1e8yj… consensus=34658 final=0 modes=7B:DIRECT
weight_pipeline addr=gonka1m6s8… consensus=0 final=0 modes=7B:NONE
Universal power capping applied originalTotalPower=81702 cappedTotalPower=0
Adding member … weight=0  (all 4 participants)
```

Consensus weights were computed correctly (~81k total on 7B). **Universal power capping** then collapsed everything to zero.

## Root cause

### Why a zero-weight host is still in settlement

`ComputeNewWeights` includes participants who **passed PoC on any model** (or are preserved). There is no filter for “will have non-zero consensus weight on an eligible group.”

Later, `ComputeConsensusWeights` overwrites `p.Weight` from eligible groups only. A host that mined **4B** but where only **7B** is eligible gets `consensus=0` — but **stays in `activeParticipants`**.

### Why power capping zeroed everyone

`applyEpochPowerCapping` passes the full `activeParticipants` slice to `CalculateOptimalCap` with no `Weight > 0` filter.

The algorithm used **participant headcount** (`len(participants) == 4`) in the 30% threshold formula, including the zero-weight guardian. Sorted powers: `[0, 10238, 34658, 36806]`.

When the first **positive** weight triggered the cap with `sumPrev=0`:

```
cap = (0.30 * 0) / (1 - 0.30 * 3) = 0
```

Every host was then capped to 0.

**Collateral was not involved** (`grace_period_end_epoch=180`, grace skip logged).

### Contributing testnet conditions (not required to trigger the bug)

- Botched 4B→7B transition: PoC mined on 4B, hardware reassigned join hosts to 7B
- Only 7B eligible at settlement (4B failed VMin after join hosts moved)
- Guardian had `modes=7B:NONE` (no delegation tx) and `consensus=0` on 7B

On mainnet steady state, a delegating non-7B host would still have `consensus=0` on the sole eligible group but often positive weight from another eligible model. The bug also applies during **model bootstrap** when old-model miners sit in `activeParticipants` with `Weight=0`.

## Proposed fix

**Files to change:**

| File | Change |
|------|--------|
| `inference-chain/x/inference/keeper/bitcoin_rewards.go` | `CalculateOptimalCap`: skip `Weight <= 0` in threshold math; use `positiveCount` instead of headcount; bail out if `cap <= 0 && totalPower > 0` |
| `inference-chain/x/inference/keeper/bitcoin_rewards_test.go` | Add regression test for epoch-15 scenario |

**Reference commit:** `7f3c00e95` on branch `do/guardian-tiebreaker-weightless-votes` (PR #1394 was closed; re-apply from this commit).

### `bitcoin_rewards.go` — key changes in `CalculateOptimalCap`

1. Build `participantPowers` only from entries with `Weight > 0`
2. Early return if `positiveCount <= 1`
3. Use `positiveCount` (not `len(participants)`) in threshold loop and cap formula
4. Safety net: if computed `cap <= 0` while `totalPower > 0`, return unchanged (no capping)
5. Apply step unchanged: still iterates all participants; zero-weight entries stay zero

```go
participantPowers := make([]ParticipantPowerInfo, 0, participantCount)
for i, participant := range participants {
    if participant.Weight <= 0 {
        continue
    }
    participantPowers = append(participantPowers, ParticipantPowerInfo{...})
}

positiveCount := len(participantPowers)
if positiveCount <= 1 {
    return participants, totalPower, false
}

// threshold loop uses positiveCount instead of participantCount
// ...

if cap <= 0 && totalPower > 0 {
    return participants, totalPower, false
}
```

### `bitcoin_rewards_test.go` — regression test

```go
func TestApplyPowerCappingForWeights_SkipsZeroWeightParticipants(t *testing.T) {
    participants := []*types.ActiveParticipant{
        {Index: "guardian", Weight: 0},
        {Index: "host-a", Weight: 10238},
        {Index: "host-b", Weight: 34658},
        {Index: "host-c", Weight: 36806},
    }
    capped, wasCapped := ApplyPowerCappingForWeights(participants)
    // total must remain positive; guardian stays at 0
}
```

## Test plan

```bash
go test ./inference-chain/x/inference/keeper/ -run TestApplyPowerCappingForWeights_SkipsZeroWeightParticipants -count=1
go test ./inference-chain/x/inference/module/ -run TestApplyPowerCapping -count=1
```

## Related code paths (for reviewers)

- Settlement: `inference-chain/x/inference/module/module.go` — `onEndOfPoCValidationStage` → `applyEpochPowerCapping`
- Cap entry: `inference-chain/x/inference/module/power_capping.go` → `ApplyPowerCapping`
- Cap algorithm: `inference-chain/x/inference/keeper/bitcoin_rewards.go` — `ApplyPowerCappingForWeights`, `CalculateOptimalCap`
- Design (original, no zero-weight filter): `proposals/early-network-protection/early-network-protection-plan.md`

## Optional follow-ups (separate from this fix)

- Filter or document zero-weight `activeParticipants` before power capping at the call site
- Harden multi-model transition: build delegation groups from PoC-proven models before `setModelsForParticipants` (`model_assignment.go`)
- Require bootstrap delegation before sole-eligible-group settlement during model rollout
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/maria-mitina">@maria-mitina</a></span>
    <span class="issues-meta-item">commented 2026-07-08 23:18 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>fixed, thank you @DimaOrekhovPS </p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1395](https://github.com/gonka-ai/gonka/issues/1395) every hour.
