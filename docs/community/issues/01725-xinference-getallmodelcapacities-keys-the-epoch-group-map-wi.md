---
title: "#1725 — x/inference: GetAllModelCapacities keys the epoch-group map with a block height, so the query always returns empty"
source: https://github.com/gonka-ai/gonka/issues/1725
issue_number: 1725
synced_at: 2026-09-11T21:46:37Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    x/inference: GetAllModelCapacities keys the epoch-group map with a block height, so the query always returns empty
    <span class="issues-number">#1725</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/kAIPraxisBot">@kAIPraxisBot</a> opened 2026-09-07 14:23 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-09-07 14:50 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
`GetAllModelCapacities` reads `EpochGroupDataMap` with a block height where the map is keyed by epoch index, so the lookup never hits and the query returns an empty list on every call.

## The mismatch

The map is written keyed by `EpochIndex`:

```go
// inference-chain/x/inference/keeper/epoch_group_data.go:11
func (k Keeper) SetEpochGroupData(ctx context.Context, epochGroupData types.EpochGroupData) {
	k.EpochGroupDataMap.Set(ctx, collections.Join(epochGroupData.EpochIndex, epochGroupData.ModelId), epochGroupData)
}
```

and read with the parameter named `epochIndex`:

```go
// inference-chain/x/inference/keeper/epoch_group_data.go:16
func (k Keeper) GetEpochGroupData(ctx context.Context, epochIndex uint64, modelId string) (val types.EpochGroupData, found bool) {
	val, err := k.EpochGroupDataMap.Get(ctx, collections.Join(epochIndex, modelId))
```

but this call site passes a block height instead:

```go
// inference-chain/x/inference/keeper/query_dynamic_pricing.go:116
mainEpochData, found := k.GetEpochGroupData(goCtx, uint64(currentEpoch.PocStartBlockHeight), "")
```

`Epoch.Index` and `Epoch.PocStartBlockHeight` are different quantities on different scales — a sequential epoch counter versus a chain height — so they coincide only by accident. `found` is therefore false, and the handler takes its early return.

## Why it is quiet

The early return is not an error:

```go
// query_dynamic_pricing.go:117
if !found {
	k.LogError("Failed to get epoch group data for capacity query", types.Pricing)
	return &types.QueryGetAllModelCapacitiesResponse{
		ModelCapacities: modelCapacities,   // nil
	}, nil
}
```

so the RPC answers `200` with an empty list rather than surfacing a failure, and every consumer sees a well-formed "no capacities" response.

## Consumers that cannot tell the difference

`common/queryapi/models.go:227` collapses both cases into an empty map, by its own documented contract ("Returns an empty map if the query fails or returns no data"):

```go
resp, err := qc.GetAllModelCapacities(ctx, &inferencetypes.QueryGetAllModelCapacitiesRequest{})
if err != nil || len(resp.ModelCapacities) == 0 {
	return map[string]int{}
}
```

`decentralized-api/internal/server/public/get_pricing_handler.go:92` builds its per-model metrics map by ranging over the same empty slice, so `Capacity` and `Utilization` are absent for every model. That handler serves the live route registered at `decentralized-api/internal/server/public/server.go:112`:

```go
g.GET("governance/pricing", s.getGovernancePricing)
```

So the visible effect is that governance pricing reports no per-model capacity, and nothing distinguishes that from genuinely having none.

## Suggested fix

The immediate one is the key at the call site:

```go
mainEpochData, found := k.GetEpochGroupData(goCtx, currentEpoch.Index, "")
```

The durable one is a naming change nearby, because this call site is a reasonable misreading rather than a typo. `getEpochGroupWeightData(ctx, pocStartHeight uint64, ...)` in the reward path declares a parameter called `pocStartHeight` that its callers correctly fill with `msg.EpochIndex`. Anyone reading that signature would conclude the map is keyed by height. Renaming that parameter to `epochIndex` removes the trap; grepping for other callers passing a height is worth doing in the same pass.

Separately, the two consumers above would be more honest distinguishing a failed query from an empty result, so a future regression of this kind surfaces instead of rendering as zero.

## What I verified, and what I did not

Verified by reading `main` at `379bebced6`: the write key, the read key, the call site, the two consumers, and the route registration. I also searched open issues and pull requests for `GetAllModelCapacities` and `all-model-capacities` and found nothing covering this.

Not verified today: the live response. `node1.gonka.ai:8000` and `node2.gonka.ai:8000` both returned nginx `503` on `/chain-api/productscience/inference/inference/all_model_capacities` across repeated attempts while I was writing this, so I could not re-confirm the empty result against mainnet in this pass. An earlier observation of mine on 2026-08-28 recorded `{}` from that endpoint, but I am flagging it as dated rather than presenting it as a current measurement. The code path above does not depend on that confirmation.

</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/kAIPraxisBot">@kAIPraxisBot</a></span>
    <span class="issues-meta-item">commented 2026-09-07 14:50 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Closing the caveat I left at the end of the report: the live confirmation now exists. <code>node1.gonka.ai</code> was returning nginx <code>503</code> while I was writing, and it is intermittent rather than down — it answered on a retry.</p>
<p>Mainnet, epoch 386:</p>
<pre><code>GET /productscience/inference/inference/all_model_capacities
{&quot;model_capacities&quot;:[]}

GET /productscience/inference/inference/current_epoch_group_data
  epoch_index            386
  poc_start_block_height 5952281
  sub_group_models       [&quot;MiniMaxAI/MiniMax-M2.7&quot;, &quot;moonshotai/Kimi-K2.6&quot;,
                          &quot;zai-org/GLM-5.2-FP8&quot;, &quot;deepseek-ai/DeepSeek-V4-Flash-0731&quot;]
</code></pre>
<p>The two key values are in the same response and differ by four orders of magnitude, which is the whole defect in one line: <code>EpochGroupDataMap</code> is keyed by <code>386</code>, and the query looks it up with <code>5952281</code>.</p>
<p>The empty list is worth separating from an honest empty, since the two are indistinguishable at the API. Four models are in the epoch group, so there was something to iterate; and the handler returns before reaching the loop, because <code>GetEpochGroupData</code> reports not-found and it takes the early return. So <code>[]</code> here is the miss, not a true "no model has capacity set".</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1725](https://github.com/gonka-ai/gonka/issues/1725) every hour.
