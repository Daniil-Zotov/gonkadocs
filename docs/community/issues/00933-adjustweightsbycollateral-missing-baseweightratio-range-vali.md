---
title: "#933 — AdjustWeightsByCollateral missing baseWeightRatio range validation — weight inflation for uncollateralized participants"
source: https://github.com/gonka-ai/gonka/issues/933
issue_number: 933
synced_at: 2026-07-06T09:52:13Z
---

> 🔄 **Авто-синхронизация:** из [Issue #933](https://github.com/gonka-ai/gonka/issues/933) каждые 6 часов. 

# 🔴 AdjustWeightsByCollateral missing baseWeightRatio range validation — weight inflation for uncollateralized participants

**Автор:** [@unameisfine](https://github.com/unameisfine) · **Состояние:** Closed · **Создано:** 2026-03-23 01:42 UTC · **Обновлено:** 2026-04-27 22:28 UTC

---

## 📝 Описание

## Description

`calculateRequiredCollateral` (collateral.go:53) correctly validates that `baseWeightRatio` is in the range [0, 1):

```go
if err != nil || bwr.IsNegative() || bwr.GTE(math.LegacyOneDec()) {
    return math.ZeroInt()
}
```

`AdjustWeightsByCollateral` (collateral.go:100) converts the same parameter but has no equivalent guard. If governance sets `baseWeightRatio >= 1.0`:

- `baseWeight = potentialWeight × ratio` exceeds `potentialWeight`
- `collateralEligibleWeight = potentialWeight - baseWeight` goes negative
- Participant **without** collateral: `effectiveWeight = baseWeight` (inflated)
- Participant **with** collateral: `activatedWeight = min(negative, positive) = negative`, so effective weight is reduced

Example with `baseWeightRatio = 1.5`, `potentialWeight = 100`:
- No collateral: `effectiveWeight = 150` (50% inflation)
- With collateral: `effectiveWeight = 100` (normal)

This inverts the collateral incentive — participants are rewarded for NOT depositing collateral.

## Fix

Add the same range guard after `baseWeightRatio` conversion in `AdjustWeightsByCollateral`:

```go
if baseWeightRatio.IsNegative() || baseWeightRatio.GTE(math.LegacyOneDec()) {
    return fmt.Errorf("base_weight_ratio %s is out of valid range [0, 1)", baseWeightRatio.String())
}
```

---

## 💬 Комментарии (3)

### Комментарий 1 — [@tcharchian](https://github.com/tcharchian)

*2026-03-23 05:10 UTC*

@unameisfine, new issues need to go through the triage process first. To help move things forward a bit faster, I’d recommend posting them in Discord or any other available channels so the community can take a look and share early feedback.

### Комментарий 2 — [@gmorgachev](https://github.com/gmorgachev)

*2026-04-26 20:00 UTC*

> If governance sets baseWeightRatio >= 1.0

why would do that? that's contradict of the idea of base weight ratio

### Комментарий 3 — [@unameisfine](https://github.com/unameisfine)

*2026-04-26 22:03 UTC*

Fair point — governance setting an invalid ratio is unrealistic. Closing the PR.
