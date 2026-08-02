---
title: "#1450 — Dynamic pricing: price pinned at min by integer truncation; capacity proxy miscalibrated per model"
source: https://github.com/gonka-ai/gonka/issues/1450
issue_number: 1450
synced_at: 2026-08-02T03:58:45Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Dynamic pricing: price pinned at min by integer truncation; capacity proxy miscalibrated per model
    <span class="issues-number">#1450</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/len5ky">@len5ky</a> opened 2026-07-14 18:26 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-07-24 18:11 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Reporting two verified defects in the dynamic-pricing keeper. Everything below
was checked against tag `release/v0.2.13` (the mainnet chain version) and
against live mainnet state via `node3.gonka.ai` on 2026-07-14. I run a
high-volume reseller on top of Gonka inference, so how the per-token price
responds to load matters directly — that's why I went through this code path
carefully.

Two separate problems, one small and mechanical, one structural. The mechanical
one is the more urgent: as of today, **every model's price on mainnet
is pinned at 1 ngonka, and the utilization-driven update cannot raise it at any
utilization under current params — only a param, code, or state intervention can.**

---

## 1. Integer truncation makes the price floor an absorbing state

### The code

`CalculateModelDynamicPrice` computes the new price as a decimal and truncates
toward zero — in both branches:

[`inference-chain/x/inference/keeper/dynamic_pricing.go#L205-L216`](https://github.com/gonka-ai/gonka/blob/release/v0.2.13/inference-chain/x/inference/keeper/dynamic_pricing.go#L205-L216)

```go
} else {
    // Above stability zone - increase price (with cap)
    utilizationExcess := utilization.Sub(upperBound)
    adjustmentFactor := one.Add(utilizationExcess.Mul(elasticity))

    // Apply maximum increase cap (2% per block)
    if adjustmentFactor.GreaterThan(maxIncreasePerBlock) {
        adjustmentFactor = maxIncreasePerBlock
    }

    newPriceDec := decimal.NewFromUint64(currentPrice).Mul(adjustmentFactor)
    newPrice = uint64(newPriceDec.IntPart())          // <-- truncation
```

The maximum increase per block is ×1.02 (elasticity 0.05 × max excess 0.40).
With integer prices, `floor(p × 1.02) > p` requires **p ≥ 50**. For any price of
49 ngonka or below, the increase branch is a no-op at *any* utilization:

```
p = 1:   1 × 1.02 = 1.02  → IntPart → 1
p = 49: 49 × 1.02 = 49.98 → IntPart → 49
p = 50: 50 × 1.02 = 51.0  → IntPart → 51   (first price that can move up)
```

Decreases keep working all the way down to the floor clamp (truncation *helps*
them: 2 × 0.98 = 1.96 → 1), and the `MinPerTokenPrice` clamp
([#L223-L228](https://github.com/gonka-ai/gonka/blob/release/v0.2.13/inference-chain/x/inference/keeper/dynamic_pricing.go#L223-L228))
is applied *after* truncation, so with `min_per_token_price = 1` it doesn't
rescue anything. Net effect: **any stored price below 50 ngonka is a one-way
trap for the utilization mechanism.** Prices can fall into the 1–49 range but can
never climb out of it through utilization alone, regardless of demand. The only
other writers of the price map are the grace-period initializer (below) and the
missing-price fallback to `base_per_token_price` for a model with no stored price
([#L151-L157](https://github.com/gonka-ai/gonka/blob/release/v0.2.13/inference-chain/x/inference/keeper/dynamic_pricing.go#L151-L157));
neither applies to an already-priced model after the grace boundary, so escaping
the trap requires a param change, a code change, or a state migration.

### How mainnet got there, and where it is now

`UpdateDynamicPricing` runs for every model in `BeginBlock`
([`module/module.go#L188-L194`](https://github.com/gonka-ai/gonka/blob/release/v0.2.13/inference-chain/x/inference/module/module.go#L188-L194)).
While `epoch ≤ grace_period_end_epoch` it instead sets every model to the grace
price, ending with a one-time base-price initialization at the boundary epoch
([`dynamic_pricing.go#L49-L53`](https://github.com/gonka-ai/gonka/blob/release/v0.2.13/inference-chain/x/inference/keeper/dynamic_pricing.go#L49-L53),
[#L233-L266](https://github.com/gonka-ai/gonka/blob/release/v0.2.13/inference-chain/x/inference/keeper/dynamic_pricing.go#L233-L266)).
After that, with `base_per_token_price = 100`, `stability_zone_lower_bound = 0.40`
and demand below the stability zone, the price decays at up to −2%/block — and
integer truncation makes it faster than the continuous math suggests: at the max
rate, 100 falls below the p=50 trap line in 26 blocks (≈2 minutes) and sits at
the floor of 1 within 74 blocks (≈6 minutes; below 50, `floor(0.98p)` loses a
full 1 every block). Mainnet params say `grace_period_end_epoch = 90` and the
chain is past epoch 300, so this happened long ago.

Live confirmation (2026-07-14):

```
GET https://node3.gonka.ai/chain-api/productscience/inference/inference/all_model_per_token_prices
```

returns **`"price": "1"` for all 8 models**, including `moonshotai/Kimi-K2.6`,
`zai-org/GLM-5.2-FP8`, `MiniMaxAI/MiniMax-M2.7`. Since `RecordInferencePrice`
locks this price onto every inference at start/finish
([`dynamic_pricing.go#L268-L297`](https://github.com/gonka-ai/gonka/blob/release/v0.2.13/inference-chain/x/inference/keeper/dynamic_pricing.go#L268-L297),
called from `msg_server_start_inference.go#L97` and `msg_server_finish_inference.go#L115`),
all mainnet inference is currently settling at 1/100th of the intended base
price — and will continue to, even if demand saturates the network, until a
code, param, or state change intervenes.

### Cheap fixes

- **Code:** round up on the increase branch, or guarantee a minimum step
  (`newPrice = max(newPrice, currentPrice+1)` when `adjustmentFactor > 1`), or
  store prices at higher resolution (e.g. micro-ngonka internally).
- **No-code mitigations via governance:** raise `min_per_token_price` to ≥ 50 —
  the clamp runs after truncation and reads the param every block, so that
  immediately restores upward mobility (50 → 51 → 52 …) without a chain upgrade.
  Alternatively, extending `grace_period_end_epoch` past the current epoch
  re-triggers the grace path and re-initializes all prices at the new boundary.

---

## 2. The utilization denominator is a per-model-wrong constant

### The formula as implemented

Per model, per block:

```
utilization = averageLoadPerBlock / (capacity × 5s)
0.40 ≤ u ≤ 0.60 → no change; below → down (≤2%/block); above → up (≤2%/block)
```

**The numerator is fine.** It's a rolling ~60s (12-block) average of real
`prompt_tokens + completion_tokens` of completed inferences of that exact model
([`module/inference_validation_endblock.go#L58-L64`](https://github.com/gonka-ai/gonka/blob/release/v0.2.13/inference-chain/x/inference/module/inference_validation_endblock.go#L58-L64),
averaged in [`keeper/rolling_window_state.go#L116-L130`](https://github.com/gonka-ai/gonka/blob/release/v0.2.13/inference-chain/x/inference/keeper/rolling_window_state.go#L116-L130)).
The chain records whatever `completion_token_count` the executor submits; in
API-side measurements, Gonka's reported `completion_tokens` for Kimi K2.6
includes reasoning tokens, so the recorded load does appear to track real work.

**The denominator is a proxy that the code itself flags as temporary.** Capacity
is the model sub-group's total PoC nonce weight, taken as tokens/second:

[`keeper/dynamic_pricing.go#L352-L365`](https://github.com/gonka-ai/gonka/blob/release/v0.2.13/inference-chain/x/inference/keeper/dynamic_pricing.go#L352-L365)

```go
// TODO: The proposal mentions copying from a `total_throughput` field, but this field
// doesn't exist in the current EpochGroupData structure. For now, we use TotalWeight
// as a proxy for capacity (tokens per second), as 1000 nonce of PoC produce aproximetely
// 1000 tokens for of QwQ-32B model. ...
capacity := modelEpochData.TotalWeight
```

(The TODO's first sentence is stale at this tag: `EpochGroupData.TotalThroughput`
now exists — `proto/inference/inference/epoch_group_data.proto#L38` — but it is
always zero in practice, see below.) So the ratio assumes **1 PoC nonce ≈ 1
token/s, calibrated on QwQ-32B**, applied uniformly to every model.

I checked whether any per-model normalization enters this weight upstream, and
found none: a model sub-group's member weight is the sum of raw `PocWeight` of
the MLNodes allocated to that model — the code comment says "no coefficient"
explicitly
([`epochgroup/epoch_group.go#L263-L272`](https://github.com/gonka-ai/gonka/blob/release/v0.2.13/inference-chain/x/inference/epochgroup/epoch_group.go#L263-L272)) —
and the per-model `weight_scale_factor` (0.90 for Kimi on mainnet) applies only
to rewards and consensus voting weight, never to the pricing denominator.
The devshard gateway's admission control converts the *same* raw weight
into serving capacity at 5 concurrent requests per 10,000 weight **per devshard
instance** (`devshard/cmd/devshardctl/gateway_limiter.go`, tag
`release/devshard/v2.0.0`); since multiple uncoordinated shards each take a
slice, the workable network total is roughly **32 concurrent per 10,000 weight**
(a rough figure from the Gonka team, not on-chain). At the ~20–26 tokens/s decode
measured per Kimi stream, that is ~640–830 tokens/s per 10,000 weight, while the
pricing keeper assumes 10,000 tokens/s for the same 10,000 weight. The two
weight→capacity conversions in this codebase disagree by **~12–16×**, and both
are model-uniform.

### The on-chain data says that constant can't be right

The model registry already carries a per-model `throughput_per_nonce` (mainnet
values via `.../inference/models_all`):

| model | `throughput_per_nonce` |
|---|---|
| `MiniMaxAI/MiniMax-M2.7` | 5000 |
| `moonshotai/Kimi-K2.6` | 1500 |
| `zai-org/GLM-5.2-FP8` | 700 |

That's a 7× spread across the three currently served models. Whatever the
intended units, the same nonce buys very different token throughput per model —
so a single `weight × 1` capacity constant means the 0.40/0.60 stability band
sits at a different (and unknown) *true* hardware utilization for each model.

For Kimi K2.6 concretely (live values, epoch 326, 2026-07-14): the sub-group
`TotalWeight` is **95,298**, so the keeper assumes the Kimi fleet serves ~95k
tokens/s. The price stops falling only above ~38k tok/s of sustained
completed-token load (U = 0.4) and starts rising only above ~57k tok/s
(U = 0.6). Two independent estimates of what the Kimi fleet can actually sustain
both land far below that:

- **Hardware estimate:** with a rough PoC-weight→GPU calibration (±2×), Kimi's
  share is on the order of 65 B200-class GPUs (~6–11 serving replicas),
  plausible aggregate *decode* throughput ~12–36k tokens/s — the capacity
  constant overstates decode capacity roughly **3–8×**.
- **Concurrency estimate:** at ~32 workable concurrent per 10,000 weight, Kimi's
  ~95k weight admits ~300 concurrent streams; at the measured ~20–26 tok/s per
  stream that's **~6–8k tokens/s** of decode-bound load — an overstatement of
  **~12–16×**.

Either way, even the fleet's full decode ceiling sits *below the 0.40 lower
bound*. Under organic, decode-bound demand, Kimi's measured utilization can never
reach the stability zone: the mechanism can only lower Kimi's price, never hold
or raise it. (Sub-group weight is also volatile — 38k–95k observed across recent
epochs — so the thresholds themselves swing ~2.5× epoch to epoch.)

One caveat, and it cuts both ways: load counts
`prompt + completion` tokens equally, and prefill is far cheaper than decode. A
prompt-heavy workload can post completed-token rates well above decode
throughput — at ~300 admittable concurrent streams, a fleet of max-length-prompt
requests could plausibly cross even the 0.6 threshold. So the thresholds are
unreachable for real demand yet *reachable by deliberate prompt-stuffing*, which
means the price signal is also manipulable upward with relatively cheap traffic.
Separately, rejected demand never becomes a completed inference (429s from the
gateways under load are observable in benchmarking), so genuine congestion is
invisible to this utilization signal, which counts only completed inferences.

### The fix is already half-built

- `EpochGroupData.TotalThroughput` exists and is summed per model sub-group at
  epoch formation
  ([`epochgroup/epoch_group.go#L190-L196`](https://github.com/gonka-ai/gonka/blob/release/v0.2.13/inference-chain/x/inference/epochgroup/epoch_group.go#L190-L196)) —
  but the per-node `MLNodeInfo.Throughput` it sums is never assigned anywhere at
  this tag, so the field is zero for every sub-group (verified in live epoch
  data too), and the pricing path ignores it anyway in favor of `TotalWeight`.
- There's already a TODO to populate node throughput from the governance
  `ThroughputPerNonce`
  ([`module/model_assignment.go#L360-L362`](https://github.com/gonka-ai/gonka/blob/release/v0.2.13/inference-chain/x/inference/module/model_assignment.go#L360-L362)).

Wiring `capacity = Σ(member weight × ThroughputPerNonce)` (in whatever the
intended units are) through `CacheAllModelCapacities` would make the stability
band mean the same thing for every model, using data that's already on chain.

### Smaller observations on the same path

- Load is attributed in the block a finished inference drains from the queue, and
  only `IsCompleted()` inferences count — in-flight and failed requests are
  invisible to utilization. Over a short 12-block window this makes the signal
  bursty.
- If a model's sub-group has `TotalWeight ≤ 0`, capacity silently defaults to
  1000 tokens/s (`dynamic_pricing.go#L360-L365`).
- The single-model price query (`.../model_per_token_price/{id}`) returns
  `12 Not Implemented` through the public chain-api gateways; only
  `all_model_per_token_prices` works. Minor, but it hid the floor-pinning from
  casual inspection.

---

## Proposed fixes

Two PRs accompany this issue, one per defect:

- **Part 1 — `fix(x/inference): ceil price increases so sub-50 prices can rise`**
  — quantize the increase branch upward (`newPriceDec.Ceil().IntPart()`) so any
  above-stability-zone block raises the price by at least one quantum; sub-50
  prices are no longer trapped. Decrease branch left floored. Consensus-breaking.
- **Part 2 — `fix(x/inference): derive pricing capacity from per-model
  throughput per tokenomics-v2 spec`** — populate `MLNodeInfo.Throughput` from
  the registry (`PocWeight × ThroughputPerNonce / UnitsOfComputePerToken`) so
  `CacheAllModelCapacities` prefers `TotalThroughput` over the `TotalWeight`
  proxy, with `TotalWeight`/default-1000 fallback preserved. Implements the two
  in-tree TODOs and `tokenomics-v2/dynamic-pricing.md` §2.2.3. Consensus-breaking.

---

## Open points not addressed by these PRs

- Whether the current all-models-at-min-price state is known and accepted for
  this phase (effectively a free period) or an unintended consequence — this
  affects how urgent the fix is. (The units/semantics of `ThroughputPerNonce`
  are raised in PR 2 of 2's "Units assumption" section.)
- The load numerator weights prompt tokens 1:1 with completion tokens while
  prefill is far cheaper than decode; this both hides decode congestion and lets
  prompt-heavy traffic move the price. Neither PR changes this — flagged as a
  separate design question.

</div>

---

> 🔄 **Auto-synced** from [Issue #1450](https://github.com/gonka-ai/gonka/issues/1450) every hour.
