---
title: "#849 — Bug: DKG permanent failure — dealer consensus uses unweighted participant votes but quorum uses slot weights"
source: https://github.com/gonka-ai/gonka/issues/849
issue_number: 849
synced_at: 2026-08-11T11:10:19Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Bug: DKG permanent failure — dealer consensus uses unweighted participant votes but quorum uses slot weights
    <span class="issues-number">#849</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/Mayveskii">@Mayveskii</a> opened 2026-03-03 12:04 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-03-12 22:56 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Location

`inference-chain/x/bls/keeper/phase_transitions.go` — lines 74 and 295–318

## Description

The DKG pipeline uses two independent threshold checks with **different weighting schemes** that are fundamentally inconsistent:

```go
// 1. Transition to VERIFYING — slot-weighted quorum (correct)
if slotsWithDealerParts > epochBLSData.ITotalSlots/2 { ... }

// 2. Dealer consensus — unweighted (count of participants, NOT slots)
dealerIsValid := totalVotes > 0 && validVotes > totalVotes/2
```

### Concrete failure scenario

Suppose:
- Participant A holds **60% of total slots**
- Participants B, C, D each hold **~13% of slots**

1. A submits dealer parts → `slotsWithDealerParts > ITotalSlots/2` → DKG transitions to **VERIFYING** ✓
2. B, C, D vote A's dealer **invalid** (3 vs 1 participant votes → majority by count)
3. A votes B, C, D invalid (1 vs 3 — minority by count)
4. `DetermineValidDealersWithConsensus` marks **all dealers invalid**
5. `ComputeGroupPublicKey` returns `"no valid dealers found"`
6. `CompleteDKG` returns an error → **DKG permanently stuck for this epoch**

B, C, D together hold only ~40% of slots and could never form a DKG quorum alone — yet they can destroy the epoch's DKG by voting as a participant-count majority.

### Root cause

`DetermineValidDealersWithConsensus` counts one vote per participant regardless of slot weight:

```go
for _, verification := range epochBLSData.VerificationSubmissions {
    if verification != nil && len(verification.DealerValidity) > 0 {
        totalVotes++
        if verification.DealerValidity[dealerIndex] {
            validVotes++
        }
    }
}
dealerIsValid := totalVotes > 0 && validVotes > totalVotes/2
```

While everywhere else in the DKG pipeline thresholds are measured in **slots**, not participant count.

## Impact

**High (DoS)** — a minority coalition of participants (by slot weight) can permanently break DKG for an epoch by voting down dealers that collectively hold a slot majority. This blocks threshold signing for the entire epoch.

## Fix Direction

Replace the unweighted participant vote count with a **slot-weighted vote** in `DetermineValidDealersWithConsensus`, consistent with how quorum is measured everywhere else:

```go
validSlots := uint32(0)
totalSlots := uint32(0)

for i, verification := range epochBLSData.VerificationSubmissions {
    if verification != nil && len(verification.DealerValidity) > 0 {
        participant := epochBLSData.Participants[i]
        slots := participant.SlotEndIndex - participant.SlotStartIndex + 1
        totalSlots += slots
        if dealerIndex < len(verification.DealerValidity) && verification.DealerValidity[dealerIndex] {
            validSlots += slots
        }
    }
}

dealerIsValid := totalSlots > 0 && validSlots > totalSlots/2
```

</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Mayveskii">@Mayveskii</a></span>
    <span class="issues-meta-item">commented 2026-03-03 12:56 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Fix submitted in PR #852</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/x0152">@x0152</a></span>
    <span class="issues-meta-item">commented 2026-03-12 20:08 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi @Mayveskii</p>
<p>As discussed in #852, this problem is already covered by issue #823
Could you please close this issue?</p>
<p>Thanks!</p>
<p>P.S. I think #848 could be closed as well (as we discussed in #851)</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #849](https://github.com/gonka-ai/gonka/issues/849) every hour.
