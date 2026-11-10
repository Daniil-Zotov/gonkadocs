---
title: "#2256 — Do not halt consensus when the first epoch has no eligible PoC participants"
source: https://github.com/gonka-ai/gonka/issues/2256
issue_number: 2256
synced_at: 2026-11-10T17:57:18Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Do not halt consensus when the first epoch has no eligible PoC participants
    <span class="issues-number">#2256</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/maria-mitina">@maria-mitina</a> opened 2026-11-10 16:41 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-11-10 16:42 UTC</span>
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

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/maria-mitina">@maria-mitina</a></span>
    <span class="issues-meta-item">commented 2026-11-10 16:42 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@tcharchian this is needed to unblock testnet</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2256](https://github.com/gonka-ai/gonka/issues/2256) every hour.
