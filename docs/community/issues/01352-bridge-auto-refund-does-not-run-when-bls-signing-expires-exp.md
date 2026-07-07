---
title: "#1352 — Bridge: auto-refund does not run when BLS signing expires (EXPIRED)"
source: https://github.com/gonka-ai/gonka/issues/1352
issue_number: 1352
synced_at: 2026-07-07T04:28:03Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Bridge: auto-refund does not run when BLS signing expires (EXPIRED)
    <span class="issues-number">#1352</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item">[@maria-mitina](https://github.com/maria-mitina) opened 2026-06-19 16:47 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-06-27 01:04 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content">
## Summary

When an outbound `RequestBridgeMint` BLS request reaches terminal **`EXPIRED`** (threshold not met), the chain emits `inference.bls.EventThresholdSigningFailed` but **does not** auto-refund bridge escrow. GNK stays locked until the user calls **`cancel-bridge-operation`** with the plaintext `request_id` from `bridge_mint_requested`.

Reproduced **twice** on `gonka-testnet-4` (manual test case [**#18**)](https://linear.app/gonka-core/issue/QA-33/verify-ethereumgnk-transaction-edge-cases#comment-8263c799). Unit tests pass in isolation; live integration fails.

Full evidence: `docs/bridge-auto-refund-on-expired-bug.md` (in working tree).

## Expected

`finalizeFailedThresholdSigningRequest` → `BlsHooks.AfterThresholdSigningFailed` → `ProcessAutoRefundForFailedBridgeOperation` → escrow refund + `bridge_operation_auto_refunded` + BLS → `CANCELLED`.

## Actual (run B @ block 36114)

| Check | Result |
|-------|--------|
| Mint height | 36114 |
| BLS id | `KDTcSiJ3Jrv45kvMOivlDDznH4MT3bKLB1QYQKRpEuA=` |
| Terminal block | 36144 — `EventThresholdSigningFailed` |
| `bridge_operation_auto_refunded` | **Absent** |
| Escrow while EXPIRED | 29B ngonka (+1 GNK locked) |
| BLS status | `EXPIRED` (not `CANCELLED`) |
| Manual cancel tx `9AA0F016…` (plaintext `req_36114_…`) | **Success** → escrow 28B |

Earlier run A (mint `8E610948…` @ 35726): same pattern — EXPIRED, no auto-refund, manual cancel worked.

## Code path

- `x/bls/keeper/threshold_signing.go`: `finalizeFailedThresholdSigningRequest` / `maybeCloseRetryAfterFailedPostProcess`
- `x/inference/module/bls_hooks.go`: `AfterThresholdSigningFailed`
- `x/inference/keeper/bridge_pending_refund.go`: `ProcessAutoRefundForFailedBridgeOperation`

Silent `(false, nil)` if hooks empty or pending not found — **no retry queue** for failure hooks.

## Test gap

`TestProcessAutoRefundForFailedBridgeOperation_Mint` calls refund logic **directly** and sets pending **after** expiry — does not wire `BlsHooks` on BLS keeper through `ProcessThresholdSigningDeadlines`.

## Workaround

`cancel-bridge-operation --request-id <plaintext req_<height>_…>` — **not** BLS base64 id.

## Suggested fixes

1. Integration test: mint → expire with wired `BlsHooks` → assert auto-refund.
2. Verify `InvokeSetBlsHooks` on deployed testnet/mainnet binaries.
3. Log when failure hook returns `(false, nil)`.
4. Optional: failure-hook retry queue (like completed post-process).

## Severity

**Medium** — funds stuck in escrow without user action; manual cancel required (easy to get wrong `request_id` format). Reduced from High because the expired signature situation will happen during incidents, not normal operation.
</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@maria-mitina](https://github.com/maria-mitina)</span>
    <span class="issues-meta-item">commented 2026-06-19 17:03 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    # Testnet evidence retrieval (`gonka-testnet-4`)

Run on seed host `702111`:

```bash
ssh decentai@xj7-5.s.filfox.io -p 18222
cd /srv/dai
```

## Environment

```bash
export NODE=http://localhost:8000/chain-rpc/
export INF_HOME=/srv/dai/.inference
export CHAIN_ID=gonka-testnet-4
export BIN=/srv/dai/inferenced

# Run B (primary reproduction)
export MINT_HEIGHT=36114
export FAIL_HEIGHT=36144
export BLS_ID='KDTcSiJ3Jrv45kvMOivlDDznH4MT3bKLB1QYQKRpEuA='
export CANCEL_TX='9AA0F01607708D5AA2CAF0D0BD0D3CA308510328753B7412CA439816D1E1D5B9'
export ESCROW=gonka1cjwjmyguyjaey70cgxxclxjh4wph3c8w0vvv63
export MINTER=gonka1fvp2q5ly3su27q40nzh8f2cgymwudqa3ar2zmj
```

## 1. Chain height + BLS params

```bash
curl -s "$NODE/status" | jq '{height: .result.sync_info.latest_block_height, time: .result.sync_info.latest_block_time, chain: .result.node_info.network}'

$BIN query bls params --node "$NODE" --home "$INF_HOME" -o json \
  | jq '{signing_deadline_blocks, max_signing_attempts}'
```
Result 
```
{
  "height": "45291",
  "time": "2026-06-20T05:28:57.967035312Z",
  "chain": "gonka-testnet-4"
}
{
  "signing_deadline_blocks": null,
  "max_signing_attempts": null
}
```
## 2. Mint block — events + save plaintext `request_id`

```bash
curl -s "$NODE/block_results?height=$MINT_HEIGHT" | python3 -c "
import sys, json, base64, binascii
r = json.load(sys.stdin)['result']
for txr in r.get('txs_results', []) or []:
  for ev in txr.get('events', []) or []:
    t = ev.get('type','')
    if t == 'bridge_mint_requested' or 'ThresholdSigning' in t:
      print('===', t, '===')
      for a in ev.get('attributes',[]):
        k,v = a.get('key'), a.get('value','')
        print(f'  {k}: {v[:120]}...' if len(v)>120 else f'  {k}: {v}')
      if 'ThresholdSigningRequested' in t:
        a = {x['key']: x['value'] for x in ev.get('attributes',[])}
        raw = a['request_id'].strip('\"')
        try: b = base64.b64decode(raw)
        except: b = bytes.fromhex(raw)
        print('  KEY_hex=', binascii.hexlify(b).decode())
"

curl -s "$NODE/block_results?height=$MINT_HEIGHT" | python3 -c "
import sys, json
for txr in json.load(sys.stdin)['result'].get('txs_results', []) or []:
  for ev in txr.get('events', []) or []:
    if ev.get('type')=='bridge_mint_requested':
      for a in ev['attributes']:
        if a['key']=='request_id':
          open('/tmp/bridge_req_id.txt','w').write(a['value'])
          print('saved', len(a['value']), 'chars -> /tmp/bridge_req_id.txt')
"

wc -c /tmp/bridge_req_id.txt
```
The result will be 
```
wc -c /tmp/bridge_req_id.txt
=== inference.bls.EventThresholdSigningRequested ===
  current_epoch_id: "100"
  deadline_block_height: "36124"
  encoded_data: "AAAAAAAAAGR6BXY4EcPwvc/4BgmWVRU5T0QnRdqmEG9Vxbe07a56Oyg03Eoidya7+OZLzDor5Qw85x+DE92yiwdUGECkaRLgAAAAAAAAAAAAAAAAAAAAAAA...
  message_hash: "C7anTdy4LtPfIbWxPX/OtO0oqqjyX2jOJ4LK2N9flI0="
  request_id: "KDTcSiJ3Jrv45kvMOivlDDznH4MT3bKLB1QYQKRpEuA="
  msg_index: 0
  KEY_hex= 2834dc4a227726bbf8e64bcc3a2be50c3ce71f8313ddb28b07541840a46912e0
=== bridge_mint_requested ===
  user: gonka1fvp2q5ly3su27q40nzh8f2cgymwudqa3ar2zmj
  amount: 1000000000
  destination_address: 0x274563BDF552ca7cC4E0C096e594D42fE21d5a35
  destination_bridge_address: 0x53eA3fF2057B7B7fb3d96A4ef63AE10558c08A9b
  chain_id: ethereum
  request_id: req_36114_0acd010aca010a292f696e666572656e63652e696e666572656e63652e4d7367526571756573744272696467654d696e74129c010a2c67...
  epoch_index: 100
  bls_request_id: req_36114_0acd010aca010a292f696e666572656e63652e696e666572656e63652e4d7367526571756573744272696467654d696e74129c010a2c67...
  msg_index: 0
saved 738 chars -> /tmp/bridge_req_id.txt
738 /tmp/bridge_req_id.txt
```

## 3. Verify `keccak256(plaintext)` matches BLS `request_id`

```bash
cd /srv/dai/gonka/proposals/ethereum-bridge-contact
REQ_ID="$(cat /tmp/bridge_req_id.txt)" node -e "
const { keccak256, toUtf8Bytes } = require('ethers');
const b = Buffer.from(keccak256(toUtf8Bytes(process.env.REQ_ID)).slice(2), 'hex');
console.log('computed=', b.toString('base64'));
console.log('expected =', 'KDTcSiJ3Jrv45kvMOivlDDznH4MT3bKLB1QYQKRpEuA=');
console.log('match=', b.toString('base64') === 'KDTcSiJ3Jrv45kvMOivlDDznH4MT3bKLB1QYQKRpEuA=');
"
```
Result
```
computed= KDTcSiJ3Jrv45kvMOivlDDznH4MT3bKLB1QYQKRpEuA=
expected = KDTcSiJ3Jrv45kvMOivlDDznH4MT3bKLB1QYQKRpEuA=
match= true
```
## 4. BLS signing request state

```bash
cd /srv/dai
$BIN query bls signing-history \
  --node "$NODE" --home "$INF_HOME" \
  --page-limit 500 -o json \
  | jq --arg id "$BLS_ID" '.signing_requests[] | select(.request_id==$id)'

$BIN query bls signing-history --node "$NODE" --home "$INF_HOME" --page-limit 500 --status-filter expired -o json \
  | jq '.signing_requests[] | {request_id, status, created_block_height, deadline_block_height, attempt}'

$BIN query bls signing-history --node "$NODE" --home "$INF_HOME" --page-limit 500 --status-filter cancelled -o json \
  | jq '.signing_requests[] | {request_id, status, created_block_height, deadline_block_height, attempt}'
```
Result - it is Cancelled because i cancelled manually the EXPIRED BLS tx and refunded manually as a test.
```
{
  "request_id": "KDTcSiJ3Jrv45kvMOivlDDznH4MT3bKLB1QYQKRpEuA=",
  "current_epoch_id": "100",
  "chain_id": "egV2OBHD8L3P+AYJllUVOU9EJ0XaphBvVcW3tO2uejs=",
  "data": [
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAE=",
    "CsXlVAEeF4b1Bz8kMHvW1ii+NAmDSyqIoH38Wvmzcu4=",
    "J0VjvfVSynzE4MCW5ZTUL+IdWjU=",
    "U+o/8gV7e3+z2WpO9jrhBVjAips=",
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADuaygA="
  ],
  "encoded_data": "AAAAAAAAAGR6BXY4EcPwvc/4BgmWVRU5T0QnRdqmEG9Vxbe07a56Oyg03Eoidya7+OZLzDor5Qw85x+DE92yiwdUGECkaRLgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEKxeVUAR4XhvUHPyQwe9bWKL40CYNLKoigffxa+bNy7idFY731Usp8xODAluWU1C/iHVo1U+o/8gV7e3+z2WpO9jrhBVjAipsAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAO5rKAA==",
  "message_hash": "C7anTdy4LtPfIbWxPX/OtO0oqqjyX2jOJ4LK2N9flI0=",
  "status": "THRESHOLD_SIGNING_STATUS_CANCELLED",
  "created_block_height": "36114",
  "deadline_block_height": "36144",
  "attempt": 3
}
jq: error (at <stdin>:3): Cannot iterate over null (null)
{
  "request_id": "KDTcSiJ3Jrv45kvMOivlDDznH4MT3bKLB1QYQKRpEuA=",
  "status": "THRESHOLD_SIGNING_STATUS_CANCELLED",
  "created_block_height": "36114",
  "deadline_block_height": "36144",
  "attempt": 3
}
{
  "request_id": "7Zr3ERnMcKniqxDd9eEqnM91iVLtvrrY+uAYUIIEOdg=",
  "status": "THRESHOLD_SIGNING_STATUS_CANCELLED",
  "created_block_height": "35726",
  "deadline_block_height": "35756",
  "attempt": 3
}
```
## 5. Failure block — `EventThresholdSigningFailed`, no auto-refund

```bash
curl -s "$NODE/block_results?height=$FAIL_HEIGHT" | python3 -c "
import sys, json
for ev in json.load(sys.stdin)['result'].get('finalize_block_events', []) or []:
  t = ev.get('type','')
  if 'bridge' in t or 'ThresholdSigning' in t:
    print('EVENT:', t)
    for a in ev.get('attributes',[]):
      print(' ', a.get('key'), '=', (a.get('value') or '')[:120])
"

for H in $(seq 36140 36148); do
  curl -s "$NODE/block_results?height=$H" | python3 -c "
import sys, json
h=int('$H')
for ev in json.load(sys.stdin)['result'].get('finalize_block_events', []) or []:
  t=ev.get('type','')
  if 'auto_refunded' in t or 'ThresholdSigning' in t:
    print(h, t)
"
done
```
Result
```
EVENT: inference.bls.EventThresholdSigningFailed
  current_epoch_id = "100"
  reason = "deadline expired"
  request_id = "KDTcSiJ3Jrv45kvMOivlDDznH4MT3bKLB1QYQKRpEuA="
  mode = EndBlock
36144 inference.bls.EventThresholdSigningFailed
```
## 6. Escrow + minter balances

```bash
curl -s "http://localhost:8000/chain-api/cosmos/bank/v1beta1/balances/$ESCROW" \
  | jq '{escrow: .balances[]|select(.denom=="ngonka")}'

curl -s "http://localhost:8000/chain-api/cosmos/bank/v1beta1/balances/$MINTER" \
  | jq '{minter: .balances[]|select(.denom=="ngonka")}'
```
Result - the 1 GNK returned after i manually cancelled 
```
{
  "escrow": {
    "denom": "ngonka",
    "amount": "28000000000"
  }
}
{
  "minter": {
    "denom": "ngonka",
    "amount": "8956654055738664"
  }
}
```

## 7. Manual cancel tx (recovery)

```bash
$BIN query tx "$CANCEL_TX" --node "$NODE" -o json \
  | jq '{height, txhash, codespace, code, raw_log, events: [.events[]? | select(.type|test("bridge"))]}'

H=$($BIN query tx "$CANCEL_TX" --node "$NODE" -o json | jq -r .height)
curl -s "$NODE/block_results?height=$H" | python3 -c "
import sys, json
for txr in json.load(sys.stdin)['result'].get('txs_results',[]) or []:
  for ev in txr.get('events',[]) or []:
    if 'bridge' in ev.get('type',''):
      print(ev['type'])
      for a in ev.get('attributes',[]): print(' ', a['key'], '=', a['value'][:100])
"
```
Result - proof of manual cancel and refund
```
{
  "height": "36453",
  "txhash": "9AA0F01607708D5AA2CAF0D0BD0D3CA308510328753B7412CA439816D1E1D5B9",
  "codespace": "",
  "code": 0,
  "raw_log": "",
  "events": [
    {
      "type": "bridge_operation_cancelled",
      "attributes": [
        {
          "key": "request_id",
          "value": "req_36114_0acd010aca010a292f696e666572656e63652e696e666572656e63652e4d7367526571756573744272696467654d696e74129c010a2c676f6e6b61316676703271356c7933737532377134306e7a683866326367796d7775647161336172327a6d6a120a313030303030303030301a2a3078323734353633424446353532636137634334453043303936653539344434326645323164356133352208657468657265756d2a2a30783533654133664632303537423742376662336439364134656636334145313035353863303841396212580a500a460a1f2f636f736d6f732e63727970746f2e736563703235366b312e5075624b657912230a2102b0f9d5a7e59fff1abd8e0f54a19b54250d26b3f568632b298c0e5f0c492f699f12040a020801183e120410a48e321a40b1c6d90b1ebf7ff8d18ac6ed3b8fd1c170727919135adc6cd5f2d083b7d070fb04723dd6f7c961f077933bdbfca6c337b82f5ceb727907834200cacd2ee34e77",
          "index": true
        },
        {
          "key": "creator",
          "value": "gonka1fvp2q5ly3su27q40nzh8f2cgymwudqa3ar2zmj",
          "index": true
        },
        {
          "key": "operation_type",
          "value": "mint",
          "index": true
        },
        {
          "key": "cancel_mode",
          "value": "user",
          "index": true
        },
        {
          "key": "refund_recipient",
          "value": "gonka1fvp2q5ly3su27q40nzh8f2cgymwudqa3ar2zmj",
          "index": true
        },
        {
          "key": "msg_index",
          "value": "0",
          "index": true
        }
      ]
    }
  ]
}
bridge_operation_cancelled
  request_id = req_36114_0acd010aca010a292f696e666572656e63652e696e666572656e63652e4d736752657175657374427269646765
  creator = gonka1fvp2q5ly3su27q40nzh8f2cgymwudqa3ar2zmj
  operation_type = mint
  cancel_mode = user
  refund_recipient = gonka1fvp2q5ly3su27q40nzh8f2cgymwudqa3ar2zmj
  msg_index = 0
```
## 8. Node logs (hook errors)

```bash
docker logs node 2>&1 | grep -iE \
  '2834dc4a|KDTcSiJ3|threshold signing fail|auto-refund|Failed to run threshold|failed to auto-refund|36144' \
  | tail -50
```
Result - None in the logs. 
## 9. Pending refund map (export)

```bash
$BIN export --home "$INF_HOME" --node "$NODE" 2>/dev/null \
  | jq '{
      pending_mint_refunds: (.app_state.inference.bridge.pending_mint_refunds // []),
      count: ((.app_state.inference.bridge.pending_mint_refunds // []) | length)
    }'
```
Result - Nothing - the refund was not listed in pending... 

---

## Run A (earlier attempt @ 35726)

```bash
export MINT_HEIGHT=35726
export FAIL_HEIGHT=35756
export BLS_ID='7Zr3ERnMcKniqxDd9eEqnM91iVLtvrrY+uAYUIIEOdg='
# re-run sections 2–5 with these heights
```

## Notes

- `cancel-bridge-operation --request-id` must be the **plaintext** `req_<height>_…` from `bridge_mint_requested` (`/tmp/bridge_req_id.txt`), **not** the BLS base64 id (`KDTcSiJ3…=`).
- BLS failure events appear in **`finalize_block_events`**, not `txs_results`.
- Use `--page-limit` (not `--limit`) for `query bls signing-history`.

  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@maria-mitina](https://github.com/maria-mitina)</span>
    <span class="issues-meta-item">commented 2026-06-20 05:27 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    at the moment all filfox servers are down 

<img width="597" height="87" alt="Image" src="https://github.com/user-attachments/assets/38a75e11-eb3d-4c65-a54f-dc9e98227a2b" />

when they come back, i will need to take back and restore the environment to continue with testing. The data above will be gone. But we can simulate again on request
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1352](https://github.com/gonka-ai/gonka/issues/1352) every hour.
