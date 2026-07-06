---
title: "#1285 — Bridge: merge ETH README messageHash quickfix into v0.2.14"
source: https://github.com/gonka-ai/gonka/issues/1285
issue_number: 1285
synced_at: 2026-07-06T09:51:55Z
---

> 🔄 **Авто-синхронизация:** из [Issue #1285](https://github.com/gonka-ai/gonka/issues/1285) каждые 6 часов. 

# 🟢 Bridge: merge ETH README messageHash quickfix into v0.2.14

**Автор:** [@Ryanchen911](https://github.com/Ryanchen911) · **Состояние:** Open · **Создано:** 2026-06-01 02:34 UTC · **Обновлено:** 2026-06-02 17:47 UTC

**Веха:** v0.2.14

---

## 📝 Описание

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

---

## 💬 Комментарии (4)

### Комментарий 1 — [@tcharchian](https://github.com/tcharchian)

*2026-06-02 00:50 UTC*

@Ryanchen911, are you ready to write a fix?

### Комментарий 2 — [@Ryanchen911](https://github.com/Ryanchen911)

*2026-06-02 07:15 UTC*

Sure, we will take it,@bonujel is our new colleague of 6block, he will do it.


### Комментарий 3 — [@bonujel](https://github.com/bonujel)

*2026-06-02 08:24 UTC*

Picking this up — I'll cherry-pick the README `messageHash` fix from `gl/eth-readme-quickfix` onto the v0.2.14 line and open a PR shortly.

### Комментарий 4 — [@tcharchian](https://github.com/tcharchian)

*2026-06-02 17:47 UTC*

@GLiberman fyi
