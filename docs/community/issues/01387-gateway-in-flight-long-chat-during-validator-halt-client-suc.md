---
title: "#1387 — Gateway in-flight long chat during validator halt: client success vs request outcome failed"
source: https://github.com/gonka-ai/gonka/issues/1387
issue_number: 1387
synced_at: 2026-07-13T13:28:09Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Gateway in-flight long chat during validator halt: client success vs request outcome failed
    <span class="issues-number">#1387</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item">[@maria-mitina](https://github.com/maria-mitina) opened 2026-07-02 15:00 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-07-06 05:24 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span></div>
</div>

<div class="issues-content" markdown="1">
## Summary

During **gonka-testnet-4** experiments on host **702111**, a long streaming chat through the devshard **gateway** (`POST http://127.0.0.1:18080/v1/chat/completions`) was started while all validator **`node`** containers on the 4-node fleet were stopped for **20 seconds**.

**Observed split behavior:**

| Layer | Result |
|-------|--------|
| HTTP client (curl/SSE) | Full stream, `[DONE]`, `curl_exit=0` |
| Gateway per-request accounting | `request_fully_settled` → **`outcome=failed`**, `winner_nonce=0` |
| Escrow finalize + on-chain settle | **Succeeded** (escrow closed on chain) |

This is confusing for operators and developers: users get a complete answer, metrics/logs show failure, and the escrow can still be settled.

---

## Environment

- **Chain:** `gonka-testnet-4`
- **Gateway host:** 702111 (`decentai@xj7-5.s.filfox.io:18222`)
- **Gateway:** `devshardctl-multi` on `:18080`, v2 binary mount, `DEVSHARD_ROUTE_PREFIX=/devshard/v2`
- **Model:** `Qwen/Qwen3-4B-Instruct-2507`
- **Orchestration:** `deploy/join/scripts/devshard-gateway-v2-inflight-orchestrate.sh`
- **Halt:** `prepare-compose-restart.sh coordinated-halt node 20 testnet-4` (702111, 702112, 702127, 702105)

---

## Test runs

### Escrow 30 (first run)

| Step | Result |
|------|--------|
| Long stream via gateway | ✓ 3648 chunks, `[DONE]` |
| Node halt overlap | ✓ stream active while all nodes down |
| Gateway request outcome | **failed** (`pairwise_ab_sample`, `winner_nonce=0`) |
| Finalize | Failed initially (`POST /v1/finalize` → 400 multi-devshard); succeeded with `POST /devshard/30/v1/finalize` |
| On-chain settle | ✓ `settled: true` |

### Escrow 31 (rerun, fixed finalize URL)

| Step | Result |
|------|--------|
| Long stream via gateway | ✓ 3892 chunks, `[DONE]`, 53s |
| Node halt overlap | ✓ (nodes down 14:49:56–14:50:34 UTC; stream ended 14:50:15) |
| Gateway request outcome | **failed** (`primary_unresponsive`, `winner_nonce=0`) |
| Finalize + settle | ✓ end-to-end |

**Settlement txs:** escrow 30 `CD619F85…`, escrow 31 `4B7DAC411DDF22B03BDFB6A71C353A96D565F7B52A64B150EC6B6FE48F7FD250`

---

## Timeline (escrow 31, UTC)

```
14:49:22  stream start (gateway direct)
14:49:22  first SSE chunk
14:49:56  ALL_NODE_DOWN (4 hosts)
14:50:15  stream [DONE] (3892 chunks) — nodes still down
14:50:27  gateway request_fully_settled outcome=failed
14:50:34  ALL_NODE_STARTED
```

---

## Root cause (protocol vs HTTP)

The gateway redundancy engine treats a request as **successful** only when a non-probe attempt is **protocol-finished** (`session.IsNonceFinished`), not when SSE content was delivered.

Relevant logic: `devshard/cmd/devshardctl/redundancy.go` → `finishRaceOutcome()`.

### What the logs show (both runs)

1. **Streaming succeeds to the client**
   - `first_token`, `stream_forwarding_started`, `send_completed` with thousands of chunks.

2. **Protocol finish fails after content**
   - `winner_failed_after_content`
   - `process_response_failed` with **`invalid state signature from host`** (signer address mismatch vs expected participant key).
   - Example (escrow 31):
     ```
     winner_failed_after_content … error="invalid state signature from host: host 1: expected gonka1l7q…jsjz5mrq, got gonka1ywc7pl…hkhngk"
     ```

3. **Race summary marks winner but not finished**
   - `race_completed … winner=true finished=false responsive=true output_chunks=3892`

4. **Timeout path during halt cannot recover**
   - `timeout_started … reason=refused`
   - Votes insufficient or timeout diff fails with same signature errors.
   - Final: `request_failed` → `inference: no non-probe attempt finished`
   - `request_fully_settled … winner_nonce=0 outcome=failed`

### Why finalize/settle still works

Per-request failure (`request_fully_settled`) is **not** the same as escrow session closure. Finalize snapshots the escrow state machine (`POST /devshard/{id}/v1/finalize`) and can produce valid settlement JSON even when the inflight HTTP request was marked failed.

---

## Developer-facing interpretation

| Question | Answer |
|----------|--------|
| Did the user get a response? | **Yes** — full long stream with `[DONE]`. |
| Did the gateway record a successful inference for that HTTP request? | **No** — `outcome=failed`, `winner_nonce=0`. |
| Was the escrow closed on chain? | **Yes** — after finalize (per-escrow URL). |
| Likely trigger during halt | Validator stop → chain/session signature validation breaks mid-stream → protocol finish fails while HTTP stream continues via API/ML. |

---

## Related fixes already made (scripts only, testnet)

- Gateway finalize must use **`/devshard/{escrow_id}/v1/finalize`** when multiple devshards are registered (not bare `/v1/finalize`).
- New scripts: `devshard-gateway-v2-inflight-node-halt-test.sh`, `devshard-gateway-v2-inflight-orchestrate.sh`.

---

## Suggested follow-ups

1. **Product/observability:** surface both client stream status and gateway `request_fully_settled.outcome` in test reports; alert on `failed` may false-positive when users received full content.
2. **Protocol behavior during validator halt:** clarify expected behavior when `node` is down but `api`/ML keep serving — should timeout votes succeed? should long streams after content be exempt (280s exemption exists but streams were ~53s)?
3. **`invalid state signature from host` during halt:** investigate whether this is expected (chain unavailable) or a bug in signer selection when validators restart.
4. **Finalize URL:** ensure gateway docs/runbooks and admin tooling always use per-escrow finalize in multi-escrow mode.

---

## Logs & evidence

**Gist (all attached logs):** https://gist.github.com/maria-mitina/4ef1f1e6813d768b21838cc9defdb0eb

Local copy in repo (not yet committed):

```
docs/evidence/devshard-gateway-inflight-node-halt/
├── README.md
├── gateway-escrow-30-request.log    # devshardctl-multi stages, escrow 30
├── gateway-escrow-31-request.log    # devshardctl-multi stages, escrow 31
├── stream-meta-escrow-31.meta       # client stream metadata
├── stream-escrow-31-last30.sse      # SSE tail incl. [DONE]
├── orchestrate-escrow-30.log        # orchestrator output (run 1)
└── orchestrate-rerun-escrow-31.log  # orchestrator output (rerun)
```

### Key log lines (escrow 31)

<details>
<summary>Client stream meta</summary>

```
curl_exit=0
stream_complete=true
chunk_lines=3892
duration_sec=53
client_url=http://127.0.0.1:18080/v1/chat/completions
```

</details>

<details>
<summary>Gateway settlement</summary>

```
stage=race_completed … winner=true finished=false … output_chunks=3892
stage=winner_failed_after_content … invalid state signature from host
stage=request_fully_settled … winner_nonce=0 decision=primary_unresponsive outcome=failed
```

</details>

---

## Reproduce

```bash
# On laptop (requires APPROVE=1)
cd deploy/join
APPROVE=1 HALT_SEC=20 HALT_SERVICES=node \
  ./scripts/devshard-gateway-v2-inflight-orchestrate.sh run
```

Requires gateway on 702111 with v2 binary mount and Inference phase (PoC finished).
</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@tcharchian](https://github.com/tcharchian)</span>
    <span class="issues-meta-item">commented 2026-07-03 07:29 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>hey @qdanik, would you be interested to work on this issue? </p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@qdanik](https://github.com/qdanik)</span>
    <span class="issues-meta-item">commented 2026-07-05 22:18 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@tcharchian you can assign it to me</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1387](https://github.com/gonka-ai/gonka/issues/1387) every hour.
