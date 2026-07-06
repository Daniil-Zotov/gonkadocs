---
title: "#1358 — Inbound bridge votes lost after upgrade simulation (node unavailable for some minutes for upgrade) — no retry, deposits stuck BRIDGE_PENDING"
source: https://github.com/gonka-ai/gonka/issues/1358
issue_number: 1358
synced_at: 2026-07-06T09:51:44Z
template: issues-main.html
---

> 🔄 **Авто-синхронизация:** из [Issue #1358](https://github.com/gonka-ai/gonka/issues/1358) каждые 6 часов. 

# 🟢 Inbound bridge votes lost after upgrade simulation (node unavailable for some minutes for upgrade) — no retry, deposits stuck BRIDGE_PENDING

**Автор:** [@maria-mitina](https://github.com/maria-mitina) · **Состояние:** Open · **Создано:** 2026-06-22 17:39 UTC · **Обновлено:** 2026-06-27 01:04 UTC

**Метки:** `bug` `Priority: High`

**Веха:** v0.2.14

---

## 📝 Описание

## Summary

Upgrade simulation (paused only the Gonka `node` container which halts the chain) while bridge (Geth) and `api` stay up. Inbound bridge deposits are detected and queued on unpause, but **validator votes can be lost silently** with no automatic recovery. Deposits can remain **`BRIDGE_PENDING`** indefinitely (majority never reached, no mint).

Observed on **gonka-testnet-4** (3 validators) during a controlled `docker pause node` test with Sepolia USDT inbound.

Full write-up in repo: `docs/bridge-inbound-pause-test-report.md`

## Test artifact

| Field | Value |
|-------|--------|
| Sepolia block | `11116928` |
| Receipt index | `199` |
| Receipts root | `0x89909ccf6494c61516e0e0bfe45867dc96a566b500566b39ad3462d5ab38068f` |
| USDT contract | `0x7169d38820dfd117c3fa1f22a697dba58d90ba06` |
| Gonka recipient | `gonka1qdwgkcxww42sxmcm9gk0trvugev2g0248upwyq` |

**On-chain result:** `BRIDGE_PENDING`, 1 validator (`gonka1zwcutshh…`), `totalValidationPower: 21459`. Wrapped USDT balance unchanged at **2**.

## Observed behavior

1. **During pause:** Chain height stalled (~12 min); API logged stale block time. Bridge Geth timed out on `GET /v1/bridge/addresses`.
2. **On unpause (~16:39:20–24):** Bridge burst-posted block `11116928` to all three APIs. Join validators logged `Processing receipt` with **no** `Error processing bridge exchange`.
3. **On-chain:** Join votes **not** recorded. Seed voted later (~16:46:27); only one validator on-chain — insufficient for majority mint.

## Root cause (three compounding gaps)

### 1. API bridge queue: process once, no retry

`getNextBlock()` deletes the block from `pendingBlocks` before processing. Failed votes are not re-queued. The 5-minute ticker only drains remaining queue entries.

`decentralized-api/internal/server/public/bridge_handlers.go` — `getNextBlock`, `processReceipt`

### 2. `MsgBridgeExchange` uses `SendTransactionAsyncNoRetry`

Bridge votes bypass the halt-aware retry path used by PoC/validation:

- `updateChainHalt()` halt flag is **ignored**; broadcast still attempted during stale/halted chain.
- `broadcastMessage` returns `nil` error even when `resp.Code != 0` (CheckTx failure only logged as `Broadcast failed immediately` in tx_manager).

`decentralized-api/cosmosclient/cosmosclient.go` — `BridgeExchange`  
`decentralized-api/cosmosclient/tx_manager/tx_manager.go` — `SendTransactionAsyncNoRetry`, `broadcastMessage`

### 3. Geth bridge does not replay delivered blocks

Each finalized Ethereum block is POSTed once to `/admin/v1/bridge/block`. HTTP 200 (`Block queued`) advances the cursor regardless of whether the on-chain vote succeeded. No reconciliation for `BRIDGE_PENDING` txs.

`bridge/script.sh` (`--bridge.postblock`)

## Likely failure mode at unpause

Unordered txs use `timeout = latestBlockTime + 60s`. After a long pause, `latestBlockTime` is stale → timeout can be **in the past** → CheckTx rejection. Bridge handler still logs `Processing receipt` and drops the block from queue.

## Impact

- Inbound bridge deposits can stall at `BRIDGE_PENDING` forever
- `Processing receipt` log is misleading (success appearance on failure)
- No self-heal without manual re-post or manual `bridge-exchange` CLI

## Suggested fixes (priority order)

1. Surface broadcast failures in `BridgeExchange` (`resp.Code != 0` / `classifyBroadcastResponse`)
2. Use retry/halt-aware tx path for bridge votes (`SendTransactionAsyncWithRetry` or equivalent)
3. Do not remove block from queue until vote broadcast succeeds (or keep failed-receipt retry set)
4. *(Optional)* Reconciliation loop: local validator submits missing votes for known `BRIDGE_PENDING` receipts
5. *(Optional)* Geth cursor ack only after processing success (API contract change)

## Verification

```bash
inferenced q inference bridge-transaction \
  --origin-chain ethereum --block-number 11116928 --receipt-index 199 \
  --node http://localhost:8000/chain-rpc/ -o json

docker logs api 2>&1 | grep -iE 'Broadcast failed|node block time is stale|Error processing bridge'
```
