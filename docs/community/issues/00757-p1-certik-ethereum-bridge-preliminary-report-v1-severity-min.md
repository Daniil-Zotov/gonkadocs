---
title: "#757 —  [P1] Certik, Ethereum Bridge, Preliminary Report (v1), Severity: Minor [Priority 5]"
source: https://github.com/gonka-ai/gonka/issues/757
issue_number: 757
synced_at: 2026-08-11T13:49:05Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
     [P1] Certik, Ethereum Bridge, Preliminary Report (v1), Severity: Minor [Priority 5]
    <span class="issues-number">#757</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-02-14 00:39 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-04-09 23:23 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #f86c7a; color: #24292f; border-color: #f86c7a;">Priority: High</span></div>
</div>

<div class="issues-content" markdown="1">
- [x] GEB-06 | Known Security Issue in Upstream Dependencies - https://github.com/gonka-ai/gonka/pull/675
- [x] GEB-07 | Weak Address Validation in `withdraw()` in `wrapped-token` Contract - https://github.com/gonka-ai/gonka/pull/814
- [x] GEB-08 | `ADMIN` Role Cannot Not Be Updated https://github.com/gonka-ai/gonka/pull/949
- [x] GEB-09 | Migration From cw20‑base Leaves Required Wrapped‑Token State Uninitialized https://github.com/gonka-ai/gonka/pull/949
- [x] GEB-10 | Migration of `community‑sale` Lacks Compatibility Checks and State Validation - https://github.com/gonka-ai/gonka/pull/814
- [x] GEB-18 | Slot Donation Picks Under-Allocated Donor, Enabling Sybil Weight Inflation - #822 
- [x] GEB-19 | Secret Shares Logged in `logging.Debug` - #822 
- [x] GEB-20 | Decoding Returns Zero If Fails https://github.com/gonka-ai/gonka/pull/949
- [x] GEB-21 | Ineffective Polynomial Degree Check in `evaluatePolynomial()` https://github.com/gonka-ai/gonka/pull/949
- [x] GEB-22 | Unchecked `amountToBytes32()` Panic on Oversized Amounts https://github.com/gonka-ai/gonka/pull/949
- [x] GEB-23 | Missing Validation of `MsgRequestThresholdSignature.ValidateBasic()` for `chain_id`/`request_id` and Data Chunk Sizes - #822 
- [x] GEB-24 | Insufficient Validation for Dealer Part Submissions in `MsgSubmitDealerPart.ValidateBasic()` - #822 
- [x] GEB-25 | Missing Validation in Group Key Validation Signatures in `MsgSubmitGroupKeyValidationSignature.ValidateBasic()` - #822 
- [x] GEB-26 | Missing Validation in Partial Signature Submissions in `MsgSubmitPartialSignature.ValidateBasic()` - #822 
- [x] GEB-27 | Unbounded `DealerValidity` in Verification Vector Submissions of `MsgSubmitVerificationVector.ValidateBasic()` - #822 
- [x] GEB-37 | DKG Process Can Be Stuck Due to Internal Errors https://github.com/gonka-ai/gonka/pull/949
- [x] GEB-38 | Inconsistent Comparison of Deadline Block https://github.com/gonka-ai/gonka/pull/949
- [x] GEB-39 | Missing Validation of `msg.Amount` Being Positive in `MsgRequestBridgeWithdrawal` - https://github.com/gonka-ai/gonka/pull/814
- [x] GEB-40 | Broken Cleanup Logic https://github.com/gonka-ai/gonka/pull/949
- [x] GEB-42 | Unhandled Error of `EmitTypedEvent()` https://github.com/gonka-ai/gonka/pull/949
- [x] GEB-43 | Valid Dealers Can Be Less Than Threshold https://github.com/gonka-ai/gonka/pull/949
- [x] GEB-47 | Hard-coded threshold for BLS signature https://github.com/gonka-ai/gonka/pull/949
- [x] GEB-48 | Missing Signed Status in `parseEpochDataFromJSON()` https://github.com/gonka-ai/gonka/pull/949
- [x] GEB-49 | Missing Check of Withdrawal and Mint Amount https://github.com/gonka-ai/gonka/pull/949
- [x] GEB-56 | Missing Validation of Epoch Id in `RequestThresholdSignature()` https://github.com/gonka-ai/gonka/pull/949
- [x] GEB-57 | Slot Range Silently Clamped Instead of Failing https://github.com/gonka-ai/gonka/pull/949
</div>

---

> 🔄 **Auto-synced** from [Issue #757](https://github.com/gonka-ai/gonka/issues/757) every hour.
