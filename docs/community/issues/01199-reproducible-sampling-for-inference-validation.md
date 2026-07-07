---
title: "#1199 — Reproducible sampling for inference validation"
source: https://github.com/gonka-ai/gonka/issues/1199
issue_number: 1199
synced_at: 2026-07-07T08:46:32Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Reproducible sampling for inference validation
    <span class="issues-number">#1199</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-05-19 23:17 UTC</span>
    <span class="issues-meta-item">5 comments</span>
    <span class="issues-meta-item">Updated 2026-07-06 02:53 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #4cbc0f; color: #24292f; border-color: #4cbc0f;">up-for-grabs</span></div>
</div>

<div class="issues-content" markdown="1">
Review the existing reproducible / deterministic sampling work for inference validation and prepare a careful path toward adding it to MLNode versions.

This task is related to the known inference validation vulnerability described in the inference validation proposal. The proposed direction is a two-stage validation system with a cheap sequence check before the existing distribution check.

The goal is to take over the existing experiments and base implementation, review them carefully for vulnerabilities, and define a safe non-enforcing rollout path before any strict validation behavior is enabled.

## Context

Relevant materials:

* Inference validation proposal, section “Proper Fix: Two-Stage Validation System”:
    https://github.com/gonka-ai/gonka/blob/main/proposals/inference-validation/inference-validation.md#proper-fix-two-stage-validation-system
* Existing deterministic sampling / validation document and base implementation by @tamazgadaev:
    https://github.com/gonka-ai/vllm/blob/tg/detemrinistic_sampling_dump/docs/DETERMINISTIC_SAMPLING_VALIDATION.md

Please use these documents as the source of truth for the proposed design, implementation status, artifact format, implementation plan, tests, and known limitations.  ￼

## Task

Review the existing proposal and deterministic sampling implementation, then prepare a safe path toward gradual MLNode integration.

This task is not primarily about writing new code immediately. The important part is to carefully review the approach, check for vulnerabilities, and define how to introduce it softly into MLNode versions while collecting data and avoiding strict enforcement at first.

## Review scope

Please review:

1. The two-stage validation design from the inference validation proposal.
2. Deterministic sampling validation document.
3. The existing branch / base implementation.
4. Current implementation status.
5. What can be added to MLNode versions softly.
6. What should remain non-enforcing for now.
7. What data should be collected before enabling stricter validation.

## Review points

1. Confirm alignment with the proposed fix

Check whether the current implementation matches the two-stage validation direction described in the proposal.

Please focus on whether the implementation correctly supports:

* sequence / sampling replay validation;
* existing distribution validation;
* the intended order of checks;
* the intended protection against the known validation weakness.

2. Review seed, RNG, and replay logic

Check whether the seed generation, RNG initialization, and replay logic are implemented consistently with the:

* Inference validation proposal, section “Proper Fix: Two-Stage Validation System”:
    https://github.com/gonka-ai/gonka/blob/main/proposals/inference-validation/inference-validation.md#proper-fix-two-stage-validation-system
* Existing deterministic sampling / validation document and base implementation by @tamazgadaev:
    https://github.com/gonka-ai/vllm/blob/tg/detemrinistic_sampling_dump/docs/DETERMINISTIC_SAMPLING_VALIDATION.md

Please verify whether the validator can reliably replay the sampling step from the provided artifact and seed data.

3. Review artifact contents

Check whether the artifact contains everything required for replay and validation.

Please compare the artifact requirements in the proposal with the artifact format described in @tamazgadaev’s document.

4. Review implementation status

Using prvided documents above , identify:

* what already exists;
* what still needs to be modified;
* what still needs to be created;
* whether the implementation plan in the document is still accurate;
* whether the existing code is ready to be included in MLNode versions softly.

5. Review safe MLNode rollout

The intended direction is to start introducing this into MLNode versions gradually and collect data, without turning on strict enforcement immediately.

Please identify:

* what can be added behind a flag;
* what can run in non-enforcing mode;
* what data should be collected;
* what should block strict enforcement;
* which parts are safe to include now;
* which parts should wait.

6. Review vulnerabilities and edge cases

Carefully check the approach for possible vulnerabilities or edge cases before it becomes enforcing validation logic.

Please focus on the actual proposed mechanism and the limitations already documented in the linked materials.

Expected output

Please provide a short report with:

* whether the existing implementation matches the two-stage validation proposal;
* what is already implemented;
* what still needs to be modified or created;
* whether the current state is ready for soft MLNode integration;
* what should remain non-enforcing;
* what data should be collected before strict validation;
* vulnerabilities, edge cases, or mismatches found during review;
* recommended next steps;
* final recommendation:
    * ready for soft MLNode integration
    * ready after minor fixes
    * needs additional review
    * not ready

## Notes

This should be treated as a careful validation / security review task.

The immediate rollout risk is low if the feature is introduced softly and not enforced right away. However, the validation logic itself is security-sensitive, so the implementation should be reviewed with scrupulous care before being incorporated into strict inference validation.

The priority is to take over the existing work, gradually introduce it into MLNode versions, collect data, and avoid hard enforcement until the approach is reviewed and validated.
</div>

---

## 💬 Comments (5)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Ryanchen911">@Ryanchen911</a></span>
    <span class="issues-meta-item">commented 2026-06-26 11:33 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>hi @tcharchian , does this issue need help? If yes, maybe we  can take this one.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-06-30 00:53 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@Ryanchen911, yes please! </p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/neuron7xLab">@neuron7xLab</a></span>
    <span class="issues-meta-item">commented 2026-07-02 13:28 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>I ran an adversarial pass on the deterministic sampling dump against the inference-validation proposal.</p>
<p><strong>Finding:</strong> the deterministic replay seed was not chain-bound — it was derived from request-controlled material (<code>f"{user_seed}|{prompt_token_ids}"</code>), so Stage-1 replay could be detached from the chain inference instance. The proposal requires <code>run_seed = SHA256(user_seed || inference_id_from_chain)</code>.</p>
<p>I opened a focused PR against <code>gonka-ai/vllm:tg/detemrinistic_sampling_dump</code> — gonka-ai/vllm#56 — with a chain-bound seed primitive + tests.</p>
<p>Scope note (updated as review tightened it to match vLLM's actual API):
- <code>user_seed</code> is <strong><code>int</code>-only</strong> (vLLM <code>SamplingParams.seed</code> / OpenAI <code>seed</code> are <code>Optional[int]</code>); <code>bool</code>/non-<code>int</code> fail closed, so a str <code>"7"</code> can't collide with int <code>7</code>.
- the chain id must be a non-empty <code>str</code>, hashed <strong>byte-exact</strong> (no stripping); missing/empty/whitespace-only/non-<code>str</code> fail closed.
- framing is <strong>byte-length-prefixed SHA256 over UTF-8</strong> (portable to Go/Rust/JS), not raw concatenation.</p>
<p>Honest status: reproducible from <code>pull/56/head</code>; 10 invariant tests + a golden vector verified locally (isolated harness — full <code>pytest</code> needs a built vLLM env); CI is <code>action_required</code> (fork approval gate), so not green yet. Complementary to @Ryanchen911's review, not a takeover.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Ryanchen911">@Ryanchen911</a></span>
    <span class="issues-meta-item">commented 2026-07-06 01:30 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@neuron7xLab thanks for the focused pass and PR — this lands squarely on the highest-priority item in our‘s review. We flagged the same seed-domain issue: the _dump/v011 derivation f"{user_seed}|{prompt_token_ids}" is request-controlled on both components, so Stage-1 replay can be ground/detached from the chain inference instance. Binding to inference_id_from_chain per the proposal is exactly right.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Ryanchen911">@Ryanchen911</a></span>
    <span class="issues-meta-item">commented 2026-07-06 02:53 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <h2>Review summary — reproducible sampling for inference validation</h2>
<p>We reviewed the two-stage validation design (proposal §"Proper Fix") against the actual code on all three vllm branches (<code>_dump</code>, <code>v011</code>, <code>_merged</code>) plus the gonka chain-side validator, with an eye on a safe soft-rollout path.</p>
<p><strong>Final recommendation: needs additional review — not ready for soft MLNode integration yet.</strong> The design is sound and matches the two-stage proposal; the implementation is real but split across two branches (each ~half) and not yet end-to-end runnable against real executor artifacts.</p>
<p><strong>Three blockers gate enforcement:</strong>
- <strong>S1 — seed not chain-bound.</strong> Both branches seed from <code>f"{user_seed}|{prompt_token_ids}"</code> (executor-controllable → grindable + tokenizer-fragile). The proposal requires <code>SHA256(user_seed ‖ inference_id_from_chain)</code>. Primitive fix now in flight: <code>gonka-ai/vllm#56</code> (<code>derive_chain_bound_seed</code>) — should converge with #13 and get wired into a call site.
- <strong>E1 — executor (GPU float) vs validator (CPU decimal) weights aren't bit-identical.</strong> Zero-tolerance replay will false-reject real artifacts until the executor path adopts the decimal pipeline (ADR 0003; needs GPU verification).
- <strong>S3 — no Python↔Go parity.</strong> The chain validator is Go; there is no Go implementation of the decimal pipeline/RNG and cross-language bit-parity has never been tested.</p>
<p><strong>Safe now / non-enforcing:</strong> the integer <code>deterministic_utils.py</code> as a torch-free library (after the S2 local-decimal-context fix, ADR 0002); the perplexity quick-fix as telemetry (gonka's <code>get_metric</code> ≈ 1/PPL); everything behind <code>VLLM_DETERMINISTIC_SAMPLING</code>, recording verdicts without slashing while collecting Stage-1 false-positive data (target: zero, by model/quant/hardware).</p>
<p>Full report below (findings S1/E1/S3/A1/A2/S2 + edge cases + rollout data + next steps).</p>
<details>
<summary><b>Full review report (click to expand)</b></summary>
<h1>Issue #1199 — Reproducible Sampling for Inference Validation: Review Report</h1>
<p><strong>Reviewers:</strong> @Ryanchen911, @bonujel · <strong>Date:</strong> 2026-07-03
<strong>Scope:</strong> Security/validation review of the two-stage validation design and the base deterministic-sampling implementation, plus a safe MLNode rollout path.</p>
<p><strong>Sources reviewed</strong>
- Proposal: <code>proposals/inference-validation/inference-validation.md</code> (§"Proper Fix: Two-Stage Validation System")
- Design doc: <code>docs/DETERMINISTIC_SAMPLING_VALIDATION.md</code>
- Actual code across <strong>three</strong> vllm branches (source of truth for status):
  - <code>gonka-ai/vllm @ tg/detemrinistic_sampling_dump</code> — integer (decimal) sampling algorithm, unwired
  - <code>gonka-ai/vllm @ tg/deterministic_sampling_v011</code> — full system skeleton, float sampling
  - <code>bonujel/vllm @ tg/deterministic_sampling_merged</code> — merge of the two + validator replay + ADRs
  - <code>gonka-ai/vllm#56</code> (@neuron7xLab) — chain-bound seed primitive (<code>derive_chain_bound_seed</code>) + tests, addresses S1
- Gonka side: <code>mlnode/packages/benchmarks/src/validation/utils.py</code>, <code>decentralized-api/internal/validation/inference_validation.go</code></p>
<hr />
<h2>TL;DR / Final recommendation</h2>
<p><strong>Needs additional review — not ready for soft MLNode integration yet.</strong></p>
<p>The <em>design</em> is sound and substantially aligned with the two-stage proposal. The
<em>implementation is split across two branches, each doing roughly half</em>:</p>
<ul>
<li><strong><code>v011</code></strong> has the full system skeleton — <code>VLLM_DETERMINISTIC_SAMPLING</code> env flag, worker
  seed wiring (<code>gpu_model_runner.py</code>), a <code>deterministic_sampler.py</code>, and the validator-side
  <code>validation_logic.py</code> (replay + distance). <strong>But its executor sampling path uses GPU
  float32</strong>, which drifts across GPUs/drivers and can flip a token when a probability sits
  on a filter boundary → risk of falsely flagging an honest participant.</li>
<li><strong><code>_dump</code></strong> fixes exactly that: an <strong>integer (decimal) weight pipeline</strong> that is
  bit-stable and won't drift. <strong>But it is only the algorithm — nothing imports it.</strong></li>
</ul>
<p>The <strong><code>_merged</code></strong> branch is the right next move: it ports the integer algorithm
onto the skeleton, adds a pure-CPU validator replay (<code>validation_sampling.py</code>,
<code>verify_sampling_from_logprobs</code>), pins the float→string form, and records the open blockers
as ADRs. It is verified <strong>validator-side only</strong> — the executor still emits float-derived
weights, so replay against <em>real</em> executor artifacts will still false-reject until the
executor path is switched to the decimal pipeline (ADR 0003).</p>
<p>The core integer primitive is adoptable as a library today. The executor hot-path change,
the seed hardening, and cross-language (Python↔Go) parity must land before this becomes
enforcing validation logic.</p>
<hr />
<h2>1. Does the implementation match the two-stage proposal?</h2>
<p><strong>Design: yes, with one naming remap and one mechanism upgrade.</strong></p>
<table>
<thead>
<tr>
<th>Proposal</th>
<th>Doc</th>
<th>Match</th>
</tr>
</thead>
<tbody>
<tr>
<td>Stage 1 — Sequence Check (cheap, RNG replay)</td>
<td>"Check 2" — Sampling Replay</td>
<td>✅ same purpose</td>
</tr>
<tr>
<td>Stage 2 — Distribution Check (expensive)</td>
<td>"Check 1" — Logprob Distance</td>
<td>✅ same purpose</td>
</tr>
<tr>
<td>Order: cheap check first, reject before expensive</td>
<td>Check 2 runs <em>before</em> inference, Check 1 <em>after</em></td>
<td>✅ consistent (cheap-first)</td>
</tr>
</tbody>
</table>
<p>The confusing part is only naming: the proposal's <strong>Stage 1</strong> is the doc's <strong>Check 2</strong>. Execution order is still correct — the cheap CPU replay gates the expensive GPU inference.</p>
<p><strong>Mechanism upgrade (acceptable, arguably better than the proposal):</strong>
- Proposal Stage 1 samples directly over the artifact's top-k list: <code>verify chosen == top_k[sampled_index]</code>.
- Doc/impl runs the <em>full</em> decimal pipeline (temperature → softmax → top_k/top_p/min_p → quantize to int weights) then SHA256 categorical sampling.</p>
<p>The doc's version reproduces the real sampling parameters, so it's a stronger binding. Fine — but it is <em>more</em> code to get bit-exactly right on both sides, which raises the false-positive risk (see §6).</p>
<p><strong>Does Stage 1 actually close the pre-fill hole?</strong> Yes, in principle. A pre-fill attacker generates the sequence with a cheap model and computes real-model logprobs in a single pass. Stage 1 forces the reported token at each position to equal <code>deterministic_sample(real_model_logprobs, RNG)</code>. The cheap model's chosen token generally won't match that, so the artifact is rejected — unless the attacker re-samples each position from the real-model distribution token-by-token, which <em>is</em> real sequential generation. That's exactly the cost we want to impose. This holds <strong>only if the RNG stream can't be ground</strong>, which depends on seed binding (see §2, finding S1).</p>
<hr />
<h2>2. Seed, RNG, and replay logic</h2>
<p><code>Sha256CounterRNG</code> (<code>deterministic_utils.py</code>) is clean and portable: <code>u64 = SHA256(seed_bytes ‖ counter_be)[:8]</code>, counter++ per draw, unbiased rejection sampling in <code>uint64_below</code>, linear-scan categorical sampler. This is trivially reproducible in Go and Python and is the right primitive.</p>
<p><strong>Finding S1 (design mismatch, security-relevant) — seed derivation diverges from the proposal.</strong>
- Proposal: <code>run_seed = SHA256(user_seed ‖ inference_id_from_chain)</code> — bound to the chain-issued, unpredictable inference ID.
- Doc/impl: <code>seed_str = f"{user_seed}|{prompt_token_ids}"</code> — bound to user seed + prompt tokens, <strong>not</strong> the chain inference ID.</p>
<p>Consequences of the doc's choice:
1. <strong>No binding to chain identity</strong> → the same <code>(user_seed, prompt)</code> yields the same RNG stream, enabling precomputation and cross-request artifact replay. The proposal deliberately mixes in <code>inference_id</code> to prevent this.
2. <strong>Requires the validator to re-tokenize the prompt identically.</strong> Any tokenizer version/config drift between executor and validator changes <code>prompt_token_ids</code> → different seed → guaranteed replay mismatch → <strong>false fraud on an honest inference</strong>. This is a latent false-positive source.</p>
<p>This must be reconciled before enforcement. Recommend adopting the proposal's <code>inference_id</code>-bound seed (the chain already stores <code>inference_id</code>), or at minimum mixing it in.</p>
<p><strong>Status — a focused PR now addresses the primitive.</strong> <code>gonka-ai/vllm#56</code> (@neuron7xLab) was
opened against <code>_dump</code>, adding <code>derive_chain_bound_seed(user_seed, inference_id_from_chain)</code>
to <code>deterministic_utils.py</code> + 10 invariant tests + a golden vector, and correcting the doc's
seed derivation everywhere. Reviewed the diff — the design is careful and directly
addresses S1:
- Uses <strong>byte-length-prefixed, domain-separated SHA256 over UTF-8</strong> (not raw concat), which
  also removes the concatenation-ambiguity bug in the naive <code>f"{seed}{id}"</code> form
  (<code>(4,"2x")</code> vs <code>(42,"x")</code>). This is the right framing for Python↔Go parity (S3).
- <strong>Fails closed</strong>: rejects missing/empty/non-<code>str</code>/non-printable-ASCII/over-length chain id,
  and non-exact-<code>int</code> / out-of-int64-range <code>user_seed</code>. The printable-ASCII-only rule is a
  deliberate, well-reasoned choice to keep the accept/reject boundary language-invariant
  (a <code>strip()</code>/whitespace predicate differs per runtime and would split consensus).
- <strong>Scoped honestly</strong>: it lands only the primitive — <strong>no call site constructs the seed yet</strong>.
  <code>gpu_model_runner.py</code> still needs wiring, and MLNode must actually pass the chain
  <code>inference_id</code> into vLLM. So S1 moves from "unaddressed" to "primitive ready, wiring +
  MLNode plumbing still open." CI is fork-gated (not green yet).
- Overlaps PR #13 (same idea on <code>main</code>, bound to <code>request_id</code>); note that vLLM's <code>request_id</code>
  is executor-controllable (<code>"chatcmpl-"+X-Request-Id</code>/<code>uuid4()</code>), so #56's insistence on a
  <em>chain</em>-provided id that fails closed when absent is the safer contract. These should
  converge into one primitive.</p>
<p><strong>Remaining S1 work:</strong> wire <code>derive_chain_bound_seed</code> into the worker, define how MLNode
sources and passes <code>inference_id_from_chain</code>, and confirm the Go validator uses the identical
framing (folds into S3 parity).</p>
<p><strong>Finding S2 — global decimal context mutation.</strong> <code>deterministic_utils.py</code> sets <code>getcontext().prec = 10</code> / <code>ROUND_HALF_EVEN</code> at import time. <code>getcontext()</code> is process-global; in the vLLM serving process this silently reconfigures Decimal for every other consumer, and conversely any other module that touches the context breaks reproducibility. Use <code>decimal.localcontext()</code> around the pipeline instead of mutating the global context.</p>
<hr />
<h2>3. Artifact contents</h2>
<p>The artifact format in the doc (§"Artifact Format") contains what replay needs: per-position <code>token</code> (sampled ID as string), <code>logprobs</code> (post-penalty, token-ID-keyed), and <code>request_params</code> including <code>seed</code>, <code>temperature</code>, <code>top_p</code>, <code>top_logprobs</code>. This matches the proposal's storage requirements (top-k probs + exact token sequence, already on-chain) plus the added <code>run_seed</code>.</p>
<p><strong>Finding A1 (contract mismatch, real divergence risk) — float vs string logprobs.</strong>
- Doc reference impl: <code>logprobs_to_weights(logprobs: dict[str, float])</code> and converts via <code>Decimal(repr(f))</code>.
- Actual <code>deterministic_utils.logprobs_to_weights(logprob_strings: Dict[str, str])</code> takes <strong>strings already</strong> and does <code>Decimal(s)</code> directly — no <code>repr</code>.</p>
<p>The entire reproducibility guarantee rests on both sides producing the <em>identical</em> decimal string from the same float64. The doc says that canonical form is <code>repr(float)</code>; the <code>_dump</code> primitive pushes that responsibility to the caller and never pins it. If executor and validator stringify the float differently (<code>repr</code> vs <code>json.dumps</code> vs <code>%.17g</code>), weights diverge and an honest inference is flagged as fraud. <strong>There must be exactly one shared function that owns float→string, used by both sides, with the canonical form pinned in the spec.</strong></p>
<p><strong>Status (<code>_merged</code>):</strong> partially addressed. On <code>_merged</code>, <code>validation_sampling.verify_sampling_from_logprobs</code> pins the conversion to <code>repr(f)</code> at a single point and records it in ADR 0001. Two gaps remain: (a) this pins it only on the <em>validator</em> side — the executor path must use the identical function (tied to ADR 0003), and (b) the Go chain-side validator must reproduce the same canonical string, which is untested (see S3 below).</p>
<p><strong>Finding A2 — resolved vs user-specified params.</strong> The doc correctly notes (Tricky Moments §2) the artifact must record <em>resolved</em> sampling params (after model defaults), not user-specified. The gonka <code>RequestParams</code>/<code>inference()</code> path currently forwards only user-set extras; this needs verification once wiring exists.</p>
<hr />
<h2>4. Implementation status (code is the source of truth)</h2>
<p><strong>The work is split across two gonka-ai branches, each implementing a different half of the
same feature.</strong> Neither is end-to-end runnable on its own; the <code>_merged</code> branch is
the first that runs validator-side.</p>
<table>
<thead>
<tr>
<th>Item (doc Steps)</th>
<th><code>_dump</code> (integer algo)</th>
<th><code>v011</code> (skeleton)</th>
<th><code>_merged</code> (consolidated)</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>deterministic_utils.py</code> — integer/decimal weight pipeline</td>
<td>✅ present, <strong>unwired</strong></td>
<td>✅ present (float variant used by sampler)</td>
<td>✅ ported onto skeleton</td>
</tr>
<tr>
<td><code>VLLM_DETERMINISTIC_SAMPLING</code> env flag (Step 2)</td>
<td>❌</td>
<td>✅</td>
<td>✅</td>
</tr>
<tr>
<td><code>deterministic_sampler.py</code> / sampler branch (Step 3)</td>
<td>❌</td>
<td>✅ <strong>but GPU float32</strong></td>
<td>✅ (executor still float — ADR 0003)</td>
</tr>
<tr>
<td><code>gpu_model_runner.py</code> seed derivation (Step 4)</td>
<td>❌</td>
<td>✅ <code>f"{seed}\|{prompt_repr}"</code> (no <code>inference_id</code>)</td>
<td>✅ (same, seed not yet hardened)</td>
</tr>
<tr>
<td><code>EnforcedToken.logprobs</code> / data model (Step 6)</td>
<td>❌ (<code>token</code>/<code>top_tokens</code> only)</td>
<td>⚠️ partial in <code>validation.py</code></td>
<td>⚠️ partial</td>
</tr>
<tr>
<td>Validator replay — Check 2 (Step 7)</td>
<td>❌</td>
<td>✅ <code>validation_logic.verify_sampling_sequence</code></td>
<td>✅ <code>validation_sampling.verify_sampling_from_logprobs</code> (pure CPU)</td>
</tr>
<tr>
<td>Validator distance — Check 1 (Step 7)</td>
<td>❌</td>
<td>✅ <code>validation_logic.position_distance/compute_distance</code></td>
<td>✅</td>
</tr>
<tr>
<td><code>serving_chat.py</code> orchestration + response fields (Step 5)</td>
<td>❌</td>
<td>⚠️ partial</td>
<td>⚠️ partial</td>
</tr>
<tr>
<td>Tests (Step 9)</td>
<td>⚠️ <code>test_sampler_interface.py</code> stale/broken</td>
<td>some</td>
<td>✅ <code>test_replay_smoke.py</code> (self-consistent artifacts only)</td>
</tr>
</tbody>
</table>
<p>Across both branches the validator replay + distance logic <strong>does exist</strong> (on <code>v011</code>,
<code>validation_logic.py</code>), and the <code>_merged</code> branch adds a clean pure-CPU replay module with a
passing smoke test. The stale/broken <code>test_sampler_interface.py</code> (imports <code>sampling_weights</code>,
<code>deterministic_rngs</code>, etc. — the superseded weight-reporting design) is a <code>_dump</code>-branch
artifact, superseded by the merge.</p>
<p><strong>The real completeness gap is not "missing files" — it's two incompatible weight paths
(ADR 0003).</strong> The executor produces weights on GPU as <code>(probs * 2^16).round()</code> from
float32 softmax; the validator derives weights from logprob <em>strings</em> via the pure-decimal
pipeline. These are <strong>not bit-identical</strong> (GPU float drift; <code>.round()</code> is not decimal
HALF_EVEN). So the zero-tolerance replay (Check 2) will <strong>false-reject real executor artifacts</strong>
until the executor hot path is switched to the decimal pipeline. This is correctly scoped out
of the merge (needs GPU + production hot-path change) and documented as a blocker, not an
optional optimization — which is the right call.</p>
<p><strong>Net:</strong> substantially more exists than "one primitive module." What's missing for
enforcement is: (1) executor path → decimal weights (ADR 0003), (2) seed hardening (S1),
(3) Python↔Go parity. All three touch the model hot path or the protocol and require GPU to
verify.</p>
<hr />
<h2>5. Safe MLNode rollout</h2>
<p><strong>Safe to adopt now</strong>
- The <code>_dump</code>/<code>_merged</code> integer <code>deterministic_utils.py</code> as a standalone, torch-free library, <em>after</em> fixing S2 (local decimal context — ADR 0002 already proposes this). Add its unit tests (RNG reproducibility, pipeline determinism, categorical sampling) — and, importantly, a <strong>Python↔Go parity test</strong> since the chain side is Go.
- The <code>_merged</code> validator-side replay (<code>validation_sampling.py</code>) as the reference Check-2 implementation, with the explicit understanding (ADR 0003) that it only matches <em>self-consistent</em> artifacts until the executor path is converted.
- The interim <strong>perplexity quick-fix</strong> is a lower-risk parallel track: gonka's <code>get_metric</code> in <code>validation/utils.py</code> already computes the geometric mean of per-token probs (≈ 1/PPL). It can ship as non-enforcing telemetry well before the full two-stage system.</p>
<p><strong>Behind a flag / non-enforcing first</strong>
- Everything else goes behind <code>VLLM_DETERMINISTIC_SAMPLING</code> (default off).
- Executor emits <code>deterministic_sampling_valid</code> + <code>distances</code>; the chain <strong>records but does not slash</strong> on Stage-1 (replay) failures during the data-collection phase.
- The executor-path decimal conversion (ADR 0003) can land behind the same flag and run in shadow (compute decimal weights alongside the float path, log divergences) before it drives anything.</p>
<p><strong>Data to collect before enabling strict enforcement</strong>
- Stage-1 <strong>false-positive rate</strong>: honest inferences that fail replay, broken down by model, quantization, and hardware/arch. Target: <strong>zero</strong> false positives (a slashing system's cost of wrongly flagging an honest participant is far higher than a missed fraud).
- Distance distributions with vs without deterministic mode (does the reordered penalty pipeline shift Check-1 thresholds?).
- Tokenizer determinism across MLNode versions (directly tied to finding S1).
- <strong>Realistic performance:</strong> the doc's ~18µs/position is a single-position microbenchmark. Measure at production batch sizes with top-K CPU transfer and the reordered penalty path in the hot loop.
- Python↔Go bit-parity on shared test vectors.</p>
<p><strong>What should block strict enforcement</strong>
- <strong>E1 — executor path emits decimal-derived weights</strong> (ADR 0003). Until this lands, real artifacts false-reject; this is the single biggest blocker.
- <strong>S1 — seed derivation</strong> reconciled and bound to <code>inference_id</code>.
- <strong>A1/S3 — canonical float string</strong> pinned and shared by <em>one</em> function across executor, Python validator, and the Go chain path; proven by parity vectors.
- Zero observed Stage-1 false positives over a large honest sample.
- Cross-node / cross-arch reproducibility CI green, including Go parity.</p>
<p><strong>Should wait</strong>
- Any executor <code>sampler.py</code> hot-path change beyond shadow mode (perf + correctness risk; GPU verification required).
- Turning Stage-1 replay failures into slashing.</p>
<hr />
<h2>6. Vulnerabilities / edge cases</h2>
<ol>
<li><strong>S1 — seed not bound to <code>inference_id</code></strong> (design): both branches derive <code>f"{seed}|{prompt_repr}"</code>. The seed component is executor-controllable, so an attacker can locally re-roll seeds until one makes a forged result pass replay; it also makes the check tokenizer-fragile → false fraud. <em>Highest priority security bug — blocks enforcement.</em> <strong>Primitive fix in flight: <code>gonka-ai/vllm#56</code> (<code>derive_chain_bound_seed</code>), not yet wired into a call site (see §2).</strong></li>
<li><strong>E1 — executor (GPU float) vs validator (CPU decimal) weight paths are not bit-identical</strong> (impl, ADR 0003): <code>(probs*2^16).round()</code> on float32 ≠ decimal HALF_EVEN pipeline. Zero-tolerance replay false-rejects real artifacts. <em>Biggest completeness blocker.</em></li>
<li><strong>S3 — no Python↔Go parity implementation</strong> (impl): the chain validator is Go; there is no Go implementation of the decimal pipeline / RNG, and cross-language bit-parity has never been tested. Divergence here = false fraud at scale. <em>Blocks enforcement.</em></li>
<li><strong>A1 — float→string canonicalization</strong> (design/impl): pinned to <code>repr(f)</code> on the validator in <code>_merged</code> (ADR 0001), but not yet shared with the executor or the Go side. Tied to E1/S3.</li>
<li><strong>S2 — global decimal context mutation</strong> (impl): <code>_dump</code> mutates <code>getcontext()</code> at import; use <code>localcontext()</code> (ADR 0002 proposes this).</li>
<li><strong>Candidate-token ordering mismatch</strong> (impl): one side sorts by token-ID string, another by numeric ID. Even with bit-identical weights, an order mismatch shifts the categorical index → false fraud. Must be pinned to one order on all three sides.</li>
<li><strong>Temperature = 0 (greedy)</strong> bypasses the decimal pipeline and the replay check entirely; Stage 1 contributes <em>nothing</em> at temp 0 — only the distance check defends. Acceptable (argmax is deterministic and pre-fill still needs matching argmax), but it means a class of inferences has no sequence binding. Document explicitly or disallow temp-0 in validation.</li>
<li><strong>Top-K clamping</strong> (<code>top_k</code> effectively <code>min(top_k, max_num_logprobs)</code>): if <code>top_logprobs</code> is unset the server must apply a fixed default, and the artifact must record it, or executor/validator reconstruct different distributions. <code>min_p</code> empty-set fallback (pick max) and residual tie-break (<code>(weight, token_id)</code> lexicographic) must be identical on all sides — no cross-language test yet.</li>
<li><strong><code>sample_categorical_weights</code> total ≤ 0 → returns last index</strong> silently. Consistent across sides, but in zero-tolerance validation a silent fallback can mask an upstream bug; prefer to raise or log.</li>
<li><strong>Distance check unchanged</strong> as the sole defense against wrong-model/quantization; Stage 1 adds nothing there. Enforcement still hinges on distance-threshold calibration, which this work does not address.</li>
</ol>
<hr />
<h2>7. Recommended next steps</h2>
<ol>
<li><strong>Land the executor decimal-weight path</strong> (E1 / ADR 0003) behind the flag, first in shadow mode (log float-vs-decimal divergence), then as the artifact source. Requires GPU verification.</li>
<li><strong>Reconcile seed derivation</strong> with the proposal — bind <code>run_seed</code> to chain <code>inference_id</code> (S1). Primitive already proposed in <code>gonka-ai/vllm#56</code>; converge it with PR #13, then <strong>wire it into <code>gpu_model_runner.py</code></strong> and define how MLNode passes <code>inference_id_from_chain</code> into vLLM.</li>
<li><strong>Pin one candidate-token order and one float→string form</strong> shared by executor, Python validator, and the Go chain path (A1/S3, ordering).</li>
<li><strong>Write the Go implementation + a Python↔Go parity vector test</strong> (fixed inputs → expected weights + expected token), run in both CIs (S3). This is the gate that "cross-language reproducibility" has never actually been tested.</li>
<li><strong>Fix S2</strong> (local decimal context, ADR 0002) and land the integer <code>deterministic_utils.py</code> + real unit tests.</li>
<li><strong>Retire the stale <code>test_sampler_interface.py</code></strong> (superseded by the merge).</li>
<li><strong>Continue consolidating on the <code>_merged</code> branch</strong>; complete serving-layer orchestration + response fields (<code>deterministic_sampling_valid</code>, <code>distances</code>) non-enforcing.</li>
<li><strong>Ship the perplexity quick-fix as telemetry</strong> in parallel (low risk, uses existing <code>get_metric</code>).</li>
<li><strong>Run the non-enforcing data-collection phase</strong>; gate strict enforcement on the exit criteria in §5.</li>
</ol>
<hr />
<h2>8. Requested summary answers</h2>
<ul>
<li><strong>Matches the two-stage proposal?</strong> Design yes (naming remap + a stronger replay mechanism); one seed-derivation divergence (S1) to reconcile.</li>
<li><strong>Already implemented?</strong> <code>v011</code> has the full skeleton + validator replay/distance (float sampling); <code>_dump</code> has the bit-stable integer algorithm (unwired); <code>_merged</code> unifies them and adds a pure-CPU validator replay with a passing smoke test. Not end-to-end runnable against real executor artifacts yet.</li>
<li><strong>Still to modify/create?</strong> Executor decimal-weight path (E1/ADR 0003), seed hardening (S1), Go parity implementation + tests (S3), shared token-ordering/float-string contract, serving orchestration + response fields.</li>
<li><strong>Ready for soft MLNode integration?</strong> Not yet — but the <code>_merged</code> branch is the correct consolidation and is validator-side runnable.</li>
<li><strong>Keep non-enforcing:</strong> all Stage-1 replay verdicts until E1/S1/S3 are closed and false-positive data is in.</li>
<li><strong>Data before strict validation:</strong> Stage-1 false-positive rate by model/quant/hardware, tokenizer determinism, realistic perf, Python↔Go parity.</li>
<li><strong>Vulnerabilities/mismatches:</strong> S1 (seed↔inference_id — primitive fix in flight, <code>vllm#56</code>), E1 (executor float vs validator decimal weights), S3 (no Go parity), A1 (float string), token-ordering, S2 (global decimal ctx), temp-0 gap, top-K/default handling.</li>
<li><strong>Final recommendation:</strong> <strong>Needs additional review.</strong> The integer primitive is adoptable as a library now; the <code>_merged</code> branch is the right base to continue on; but the executor hot-path conversion (E1), seed hardening (S1), and cross-language parity (S3) must land — all requiring GPU/protocol changes — before any enforcement.</li>
</ul>
</details>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1199](https://github.com/gonka-ai/gonka/issues/1199) every hour.
