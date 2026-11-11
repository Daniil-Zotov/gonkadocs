---
title: "#2256 — Do not halt consensus when the first epoch has no eligible PoC participants"
source: https://github.com/gonka-ai/gonka/issues/2256
issue_number: 2256
synced_at: 2026-11-11T06:43:46Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Do not halt consensus when the first epoch has no eligible PoC participants
    <span class="issues-number">#2256</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/maria-mitina">@maria-mitina</a> opened 2026-11-10 16:41 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-11-10 21:03 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #a2eeef; color: #24292f; border-color: #a2eeef;">enhancement</span></div>
</div>

<div class="issues-content" markdown="1">
## Summary

`onEndOfPoCValidationStage` returns `no eligible participants for upcoming epoch %d` when seating and the epoch fallback both produce an empty set. EndBlock returns that error, and CometBFT panics in `finalizeCommit` (`failed to apply block`).

On a fresh chain this happens at the first PoC. `fallbackActiveParticipantsFromCurrentEpoch` returns immediately when `upcomingEpoch.Index <= 1` (`EpochFallback: not applicable for the first epoch`). Before v0.2.16 (`061ce0366`, weightcap) the same empty set logged `epoch_error` and returned, so the block committed and the genesis validator kept signing. v0.2.16 turned that return into an error.

Mainnet is long past epoch 0 and 1. For `upcomingEpoch.Index > 1` the fallback still carries the current epoch's validators, and a truly empty carry should keep failing the block.

## Observed on gonka-testnet-4

Height 265 is the end of the first PoC validation window (stage start 160). All five participants had `PoCV2StoreCommit` counts, and every `MsgSubmitPocValidationsV2` vote was `validated_weight=-1` (`fraud_detected=true` from the MLNode callback). Epoch formation found no positive weight. The node logged:

`CONSENSUS FAILURE!!! err="failed to apply block; error no eligible participants for upcoming epoch 1"`

`committed state` was logged through height 264. Restarting the same binary panics on 265 again.

## Suggestion

In `inference-chain/x/inference/module/module.go`, only skip the consensus error for the first epoch:

```go
if len(activeParticipants) == 0 {
    if upcomingEpoch.Index <= 1 {
        am.LogError("onEndOfPoCValidationStage: no eligible participants for the first epoch; continuing", types.PoC,
            "upcomingEpoch.Index", upcomingEpoch.Index)
        sdkCtx := sdk.UnwrapSDKContext(ctx)
        sdkCtx.EventManager().EmitEvent(sdk.NewEvent(
            "epoch_error",
            sdk.NewAttribute("stage", "empty_epoch_fallback"),
            sdk.NewAttribute("epoch", fmt.Sprintf("%d", upcomingEpoch.Index)),
            sdk.NewAttribute("error_category", "epoch_formation"),
        ))
        return nil
    }
    return fmt.Errorf("no eligible participants for upcoming epoch %d", upcomingEpoch.Index)
}
```

Use the same `Index <= 1` guard on the later `no eligible fallback participants` return. Leave the `no positive final weight` errors unchanged; those run for every epoch.

`TestOnEndOfPoCValidationStage_EmptyFallbackHalts` expects the error and needs to match this split: a first-epoch empty set returns nil and writes no epoch output; a later-epoch empty set still returns the error.

## Why this does not change mainnet

The guard reads chain state, not the binary's age. On mainnet the upcoming epoch index is already greater than 1, so execution stays on `return fmt.Errorf(...)`, which is the current behavior. A normal PoC failure on a later epoch still uses `fallbackActiveParticipantsFromCurrentEpoch` and still halts if that carry is empty.

This does not treat `validated_weight=-1` as a pass. Epoch 1 still gets no active participants; the genesis validator keeps producing blocks.
</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/maria-mitina">@maria-mitina</a></span>
    <span class="issues-meta-item">commented 2026-11-10 16:42 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@tcharchian this is needed to unblock testnet</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/maria-mitina">@maria-mitina</a></span>
    <span class="issues-meta-item">commented 2026-11-10 20:56 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>The issue above only shifted the chain halt left and put it sooner. The rebuilt binary still ended up with a chain halt due to the root cause below. The issue above could be left alone, however fixing it could buy some time to slow models loading in mlnode and not being on time for epoc 0 and 1 POCs. </p>
<p>The real source of the issue was validation votes -1 (fraud detected) for all hosts (including themselves) when testnet machines used mlnode ghcr.io/gonka-ai/mlnode:3.0.16@sha256:1b9b7ce55feecab837f1d7ce974fc5f377ae0a04a4fb403eeeb50130e7728ee1
this mlnode is default on upgrade 2.16 branch. 
after changing mlnodes to ghcr.io/gonka-ai/mlnode:4.0.0-sigma2 the root cause issue is gone, </p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2256](https://github.com/gonka-ai/gonka/issues/2256) every hour.
