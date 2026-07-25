---
title: "#342 — [P0] Security: Minor"
source: https://github.com/gonka-ai/gonka/issues/342
issue_number: 342
synced_at: 2026-07-25T03:45:56Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    [P0] Security: Minor
    <span class="issues-number">#342</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2025-09-04 21:21 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2025-10-09 20:05 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
- [x] GOC-19 | Count Participant With Zero Balance Is Missing Balance Check
- [x] GOC-20 | Go Package Dependency Issues
- [x] GOC-22 | Inconsistent Epoch ID Handling In `GetPreviousEpochMLNodesWithInferenceAllocation`
- [x] GOC-29 | New Participants Initialized As ACTIVE Instead Of RAMPING
- [x] GOC-24 | Misleading Function Name In `storeMLNodeInfo`
- [x] GOC-25 | Misleading Log In Function `SetComputeValidators`
- [x] GOC-32 | Missing Error Handling For `GetPreservedNodesByParticipant`
- [x] GOC-33 | Println Usage In Production Code
- [x] GOC-34 | Var Can Be Declared As Constant
- [x] GOC-35 | Unhandled Error In Function `submitValidationProposals`
- [x] GOC-37 | Unused Variable
- [x] GOC-38 | Incorrect Comments
- [x] GOC-06 | Redundant SetParticipant In `handleExpiredInference`
- [x] GOC-36 | Redundant Maps And Double-Pass Iteration In `SetComputeValidators`
- [x] GOI-15 | Potential Division By Zero Leads To Panic
- [x] GOI-20 | Incorrect Remainder Distribution In Legacy Weight Allocation
- [x] GOI-05 | Stale Object Used For Completion Check In `FinishInference`
- [x] GOI-19 | Missing `nil` Check For `GetPubKey()` Could Lead To Panic
- [x] GOI-29 | Interface Mismatch In `RunMembershipService` Vs `RunManager`
- [x] GOI-07 | Constants Declaration Should Be Grouped At The Top Of The File
- [x] GOI-08 | Inconsistent Constant Declaration Pattern
- [x] GOI-31 | Unused Errors
- [x] GOI-33 | Duplicated Constant `DefaultMaxTokens`
- [x] GOI-34 | Incorrect Timeout Logging Value
- [x] GOI-35 | Redundant Boolean Comparison
- [x] GOI-09 | In `distributeLegacyWeight `, for each hardware node the code linearly scans newMLNodes to find an existing node with matching `NodeId `. This is O(H*N) and can degrade when many nodes exist.
- [x] GOI-10 | For each governance model, the code scans all `originalMLNodes` and `callsslices.Contains(supportedModelsByNode[mlNode.NodeId], model.Id) `to decide assignment. This is O(MNK) where K `ismodels` per node.

Ignore the following:

- [ ] GOC-10 | Subsidy Calculation Mints Total Payout Instead Of Reward Causing Systematic Over-Mint: Irrelevant given the switch to Bitcoin style rewards
- [ ] GOI-12 | Cryptographic Signature Collision In Sign/Verify Functions: we acknowledge that it's a good point but it's not a vulnerability. Going to fix it in the future
- [ ] GOC-09 | Reputation-Based Validation Reduction Undermines Byzantine Fault Tolerance: we're not lowering P to zero, only to 1% => we still have regular check (like every couple seconds under high load)























</div>

---

> 🔄 **Auto-synced** from [Issue #342](https://github.com/gonka-ai/gonka/issues/342) every hour.
