---
title: "#1200 — Independent review of PoC-decode results"
source: https://github.com/gonka-ai/gonka/issues/1200
issue_number: 1200
synced_at: 2026-09-29T08:40:48Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Independent review of PoC-decode results
    <span class="issues-number">#1200</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-05-19 23:36 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-09-28 21:41 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #4cbc0f; color: #24292f; border-color: #4cbc0f;">up-for-grabs</span></div>
</div>

<div class="issues-content" markdown="1">
Independently review and re-check the PoC-decode approach from https://github.com/gonka-ai/gonka/issues/1135 and the Axel-T experiments.

Current PoC correlates reasonably well with inference compute, but memory-usage coverage can be improved. The concern is that specialized versions could significantly accelerate PoC without equivalently improving real inference.

PoC-decode proposes extending Proof-of-Compute from prefill to decode steps.

Context

Relevant materials:

* Main issue: https://github.com/gonka-ai/gonka/issues/1135
* Presentation: https://docs.google.com/presentation/d/11zXgKd8q3t7SZ_wqfiMvCqTWqiKxJw65AFmAWDnMcL8/edit
* Experiment artifacts: https://drive.google.com/drive/folders/1tVh6mTsazMfjtSz-J0MTN8KYD5B9g1Bq
* Implementation branch: https://github.com/axeltec-software/vllm/tree/axeltec/poc-decode-proposal

Please use these materials as the source of truth.

## Task

Review the PoC-decode proposal and independently re-check the results.

The task should be treated as a critical review, not just a confirmation that the implementation runs.

## Review scope

Please check:

1. Whether the results from #1135 are reproducible.
2. Whether the hypothesis is confirmed beyond the initial experiments.
3. Whether the method should be tested on different models.
4. Whether the implementation can be integrated into the current vLLM path if the results are confirmed.
5. What makes migration painful and how to reduce that pain.
6. Whether a safer rollout can start only with new models.

## Review points

1. Re-check the reported results

Review the experiments from #1135 and the linked Axel-T materials.

Confirm whether the reported PoC-decode results hold under independent review.

2. Validate on different models

The current experiments provide the first confirmation of the hypothesis, but independent confirmation on different models is required before integration decisions.

Please identify and run, or define, the minimum additional model checks needed.

3. Review the implementation branch

Review the Axel-T vLLM branch:

https://github.com/axeltec-software/vllm/tree/axeltec/poc-decode-proposal

Check whether the implementation matches the method described in #1135 and whether it can be prepared for integration into the current vLLM path if the hypothesis is confirmed.

4. Review migration impact

Migration may be painful.

Please identify:

* what makes migration difficult;
* what can be done to reduce migration pain;
* whether rollout can start only with new models;
* what should be avoided during initial rollout.

5. Critical risk review

Risk level is medium: there is an initial positive signal, but the method still needs an honest critical review.

Please document:

* what is confirmed;
* what is not confirmed yet;
* what requires more experiments;
* what could block integration.

## Notes

This task is about independent verification and critical review.
If the results are confirmed on different models, the next step can be integration into the current vLLM path.
</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Ryanchen911">@Ryanchen911</a></span>
    <span class="issues-meta-item">commented 2026-09-26 03:04 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>hi @tcharchian , do you need help with this? Maybe I can take on this task.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-09-28 21:41 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Scope addendum, so a review of this issue matches the code as of 2026-09-28. The materials listed above (issue #1135, the April <code>axeltec-software/vllm</code> branch <code>axeltec/poc-decode-proposal</code>, the slides, and the Drive folder) are the original proposal. They are not the current integration target.</p>
<h2>What is already in production</h2>
<p><code>gonka</code> main runs PoC v2, not the prefill-only procedure this issue was written against.</p>
<ul>
<li>Method and rollout: <code>proposals/poc/README.md</code>. Random <code>inputs_embeds</code>, per-layer Householder transforms, a <code>k_dim=12</code> FP16 vector, L2 distance plus a binomial test, off-chain MMR commits. Model: <code>Qwen/Qwen3-235B-A22B-Instruct-2507-FP8</code>.</li>
<li>MLNode image base: <code>ghcr.io/gonka-ai/vllm:v0.25.1-poc-v4</code> (<code>mlnode/packages/api/Dockerfile</code>).</li>
<li>The chain stores commits, weight distribution, and validations. It has no decode scheme and no <code>k_point_ids</code> artifact. <code>docs/gonka_poc.md</code> still describes the older on-chain batch flow and is not the baseline.</li>
</ul>
<p>A review that only re-checks the April branch will miss the protocol a decode scheme has to fit.</p>
<h2>Where decode PoC actually lives</h2>
<p>Compute is the out-of-tree <code>gonka-poc</code> plugin (<code>gonka-ai/gonka-vllm-plugins</code>). The vLLM tree only has engine seams. Latest published plugin tag is <code>v0.1.6</code>. Tag <code>v0.2.0</code> is referenced by the 0.30 image recipe and is not cut yet.</p>
<table>
<thead>
<tr>
<th>Line</th>
<th>Engine</th>
<th>Plugin</th>
</tr>
</thead>
<tbody>
<tr>
<td>vLLM 0.25.1, shared batch</td>
<td><a href="https://github.com/gonka-ai/vllm/pull/100">gonka-ai/vllm#100</a> (open)</td>
<td><a href="https://github.com/gonka-ai/gonka-vllm-plugins/pull/8">gonka-vllm-plugins#8</a> (merged 2026-09-21)</td>
</tr>
<tr>
<td>vLLM 0.28, GLM-5.3-Flash</td>
<td><a href="https://github.com/gonka-ai/vllm/pull/113">gonka-ai/vllm#113</a> (open)</td>
<td><a href="https://github.com/gonka-ai/gonka-vllm-plugins/pull/12">gonka-vllm-plugins#12</a> (merged)</td>
</tr>
<tr>
<td>vLLM 0.30.0, v1 runner</td>
<td><a href="https://github.com/gonka-ai/vllm/pull/115">gonka-ai/vllm#115</a> (open; includes #114)</td>
<td><a href="https://github.com/gonka-ai/gonka-vllm-plugins/pull/20">gonka-vllm-plugins#20</a> (open)</td>
</tr>
</tbody>
</table>
<p><code>params.scheme</code> selects the proof. Omitting it keeps <code>prefill</code>, artifact-compatible with plugin <code>v0.1.3</code>. <code>decode</code> is the chained sphere-k trajectory. Both schemes are in scope: a decode change that moves prefill artifacts is a production break.</p>
<h2>What the review still has to cover</h2>
<p>These are already measured or already written, and they are not in the original task list.</p>
<ol>
<li>
<p><strong>Reproducibility is no longer only Qwen2.5-7B.</strong> #1135 comments add Qwen3-235B on A100 and H100. <a href="https://github.com/gonka-ai/vllm/pull/115">vllm#115</a> reports DeepSeek-V4-Flash-0731 FP8 on 1×B300: honest rerun 0/64 with margin 0.022 on the v1 runner, matching 0.25.1; the default v2 runner is 5/64 with margin 0.153 because artifacts depend on batch shape. <code>cudagraph_mode: PIECEWISE</code> does not fix that. <code>VLLM_USE_V2_MODEL_RUNNER</code> is forced to 0 on that branch. GLM-5.3-Flash is a third line. Production consensus model is still Qwen3-235B-FP8, and that pair is not in the 0.30 table.</p>
</li>
<li>
<p><strong>Fraud checks that exist, and the ones that do not.</strong> On the 0.30 image: one tampered step is 63/64, a wrong block hash is 64/64, and a <code>k=16</code> reference is a mismatch rather than a 400. The open question from #1135 still stands: with 16 points in 256 dimensions, a near-miss model (same base, different quant, or a close fine-tune) can stay inside the same cell as honest cross-hardware noise. A <code>SPHERE_POINTS</code> × fraud-distance sweep is still required before an integration decision.</p>
</li>
<li>
<p><strong>Validator cost.</strong> Validation is teacher-forced over the host's k-point chain, so per-nonce cost is a real decode, not a single prefill. Sampling nonces reduces the count, not the cost of each nonce. The parallel-prefill alternative (embeddings are a function of the chain, which validation already has) is unconfirmed, because prefill and decode kernels are not bit-identical and that delta adds to the honest-mismatch baseline.</p>
</li>
<li>
<p><strong>Engine hazards already found.</strong></p>
</li>
<li>A preempted PoC row whose artifact arrives later kills the next <code>schedule()</code> unless it is finished through the waiting queue (#115; missing on the earlier 0.28/0.30 ports).</li>
<li>Decode-chain cache keys must include every seed input. Keying on the nonce alone made a validator reuse the previous round's seeds: step 0 matched, later steps diverged, artifacts looked normal (plugin #8).</li>
<li>Prefill mining writes KV in place and was leaving those blocks cached. The next chat then read PoC KV: inference validation on MiniMax-M2.7 went from 16/16 to 0/16. Plugin #20 restores the prefix-cache reset for the prefill scheme only. Decode rows go through the scheduler and leave the cache alone.</li>
<li>KV capacity for DeepSeek on 0.30 is about half of 0.25.1 at the same flags (1.18M vs 2.41M tokens).</li>
<li>
<p>Prefill-scheme L2 against 0.25.1 artifacts has median 0.182 on that image. "Same scheme" is not "same bytes" across vLLM versions.</p>
</li>
<li>
<p><strong>Migration is a scheme switch inside v2, not a port of the April branch.</strong> A chain that never sends <code>scheme</code> stays on prefill, so decode can ship in the image before it affects weight. Weight, slashing, and the MMR artifact (<code>k_dim</code> vector, not a k-point sequence) do not change until the chain grows a decode artifact and a validation rule. The existing pattern for that is confirmation-PoC tracking plus a grace epoch (<code>poc_v2_enabled</code>, <code>confirmation_poc_v2_enabled</code>), not a flag day. "Start with new models only" has to be checked against multi-model PoC (<code>proposals/multi-model-poc/</code>): Qwen3-235B-FP8 is still the only consensus-eligible group.</p>
</li>
<li>
<p><strong>Mixed batch vs mining round.</strong> The plugin design runs PoC nonces and chat in one scheduler and one batch. The 0.30 measurement still reports chat <code>503</code> for the duration of <code>init/generate</code> (2048 nonces) and <code>200</code> after. Those two statements need to be reconciled in the review: shared-batch admission is not the same as an exclusive mining round.</p>
</li>
</ol>
<p>Please treat <a href="https://github.com/gonka-ai/vllm/pull/100">gonka-ai/vllm#100</a>, <a href="https://github.com/gonka-ai/vllm/pull/115">gonka-ai/vllm#115</a>, <a href="https://github.com/gonka-ai/gonka-vllm-plugins/pull/8">gonka-vllm-plugins#8</a>, and <a href="https://github.com/gonka-ai/gonka-vllm-plugins/pull/20">gonka-vllm-plugins#20</a> as in scope, together with #1135. The April branch is the origin of the method, not the tree to review for integration.</p>
<p>@Ryanchen911 this is the current scope if you take the review.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1200](https://github.com/gonka-ai/gonka/issues/1200) every hour.
