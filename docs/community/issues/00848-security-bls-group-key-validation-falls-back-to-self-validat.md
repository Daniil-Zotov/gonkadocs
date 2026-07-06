---
title: "#848 — Security: BLS group key validation falls back to self-validation when previous epoch data is missing"
source: https://github.com/gonka-ai/gonka/issues/848
issue_number: 848
synced_at: 2026-07-06T09:52:38Z
template: issues-main.html
---

> 🔄 **Auto-synced:** from [Issue #848](https://github.com/gonka-ai/gonka/issues/848) every 6 hours. 

# 🔴 Security: BLS group key validation falls back to self-validation when previous epoch data is missing

**Author:** [@Mayveskii](https://github.com/Mayveskii) · **State:** Closed · **Created:** 2026-03-03 12:03 UTC · **Updated:** 2026-03-12 22:56 UTC

---

## 📝 Описание

## Location

`inference-chain/x/bls/keeper/msg_server_group_validation.go` — lines 64–74

## Description

When `GetEpochBLSData` fails with `ErrEpochBLSDataNotFound` for the previous epoch, the code silently falls back to using the **new epoch's own data** as the previous epoch:

```go
previousEpochBLSData, err := ms.GetEpochBLSData(ctx, previousEpochId)
if err != nil {
    if errors.Is(err, types.ErrEpochBLSDataNotFound) {
        previousEpochBLSData = newEpochBLSData // fallback to self
    }
}
```

This creates **circular self-validation**:
- Participants are looked up from `previousEpochBLSData` — which is now the **new epoch's own participants**
- Slot public keys for per-slot signature verification come from `newEpochBLSData.SlotPublicKeys`
- The final aggregated signature is verified against `previousEpochBLSData.GroupPublicKey` — which is now the **new epoch's own group key**

Result: any participant in epoch N can sign and submit a valid group key validation for epoch N using epoch N's own keys — completely bypassing the intended cross-epoch chain-of-custody.

## When This Triggers

- Previous epoch BLS data was pruned (expected over time)
- State sync or snapshot restore on a new node
- First epoch after a chain upgrade where old BLS data is absent

## Impact

**Critical (security)** — the cryptographic chain-of-custody for group key transitions is bypassed. A single malicious participant can self-certify a new group key without legitimate cross-epoch consensus.

## Fix Direction

Return an error instead of silently falling back:

```go
if errors.Is(err, types.ErrEpochBLSDataNotFound) {
    return nil, fmt.Errorf("previous epoch %d BLS data not found, cannot validate group key", previousEpochId)
}
```

If bootstrapping for the very first epoch is required, handle it explicitly with a dedicated flag/check rather than a silent fallback.


---

## 💬 Comments (2)

### Комментарий 1 — [@Mayveskii](https://github.com/Mayveskii)

*2026-03-03 12:15 UTC*

Investigated the fallback path at line 74 of `msg_server_group_validation.go`.

When `previousEpochBLSData` is not found, the code assigns `previousEpochBLSData = newEpochBLSData`.
This means:
1. `verifyBLSPartialSignatureBlst` checks signatures against the new epoch's own slot keys
2. `verifyFinalSignatureBlst` checks the aggregate against the new epoch's own `GroupPublicKey`

A validator who controls epoch N's DKG output can trigger this path to get epoch N+1's key
accepted without any external verification. Fix: return error when previous epoch data is missing.

PR: https://github.com/Mayveskii/gonka/pull/new/fix/848-bls-self-validation

### Комментарий 2 — [@Mayveskii](https://github.com/Mayveskii)

*2026-03-03 12:16 UTC*

> Investigated the fallback path at line 74 of `msg_server_group_validation.go`.
> 
> When `previousEpochBLSData` is not found, the code assigns `previousEpochBLSData = newEpochBLSData`. This means:
> 
> 1. `verifyBLSPartialSignatureBlst` checks signatures against the new epoch's own slot keys
> 2. `verifyFinalSignatureBlst` checks the aggregate against the new epoch's own `GroupPublicKey`
> 
> A validator who controls epoch N's DKG output can trigger this path to get epoch N+1's key accepted without any external verification. Fix: return error when previous epoch data is missing.
> 
> PR: https://github.com/Mayveskii/gonka/pull/new/fix/848-bls-self-validation

## Summary

Closes #848

When `GetEpochBLSData` for `previousEpochId` returned `ErrEpochBLSDataNotFound`,
the handler silently fell back to `previousEpochBLSData = newEpochBLSData`.

This allowed any epoch to self-certify its own group key:
- partial signatures were verified against the **new epoch's own** individual keys
- the aggregated final signature was verified against the **new epoch's own** `GroupPublicKey`

The chain-of-trust between epochs was completely bypassed.

## Fix

Removed the fallback entirely. When previous epoch data is unavailable, the handler
now returns an explicit error. This is the only correct behavior — group key validation
is meaningless without an independent previous epoch as the verifier.

## Files changed

- `inference-chain/x/bls/keeper/msg_server_group_validation.go`
  - removed unused `errors` import
  - replaced 13-line silent fallback with a hard error return
