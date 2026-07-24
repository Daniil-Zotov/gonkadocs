---
title: "#1080 — Bridge: Stale epoch keys can authorize withdrawals up to 365 epochs after rotation"
source: https://github.com/gonka-ai/gonka/issues/1080
issue_number: 1080
synced_at: 2026-07-24T19:51:01Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Bridge: Stale epoch keys can authorize withdrawals up to 365 epochs after rotation
    <span class="issues-number">#1080</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/Doog-bot534">@Doog-bot534</a> opened 2026-04-16 03:24 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-07-10 05:34 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

`withdraw()` and `mintWithSignature()` in `BridgeContract.sol` accept signatures from **any historical epoch** as long as the epoch's group key has not been cleaned up by `_cleanupOldEpochs`. The cleanup only removes epochs older than `latestEpochId - 365`.

This means validators who rotated out of the active set **can still sign valid withdrawal/mint transactions for up to 365 epochs** (~1 year depending on epoch length) using their old threshold key shares.

## Root Cause

**File:** `proposals/ethereum-bridge-contact/contracts/BridgeContract.sol:332-335`

The signature verification checks:
1. The epoch has a valid group key (`!_isGroupKeyEmpty`) ✅
2. The signature is valid against that epoch's key ✅
3. The request hasn't been processed for that epochId ✅

But it does NOT check:
- Whether the epoch is recent (e.g., within last 2-3 epochs)
- Whether the signing key is still the current active key

## Exploit Scenario

1. Validator set V1 controls epoch N's threshold key
2. Key rotation happens → new validator set V2 controls epoch N+1
3. Retired validators from V1 still hold threshold key shares for epoch N
4. V1 members collude to sign a fraudulent withdrawal using epoch N's key
5. Withdrawal succeeds because epoch N's key is still valid for 365 more epochs

## Impact

**High** — Fund theft by retired validators. The entire security model of key rotation is undermined if old keys remain valid indefinitely.

## Suggested Fix

Restrict `withdraw()` and `mintWithSignature()` to only accept signatures from the last 2-3 epochs:

```solidity
require(epochId >= latestEpochId - MAX_VALID_EPOCH_AGE, "epoch too old");
```

Where `MAX_VALID_EPOCH_AGE` is a small constant (e.g., 2-3) to allow for brief transition periods.

## Additional Bridge Findings

### [Medium] Cross-epoch replay via per-epoch processedRequests

`processedRequests[epochId][requestId]` is scoped per-epoch. The same `requestId` with a **different epochId** can be executed again if validators sign it under a different epoch's key. Should use a global `mapping(bytes32 => bool)` instead.

### [Medium] _negateG1 lacks modular arithmetic validation

If input y-coordinate >= field prime p, the subtraction produces an incorrect result without reverting. While the pairing check should fail downstream, this is a defense gap.

---

Payout address: `gonka10zaal553duxp05nvfpqtsqrm2g0j6j34r8nan7`
</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Ryanchen911">@Ryanchen911</a></span>
    <span class="issues-meta-item">commented 2026-06-23 05:59 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>hi @tcharchian , does this issue need help, maybe I can fix it.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-06-25 01:46 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hey @Ryanchen911, let's wait for triage from @GLiberman first please </p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1080](https://github.com/gonka-ai/gonka/issues/1080) every hour.
