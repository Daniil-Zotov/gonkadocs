---
title: "#1370 — Bridge Scenario A: inbound USDT stuck BRIDGE_PENDING after coordinated node halt (4-validator testnet)"
source: https://github.com/gonka-ai/gonka/issues/1370
issue_number: 1370
synced_at: 2026-08-02T12:17:31Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Bridge Scenario A: inbound USDT stuck BRIDGE_PENDING after coordinated node halt (4-validator testnet)
    <span class="issues-number">#1370</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/maria-mitina">@maria-mitina</a> opened 2026-06-28 07:37 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-06-29 10:50 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

Manual reproduction of **Scenario A** (coordinated `node` halt with `bridge` + `api` kept running) on **gonka-testnet-4** with a live **Sepolia USDT** inbound deposit. Result: **FAIL** — deposit ingested by API on all hosts, but only **1/4** validator votes landed on-chain; deposit remains **`BRIDGE_PENDING`** with no second USDT mint.

Relates to #1358.

## Test environment

| Item | Value |
|------|--------|
| Network | `gonka-testnet-4` |
| Validators | 4 hosts on `xj7-5.s.filfox.io` |
| Images | `api:0.2.13-post1`, `bridge:0.2.14`, `inferenced:0.2.13` |
| Sepolia bridge | `0x5941d32709048aded24A1b7E1abFCe1Cf70210FB` |
| Sepolia USDT | `0x7169D38820dfd117C3FA1f22a697dBA58d90BA06` |

### Hosts

| SSH port | Hostname | Validator address |
|----------|----------|-------------------|
| 18222 | 702111 | `gonka1uthgqf4yapkw5356uud29cjk7u4rqd52pc6j0w` |
| 18223 | 702127 | `gonka1qrz72h8qf9dmjaqs26jxmq2q9aymh0667gmuzv` |
| 18226 | 702105 | `gonka1kz8n0devnsjq9g7plw7r5nrlxl8h6t22j3nna4` |
| 18221 | 702112 | `gonka1g5g4fmutlzv5t9mdhsf0ldc4rgjhmf0vakwc3w` |

## Sepolia deposit (test transaction)

| Field | Value |
|-------|--------|
| **Tx hash** | `0xbfc879d10c489090df4ba7a245075909564c915d228cd1252409497a0ab3266f` |
| **Etherscan** | https://sepolia.etherscan.io/tx/0xbfc879d10c489090df4ba7a245075909564c915d228cd1252409497a0ab3266f |
| Sepolia block | `11156647` |
| Sepolia time | 2026-06-28 07:00:36 UTC |
| Receipt index | `212` |
| Receipts root | `0x09cf1eff7decf066a0e23616c408ac93f6a1dd88df2581b16b3abd41268530b0` |
| Amount | 1 USDT (`1000000` base units) |
| ETH sender | `0x274563BDF552ca7cC4E0C096e594D42fE21d5a35` |
| Gonka recipient | `gonka1qdwgkcxww42sxmcm9gk0trvugev2g0248upwyq` |

## Procedure

1. User sent Sepolia USDT to bridge contract while chain was syncing.
2. **~07:11 UTC** — all four `node` containers stopped manually (`dc stop node`); `api` + `bridge` kept running.
3. During halt (~9 min): bridge handshake stalled at **11156632**; Geth could not post (API unreachable while `node` down broke API startup).
4. **~07:20 UTC** — all `node` containers restarted.
5. Geth burst-posted blocks **11156633–11156664** to all APIs.
6. Block **11156647** (deposit) processed on every host.

## Voting map

| Port | Host | Validator | Processed receipt? | On-chain vote? | Result |
|------|------|-----------|-------------------|----------------|--------|
| **18221** | 702112 | `gonka1g5g4f…` | Yes @ **07:20:38** | **Yes** | Vote recorded |
| **18222** | 702111 | `gonka1uthgqf…` | Yes @ **07:20:25** | **No** | Broadcast failed |
| **18223** | 702127 | `gonka1qrz72h…` | Yes @ **07:20:25** | **No** | Broadcast failed |
| **18226** | 702105 | `gonka1kz8n0d…` | Yes @ **07:20:25** | **No** | Broadcast failed |

## On-chain state (after test)

```bash
inferenced q inference bridge-transaction \
  --origin-chain sepolia --block-number 11156647 --receipt-index 212
```

| Field | Value |
|-------|--------|
| Status | `null` (`BRIDGE_PENDING`) |
| Epoch | `45` |
| Validators | 1 — `gonka1g5g4fmutlzv5t9mdhsf0ldc4rgjhmf0vakwc3w` |
| `totalValidationPower` | `18237` (insufficient quorum on 4-validator set) |
| Wrapped USDT balance | `1000000` (unchanged — prior deposit only; **second 1 USDT not minted**) |

## Why three hosts failed

All three failing hosts logged `Processing receipt` (looks successful) then immediately:

```
ERROR Broadcast failed immediately subsystem=Messages code=18
rawLog="unordered tx ttl exceeds 10m0s: invalid request"
originalMsgType=/inference.inference.MsgBridgeExchange
```

**18223** and **18226** also logged stale block time at the same instant:

```
WARN node block time is stale
latestBlockTime=2026-06-28T07:11:32.174Z
drift=8m53s
```

`07:11:32` is the **last chain block time before the halt**. Votes were broadcast in the **first second** after `node` restart (`07:20:25`) while the API still used stale block time for unordered tx TTL signing. CheckTx rejected the txs; `SendTransactionAsyncNoRetry` does not retry; bridge queue does not re-queue.

**Why 18221 succeeded:** same receipt processed **13 seconds later** (`07:20:38`) after block time refreshed — no `Broadcast failed` line; vote landed on-chain.

## Root cause (same as #1358)

1. `MsgBridgeExchange` uses `SendTransactionAsyncNoRetry` (no halt-aware retry).
2. Broadcast CheckTx failures are logged but **not surfaced** to bridge handler.
3. Geth cursor advances on HTTP 200; no replay.
4. API logs `Processing receipt` even when vote failed.

## Attached logs

Full API + bridge log extracts for blocks **11156630–11156670** and broadcast-error context:

**Gist:** https://gist.github.com/maria-mitina/6dc628e81592ec99dc094624c01d4ac9

| Gist file | Contents |
|-----------|----------|
| `api-18222-702111.log` | API logs — genesis host; `Broadcast failed` @ 07:20:25 |
| `api-18223-702127.log` | API logs — `stale` + `Broadcast failed` @ 07:20:25 |
| `api-18226-702105.log` | API logs — `stale` + `Broadcast failed` @ 07:20:25 |
| `api-18221-702112.log` | API logs — successful vote @ 07:20:38 (no broadcast error) |
| `bridge-18222-702111.log` | Bridge Geth — halt/unpause, API connectivity errors |
| `bridge-18223-702127.log` | Bridge Geth |
| `bridge-18226-702105.log` | Bridge Geth |
| `bridge-18221-702112.log` | Bridge Geth |

### Key log excerpts

**18223 @ 07:20:25 (failed):**
```
Processing receipt ... blockNumber=11156647 receiptIndex=212
WARN node block time is stale latestBlockTime=2026-06-28T07:11:32.174Z drift=8m53.520114365s
ERROR Broadcast failed immediately ... rawLog="unordered tx ttl exceeds 10m0s: invalid request"
```

**18221 @ 07:20:38 (succeeded):**
```
Processing receipt ... blockNumber=11156647 receiptIndex=212
(no Broadcast failed line)
```

## Suggested fixes

1. Use `SendTransactionAsyncWithRetry` for `MsgBridgeExchange`, or wait for fresh block time before broadcasting after halt.
2. Surface `resp.Code != 0` as failure to bridge handler (HTTP 500, do not advance processing).
3. Do not remove block from queue until vote confirmed on-chain.
4. Optional: reconciliation loop for `BRIDGE_PENDING` receipts.

## Recovery

Manual `bridge-exchange` from validators on **18222**, **18223**, **18226** with receipt index `212` and receipts root above.

## References

- #1358
- Prior pause test: `docs/bridge-inbound-pause-test-report.md`
- Scenario runbook: `docs/bridge-upgrade-scenario-a-runbook.md`
</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/maria-mitina">@maria-mitina</a></span>
    <span class="issues-meta-item">commented 2026-06-28 07:37 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <h2>Log file direct links (gist)</h2>
<p>Gist: https://gist.github.com/maria-mitina/6dc628e81592ec99dc094624c01d4ac9</p>
<h3>API logs (broadcast failure window)</h3>
<ul>
<li><a href="https://gist.githubusercontent.com/maria-mitina/6dc628e81592ec99dc094624c01d4ac9/raw/api-18222-702111.log">api-18222-702111.log</a> — <strong>Broadcast failed</strong> @ 07:20:25</li>
<li><a href="https://gist.githubusercontent.com/maria-mitina/6dc628e81592ec99dc094624c01d4ac9/raw/api-18223-702127.log">api-18223-702127.log</a> — <strong>stale + Broadcast failed</strong> @ 07:20:25</li>
<li><a href="https://gist.githubusercontent.com/maria-mitina/6dc628e81592ec99dc094624c01d4ac9/raw/api-18226-702105.log">api-18226-702105.log</a> — <strong>stale + Broadcast failed</strong> @ 07:20:25</li>
<li><a href="https://gist.githubusercontent.com/maria-mitina/6dc628e81592ec99dc094624c01d4ac9/raw/api-18221-702112.log">api-18221-702112.log</a> — successful vote @ 07:20:38</li>
</ul>
<h3>Bridge (Geth) logs (blocks 11156630–11156670 + halt period)</h3>
<ul>
<li><a href="https://gist.githubusercontent.com/maria-mitina/6dc628e81592ec99dc094624c01d4ac9/raw/bridge-18222-702111.log">bridge-18222-702111.log</a></li>
<li><a href="https://gist.githubusercontent.com/maria-mitina/6dc628e81592ec99dc094624c01d4ac9/raw/bridge-18223-702127.log">bridge-18223-702127.log</a></li>
<li><a href="https://gist.githubusercontent.com/maria-mitina/6dc628e81592ec99dc094624c01d4ac9/raw/bridge-18226-702105.log">bridge-18226-702105.log</a></li>
<li><a href="https://gist.githubusercontent.com/maria-mitina/6dc628e81592ec99dc094624c01d4ac9/raw/bridge-18221-702112.log">bridge-18221-702112.log</a></li>
</ul>
<p>Local copy path in repo workspace: <code>docs/bridge-scenario-a-2026-06-28/logs/</code></p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/maria-mitina">@maria-mitina</a></span>
    <span class="issues-meta-item">commented 2026-06-29 10:50 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>duplicate of https://github.com/gonka-ai/gonka/issues/1358 </p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1370](https://github.com/gonka-ai/gonka/issues/1370) every hour.
