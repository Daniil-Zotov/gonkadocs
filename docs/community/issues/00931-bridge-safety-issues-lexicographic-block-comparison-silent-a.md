---
title: "#931 — Bridge safety issues: lexicographic block comparison, silent address validation failure, inconsistent chain ID mapping"
source: https://github.com/gonka-ai/gonka/issues/931
issue_number: 931
synced_at: 2026-07-06T09:52:32Z
template: issues-main.html
---

> 🔄 **Auto-synced:** from [Issue #931](https://github.com/gonka-ai/gonka/issues/931) every 6 hours. 

# 🔴 Bridge safety issues: lexicographic block comparison, silent address validation failure, inconsistent chain ID mapping

**Author:** [@unameisfine](https://github.com/unameisfine) · **State:** Closed · **Created:** 2026-03-23 00:07 UTC · **Updated:** 2026-03-23 00:23 UTC

---

## 📝 Описание

## Description

Found three safety issues in the bridge module during code audit:

### 1. Lexicographic string comparison for block numbers (Medium)

**File:** `x/inference/keeper/bridge_transaction.go:114`

`CleanupOldBridgeTransactions` compares block numbers as strings:
```go
if tx.BlockNumber < maxBlockNumber {
```
This uses Go's lexicographic string comparison, which produces incorrect results for numeric values. For example, `"9" > "10"` as strings, so blocks 2-9 would NOT be cleaned up when `maxBlockNumber="10"`.

### 2. `ethereumAddressToBytes` silently returns zero bytes on error (Medium-High)

**File:** `x/inference/keeper/bridge_utils.go:26-52`

When given an invalid or empty Ethereum address, `ethereumAddressToBytes` silently returns 20 zero bytes (`0x0000...0000`) instead of reporting an error. This means BLS signatures could be computed for the zero address, potentially causing funds to be sent to `0x0` on the Ethereum side (effectively burning them).

The function is called in:
- `prepareBridgeMintSignatureData` (recipient address)
- `prepareBridgeWithdrawalSignatureData` (recipient address, token contract address)

### 3. Inconsistent chain ID mapping between mint and withdrawal (Low)

**Files:** `msg_server_request_bridge_mint.go:20` vs `msg_server_request_bridge_withdrawal.go:20`

`mintChainIdMapping` does not include `"optimism"`, while `chainIdMapping` (withdrawal) does. The comment in mint says "same as withdrawal" but they differ. This means users could withdraw to Optimism but not mint back, breaking round-trip bridge operations.

## Impact

- Issue 1: Bridge transaction cleanup fails for certain block number ranges
- Issue 2: Invalid addresses silently produce BLS signatures for zero address
- Issue 3: Asymmetric bridge support for Optimism chain
