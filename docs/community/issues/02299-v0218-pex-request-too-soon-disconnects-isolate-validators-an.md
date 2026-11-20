---
title: "#2299 — v0.2.18: "PEX request too soon" disconnects isolate validators and halt the chain"
source: https://github.com/gonka-ai/gonka/issues/2299
issue_number: 2299
synced_at: 2026-11-20T21:16:22Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    v0.2.18: "PEX request too soon" disconnects isolate validators and halt the chain
    <span class="issues-number">#2299</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/maria-mitina">@maria-mitina</a> opened 2026-11-20 09:20 UTC</span>
    <span class="issues-meta-item">3 comments</span>
    <span class="issues-meta-item">Updated 2026-11-20 10:12 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #F9EDEA; color: #24292f; border-color: #F9EDEA;">Bug</span></div>
</div>

<div class="issues-content" markdown="1">
## Summary

After the v0.2.18 upgrade on gonka-testnet-4, validators keep disconnecting each other with `sent next PEX request too soon`. The receiving node drops the peer because it sent a second PEX address request ~200 ms after the first, while `minInterval` is 10 s. It started right after the upgrade and keeps recurring every few minutes.

> **Update: this leads to a chain halt.** Repeated drops leave validators with no peers, and PEX can't find new ones (`No addresses to dial. Falling back to seeds`). On gonka-testnet-4, two validators holding 42% of the power became isolated and the chain halted at height 155452, right after the epoch 432 validator switch (the second PoC after the upgrade). Details: https://github.com/gonka-ai/gonka/issues/2299#issuecomment-7036823221

## Environment

- Chain: gonka-testnet-4, 5 validators
- Upgrade `v0.2.18` (proposal 11), applied at height 154732
- Node now: `v0.2.18-testnet-1` (commit `3a9d741`), Cosmos SDK `v0.55.0-ps1`, CometBFT `0.39.0`, go1.26.5
- Node before: `v0.2.17-testnet-4`, Cosmos SDK `v0.53.3-ps19-observability`

## Log

```
9:03AM ERR Stopping peer for error err="peer (895e19fede64f2c6389984cb8d78ac58702adb47) sent next PEX request too soon. lastReceived: 2026-11-20 09:03:19.303624221 +0000 UTC m=+331.866403687, now: 2026-11-20 09:03:19.506378047 +0000 UTC m=+332.069157513, minInterval: 10s. Disconnecting" module=p2p peer="Peer{MConn{<host-ip>:19227} 895e19fede64f2c6389984cb8d78ac58702adb47 out}"
```

## Who sends and who drops

All five nodes run v0.2.18. Disconnects logged since the upgrade (08:57 UTC):

| Node | Node ID | Drops it logged for "PEX request too soon" |
|---|---|---:|
| 18221 | `14522a9e…` | 9 |
| 18223 | `2dd3dca6…` | 2 |
| 52095 | `a654f72d…` | 1 |
| 18214 | `895e19fe…` | 0 |
| 18226 | `e5e3f091…` | 0 |

- Every other node (18214, 18223, 18226, 52095) shows up as the "too soon" sender.
- 18221 does most of the dropping, probably because the others use it as their address source (seed or persistent peer).

Timeline of 18221's drops: 08:58 (18223), 09:03 (18214), 09:05 (18223, 52095), 09:06, 09:10, 09:11 (18226), 09:13 (18223). On 18221 these lines appear only after the upgrade: 9 in the last 24 hours, all after the 08:57 halt.

## Impact so far

| Check | Before upgrade | After upgrade |
|---|---|---|
| Average block time | 5.35 s (blocks 154332–154731) | 5.52 s (238 blocks) |
| Signatures in the last 50 blocks | – | 5 of 5 in every block |
| Missed-blocks counter | – | 0 for all validators, none jailed |

No missed votes yet. But validator-to-validator connections are being torn down every few minutes. On a bigger network or under load, this could cost votes and slow down peer discovery.

## Likely cause (not confirmed in code)

The v0.2.18 node (SDK 0.55 / CometBFT 0.39) sends PEX address requests faster than its own peers accept. The two requests 200 ms apart look like a request on peer connect plus one from the ensure-peers timer, with nothing to throttle them against the 10 s `minInterval`. This is an inference from the logs. Things worth checking:
- the PEX `ensurePeersPeriod` and request throttling in the CometBFT version bundled with v0.2.18
- whether the default p2p/PEX config changed between v0.2.17 and v0.2.18
- whether the receiver's `minInterval` check now runs against requests that the old version would have spaced out

## Steps to reproduce

1. Run a multi-validator network on v0.2.17 and upgrade it to v0.2.18.
2. Grep the node logs: `docker logs node 2>&1 | grep "PEX request too soon"`.


</div>

---

## 💬 Comments (3)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/maria-mitina">@maria-mitina</a></span>
    <span class="issues-meta-item">commented 2026-11-20 09:21 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@d-bogdan-engenious fyi</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/maria-mitina">@maria-mitina</a></span>
    <span class="issues-meta-item">commented 2026-11-20 09:54 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p><strong>Update (09:42 UTC):</strong> the PEX churn hasn't settled since the upgrade. On 18221 it's getting more frequent.</p>
<table>
<thead>
<tr>
<th>Window (UTC)</th>
<th style="text-align: right;">"PEX request too soon" drops on 18221</th>
</tr>
</thead>
<tbody>
<tr>
<td>08:58–09:13</td>
<td style="text-align: right;">8</td>
</tr>
<tr>
<td>09:15–09:42</td>
<td style="text-align: right;">23 (~1 per minute)</td>
</tr>
</tbody>
</table>
<p>18221 drops all four other validators: 18214 ×7, 18226 ×7, 52095 ×6, 18223 ×3 since 09:15. On their side the same disconnects show as <code>Stopping peer for error err=EOF</code> (5–8 per node).</p>
<p>Consensus is still fine. All 5 nodes are producing blocks, and there's no <code>CONSENSUS FAILURE</code>, panic or app-hash error.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/maria-mitina">@maria-mitina</a></span>
    <span class="issues-meta-item">commented 2026-11-20 10:08 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p><strong>Update (10:08 UTC): the PEX churn has escalated to a chain halt on gonka-testnet-4.</strong></p>
<p>The chain stopped at height <strong>155452</strong> (last block 10:03:44 UTC), 7 blocks after the epoch 432 <code>set_new_validators</code> (155445). This was the second PoC after the v0.2.18 upgrade.</p>
<table>
<thead>
<tr>
<th>Node</th>
<th>Height</th>
<th style="text-align: right;">Peers</th>
<th style="text-align: right;">Voting power (epoch 432)</th>
</tr>
</thead>
<tbody>
<tr>
<td>18214</td>
<td>155449 (behind)</td>
<td style="text-align: right;"><strong>0</strong></td>
<td style="text-align: right;">3826</td>
</tr>
<tr>
<td>18223</td>
<td>155452</td>
<td style="text-align: right;"><strong>0</strong></td>
<td style="text-align: right;">3694</td>
</tr>
<tr>
<td>18221</td>
<td>155452</td>
<td style="text-align: right;">1</td>
<td style="text-align: right;">3317</td>
</tr>
<tr>
<td>18226</td>
<td>155452</td>
<td style="text-align: right;">1</td>
<td style="text-align: right;">3442</td>
</tr>
<tr>
<td>52095</td>
<td>155452</td>
<td style="text-align: right;">2</td>
<td style="text-align: right;">3522</td>
</tr>
</tbody>
</table>
<p>The two isolated validators hold 7520 / 17801 power (42%), so the connected nodes can't reach 2/3 and no block can be committed.</p>
<p><strong>How the nodes get isolated</strong> (from 18214's node log):
1. 18221 keeps dropping 18214 for "PEX request too soon" (<code>Stopping peer for error err=EOF</code> on 18214's side), until 18214 is down to one outbound peer, then none.
2. PEX then can't recover:
   <code>INF Ensure peers module=pex numDialing=0 numInPeers=0 numOutPeers=1 numToDial=9
   INF We need more addresses. Sending pexRequest to random peer module=pex peer="Peer{MConn{&lt;host-ip&gt;:19241} 14522a9e… out}"
   INF No addresses to dial. Falling back to seeds module=pex</code>
   The only seed configured is unreachable, so a node that loses its peers stays isolated.
3. Before losing everything, 18214 was already falling behind (<code>commit is for a block we do not know about; set ProposalBlock=nil</code>). Every round where it was proposer timed out: block 155443 → 155444 took 65 s instead of ~5.5 s.
4. 18223 followed. With more than 1/3 of the power cut off, the chain halted.</p>
<p>So this is no longer just log noise. Under v0.2.18, PEX churn plus an empty address book progressively isolates validators until consensus stops. A chain that halts "after the second PoC" may be the same failure.</p>
<p><strong>Mitigation being considered:</strong> set <code>persistent_peers</code> to the other validators on every node, so connections are redialled regardless of PEX.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2299](https://github.com/gonka-ai/gonka/issues/2299) every hour.
