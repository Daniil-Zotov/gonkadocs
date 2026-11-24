---
title: "#2299 — v0.2.18: "PEX request too soon" disconnects isolate validators and halt the chain"
source: https://github.com/gonka-ai/gonka/issues/2299
issue_number: 2299
synced_at: 2026-11-24T11:06:00Z
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
    <span class="issues-meta-item">4 comments</span>
    <span class="issues-meta-item">Updated 2026-11-21 05:20 UTC</span>
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

## 💬 Comments (4)

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
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/gafrustam">@gafrustam</a></span>
    <span class="issues-meta-item">commented 2026-11-21 05:20 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>This looks like a CometBFT regression rather than a config change. CometBFT fixed this error in v0.38.16 (cometbft#4644, backported as #4649): <code>ensurePeers</code> asks a random peer for addresses only when it runs on the timer. v0.2.17 has that fix (v0.38.21). <code>upgrade-v0.2.18-sdk</code> (3a9d741, the commit testnet-4 runs) pins <code>github.com/cometbft/cometbft v0.40.0</code>, and neither 0.39.x nor 0.40.0 carries it. The <code>CometBFT 0.39.0</code> in the report is consistent with that: v0.40.0 still has <code>TMCoreSemVer = "0.39.0"</code> (<a href="https://github.com/cometbft/cometbft/blob/v0.40.0/version/version.go#L3-L8">version.go</a>).</p>
<pre><code class="language-go">// v0.38.21, p2p/pex/pex_reactor.go:511
if peersCount &gt; 0 &amp;&amp; ensurePeersPeriodElapsed {
    peer := peers[cmtrand.Int()%peersCount]
    r.RequestAddrs(peer)

// v0.40.0, p2p/pex/pex_reactor.go:509
peer := r.Switch.Peers().Random()
if peer != nil {
    r.RequestAddrs(peer)
</code></pre>
<p>This is the only behavioural difference in <code>p2p/pex/pex_reactor.go</code> between v0.38.21 and v0.40.0. v1.0.1 has the guard again (<code>if peer != nil &amp;&amp; ensurePeersPeriodElapsed</code>).</p>
<p>The untimed call is <code>ensurePeers(false)</code>, and <code>ReceiveAddrs</code> fires it only when the addresses came from a node listed in <code>p2p.seeds</code> (<a href="https://github.com/cometbft/cometbft/blob/v0.40.0/p2p/pex/pex_reactor.go#L375-L385">pex_reactor.go#L375-L385</a>). The response also clears <code>requestsSent</code>, and with fewer than 1000 known addresses <code>NeedMoreAddrs()</code> stays true, so the node at once asks a random peer again. When that peer is the seed again, the seed gets requests a round trip apart. On a new connection it lets the first two through, then drops the peer if a request comes less than <code>ensurePeersPeriod/3</code> = 10 s after the previous one (<a href="https://github.com/cometbft/cometbft/blob/v0.40.0/p2p/pex/pex_reactor.go#L303-L333">pex_reactor.go#L303-L333</a>). In the report's log the dropped request came ~200 ms after the previous one.</p>
<p>The report doesn't show yet that 18221 is the configured seed of the nodes it drops; in 18214's log it appears as the random peer, which both paths print. Two checks on existing data would settle it:
- effective <code>p2p.seeds</code> and <code>p2p.persistent_peers</code> on 18214, 18223, 18226 and 52095: the loop needs 18221 (<code>14522a9e…</code>) in <code>p2p.seeds</code>;
- their logs: the timer runs every 30 s, so two <code>Sending pexRequest to random peer</code> lines less than 30 s apart mean the untimed path ran.</p>
<p>On the drop the seed also calls <code>MarkBad(src, defaultBanTime)</code>, 24 h. That ban is in memory only: the address moves to <code>badPeers</code> and out of the book, and <code>addrbook.json</code> is written from the book alone (<a href="https://github.com/cometbft/cometbft/blob/v0.40.0/p2p/pex/file.go#L13-L35">file.go#L13-L35</a>), so a restart of the banning node clears it.</p>
<p>For mainnet it depends on which branch ships v0.2.18 (<code>upgrade-v0.2.18</code> still pins v0.38.21) and on each node's config. A node set up with <code>deploy/join</code> (<code>IS_GENESIS=false</code>) gets one seed from <code>set-seeds</code>, <code>node2.gonka.ai:5000</code> in <code>config.env.template</code>. <code>GENESIS_SEEDS</code> is only used with <code>IS_GENESIS=true</code> (<a href="https://github.com/gonka-ai/gonka/blob/3a9d741784f742af191210662926e41fb887578e/inference-chain/scripts/init-docker.sh#L176-L200">init-docker.sh#L176-L200</a>). If that seed stays connected as a regular peer, the same loop can start, though with many peers the random pick returns to it less often than in a 5-node network.</p>
<p>Options:
1. Pin a patched CometBFT the way cosmos-sdk is pinned: <code>replace github.com/cometbft/cometbft =&gt; github.com/gonka-ai/cometbft v0.40.0-gonka.1</code>, with the one-line change <code>if peer != nil &amp;&amp; ensurePeersPeriodElapsed {</code>.
2. For testnet-4, from the code (not tried): <code>persistent_peers</code> makes the nodes redial, but while the same validators are also in <code>p2p.seeds</code>, their PEX responses keep firing the untimed request. Listing them only in <code>persistent_peers</code> removes that trigger.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2299](https://github.com/gonka-ai/gonka/issues/2299) every hour.
