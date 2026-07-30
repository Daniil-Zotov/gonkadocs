---
title: "#933 — AdjustWeightsByCollateral missing baseWeightRatio range validation — weight inflation for uncollateralized participants"
source: https://github.com/gonka-ai/gonka/issues/933
issue_number: 933
synced_at: 2026-07-30T03:36:47Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    AdjustWeightsByCollateral missing baseWeightRatio range validation — weight inflation for uncollateralized participants
    <span class="issues-number">#933</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/unameisfine">@unameisfine</a> opened 2026-03-23 01:42 UTC</span>
    <span class="issues-meta-item">3 comments</span>
    <span class="issues-meta-item">Updated 2026-04-27 22:28 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
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
</div>

---

## 💬 Comments (3)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-03-23 05:10 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@unameisfine, new issues need to go through the triage process first. To help move things forward a bit faster, I’d recommend posting them in Discord or any other available channels so the community can take a look and share early feedback.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/gmorgachev">@gmorgachev</a></span>
    <span class="issues-meta-item">commented 2026-04-26 20:00 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <blockquote>
<p>If governance sets baseWeightRatio &gt;= 1.0</p>
</blockquote>
<p>why would do that? that's contradict of the idea of base weight ratio</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/unameisfine">@unameisfine</a></span>
    <span class="issues-meta-item">commented 2026-04-26 22:03 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Fair point — governance setting an invalid ratio is unrealistic. Closing the PR.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #933](https://github.com/gonka-ai/gonka/issues/933) every hour.
