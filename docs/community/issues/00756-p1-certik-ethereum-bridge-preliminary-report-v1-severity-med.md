---
title: "#756 —  [P1] Certik, Ethereum Bridge, Preliminary Report (v1), Severity: Medium [Priority 4]"
source: https://github.com/gonka-ai/gonka/issues/756
issue_number: 756
synced_at: 2026-07-20T22:17:40Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
     [P1] Certik, Ethereum Bridge, Preliminary Report (v1), Severity: Medium [Priority 4]
    <span class="issues-number">#756</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-02-14 00:32 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-04-09 23:23 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #f86c7a; color: #24292f; border-color: #f86c7a;">Priority: High</span></div>
</div>

<div class="issues-content" markdown="1">
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
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/GLiberman">@GLiberman</a></span>
    <span class="issues-meta-item">commented 2026-02-27 19:29 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>GEB-05, GEB-15, GEB-36</p>
<p>https://github.com/gonka-ai/gonka/pull/814</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #756](https://github.com/gonka-ai/gonka/issues/756) every hour.
