---
title: "#1506 — Gateway host-health deadlock: mass quarantine → all hosts stuck as no-winner/suspicious"
source: https://github.com/gonka-ai/gonka/issues/1506
issue_number: 1506
synced_at: 2026-08-07T05:53:43Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Gateway host-health deadlock: mass quarantine → all hosts stuck as no-winner/suspicious
    <span class="issues-number">#1506</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/maria-mitina">@maria-mitina</a> opened 2026-07-27 09:48 UTC</span>
    <span class="issues-meta-item">3 comments</span>
    <span class="issues-meta-item">Updated 2026-07-30 10:44 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

I managed to get all hosts into a kind of deadlock on testnet.

### How everyone entered quarantine

I created an escrow with the wrong owner (CLI key ≠ `DEVSHARD_PRIVATE_KEY` the gateway signs with), registered it on the gateway, and sent chat. The gateway broadcast / raced the request across participants. Every host correctly rejected with **HTTP 403** (`restricted to escrow owner`). The gateway treated each 403 as a **host health signal** and applied a **~30 min** inference quarantine to each host that answered.

I understand there are multiple ways to enter quarantine (404 session missing, transport failures, empty streams, etc.). On a small testnet this was easy to trip for the whole set at once; on mainnet that mass fan-out should be harder, but the same mechanism still exists.

### How they got stuck after unquarantine

After I cleared quarantine via `POST /v1/admin/participants/unquarantine`, every host moved into **suspicious / no-winner probation** (`failure_strikes` left after quarantine; attempts marked `primary_no_winner` / `suspicious_winner_deferred`).

They never got out, because there were **no non-suspicious winners** left who could serve the client. Probation only clears when finished good attempts call `ObserveSuccessfulInference` (strike decrement). With every usable host on probation:

1. Hosts still run inference and return real content
2. Content is deferred (`suspicious_winner_deferred`, `winner_nonce=0`) — not crowned to the client
3. Request fails / times out
4. Strike recovery does not progress in practice when no clean host can complete the request for the client

So: **wrong-owner 403 → mass quarantine → mass unquarantine into probation → no clean crown path → permanent suspicious deadlock**.

### Observed on

- Host: testnet gateway `.79`
- Image: `ghcr.io/gonka-ai/devshard-gateway:testnet-v4-local` (built from `devshard-0.2.14-v4`)
- Log signals: `participant_limit_activated status=403`, `decision=primary_suspicious`, `primary_no_winner_reason=probation`, `suspicious_winner_deferred`, `picker_exhausted`

### Suggested product fixes

1. Do **not** quarantine participants on 403 “restricted to escrow owner” (misconfigured escrow / signer mismatch, not a bad host).
2. When **no clean host remains**, crown a suspicious winner that already returned good content (or accept deferred completions toward strike recovery).
3. Add an admin “forget / fully clear” path that lifts quarantine **without** leaving the host in no-winner probation (separate from soft unquarantine).

### Ops workaround that clears the stuck state

Restart the gateway after throttle rows are cleared (in-memory probation dies with the process). Soft unquarantine alone is not enough — it re-enters probation by design.

## Other ways to reach the same mass-quarantine shape

Same pattern every time: **one shared gateway/request fault × redundancy race × immediate quarantine = whole participant set dirty**. Then unquarantine (or natural expiry) → everyone on no-winner probation → no clean crown path.

### Immediate mass quarantine (one bad chat can hit everyone)

| Trigger | Duration | Shared cause that fans out |
|--------|----------|----------------------------|
| **403 Forbidden** on `/chat/completions` | ~30m | Wrong escrow owner (this incident); other host auth rejects that return 403 on inference |
| **404 Not Found** on inference | ~30m | Dead/missing session on hosts (`session not found`), escrow never registered, hosts wiped session storage while the gateway still routes it |
| **401 + `timestamp drift`** | ~30m | Gateway clock skew vs hosts, or signed requests aged in a long queue before send (>30s) |
| **429 / 503** | ~60m | All hosts overloaded (PoC / capacity / load); every raced host reports throttle |
| **Non-EOF transport failure** | ~30m | Gateway cannot reach anyone (bad participant URLs, network cut, TLS/dial failures across the set) |

These are the dangerous ones: **one attempt per host → quarantine**, no strike streak required.

### Slower / less “one-shot” mass quarantine

| Trigger | Needs | Mass risk |
|--------|-------|-----------|
| **Empty stream** | 3 strikes → shadow quarantine | Needs repeated empty finishes; empties are only counted when **another** attempt succeeded — harder in a total failure, easier under partial success + bad model/`max_tokens` across hosts |
| **EOF transport** | 3 consecutive EOFs | Flaky shared path (proxy, LB) can accumulate under load |
| **Stalled winner** | Immediate, but **only the crowned winner** | One host at a time — not a true mass event |

Vote/gossip transport failures are intentionally **ignored** and do not quarantine.

### Same deadlock after any of the above

Mass quarantine → admin unquarantine (or natural expiry) → **all hosts enter no-winner probation** (`failure_strikes` left after quarantine) → if no clean host remains, `suspicious_winner_deferred` forever.

### Highest-likelihood mainnet analogues

1. **404 / session missing** after restart, bad register, or escrow already gone
2. **Timestamp drift** during backlog / NTP issues
3. **429/503** during PoC or overload if the race still fans out
4. **Transport** if the gateway’s view of participant endpoints is wrong for everyone

Wrong-owner **403** is the cleanest demo on a small testnet; on mainnet, **404 + drift + overload** are the realistic mass paths.

</div>

---

## 💬 Comments (3)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/maria-mitina">@maria-mitina</a></span>
    <span class="issues-meta-item">commented 2026-07-27 09:52 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <h2>Gateway log evidence (testnet <code>.79</code>)</h2>
<p>Full excerpt: https://gist.github.com/maria-mitina/1da0f9c348343d406b90483a2c8d5e4d</p>
<p><strong>Image:</strong> <code>ghcr.io/gonka-ai/devshard-gateway:testnet-v4-local</code><br />
<strong>When:</strong> 2026-07-27 ~08:55–09:12 UTC</p>
<h3>A) Wrong-owner escrow 23 → every host 403 → mass quarantine</h3>
<p>After admin clear, chat against escrow <strong>23</strong> races all hosts; each returns <code>restricted to escrow owner</code> and is quarantined:</p>
<pre><code class="language-text">2026/07/27 08:55:47 participant_quarantine_cleared ...zena4439
2026/07/27 08:55:47 decision_made escrow=23 ... decision=primary_suspicious primary_no_winner_reason=probation primary_failure_strikes=2
2026/07/27 08:55:47 participant_limit_activated ...y5fs9j0r status=403 path_kind=inference
2026/07/27 08:55:47 send_failed escrow=23 ... error=&quot;... status 403: {\&quot;message\&quot;:\&quot;restricted to escrow owner\&quot;}&quot;
... (same 403 + participant_limit_activated for every host in the race) ...
2026/07/27 08:55:50 participant_limit_activated ...ag64jcz4 status=403 path_kind=inference
</code></pre>
<h3>B) Unquarantine again → still probation / no-winner on escrow 24</h3>
<pre><code class="language-text">2026/07/27 09:00:21 participant_quarantine_cleared ... (all hosts)
2026/07/27 09:00:21 decision_made escrow=24 ... decision=primary_suspicious primary_no_winner_reason=probation primary_failure_strikes=2
2026/07/27 09:00:22 suspicious_winner_deferred escrow=24 ... host=ag64jcz4
2026/07/27 09:00:23 suspicious_winner_deferred escrow=24 ... host=zena4439
2026/07/27 09:00:23 picker_exhausted ... attempt_failed
</code></pre>
<h3>C) Hosts finish real content but nothing is crowned (client timeout)</h3>
<p>Representative request <code>req-...-96</code> — all 6 escrow hosts <code>send_completed</code> with content, all <code>suspicious_winner_deferred</code>, <code>winner_nonce=0</code>:</p>
<pre><code class="language-text">2026/07/27 09:12:17 decision_made escrow=24 ... primary_suspicious primary_no_winner_reason=probation
2026/07/27 09:12:17 suspicious_winner_deferred ... y5fs9j0r / xsz307ef
2026/07/27 09:12:18 suspicious_winner_deferred ... zena4439 / vq8mg6gt
2026/07/27 09:12:19 suspicious_winner_deferred ... ag64jcz4
2026/07/27 09:12:22 suspicious_winner_deferred ... 9umz0l4g
2026/07/27 09:12:22 send_completed ... content_chunks=1 (each host)
2026/07/27 09:12:22 picker_exhausted ... tried every host in escrow
</code></pre>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/qdanik">@qdanik</a></span>
    <span class="issues-meta-item">commented 2026-07-27 10:05 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Q1: should we manage private key verification on the escrow side and prohibit the creation of escrow with an invalid private key?</p>
<p>Q2: should we reset quarantine count after the 30 mins period (now it decrease only 1, for example: 3 -&gt; 2). Quarantine count can be changed through the env variable</p>
<p>Q3: should we reset the escrow quarantines when all participants already marked as quarantined?</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/maria-mitina">@maria-mitina</a></span>
    <span class="issues-meta-item">commented 2026-07-27 10:10 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@qdanik as for Q1:  i think this may be my testnet trick - at the moment of creation all addresses were allwed to create escrows. this is not the case on Mainnet where we have limited number of allowed brokers, and they will configure the gateway correctly to sign with their private key i guess</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1506](https://github.com/gonka-ai/gonka/issues/1506) every hour.
