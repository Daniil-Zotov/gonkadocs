---
title: "#756 —  [P1] Certik, Ethereum Bridge, Preliminary Report (v1), Severity: Medium [Priority 4]"
source: https://github.com/gonka-ai/gonka/issues/756
issue_number: 756
synced_at: 2026-07-06T09:52:21Z
template: issues-main.html
---

> 🔄 **Auto-synced:** from [Issue #756](https://github.com/gonka-ai/gonka/issues/756) every 6 hours. 

# 🔴  [P1] Certik, Ethereum Bridge, Preliminary Report (v1), Severity: Medium [Priority 4]

**Author:** [@tcharchian](https://github.com/tcharchian) · **State:** Closed · **Created:** 2026-02-14 00:32 UTC · **Updated:** 2026-04-09 23:23 UTC

**Labels:** `Priority: High`

**Веха:** v0.2.12

---

## 📝 Описание

- [x] GEB-04 | Incorrect Signing Threshold in `checkThresholdAndAggregate()` - #822 
- [x] GEB-05 | Native Denom Auto-Detection Can Be Misconfigured in `community-sale` Contract - https://github.com/gonka-ai/gonka/pull/814
- [x] GEB-13 | Aggregation of BLS Partial Signature Does Not Eliminate Duplicates - #822 
- [x] GEB-14 | User-Controlled RequestId Allows Front-Run Poisoning of Threshold Signing - https://github.com/gonka-ai/gonka/pull/949
- [x] GEB-15 | Cross-Chain Address Collision - https://github.com/gonka-ai/gonka/pull/814
- [x] GEB-16 | Bridge BLS Signatures Are Not Bound to Destination Contract - https://github.com/gonka-ai/gonka/pull/949
- [x] GEB-17 | Dealer Validation Majority Is Too Weak for Safe Key Recovery - #822 
- [x] GEB-35 | Secret Shares Not Using Consensus `ValidDealers` - #988 
- [x] GEB-36 | Authority Mismatch In `MigrateAllWrappedTokenContracts()` - https://github.com/gonka-ai/gonka/pull/814
- [x] GEB-55 | BLS Genesis Export/Import Drops In-flight DKG and Signing state - https://github.com/gonka-ai/gonka/pull/949

---

## 💬 Comments (1)

### Комментарий 1 — [@GLiberman](https://github.com/GLiberman)

*2026-02-27 19:29 UTC*

GEB-05, GEB-15, GEB-36

https://github.com/gonka-ai/gonka/pull/814
