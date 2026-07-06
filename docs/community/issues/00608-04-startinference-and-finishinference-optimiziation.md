---
title: "#608 — [0/4] `StartInference` and `FinishInference`: optimiziation"
source: https://github.com/gonka-ai/gonka/issues/608
issue_number: 608
synced_at: 2026-07-06T09:52:43Z
template: issues-main.html
---

> 🔄 **Авто-синхронизация:** из [Issue #608](https://github.com/gonka-ai/gonka/issues/608) каждые 6 часов. 

# 🔴 [0/4] `StartInference` and `FinishInference`: optimiziation

**Автор:** [@libermans](https://github.com/libermans) · **Состояние:** Closed · **Создано:** 2026-01-19 01:05 UTC · **Обновлено:** 2026-03-11 20:01 UTC

**Веха:** v0.2.11

---

## 📝 Описание

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

---

## 💬 Комментарии (1)

### Комментарий 1 — [@gmorgachev](https://github.com/gmorgachev)

*2026-03-11 20:01 UTC*

The big part of inference flow optimization is merged in https://github.com/gonka-ai/gonka/pull/812
I'm closing all `[*/4] StartInference and FinishInference: optimiziation` tasks to finalize this work in milestone 0.2.11. I think it'd be better to re-open in case of additinal optimizations required
