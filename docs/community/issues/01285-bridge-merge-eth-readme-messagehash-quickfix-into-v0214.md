---
title: "#1285 — Bridge: merge ETH README messageHash quickfix into v0.2.14"
source: https://github.com/gonka-ai/gonka/issues/1285
issue_number: 1285
synced_at: 2026-08-05T12:20:39Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Bridge: merge ETH README messageHash quickfix into v0.2.14
    <span class="issues-number">#1285</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/Ryanchen911">@Ryanchen911</a> opened 2026-06-01 02:34 UTC</span>
    <span class="issues-meta-item">4 comments</span>
    <span class="issues-meta-item">Updated 2026-07-07 23:25 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

The Ethereum bridge README currently documents the mint/withdraw `messageHash` format without the `address(this)` bridge contract field, while the actual contract source includes it.

A fix already exists on branch:

https://github.com/gonka-ai/gonka/tree/gl/eth-readme-quickfix

This ticket tracks merging that fix into the v0.2.14 line.

## Current discrepancy

README currently documents mint as:

```solidity
epochId,
GONKA_CHAIN_ID,
requestId,
ETHEREUM_CHAIN_ID,
MINT_OPERATION,
recipient,
amount
```

But the contract source uses:

```solidity
epochId,
GONKA_CHAIN_ID,
requestId,
ETHEREUM_CHAIN_ID,
MINT_OPERATION,
recipient,
address(this),
amount
```

The same applies to `withdraw`, where `address(this)` is also part of the signed payload.

## Impact

The chain-side implementation already matches the contract source, so this is not a production-safety issue.

However, third-party auditors or integrators using the README could construct an invalid message hash, causing signature verification failures.

## Acceptance criteria

- README mint `messageHash` includes `address(this)`.
- README withdraw `messageHash` includes `address(this)`.
- Documentation matches `BridgeContract.sol`.
- Fix is merged into v0.2.14.
</div>

---

## 💬 Comments (4)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-06-02 00:50 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@Ryanchen911, are you ready to write a fix?</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Ryanchen911">@Ryanchen911</a></span>
    <span class="issues-meta-item">commented 2026-06-02 07:15 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Sure, we will take it,@bonujel is our new colleague of 6block, he will do it.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/bonujel">@bonujel</a></span>
    <span class="issues-meta-item">commented 2026-06-02 08:24 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Picking this up — I'll cherry-pick the README <code>messageHash</code> fix from <code>gl/eth-readme-quickfix</code> onto the v0.2.14 line and open a PR shortly.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-06-02 17:47 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@GLiberman fyi</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1285](https://github.com/gonka-ai/gonka/issues/1285) every hour.
