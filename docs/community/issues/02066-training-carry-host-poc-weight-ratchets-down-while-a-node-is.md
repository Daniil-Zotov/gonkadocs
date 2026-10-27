---
title: "#2066 — Training carry: host PoC weight ratchets down while a node is leased (training_carry.go)"
source: https://github.com/gonka-ai/gonka/issues/2066
issue_number: 2066
synced_at: 2026-10-27T14:38:46Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Training carry: host PoC weight ratchets down while a node is leased (training_carry.go)
    <span class="issues-number">#2066</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/maria-mitina">@maria-mitina</a> opened 2026-10-20 09:11 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-10-23 23:40 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

While a node is leased to a trainshard, the host's total PoC weight can only go down, never back up. Normal PoC noise on the host's free node and sub-100% cPoC readings get turned into a permanent, compounding loss for the whole lease.

## Observed (testnet-4, 2026-10-19, host `gonka1prkaq…`, shard 3, node-18213 leased at frozen weight 8946, blocks 4725–9725)

| epoch | node1 (fresh) | node-18213 (frozen) | total |
|---|---|---|---|
| 15 | 7154 | 8946 | 16100 |
| 16 | 7303 | 8797 | 16100 |
| 17 | 7303 | 8783 | 16086 |
| 18 | 7214 | 8783 | 15997 |
| 19 | 7214 | 8783 | 15997 |
| 20 | 7333 | 8664 | 15997 |
| 21 | 7184 | 8664 | 15848 |
| 22 | 7363 | 8485 | 15848 |

node1 is just wobbling ±1.5%; the trainshard record still says 8946. Total went 16100 → 15848 (−1.6%) in 7 epochs, ≈ −1.2T ngonka/epoch by the end. A max-length lease (5000 blocks ≈ 14 epochs) would lose several percent.

## Cause

`inference-chain/x/inference/module/training_carry.go`, `trainingCarryBudget.apply`:

```go
node.PocWeight = min(node.PocWeight, weight)        // frozen node never goes back up
allowed := confirmed[last epoch] − weight(free nodes)
if frozen > allowed { scale frozen nodes down }     // but does go down
```

- Free node measures higher → `allowed` shrinks → frozen node is clipped, total unchanged.
- Free node measures lower → frozen node stays at `min(prev, …)`, does not refill → total drops.
- `confirmed` is `EffectiveConfirmedWeight`, clamped ≤ full, so a 99.9% cPoC (36193/36225) also lowers the ceiling permanently.

Clipped values are written into the active participant and come back next epoch as the carry, so the drift compounds.

## Suggested fix

Keep the cap (host total ≤ last confirmed total — the anti-gaming intent is fine) but remove the one-way drift, e.g.:

- let the frozen node refill up to its reservation-time weight when `frozen < allowed`, or
- anchor `allowed` to the reservation-time (or max-over-lease) confirmed total instead of the immediately previous epoch.

## Repro

Lease one node of a two-node host for several epochs; observe `ComputeNewWeights: Merged preserved and PoC participant` in node logs — `preservedWeight` only ever decreases.

</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/x0152">@x0152</a></span>
    <span class="issues-meta-item">commented 2026-10-20 23:57 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>https://github.com/gonka-ai/gonka/pull/1790/commits/b7eda7f92e16d95a1b66b18bf54102815a68ba2c</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2066](https://github.com/gonka-ai/gonka/issues/2066) every hour.
