---
title: "#1135 — PoC-decode proposal"
source: https://github.com/gonka-ai/gonka/issues/1135
issue_number: 1135
synced_at: 2026-07-09T15:38:34Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    PoC-decode proposal
    <span class="issues-number">#1135</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item">[@Red-Caesar](https://github.com/Red-Caesar) opened 2026-04-30 12:35 UTC</span>
    <span class="issues-meta-item">5 comments</span>
    <span class="issues-meta-item">Updated 2026-05-23 01:49 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #a2eeef; color: #24292f; border-color: #a2eeef;">enhancement</span></div>
</div>

<div class="issues-content" markdown="1">
# PoC-decode: Extending Proof-of-Compute to Decode Steps

## Summary

The current PoC procedure only validates the prefill step, but in real inference the majority of computation happens during decode. PoC-decode extends validation to cover every decode step.

The core idea: before inference begins, a fixed set of `k` reference points is placed evenly on a unit sphere. At each decode step, a slice of the model's hidden state is projected onto this sphere. The nearest reference point is identified and its index (the k-point ID) is recorded. Because different models produce different hidden states, they will land near different reference points, producing a different sequence of k-point IDs.

The method includes both inference and validation modes, and was tested against honest (same model, different hardware) and fraud (different model) scenarios using Qwen2.5-7B.

See [README](https://github.com/axeltec-software/gonka/blob/axeltec/poc-decode/proposals/poc-decode/README.md) for full details: theory, analysis, fraud resistance evaluation, and results.

## Motivation

Extends the Proof-of-Compute procedure to cover decode steps, bringing it closer to real inference workloads. Currently PoC only validates the prefill step, while in practice the majority of computation happens during decode.

## Impact

- **Affected components:** vLLM inference server, PoC validation pipeline
- **Who is impacted:** node operators (hosts), validators

## Detailed description

Validation was performed using Qwen2.5-7B across 25 block hashes × 40 nonces × 256 decode steps:

- **Honest setup** (same model, different hardware — RTX 4000 vs A100)
- **Fraud setup** (different model — AWQ vs FP8-dynamic, same hardware)

<img width="1189" height="489" alt="Image" src="https://github.com/user-attachments/assets/3a007803-2341-4893-82e9-fad85a0a16da" />


Evidence and analysis:
- [Interactive 3D sphere projection](https://axeltec-software.github.io/ReportsHelper/poc-decode/sphere_projection.html)
- [Notebooks](https://github.com/axeltec-software/gonka/tree/axeltec/poc-decode/proposals/poc-decode/notebooks):
    - `analysis.ipynb` - hidden state distributions, k-point statistics, parameter sweep
    - `fraud-k-step.ipynb` - verification that hardcoded k diverges from real inference
    - `validation.ipynb` - honest vs fraud mismatch scatter plots

## Expected outcome

- A new `--poc-decode` flag enables the extended pipeline on the vLLM server
- Each inference response includes an array of k-point IDs for all decode steps
- Validation mode compares these arrays and returns a mismatch count per request
- Fraud nodes running a different model or quantization will produce a high mismatch rate, making them detectable

## Proposed approach

1. Before inference begins, construct a unit sphere with `k=16` equidistant points.
2. After prefill, select `sphere_dim=256` dimensions from the hidden state, project onto the unit sphere, and find the nearest k-point
3. At each decode step, repeat the projection using randomly selected hidden state dimensions (seeded by the previous step's k-point ID) to ensure a uniform distribution and resist prediction
4. Return the full `k_point_ids` array alongside the normal inference output

**Alternatives considered:**
- *Fixed dimension indices per step* - rejected because it leads to a skewed k-point distribution that is easier to exploit
- *Hardcoded k values* - rejected; experiments confirm that hardcoded IDs consistently diverge from the real inference trajectory.

**Open items:**
- CUDA graph support is required for decode performance;
- The current `sphere_dim=256` and `k_points=16` configuration was chosen based on initial experiments; further parameter tuning is possible.

**Implementation:** [axeltec-software/vllm @ axeltec/poc-decode-proposal](https://github.com/axeltec-software/vllm/tree/axeltec/poc-decode-proposal)



</div>

---

## 💬 Comments (5)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@unameisfine](https://github.com/unameisfine)</span>
    <span class="issues-meta-item">commented 2026-05-04 21:40 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Nice work on the experimental validation — the honest-vs-fraud scatter plots are convincing for the 7B setup, and the seed-chaining between decode steps (using previous k-point ID to select next dimensions) is a solid anti-prediction measure.</p>
<p>A few implementation-level observations from the current PoC pipeline:</p>
<h3>1. Integration with existing validation data path</h3>
<p>Current PoC artifacts are compact: each <code>PoCArtifactV2</code> carries a nonce + opaque vector bytes, and validation produces a single scalar distance compared via binomial test (<code>pow/data.py:220-228</code>, threshold <code>PROBABILITY_MISMATCH = 5e-4</code>).</p>
<p>Decode validation adds a <code>k_point_ids</code> array that grows linearly with sequence length. For Qwen3-235B at 4K+ output tokens, that is 4K+ integers per inference. A few questions worth addressing:
- How does this array get transmitted? Embedded in the inference response alongside tokens, or via a separate PoC artifact channel?
- Does the validator need to re-run the full autoregressive decode to verify? If yes, validation cost equals inference cost (currently the validator only does a single prefill pass).</p>
<h3>2. CUDA graph support is a production blocker</h3>
<p>The proposal flags this as an open item, but it is critical: vLLM relies heavily on CUDA graphs for decode throughput. Without graph support, decode latency can increase 2-5x, which would degrade inference quality during PoC and potentially trigger <code>ExecutionTimeout</code> (currently 1200s, governance-configurable via #1094).</p>
<p>Would be good to clarify whether the sphere projection can run as a post-hoc hook on captured activations (no graph break) vs requiring inline computation that breaks graphs.</p>
<h3>3. Model generalization</h3>
<p>Experiments use Qwen2.5-7B. Production runs Qwen3-235B-A22B (MoE, FP8). Two concerns:
- MoE architectures route tokens through different expert subsets — hidden state distributions may vary more between runs of the <em>same</em> model on <em>same</em> hardware (higher honest-mismatch baseline).
- FP8 quantization introduces hardware-dependent rounding. The <code>sphere_dim=256</code> projection might amplify these differences. Is there data on how the honest-mismatch rate scales with model size and quantization?</p>
<h3>4. Chain-side integration</h3>
<p>Current <code>PoCValidationV2</code> (poc_v2.proto) returns a single <code>validated_weight</code> per participant. Decode validation would need either:
- A new message type carrying per-inference mismatch stats, or
- Aggregation into the existing weight (e.g., penalize weight proportional to decode mismatch rate)</p>
<p>The SPRT framework (<code>sprt_precompute.go</code>) currently tracks invalidation/inactivity log-likelihood ratios. Decode mismatches could feed into the same SPRT accumulator if the mismatch metric is designed as a binary pass/fail per inference.</p>
<h3>5. Parameter sensitivity</h3>
<p><code>k=16</code> points on a unit sphere in <code>sphere_dim=256</code> space — the points are extremely sparse (surface area per Voronoi cell is huge). This means small perturbations in hidden states (honest variation) are unlikely to cause mismatches, which is good for low false-positive rate. But it also means a fraud model only needs to land in the correct Voronoi cell, not reproduce the exact activation — potentially leaving room for approximate-fraud models that are "close enough."</p>
<p>Is there analysis of the detection threshold as a function of k? What happens at k=64 or k=256 — does fraud detection improve without honest-mismatch degradation?</p>
<hr />
<p>Overall a promising direction — extending PoC to decode is clearly the right move for covering real workloads. The main blockers look like CUDA graph support and the validation cost question (does the validator need full autoregressive decode?).</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@Red-Caesar](https://github.com/Red-Caesar)</span>
    <span class="issues-meta-item">commented 2026-05-21 08:24 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Sorry for the delayed reply.</p>
<p>On CUDA graph support: this is indeed a critical concern. We are currently investigating options for it.</p>
<p>On model generalization and honest-mismatch rates: we've collected mismatch data for Qwen3-235B on A100 and are in the process of collecting on H100 as well. </p>
<p><img width="1075" height="603" alt="Image" src="https://github.com/user-attachments/assets/2229e135-6618-49ba-acb2-39e76d404c1e" /></p>
<p><img width="1075" height="537" alt="Image" src="https://github.com/user-attachments/assets/4ecc6a04-6f66-4804-b01b-c9d194c56d3b" /></p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@gmorgachev](https://github.com/gmorgachev)</span>
    <span class="issues-meta-item">commented 2026-05-21 12:20 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>hi @unameisfine !</p>
<blockquote>
<p>Does the validator need to re-run the full autoregressive decode to verify? If yes, validation cost equals inference cost (currently the validator only does a single prefill pass).</p>
</blockquote>
<p>During the current PoC Generation and Validation have exact cost per nonce (the both only prefill). But validators do validate only random sample from generated nonces. That's main mechanism to make validation cheaper</p>
<blockquote>
<ol>
<li>Chain-side integration
I think this research i focused more on replacement of PoC, not an inference validation. Why do you think SPRT / per request stats is needed? I</li>
</ol>
</blockquote>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@Red-Caesar](https://github.com/Red-Caesar)</span>
    <span class="issues-meta-item">commented 2026-05-22 10:48 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Here are the results for h100</p>
<p><img width="1052" height="647" alt="Image" src="https://github.com/user-attachments/assets/5d2cfda3-8500-4d24-81fe-67edd8a58144" /></p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@unameisfine](https://github.com/unameisfine)</span>
    <span class="issues-meta-item">commented 2026-05-23 01:49 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Thanks — went through <code>vllm/poc/poc_model_runner.py</code>. Confirmed:
<code>SPHERE_DIM=256</code>, <code>SPHERE_POINTS=16</code> (L39-40), codebook built once via
Thomson-problem gradient descent, <code>nearest_sphere_index</code> = cosine-similarity
argmax. Validation flow uses <code>inference_k_points_steps</code> to drive both the
next decode embedding (<code>generate_decode_inputs</code> at L474) and the per-step dim
subset (<code>random_pick_indices</code> at L507) — with the host's reference k used in
place of the validator's own — so honest validator and host run
computationally identical forward passes; only hardware/precision noise
diverges. That sharpens a couple of things:</p>
<p>@gmorgachev on validation cost — the validator does real prefill + sequential
decode (L466-538, <code>CUDAGraphMode.NONE</code> hardcoded), so per-nonce cost ≈ full
inference cost. Sampling nonces trims the count, not the per-nonce cost. One
cheaper option exists in principle: the decode inputs are deterministic
functions of <code>(block_hash, public_key, nonce, prev_k, step)</code>, and in
validation the full prev_k chain is given upfront via
<code>inference_k_points_steps</code> — so all decode embeddings can be precomputed and
concatenated into one parallel prefill pass instead of D sequential steps.
Tradeoff: decode and prefill kernels don't yield bit-identical hidden states
(GEMV vs GEMM, KV-cache vs full-prefill attention, accumulation order) —
that delta adds to the honest-mismatch baseline. Truncating is gameable.</p>
<p>(Side note: <code>CUDAGraphMode.NONE</code> is currently hardcoded on the PoC path —
that's the production-blocker concern from earlier, still active in code.)</p>
<p>On point 4 / SPRT — withdrawn. Was assuming continuous-PoC scope; if it's
pure PoC-replacement, existing weight aggregation is enough.</p>
<p>@Red-Caesar — the A100↔A100 vs A100↔H100 agreement (~15 in both) falls out
of the design more than the hardware. Both runs project from the same
host-seeded 256-dim subset against a 16-point codebook (huge Voronoi cells
per point), so most of the FP8-dequant/hardware delta in the hidden state
stays inside the same cell — honest mismatch ends up ~the same regardless of
which hardware combo you pair. Good for a heterogeneous fleet.</p>
<p>The flip side of the same mechanism sets the fraud-detection floor.
INT4-W4A16 vs FP8 (~52) is well outside the cells; a near-miss (same base
model at FP8 vs FP8-dynamic, or a sibling fine-tune) whose hidden-state
delta is comparable to hardware noise would stay inside the cells the same
way honest cross-hardware does, and look honest. Detection works when
delta_fraud &gt;&gt; delta_hardware; the cell size sets the boundary, not the
metric per se.</p>
<p>A separation sweep over <code>SPHERE_POINTS</code> × fraud-model distance would surface
where that floor sits. Bumping <code>SPHERE_POINTS</code> from 16 to 64/256 (the
<code>build_equidistant_codebook</code> call already takes it as a parameter) tightens
cells and raises the floor at some honest-mismatch cost — the
parameter-sensitivity question from earlier, now with the cross-hardware data
anchoring the tradeoff.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1135](https://github.com/gonka-ai/gonka/issues/1135) every hour.
