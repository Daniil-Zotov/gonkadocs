---
title: "#608 — [0/4] `StartInference` and `FinishInference`: optimiziation"
source: https://github.com/gonka-ai/gonka/issues/608
issue_number: 608
synced_at: 2026-07-26T15:34:50Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    [0/4] `StartInference` and `FinishInference`: optimiziation
    <span class="issues-number">#608</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/libermans">@libermans</a> opened 2026-01-19 01:05 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-03-11 20:01 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
StartInference and FinishInference should be significantly optimized, as they are messages used frequently—potentially 1,000+ times per block. The execution time of these messages should be below 1 ms, ideally below 0.2 ms. (currently with 1000 participants, and 1 grantee per account, StartInference can be 0.4-0.5ms, and FinishInference 4-5ms)

1. The biggest contributor to the execution time of FinishInference (or late StartInference) is reading and writing EpochGroup. EpochGroup shouldn’t be read or written in frequently executed messages, and unmarshaling/marshaling that large blob is too slow. We should either move the values we need to access/edit into separate records, or process these updates in EndBlocker.
2. After EpochGroup, the next biggest contributor is signature verification.
2.1. First, we should switch to Ethereum-optimized signature verification (github.com/ethereum/go-ethereum/crypto/secp256k1).
2.2. Second, when the chain receives a StartInference transaction, we don’t need to verify the TA signature again (it’s already verified in the transaction). Similarly, when the chain receives FinishInference, there’s no need to verify Executor signatures. Also, if FinishInference arrives after StartInference, we shouldn’t re-check the TA and Developer signatures; and when we get a late StartInference, we shouldn’t re-check the Developer signature.

After these changes, benchmark StartInference and FinishInference. If they are still not below 0.2 ms, identify what else should be optimized and report back in the issue.

Also report back in this issue which messages also use EpochGroups, and which we have to optimize as well.

Additionally, for (2.2), ensure that we validate that the timestamp, request original hash, and TA address are correct (they must match InferenceId which derived from them). Also, check that the request modified hash matches: save it from the first-arriving message, and when the second arrives, verify they are equal. If they are not equal, one party is cheating:
• If FinishInference arrives late and the hashes differ, verify the TA signature. If we have valid TA signatures on both messages, then the TA is the cheater.
• If StartInference arrives late, verify the TA signature included in FinishInference; if the hashes differ, that means the TA is the cheater.
• In all other scenarios, the Executor is the cheater.
Unfortunately as TA signature doesn't derived from request original hash, it may be the issue as Executor can present TA signature from a different InferenceId (with same timestamp). So we either should change that or do on chain conversion from request original hash to request modified hash, which can be expansive/but rear (need to measure the time it requires)
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/gmorgachev">@gmorgachev</a></span>
    <span class="issues-meta-item">commented 2026-03-11 20:01 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>The big part of inference flow optimization is merged in https://github.com/gonka-ai/gonka/pull/812
I'm closing all <code>[*/4] StartInference and FinishInference: optimiziation</code> tasks to finalize this work in milestone 0.2.11. I think it'd be better to re-open in case of additinal optimizations required</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #608](https://github.com/gonka-ai/gonka/issues/608) every hour.
