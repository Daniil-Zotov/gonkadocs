---
title: "#926 — [P1] Seed for POC fix"
source: https://github.com/gonka-ai/gonka/issues/926
issue_number: 926
synced_at: 2026-07-14T10:58:48Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    [P1] Seed for POC fix
    <span class="issues-number">#926</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item">[@tcharchian](https://github.com/tcharchian) opened 2026-03-20 23:33 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-04-11 04:28 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #12a6e8; color: #24292f; border-color: #12a6e8;">Priority: Medium</span></div>
</div>

<div class="issues-content" markdown="1">
- [x] on-chain params to choose option 
- [x] MLNode support
- [x] way to monitor it
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@IgnatovFedor](https://github.com/IgnatovFedor)</span>
    <span class="issues-meta-item">commented 2026-03-31 17:54 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <h1>Proposal: Concatenated Murmur (concat_murmur)</h1>
<h2>The problem</h2>
<p><code>_seed_from_string</code> computes sha256(seed_string) but discards 224 of the 256 bits:</p>
<pre><code class="language-python">return int(h[:8], 16)  # only 32 bits used
</code></pre>
<p>With a 32-bit seed space, an attacker running Node A can find a nonce that produces the same seed as Node B's target
nonce in ~2^32 SHA256 evaluations. They then run the model once (as Node A) and submit that output as
Node A's and B's proof just with different nonces. The validator accepts it.</p>
<h2>Proposal</h2>
<p>SHA256 produces 256 bits. Split them into 8 × 32-bit words (s0, s1, ..., s7). Use each word as a murmur3 seed to
generate an independent segment of the output:</p>
<p>sha256(block_hash + public_key + nonce) → [s0 | s1 | s2 | s3 | s4 | s5 | s6 | s7]</p>
<p>output = [ murmur(s0, n/8) | murmur(s1, n/8) | ... | murmur(s7, n/8) ]</p>
<p>All 256 bits of SHA256 are consumed. The output is still N(0,1) — same murmur3 → Box-Muller pipeline,
just chunked into 8 segments that are concatenated.</p>
<h2>Why it solves the problem</h2>
<p>The attacker submits one nonce nonce_X. The verifier computes:</p>
<p>sha256(block_hash + key_B + nonce_X)  →  s0_X, s1_X, ..., s7_X</p>
<p>All 8 sub-seeds are locked to that single hash call. For the forged proof to pass, the attacker needs:</p>
<p>sha256(key_B + nonce_X) == sha256(key_A + nonce_Y)   [all 256 bits]</p>
<p>That is a SHA256 collision — 2^128 work by birthday attack. The attacker cannot attack the 8 segments independently
because changing nonce_X changes all 8 sub-seeds simultaneously through SHA256.</p>
<p>The "attack segments one by one" idea would require submitting 8 different nonces — one per segment — which the protocol
does not allow. One nonce → one hash → all 8 seeds determined at once.</p>
<h1>On-chain part</h1>
<h2>MLNode Version</h2>
<p>Add software_version field to HardwareNode proto message. The broker fetches the version from mlnode at node registration/update time and includes it in the on-chain tx. This makes the running mlnode/vllm version visible on-chain per node for auditing.</p>
<h2>PoC Stronger RNG (poc_stronger_rng_enabled)</h2>
<p>Add poc_stronger_rng_enabled bool to PocParams. When enabled via governance vote, switches PoC input vector generation from the legacy single 32-bit murmur3 seed to concatenated murmur3 using the full 256-bit SHA256 output.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #926](https://github.com/gonka-ai/gonka/issues/926) every hour.
