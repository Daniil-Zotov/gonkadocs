---
title: "#1081 — Binomial test p0 floor/ceiling mismatch — stricter downtime threshold silently never enforced"
source: https://github.com/gonka-ai/gonka/issues/1081
issue_number: 1081
synced_at: 2026-07-06T23:34:15Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Binomial test p0 floor/ceiling mismatch — stricter downtime threshold silently never enforced
    <span class="issues-number">#1081</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item">[@Doog-bot534](https://github.com/Doog-bot534) opened 2026-04-16 03:25 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-04-20 01:35 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content">
## Summary

A floor vs. ceiling inconsistency in `decimalToPermille` causes the dynamic p0 selection and the actual binomial test to use **different p0 tables**. Validators who should be punished under the stricter threshold pass the test using the more lenient table.

## Root Cause

**Files:**
- `x/inference/calculations/stats_table.go:705-711` — `decimalToPermille` uses `IntPart()` (floor)
- `x/inference/calculations/stats.go:91-94` — `MissedStatTest` calls `decimalToPermille` (floor)
- `x/inference/keeper/bitcoin_rewards.go:461` — `getDynamicP0` calls `decimalToPermilleCeil` (ceiling)
- `x/inference/keeper/bitcoin_rewards.go:471` — `ceilToSupportedP0Permille` maps to nearest supported table

**The mismatch:**
1. `getDynamicP0` selects p0 using **ceiling** permille conversion → e.g., `0.1004` → `101` → maps to p0=0.200 table (stricter)
2. `MissedStatTest` executes the test using **floor** permille conversion → `0.1004` → `100` → uses p0=0.100 table (more lenient)

**Result:** The system "thinks" it selected the stricter p0=0.200 threshold, but the actual test runs against p0=0.100. Validators who miss 15% of requests pass the p0=0.100 test but would fail p0=0.200.

## Exploit Scenario

1. Network conditions cause `getDynamicP0` to select a p0 value like 0.1004
2. The system logs that p0=0.200 threshold is in effect (ceiling path)
3. But `MissedStatTest` uses p0=0.100 table (floor path)
4. A validator strategically misses ~15% of validations
5. They pass the lenient test and collect full rewards
6. Under the intended stricter test (p0=0.200), they would be punished

## Impact

**High** — The entire dynamic downtime punishment system can be silently operating at a more lenient threshold than intended. Validators who should be penalized continue collecting full rewards.

## Suggested Fix

Use the same conversion function in both paths. Either:
- Change `MissedStatTest` to use `decimalToPermilleCeil` (enforce the stricter table)
- Or change `getDynamicP0` to use `decimalToPermille` (floor, consistent)

The first option is safer — when in doubt, enforce the stricter threshold.

---

## Additional Finding: Dynamic Pricing IntPart Truncation

**File:** `x/inference/keeper/dynamic_pricing.go:199-201`

`IntPart()` truncates toward zero. When `currentPrice` is small (1-10), repeated multiplication by `maxDecreasePerBlock` (e.g., 0.98) produces decimals like 0.98, which truncates to 0. Price gets stuck at `minPrice` and can only recover at ~2% of `minPrice` per block.

**Fix:** Use `Round(0)` instead of `IntPart()`.

## Additional Finding: Training RerankIfSomeNodesLeft Overwrites State

**File:** `x/inference/training/training_sync.go:588-593`

`SaveEpochState` is called twice — first with full state, then with active-only filtered state. The second call **overwrites** the first, permanently deleting dropped node records. If a node reconnects, its activity record is gone.

**Fix:** Single save of merged state.

---

Payout address: `gonka10zaal553duxp05nvfpqtsqrm2g0j6j34r8nan7`
</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@unameisfine](https://github.com/unameisfine)</span>
    <span class="issues-meta-item">commented 2026-04-19 19:22 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    Reviewed the code paths. I believe this mismatch is **not exploitable** in the current codebase — here's why:

**`getDynamicP0` always returns an exact permille**

`getDynamicP0` (bitcoin_rewards.go:558) returns `permilleToP0Decimal(finalPermille)`, where `finalPermille` is always one of the supported table values (50, 100, 200, 300, 400, 500) — produced by `ceilToSupportedP0Permille`.

`permilleToP0Decimal(100)` → `Decimal{Value: 100, Exponent: -3}` → exactly `0.100`.

When `MissedStatTest` receives this value: `0.100 * 1000 = 100.0` → `IntPart() = 100` → selects the correct table. Floor and ceiling are identical for exact permille values.

**The bypass case is also safe**

The only path where a non-rounded p0 reaches `MissedStatTest` is when governance sets `BinomTestP0 > 0.500` (bitcoin_rewards.go:476 — returns the raw governance value). In that case, `decimalToPermille` returns `-1` (unsupported), and `MissedStatTest` correctly falls back to the exact `BinomialPValue` computation (stats.go:96-101) — no table lookup involved.

**The inconsistency is real, the exploit scenario is not**

The two functions (`decimalToPermille` floor vs `decimalToPermilleCeil` ceil) do use different rounding, but because `getDynamicP0` always snaps to an exact supported permille before returning, the floor/ceiling difference never manifests in practice. The described scenario (p0=0.1004 using different tables) cannot occur — `getDynamicP0` would map 0.1004 to 0.200 before it ever reaches `MissedStatTest`.

Unifying the rounding functions is still reasonable as defensive hardening, but the severity should be Low (code smell) rather than High (active exploit).
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@Doog-bot534](https://github.com/Doog-bot534)</span>
    <span class="issues-meta-item">commented 2026-04-20 01:35 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    Thanks @unameisfine for the thorough walkthrough — you're right, and I've reverified against the code paths.

**Confirmed on my side:**

1. `getDynamicP0` always returns `permilleToP0Decimal(finalPermille)` where `finalPermille` ∈ {50, 100, 200, 300, 400, 500} after `ceilToSupportedP0Permille`. The returned `Decimal{Value: N, Exponent: -3}` is exactly `N/1000`, so `decimalToPermille` (floor) produces the same permille as the ceiling-based selection — no mismatch reaches `MissedStatTest`.
2. The governance `BinomTestP0 > 0.500` path returns the raw value, `decimalToPermille` returns `-1`, and `MissedStatTest` falls back to the exact `BinomialPValue` computation (stats.go:96-101). No table lookup, no rounding mismatch.
3. The claim-rewards path (`msg_server_claim_rewards.go:264`) uses raw governance `BinomTestP0` but does not go through any ceiling-based selection, so the described divergence scenario also can't manifest there.

The two rounding functions do diverge in isolation, but every production caller snaps to an exact permille before reaching the stat test. The exploit scenario as I described it is not reachable on current `main`.

Downgrading severity assessment to **Low / code hygiene** — unifying the rounding helpers would still be reasonable defensive cleanup, but this is not an active vulnerability. Closing to keep the queue clean. Apologies for the noise.
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1081](https://github.com/gonka-ai/gonka/issues/1081) every hour.
