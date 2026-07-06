---
title: "#849 — Bug: DKG permanent failure — dealer consensus uses unweighted participant votes but quorum uses slot weights"
source: https://github.com/gonka-ai/gonka/issues/849
issue_number: 849
synced_at: 2026-07-06T09:52:38Z
---

> 🔄 **Авто-синхронизация:** из [Issue #849](https://github.com/gonka-ai/gonka/issues/849) каждые 6 часов. 

# 🔴 Bug: DKG permanent failure — dealer consensus uses unweighted participant votes but quorum uses slot weights

**Автор:** [@Mayveskii](https://github.com/Mayveskii) · **Состояние:** Closed · **Создано:** 2026-03-03 12:04 UTC · **Обновлено:** 2026-03-12 22:56 UTC

---

## 📝 Описание

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


---

## 💬 Комментарии (2)

### Комментарий 1 — [@Mayveskii](https://github.com/Mayveskii)

*2026-03-03 12:56 UTC*

Fix submitted in PR #852

### Комментарий 2 — [@x0152](https://github.com/x0152)

*2026-03-12 20:08 UTC*

Hi @Mayveskii

As discussed in #852, this problem is already covered by issue #823
Could you please close this issue?

Thanks!

P.S. I think #848 could be closed as well (as we discussed in #851)
