---
title: "#1690 — First full MNode image for Decode PoC (DeepSeek): testing + coefficients"
source: https://github.com/gonka-ai/gonka/issues/1690
issue_number: 1690
synced_at: 2026-09-12T09:26:12Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    First full MNode image for Decode PoC (DeepSeek): testing + coefficients
    <span class="issues-number">#1690</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-08-31 20:21 UTC</span>
    <span class="issues-meta-item">5 comments</span>
    <span class="issues-meta-item">Updated 2026-09-11 21:37 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Decode PoC thresholds and expert seeding for DeepSeek. DeepSeek seeding is more complex than MiniMax; the scheme needs a fix before coefficients alone are useful.
Kimi Decode PoC thresholds stay on hold (unclear future of Kimi on this path).
MiniMax image verification of the current implementation is #1689. Integration / design questions are #1688.
Confirm the live on-chain id from poc_params.models if it has drifted. Target: deepseek-ai/DeepSeek-V4-Flash-0731.

**Process**
— Experiments completed and written up (hardware, models, what passed, what did not)
— Seeding scheme for DeepSeek is described (how it differs from MiniMax)
— Scheme fix is written up before threshold collection is treated as done
— If work is DeepSeek-only: notes before handover, stating that Kimi is out of scope

**Expert seeding (DeepSeek)**
— Current seeding scheme is documented
— Why MiniMax seeding is not sufficient for DeepSeek is written up
— Scheme is fixed or a concrete proposal is on this issue
— Weight distribution across seeded experts is measured
— Closer-to-uniform weights across seeded experts are shown, with notes if uniform is not possible

**Thresholds (DeepSeek)**
— Decode PoC thresholds for DeepSeek are collected after the seeding scheme is stable
— How thresholds were measured is written up (hardware, setup, logs / notebooks)
— Thresholds are not treated as acceptance of a MiniMax-style full image — that bar is #1689

**Kimi**
— Kimi Decode PoC thresholds are explicitly out of scope on this issue (on hold)

**Handover**
- [ ] Seeding scheme notes published
- [ ] DeepSeek thresholds published, or listed as blocked on the scheme fix

</div>

---

## 💬 Comments (5)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/baychak">@baychak</a></span>
    <span class="issues-meta-item">commented 2026-08-31 20:26 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>TY!</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/clanster">@clanster</a></span>
    <span class="issues-meta-item">commented 2026-08-31 20:27 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>ty</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/baychak">@baychak</a></span>
    <span class="issues-meta-item">commented 2026-09-04 23:19 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p><strong>Dependency:</strong> not blocked by <a href="https://github.com/gonka-ai/gonka/issues/1688">#1688</a>. @tcharchian — for the ordering.</p>
<ul>
<li>The DeepSeek seeding scheme lives on this issue. <a href="https://github.com/gonka-ai/gonka/issues/1688">#1688</a> says so: <code>the scheme fix itself is #1690</code>.</li>
<li>Blocking this issue on it would be circular: <a href="https://github.com/gonka-ai/gonka/issues/1689">#1689</a> waits on the algorithm freeze, and that freeze includes this scheme.</li>
<li>The work is not blocked; publishing the numbers is. The scheme change for the hash-routed layers (pseudo token ids for the seeded decode steps, natural gate logits on those layers) and the tau-grid thresholds on vLLM 0.25.1 are measured on our forks.</li>
<li>Thresholds are posted here after the scheme note is written and the constants are signed off. They are consensus parameters, and we do not publish them before they are on chain.</li>
</ul>
<p>Ordering inside this issue is unchanged: thresholds count as done only after the seeding scheme is fixed and written up.</p>
<p><strong>Next:</strong> scheme note for the hash-routed layers, on this issue by 2026-09-08. Status update every Monday, next 2026-09-07.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/baychak">@baychak</a></span>
    <span class="issues-meta-item">commented 2026-09-11 21:23 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p><strong>Status:</strong> in progress. The seeding-scheme note is written; the 2026-09-08 date was missed.</p>
<p><strong>Since last</strong></p>
<ul>
<li>The scheme is fixed and described: pseudo token ids are always on for every model, hash-MoE gates keep their natural weights, an explicit model list guards that branch, and a model outside the list carrying an integer table on its gate is refused at attach. The note follows in a separate comment.</li>
<li>Why the MiniMax scheme was not enough: PoC rows carried token id 0, so the three token-id-routed layers executed the same 6 experts out of 256 for every nonce and every step, leaving the other 250 per layer unexercised. After the fix the ids vary per nonce and per step.</li>
<li>Uniform weights across those experts are not reachable: the model's own gate supplies the weight, and forcing it drove the weight to zero and made the coverage hollow. The per-layer histogram of attested experts after the fix is not measured yet — one instrumented run on one card.</li>
<li>Kimi is out of scope rather than on hold: the model is out of the chain, and GLM 5.3 takes its slot.</li>
</ul>
<p><strong>Next:</strong> the note as a comment here; DeepSeek thresholds after the choice of statistic and the sm80 policy are settled. Decode <code>dist_threshold</code> values are already in @vbgd0's <a href="https://github.com/gonka-ai/gonka/pull/1743">#1743</a>. Update here 2026-09-14.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/baychak">@baychak</a></span>
    <span class="issues-meta-item">commented 2026-09-11 21:37 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p><strong>Seeding scheme for DeepSeek-V4-Flash under decode-PoC</strong></p>
<h2>1. How the seeding works today</h2>
<p>A nonce is 256 prompt tokens and 256 decode steps. Each step stores the index of the
nearest of 12 reflection vectors; the chain of those indices is the artifact.</p>
<p>Two things are seeded from the block hash and the nonce, so that a prover cannot choose
what the model computes:</p>
<ul>
<li><strong>the reflection vectors</strong>, drawn per block hash and per nonce;</li>
<li><strong>the MoE routing</strong>: on every routed layer the gate's expert choice is restricted to a
  seeded, step-rotating window, so a nonce sweeps experts instead of resting on the few
  the model prefers.</li>
</ul>
<p>DeepSeek-V4-Flash has 43 layers and 256 experts with top-6 per token. Forty layers are
ordinary routed layers and take the seeded window. Three layers do not: they pick experts
by token id through an integer table, <code>tid2eid[vocab, 6]</code>, plus one shared expert. The
gate on those layers supplies the weights, not the choice.</p>
<h2>2. Why the MiniMax scheme is not enough here</h2>
<p>MiniMax has no token-id-routed layers, so seeding the router covers the model.</p>
<p>On DeepSeek it does not. PoC rows carried token id 0 in every position and on every step,
because a PoC row has no real prompt. Row 0 of <code>tid2eid</code> is a constant, so the three
token-id layers executed <strong>the same 6 experts out of 256 for every nonce and every step</strong>.
The other 250 experts on each of those layers were never exercised by PoC, and experts are
not shared between layers.</p>
<p>That is room to cheat: a prover can drop or damage the 250 unexercised experts per layer
and no nonce will notice, while chat traffic that does use them degrades.</p>
<h2>3. The fix</h2>
<p>Three parts, all in the plugin:</p>
<ul>
<li><strong>Pseudo token ids, always on, for every model.</strong> A PoC row's prefill phase gets ids from
  <code>derive_pseudo_input_ids</code> (the derivation the prefill scheme already uses); each decode
  step gets its id from the chain state (base, step, previous index) under its own salt.
  The id reaches only the token-id table; the row's embedding stays seeded. With the
  token-id branch disabled the substitution is bit-identical to the old constant 0, so
  MiniMax reference artifacts are unchanged (verified numerically).</li>
<li><strong>Token-id layers keep natural gate weights.</strong> Forcing the seeded window on those gates
  set the weight to <code>sqrt(softplus(-1e4))</code>, which is zero: the expert output was multiplied
  by zero and never entered the trajectory, so the new coverage would have been hollow.
  The choice stays deterministic through the table; the weights come from the gate's own
  logits at the table indices.</li>
<li><strong>An explicit model list guards the natural-weight branch.</strong> <code>_TOKEN_ID_ROUTED_MODELS</code>
  currently holds <code>deepseek_v4</code>. A model outside the list that carries an integer 2-D table
  on its gate is refused at attach with a message naming the list, rather than being
  handled silently. A unit test covers the refusal on a synthetic gate.</li>
</ul>
<p>Structural auto-detection was considered and rejected: a model shipping a similar table
would silently change how PoC attests it, and that is a consensus property. An explicit
list forces a human to look at the model first. The boot log states what happened:
<code>hash-MoE gates left natural: 3</code> and <code>40 MoE routers seeded</code>.</p>
<h2>4. What the experts see, before and after</h2>
<p>Before the fix, per token-id layer: 6 of 256 experts, the same set for every nonce and
every step, and their contribution carried zero weight — nothing was attested at all.</p>
<p>After the fix the ids vary per nonce and per step, so the table picks vary through a run,
and the weights are the model's own gate scores at those indices. Two consequences worth
stating plainly:</p>
<ul>
<li>coverage is now bounded by how many distinct ids a run produces, not by a constant;</li>
<li>the weight distribution across the seeded experts is <strong>not</strong> uniform and cannot be made
  uniform: on these layers the model, not the scheme, decides the weight, and forcing it is
  exactly what produced the zero-weight hollow coverage.</li>
</ul>
<p>We have not yet measured the per-layer histogram of attested experts after the fix. What is
checked today is the boot-log assertion above and a regression that the verdict is
unchanged. Measuring the histogram is one instrumented run on one card; say the word and it
goes into the next campaign.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1690](https://github.com/gonka-ai/gonka/issues/1690) every hour.
