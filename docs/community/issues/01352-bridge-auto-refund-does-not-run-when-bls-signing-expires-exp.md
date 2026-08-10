---
title: "#1352 — Bridge: auto-refund does not run when BLS signing expires (EXPIRED)"
source: https://github.com/gonka-ai/gonka/issues/1352
issue_number: 1352
synced_at: 2026-08-10T02:38:40Z
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
    <span class="issues-meta-item"><a href="https://github.com/maria-mitina">@maria-mitina</a> opened 2026-06-19 16:47 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-07-07 23:26 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
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
    <span><a href="https://github.com/maria-mitina">@maria-mitina</a></span>
    <span class="issues-meta-item">commented 2026-06-19 17:03 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <h1>Testnet evidence retrieval (<code>gonka-testnet-4</code>)</h1>
<p>Run on seed host <code>702111</code>:</p>
<pre><code class="language-bash">ssh decentai@xj7-5.s.filfox.io -p 18222
cd /srv/dai
</code></pre>
<h2>Environment</h2>
<pre><code class="language-bash">export NODE=http://localhost:8000/chain-rpc/
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
</code></pre>
<h2>1. Chain height + BLS params</h2>
<pre><code class="language-bash">curl -s &quot;$NODE/status&quot; | jq '{height: .result.sync_info.latest_block_height, time: .result.sync_info.latest_block_time, chain: .result.node_info.network}'

$BIN query bls params --node &quot;$NODE&quot; --home &quot;$INF_HOME&quot; -o json \
  | jq '{signing_deadline_blocks, max_signing_attempts}'
</code></pre>
<p>Result </p>
<pre><code>{
  &quot;height&quot;: &quot;45291&quot;,
  &quot;time&quot;: &quot;2026-06-20T05:28:57.967035312Z&quot;,
  &quot;chain&quot;: &quot;gonka-testnet-4&quot;
}
{
  &quot;signing_deadline_blocks&quot;: null,
  &quot;max_signing_attempts&quot;: null
}
</code></pre>
<h2>2. Mint block — events + save plaintext <code>request_id</code></h2>
<pre><code class="language-bash">curl -s &quot;$NODE/block_results?height=$MINT_HEIGHT&quot; | python3 -c &quot;
import sys, json, base64, binascii
r = json.load(sys.stdin)['result']
for txr in r.get('txs_results', []) or []:
  for ev in txr.get('events', []) or []:
    t = ev.get('type','')
    if t == 'bridge_mint_requested' or 'ThresholdSigning' in t:
      print('===', t, '===')
      for a in ev.get('attributes',[]):
        k,v = a.get('key'), a.get('value','')
        print(f'  {k}: {v[:120]}...' if len(v)&gt;120 else f'  {k}: {v}')
      if 'ThresholdSigningRequested' in t:
        a = {x['key']: x['value'] for x in ev.get('attributes',[])}
        raw = a['request_id'].strip('\&quot;')
        try: b = base64.b64decode(raw)
        except: b = bytes.fromhex(raw)
        print('  KEY_hex=', binascii.hexlify(b).decode())
&quot;

curl -s &quot;$NODE/block_results?height=$MINT_HEIGHT&quot; | python3 -c &quot;
import sys, json
for txr in json.load(sys.stdin)['result'].get('txs_results', []) or []:
  for ev in txr.get('events', []) or []:
    if ev.get('type')=='bridge_mint_requested':
      for a in ev['attributes']:
        if a['key']=='request_id':
          open('/tmp/bridge_req_id.txt','w').write(a['value'])
          print('saved', len(a['value']), 'chars -&gt; /tmp/bridge_req_id.txt')
&quot;

wc -c /tmp/bridge_req_id.txt
</code></pre>
<p>The result will be </p>
<pre><code>wc -c /tmp/bridge_req_id.txt
=== inference.bls.EventThresholdSigningRequested ===
  current_epoch_id: &quot;100&quot;
  deadline_block_height: &quot;36124&quot;
  encoded_data: &quot;AAAAAAAAAGR6BXY4EcPwvc/4BgmWVRU5T0QnRdqmEG9Vxbe07a56Oyg03Eoidya7+OZLzDor5Qw85x+DE92yiwdUGECkaRLgAAAAAAAAAAAAAAAAAAAAAAA...
  message_hash: &quot;C7anTdy4LtPfIbWxPX/OtO0oqqjyX2jOJ4LK2N9flI0=&quot;
  request_id: &quot;KDTcSiJ3Jrv45kvMOivlDDznH4MT3bKLB1QYQKRpEuA=&quot;
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
saved 738 chars -&gt; /tmp/bridge_req_id.txt
738 /tmp/bridge_req_id.txt
</code></pre>
<h2>3. Verify <code>keccak256(plaintext)</code> matches BLS <code>request_id</code></h2>
<pre><code class="language-bash">cd /srv/dai/gonka/proposals/ethereum-bridge-contact
REQ_ID=&quot;$(cat /tmp/bridge_req_id.txt)&quot; node -e &quot;
const { keccak256, toUtf8Bytes } = require('ethers');
const b = Buffer.from(keccak256(toUtf8Bytes(process.env.REQ_ID)).slice(2), 'hex');
console.log('computed=', b.toString('base64'));
console.log('expected =', 'KDTcSiJ3Jrv45kvMOivlDDznH4MT3bKLB1QYQKRpEuA=');
console.log('match=', b.toString('base64') === 'KDTcSiJ3Jrv45kvMOivlDDznH4MT3bKLB1QYQKRpEuA=');
&quot;
</code></pre>
<p>Result</p>
<pre><code>computed= KDTcSiJ3Jrv45kvMOivlDDznH4MT3bKLB1QYQKRpEuA=
expected = KDTcSiJ3Jrv45kvMOivlDDznH4MT3bKLB1QYQKRpEuA=
match= true
</code></pre>
<h2>4. BLS signing request state</h2>
<pre><code class="language-bash">cd /srv/dai
$BIN query bls signing-history \
  --node &quot;$NODE&quot; --home &quot;$INF_HOME&quot; \
  --page-limit 500 -o json \
  | jq --arg id &quot;$BLS_ID&quot; '.signing_requests[] | select(.request_id==$id)'

$BIN query bls signing-history --node &quot;$NODE&quot; --home &quot;$INF_HOME&quot; --page-limit 500 --status-filter expired -o json \
  | jq '.signing_requests[] | {request_id, status, created_block_height, deadline_block_height, attempt}'

$BIN query bls signing-history --node &quot;$NODE&quot; --home &quot;$INF_HOME&quot; --page-limit 500 --status-filter cancelled -o json \
  | jq '.signing_requests[] | {request_id, status, created_block_height, deadline_block_height, attempt}'
</code></pre>
<p>Result - it is Cancelled because i cancelled manually the EXPIRED BLS tx and refunded manually as a test.</p>
<pre><code>{
  &quot;request_id&quot;: &quot;KDTcSiJ3Jrv45kvMOivlDDznH4MT3bKLB1QYQKRpEuA=&quot;,
  &quot;current_epoch_id&quot;: &quot;100&quot;,
  &quot;chain_id&quot;: &quot;egV2OBHD8L3P+AYJllUVOU9EJ0XaphBvVcW3tO2uejs=&quot;,
  &quot;data&quot;: [
    &quot;AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAE=&quot;,
    &quot;CsXlVAEeF4b1Bz8kMHvW1ii+NAmDSyqIoH38Wvmzcu4=&quot;,
    &quot;J0VjvfVSynzE4MCW5ZTUL+IdWjU=&quot;,
    &quot;U+o/8gV7e3+z2WpO9jrhBVjAips=&quot;,
    &quot;AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADuaygA=&quot;
  ],
  &quot;encoded_data&quot;: &quot;AAAAAAAAAGR6BXY4EcPwvc/4BgmWVRU5T0QnRdqmEG9Vxbe07a56Oyg03Eoidya7+OZLzDor5Qw85x+DE92yiwdUGECkaRLgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEKxeVUAR4XhvUHPyQwe9bWKL40CYNLKoigffxa+bNy7idFY731Usp8xODAluWU1C/iHVo1U+o/8gV7e3+z2WpO9jrhBVjAipsAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAO5rKAA==&quot;,
  &quot;message_hash&quot;: &quot;C7anTdy4LtPfIbWxPX/OtO0oqqjyX2jOJ4LK2N9flI0=&quot;,
  &quot;status&quot;: &quot;THRESHOLD_SIGNING_STATUS_CANCELLED&quot;,
  &quot;created_block_height&quot;: &quot;36114&quot;,
  &quot;deadline_block_height&quot;: &quot;36144&quot;,
  &quot;attempt&quot;: 3
}
jq: error (at &lt;stdin&gt;:3): Cannot iterate over null (null)
{
  &quot;request_id&quot;: &quot;KDTcSiJ3Jrv45kvMOivlDDznH4MT3bKLB1QYQKRpEuA=&quot;,
  &quot;status&quot;: &quot;THRESHOLD_SIGNING_STATUS_CANCELLED&quot;,
  &quot;created_block_height&quot;: &quot;36114&quot;,
  &quot;deadline_block_height&quot;: &quot;36144&quot;,
  &quot;attempt&quot;: 3
}
{
  &quot;request_id&quot;: &quot;7Zr3ERnMcKniqxDd9eEqnM91iVLtvrrY+uAYUIIEOdg=&quot;,
  &quot;status&quot;: &quot;THRESHOLD_SIGNING_STATUS_CANCELLED&quot;,
  &quot;created_block_height&quot;: &quot;35726&quot;,
  &quot;deadline_block_height&quot;: &quot;35756&quot;,
  &quot;attempt&quot;: 3
}
</code></pre>
<h2>5. Failure block — <code>EventThresholdSigningFailed</code>, no auto-refund</h2>
<pre><code class="language-bash">curl -s &quot;$NODE/block_results?height=$FAIL_HEIGHT&quot; | python3 -c &quot;
import sys, json
for ev in json.load(sys.stdin)['result'].get('finalize_block_events', []) or []:
  t = ev.get('type','')
  if 'bridge' in t or 'ThresholdSigning' in t:
    print('EVENT:', t)
    for a in ev.get('attributes',[]):
      print(' ', a.get('key'), '=', (a.get('value') or '')[:120])
&quot;

for H in $(seq 36140 36148); do
  curl -s &quot;$NODE/block_results?height=$H&quot; | python3 -c &quot;
import sys, json
h=int('$H')
for ev in json.load(sys.stdin)['result'].get('finalize_block_events', []) or []:
  t=ev.get('type','')
  if 'auto_refunded' in t or 'ThresholdSigning' in t:
    print(h, t)
&quot;
done
</code></pre>
<p>Result</p>
<pre><code>EVENT: inference.bls.EventThresholdSigningFailed
  current_epoch_id = &quot;100&quot;
  reason = &quot;deadline expired&quot;
  request_id = &quot;KDTcSiJ3Jrv45kvMOivlDDznH4MT3bKLB1QYQKRpEuA=&quot;
  mode = EndBlock
36144 inference.bls.EventThresholdSigningFailed
</code></pre>
<h2>6. Escrow + minter balances</h2>
<pre><code class="language-bash">curl -s &quot;http://localhost:8000/chain-api/cosmos/bank/v1beta1/balances/$ESCROW&quot; \
  | jq '{escrow: .balances[]|select(.denom==&quot;ngonka&quot;)}'

curl -s &quot;http://localhost:8000/chain-api/cosmos/bank/v1beta1/balances/$MINTER&quot; \
  | jq '{minter: .balances[]|select(.denom==&quot;ngonka&quot;)}'
</code></pre>
<p>Result - the 1 GNK returned after i manually cancelled </p>
<pre><code>{
  &quot;escrow&quot;: {
    &quot;denom&quot;: &quot;ngonka&quot;,
    &quot;amount&quot;: &quot;28000000000&quot;
  }
}
{
  &quot;minter&quot;: {
    &quot;denom&quot;: &quot;ngonka&quot;,
    &quot;amount&quot;: &quot;8956654055738664&quot;
  }
}
</code></pre>
<h2>7. Manual cancel tx (recovery)</h2>
<pre><code class="language-bash">$BIN query tx &quot;$CANCEL_TX&quot; --node &quot;$NODE&quot; -o json \
  | jq '{height, txhash, codespace, code, raw_log, events: [.events[]? | select(.type|test(&quot;bridge&quot;))]}'

H=$($BIN query tx &quot;$CANCEL_TX&quot; --node &quot;$NODE&quot; -o json | jq -r .height)
curl -s &quot;$NODE/block_results?height=$H&quot; | python3 -c &quot;
import sys, json
for txr in json.load(sys.stdin)['result'].get('txs_results',[]) or []:
  for ev in txr.get('events',[]) or []:
    if 'bridge' in ev.get('type',''):
      print(ev['type'])
      for a in ev.get('attributes',[]): print(' ', a['key'], '=', a['value'][:100])
&quot;
</code></pre>
<p>Result - proof of manual cancel and refund</p>
<pre><code>{
  &quot;height&quot;: &quot;36453&quot;,
  &quot;txhash&quot;: &quot;9AA0F01607708D5AA2CAF0D0BD0D3CA308510328753B7412CA439816D1E1D5B9&quot;,
  &quot;codespace&quot;: &quot;&quot;,
  &quot;code&quot;: 0,
  &quot;raw_log&quot;: &quot;&quot;,
  &quot;events&quot;: [
    {
      &quot;type&quot;: &quot;bridge_operation_cancelled&quot;,
      &quot;attributes&quot;: [
        {
          &quot;key&quot;: &quot;request_id&quot;,
          &quot;value&quot;: &quot;req_36114_0acd010aca010a292f696e666572656e63652e696e666572656e63652e4d7367526571756573744272696467654d696e74129c010a2c676f6e6b61316676703271356c7933737532377134306e7a683866326367796d7775647161336172327a6d6a120a313030303030303030301a2a3078323734353633424446353532636137634334453043303936653539344434326645323164356133352208657468657265756d2a2a30783533654133664632303537423742376662336439364134656636334145313035353863303841396212580a500a460a1f2f636f736d6f732e63727970746f2e736563703235366b312e5075624b657912230a2102b0f9d5a7e59fff1abd8e0f54a19b54250d26b3f568632b298c0e5f0c492f699f12040a020801183e120410a48e321a40b1c6d90b1ebf7ff8d18ac6ed3b8fd1c170727919135adc6cd5f2d083b7d070fb04723dd6f7c961f077933bdbfca6c337b82f5ceb727907834200cacd2ee34e77&quot;,
          &quot;index&quot;: true
        },
        {
          &quot;key&quot;: &quot;creator&quot;,
          &quot;value&quot;: &quot;gonka1fvp2q5ly3su27q40nzh8f2cgymwudqa3ar2zmj&quot;,
          &quot;index&quot;: true
        },
        {
          &quot;key&quot;: &quot;operation_type&quot;,
          &quot;value&quot;: &quot;mint&quot;,
          &quot;index&quot;: true
        },
        {
          &quot;key&quot;: &quot;cancel_mode&quot;,
          &quot;value&quot;: &quot;user&quot;,
          &quot;index&quot;: true
        },
        {
          &quot;key&quot;: &quot;refund_recipient&quot;,
          &quot;value&quot;: &quot;gonka1fvp2q5ly3su27q40nzh8f2cgymwudqa3ar2zmj&quot;,
          &quot;index&quot;: true
        },
        {
          &quot;key&quot;: &quot;msg_index&quot;,
          &quot;value&quot;: &quot;0&quot;,
          &quot;index&quot;: true
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
</code></pre>
<h2>8. Node logs (hook errors)</h2>
<pre><code class="language-bash">docker logs node 2&gt;&amp;1 | grep -iE \
  '2834dc4a|KDTcSiJ3|threshold signing fail|auto-refund|Failed to run threshold|failed to auto-refund|36144' \
  | tail -50
</code></pre>
<p>Result - None in the logs. </p>
<h2>9. Pending refund map (export)</h2>
<pre><code class="language-bash">$BIN export --home &quot;$INF_HOME&quot; --node &quot;$NODE&quot; 2&gt;/dev/null \
  | jq '{
      pending_mint_refunds: (.app_state.inference.bridge.pending_mint_refunds // []),
      count: ((.app_state.inference.bridge.pending_mint_refunds // []) | length)
    }'
</code></pre>
<p>Result - Nothing - the refund was not listed in pending... </p>
<hr />
<h2>Run A (earlier attempt @ 35726)</h2>
<pre><code class="language-bash">export MINT_HEIGHT=35726
export FAIL_HEIGHT=35756
export BLS_ID='7Zr3ERnMcKniqxDd9eEqnM91iVLtvrrY+uAYUIIEOdg='
# re-run sections 2–5 with these heights
</code></pre>
<h2>Notes</h2>
<ul>
<li><code>cancel-bridge-operation --request-id</code> must be the <strong>plaintext</strong> <code>req_&lt;height&gt;_…</code> from <code>bridge_mint_requested</code> (<code>/tmp/bridge_req_id.txt</code>), <strong>not</strong> the BLS base64 id (<code>KDTcSiJ3…=</code>).</li>
<li>BLS failure events appear in <strong><code>finalize_block_events</code></strong>, not <code>txs_results</code>.</li>
<li>Use <code>--page-limit</code> (not <code>--limit</code>) for <code>query bls signing-history</code>.</li>
</ul>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/maria-mitina">@maria-mitina</a></span>
    <span class="issues-meta-item">commented 2026-06-20 05:27 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>at the moment all filfox servers are down </p>
<p><img width="597" height="87" alt="Image" src="https://github.com/user-attachments/assets/38a75e11-eb3d-4c65-a54f-dc9e98227a2b" /></p>
<p>when they come back, i will need to take back and restore the environment to continue with testing. The data above will be gone. But we can simulate again on request</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1352](https://github.com/gonka-ai/gonka/issues/1352) every hour.
