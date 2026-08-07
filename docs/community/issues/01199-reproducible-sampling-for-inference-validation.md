---
title: "#1199 — Reproducible sampling for inference validation"
source: https://github.com/gonka-ai/gonka/issues/1199
issue_number: 1199
synced_at: 2026-08-07T22:58:27Z
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
    <span class="issues-meta-item">Updated 2026-07-15 08:54 UTC</span>
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

# Issue #1199 — Reproducible Sampling for Inference Validation: Review Report

**Reviewers:** @Ryanchen911, @bonujel · **Date:** 2026-07-03
**Scope:** Security/validation review of the two-stage validation design and the base deterministic-sampling implementation, plus a safe MLNode rollout path.

**Sources reviewed**
- Proposal: `proposals/inference-validation/inference-validation.md` (§"Proper Fix: Two-Stage Validation System")
- Design doc: `docs/DETERMINISTIC_SAMPLING_VALIDATION.md`
- Actual code across **three** vllm branches (source of truth for status):
  - `gonka-ai/vllm @ tg/detemrinistic_sampling_dump` — integer (decimal) sampling algorithm, unwired
  - `gonka-ai/vllm @ tg/deterministic_sampling_v011` — full system skeleton, float sampling
  - `bonujel/vllm @ tg/deterministic_sampling_merged` — merge of the two + validator replay + ADRs
  - `gonka-ai/vllm#56` (@neuron7xLab) — chain-bound seed primitive (`derive_chain_bound_seed`) + tests, addresses S1
- Gonka side: `mlnode/packages/benchmarks/src/validation/utils.py`, `decentralized-api/internal/validation/inference_validation.go`

---

## TL;DR / Final recommendation

**Needs additional review — not ready for soft MLNode integration yet.**

The *design* is sound and substantially aligned with the two-stage proposal. The
*implementation is split across two branches, each doing roughly half*:

- **`v011`** has the full system skeleton — `VLLM_DETERMINISTIC_SAMPLING` env flag, worker
  seed wiring (`gpu_model_runner.py`), a `deterministic_sampler.py`, and the validator-side
  `validation_logic.py` (replay + distance). **But its executor sampling path uses GPU
  float32**, which drifts across GPUs/drivers and can flip a token when a probability sits
  on a filter boundary → risk of falsely flagging an honest participant.
- **`_dump`** fixes exactly that: an **integer (decimal) weight pipeline** that is
  bit-stable and won't drift. **But it is only the algorithm — nothing imports it.**

The **`_merged`** branch is the right next move: it ports the integer algorithm
onto the skeleton, adds a pure-CPU validator replay (`validation_sampling.py`,
`verify_sampling_from_logprobs`), pins the float→string form, and records the open blockers
as ADRs. It is verified **validator-side only** — the executor still emits float-derived
weights, so replay against *real* executor artifacts will still false-reject until the
executor path is switched to the decimal pipeline (ADR 0003).

The core integer primitive is adoptable as a library today. The executor hot-path change,
the seed hardening, and cross-language (Python↔Go) parity must land before this becomes
enforcing validation logic.

---

## 1. Does the implementation match the two-stage proposal?

**Design: yes, with one naming remap and one mechanism upgrade.**

| Proposal | Doc | Match |
|---|---|---|
| Stage 1 — Sequence Check (cheap, RNG replay) | "Check 2" — Sampling Replay | ✅ same purpose |
| Stage 2 — Distribution Check (expensive) | "Check 1" — Logprob Distance | ✅ same purpose |
| Order: cheap check first, reject before expensive | Check 2 runs *before* inference, Check 1 *after* | ✅ consistent (cheap-first) |

The confusing part is only naming: the proposal's **Stage 1** is the doc's **Check 2**. Execution order is still correct — the cheap CPU replay gates the expensive GPU inference.

**Mechanism upgrade (acceptable, arguably better than the proposal):**
- Proposal Stage 1 samples directly over the artifact's top-k list: `verify chosen == top_k[sampled_index]`.
- Doc/impl runs the *full* decimal pipeline (temperature → softmax → top_k/top_p/min_p → quantize to int weights) then SHA256 categorical sampling.

The doc's version reproduces the real sampling parameters, so it's a stronger binding. Fine — but it is *more* code to get bit-exactly right on both sides, which raises the false-positive risk (see §6).

**Does Stage 1 actually close the pre-fill hole?** Yes, in principle. A pre-fill attacker generates the sequence with a cheap model and computes real-model logprobs in a single pass. Stage 1 forces the reported token at each position to equal `deterministic_sample(real_model_logprobs, RNG)`. The cheap model's chosen token generally won't match that, so the artifact is rejected — unless the attacker re-samples each position from the real-model distribution token-by-token, which *is* real sequential generation. That's exactly the cost we want to impose. This holds **only if the RNG stream can't be ground**, which depends on seed binding (see §2, finding S1).

---

## 2. Seed, RNG, and replay logic

`Sha256CounterRNG` (`deterministic_utils.py`) is clean and portable: `u64 = SHA256(seed_bytes ‖ counter_be)[:8]`, counter++ per draw, unbiased rejection sampling in `uint64_below`, linear-scan categorical sampler. This is trivially reproducible in Go and Python and is the right primitive.

**Finding S1 (design mismatch, security-relevant) — seed derivation diverges from the proposal.**
- Proposal: `run_seed = SHA256(user_seed ‖ inference_id_from_chain)` — bound to the chain-issued, unpredictable inference ID.
- Doc/impl: `seed_str = f"{user_seed}|{prompt_token_ids}"` — bound to user seed + prompt tokens, **not** the chain inference ID.

Consequences of the doc's choice:
1. **No binding to chain identity** → the same `(user_seed, prompt)` yields the same RNG stream, enabling precomputation and cross-request artifact replay. The proposal deliberately mixes in `inference_id` to prevent this.
2. **Requires the validator to re-tokenize the prompt identically.** Any tokenizer version/config drift between executor and validator changes `prompt_token_ids` → different seed → guaranteed replay mismatch → **false fraud on an honest inference**. This is a latent false-positive source.

This must be reconciled before enforcement. Recommend adopting the proposal's `inference_id`-bound seed (the chain already stores `inference_id`), or at minimum mixing it in.

**Status — a focused PR now addresses the primitive.** `gonka-ai/vllm#56` (@neuron7xLab) was
opened against `_dump`, adding `derive_chain_bound_seed(user_seed, inference_id_from_chain)`
to `deterministic_utils.py` + 10 invariant tests + a golden vector, and correcting the doc's
seed derivation everywhere. Reviewed the diff — the design is careful and directly
addresses S1:
- Uses **byte-length-prefixed, domain-separated SHA256 over UTF-8** (not raw concat), which
  also removes the concatenation-ambiguity bug in the naive `f"{seed}{id}"` form
  (`(4,"2x")` vs `(42,"x")`). This is the right framing for Python↔Go parity (S3).
- **Fails closed**: rejects missing/empty/non-`str`/non-printable-ASCII/over-length chain id,
  and non-exact-`int` / out-of-int64-range `user_seed`. The printable-ASCII-only rule is a
  deliberate, well-reasoned choice to keep the accept/reject boundary language-invariant
  (a `strip()`/whitespace predicate differs per runtime and would split consensus).
- **Scoped honestly**: it lands only the primitive — **no call site constructs the seed yet**.
  `gpu_model_runner.py` still needs wiring, and MLNode must actually pass the chain
  `inference_id` into vLLM. So S1 moves from "unaddressed" to "primitive ready, wiring +
  MLNode plumbing still open." CI is fork-gated (not green yet).
- Overlaps PR #13 (same idea on `main`, bound to `request_id`); note that vLLM's `request_id`
  is executor-controllable (`"chatcmpl-"+X-Request-Id`/`uuid4()`), so #56's insistence on a
  *chain*-provided id that fails closed when absent is the safer contract. These should
  converge into one primitive.

**Remaining S1 work:** wire `derive_chain_bound_seed` into the worker, define how MLNode
sources and passes `inference_id_from_chain`, and confirm the Go validator uses the identical
framing (folds into S3 parity).

**Finding S2 — global decimal context mutation.** `deterministic_utils.py` sets `getcontext().prec = 10` / `ROUND_HALF_EVEN` at import time. `getcontext()` is process-global; in the vLLM serving process this silently reconfigures Decimal for every other consumer, and conversely any other module that touches the context breaks reproducibility. Use `decimal.localcontext()` around the pipeline instead of mutating the global context.

---

## 3. Artifact contents

The artifact format in the doc (§"Artifact Format") contains what replay needs: per-position `token` (sampled ID as string), `logprobs` (post-penalty, token-ID-keyed), and `request_params` including `seed`, `temperature`, `top_p`, `top_logprobs`. This matches the proposal's storage requirements (top-k probs + exact token sequence, already on-chain) plus the added `run_seed`.

**Finding A1 (contract mismatch, real divergence risk) — float vs string logprobs.**
- Doc reference impl: `logprobs_to_weights(logprobs: dict[str, float])` and converts via `Decimal(repr(f))`.
- Actual `deterministic_utils.logprobs_to_weights(logprob_strings: Dict[str, str])` takes **strings already** and does `Decimal(s)` directly — no `repr`.

The entire reproducibility guarantee rests on both sides producing the *identical* decimal string from the same float64. The doc says that canonical form is `repr(float)`; the `_dump` primitive pushes that responsibility to the caller and never pins it. If executor and validator stringify the float differently (`repr` vs `json.dumps` vs `%.17g`), weights diverge and an honest inference is flagged as fraud. **There must be exactly one shared function that owns float→string, used by both sides, with the canonical form pinned in the spec.**

**Status (`_merged`):** partially addressed. On `_merged`, `validation_sampling.verify_sampling_from_logprobs` pins the conversion to `repr(f)` at a single point and records it in ADR 0001. Two gaps remain: (a) this pins it only on the *validator* side — the executor path must use the identical function (tied to ADR 0003), and (b) the Go chain-side validator must reproduce the same canonical string, which is untested (see S3 below).

**Finding A2 — resolved vs user-specified params.** The doc correctly notes (Tricky Moments §2) the artifact must record *resolved* sampling params (after model defaults), not user-specified. The gonka `RequestParams`/`inference()` path currently forwards only user-set extras; this needs verification once wiring exists.

---

## 4. Implementation status (code is the source of truth)

**The work is split across two gonka-ai branches, each implementing a different half of the
same feature.** Neither is end-to-end runnable on its own; the `_merged` branch is
the first that runs validator-side.

| Item (doc Steps) | `_dump` (integer algo) | `v011` (skeleton) | `_merged` (consolidated) |
|---|---|---|---|
| `deterministic_utils.py` — integer/decimal weight pipeline | ✅ present, **unwired** | ✅ present (float variant used by sampler) | ✅ ported onto skeleton |
| `VLLM_DETERMINISTIC_SAMPLING` env flag (Step 2) | ❌ | ✅ | ✅ |
| `deterministic_sampler.py` / sampler branch (Step 3) | ❌ | ✅ **but GPU float32** | ✅ (executor still float — ADR 0003) |
| `gpu_model_runner.py` seed derivation (Step 4) | ❌ | ✅ `f"{seed}\|{prompt_repr}"` (no `inference_id`) | ✅ (same, seed not yet hardened) |
| `EnforcedToken.logprobs` / data model (Step 6) | ❌ (`token`/`top_tokens` only) | ⚠️ partial in `validation.py` | ⚠️ partial |
| Validator replay — Check 2 (Step 7) | ❌ | ✅ `validation_logic.verify_sampling_sequence` | ✅ `validation_sampling.verify_sampling_from_logprobs` (pure CPU) |
| Validator distance — Check 1 (Step 7) | ❌ | ✅ `validation_logic.position_distance/compute_distance` | ✅ |
| `serving_chat.py` orchestration + response fields (Step 5) | ❌ | ⚠️ partial | ⚠️ partial |
| Tests (Step 9) | ⚠️ `test_sampler_interface.py` stale/broken | some | ✅ `test_replay_smoke.py` (self-consistent artifacts only) |

Across both branches the validator replay + distance logic **does exist** (on `v011`,
`validation_logic.py`), and the `_merged` branch adds a clean pure-CPU replay module with a
passing smoke test. The stale/broken `test_sampler_interface.py` (imports `sampling_weights`,
`deterministic_rngs`, etc. — the superseded weight-reporting design) is a `_dump`-branch
artifact, superseded by the merge.

**The real completeness gap is not "missing files" — it's two incompatible weight paths
(ADR 0003).** The executor produces weights on GPU as `(probs * 2^16).round()` from
float32 softmax; the validator derives weights from logprob *strings* via the pure-decimal
pipeline. These are **not bit-identical** (GPU float drift; `.round()` is not decimal
HALF_EVEN). So the zero-tolerance replay (Check 2) will **false-reject real executor artifacts**
until the executor hot path is switched to the decimal pipeline. This is correctly scoped out
of the merge (needs GPU + production hot-path change) and documented as a blocker, not an
optional optimization — which is the right call.

**Net:** substantially more exists than "one primitive module." What's missing for
enforcement is: (1) executor path → decimal weights (ADR 0003), (2) seed hardening (S1),
(3) Python↔Go parity. All three touch the model hot path or the protocol and require GPU to
verify.

---

## 5. Safe MLNode rollout

**Safe to adopt now**
- The `_dump`/`_merged` integer `deterministic_utils.py` as a standalone, torch-free library, *after* fixing S2 (local decimal context — ADR 0002 already proposes this). Add its unit tests (RNG reproducibility, pipeline determinism, categorical sampling) — and, importantly, a **Python↔Go parity test** since the chain side is Go.
- The `_merged` validator-side replay (`validation_sampling.py`) as the reference Check-2 implementation, with the explicit understanding (ADR 0003) that it only matches *self-consistent* artifacts until the executor path is converted.
- The interim **perplexity quick-fix** is a lower-risk parallel track: gonka's `get_metric` in `validation/utils.py` already computes the geometric mean of per-token probs (≈ 1/PPL). It can ship as non-enforcing telemetry well before the full two-stage system.

**Behind a flag / non-enforcing first**
- Everything else goes behind `VLLM_DETERMINISTIC_SAMPLING` (default off).
- Executor emits `deterministic_sampling_valid` + `distances`; the chain **records but does not slash** on Stage-1 (replay) failures during the data-collection phase.
- The executor-path decimal conversion (ADR 0003) can land behind the same flag and run in shadow (compute decimal weights alongside the float path, log divergences) before it drives anything.

**Data to collect before enabling strict enforcement**
- Stage-1 **false-positive rate**: honest inferences that fail replay, broken down by model, quantization, and hardware/arch. Target: **zero** false positives (a slashing system's cost of wrongly flagging an honest participant is far higher than a missed fraud).
- Distance distributions with vs without deterministic mode (does the reordered penalty pipeline shift Check-1 thresholds?).
- Tokenizer determinism across MLNode versions (directly tied to finding S1).
- **Realistic performance:** the doc's ~18µs/position is a single-position microbenchmark. Measure at production batch sizes with top-K CPU transfer and the reordered penalty path in the hot loop.
- Python↔Go bit-parity on shared test vectors.

**What should block strict enforcement**
- **E1 — executor path emits decimal-derived weights** (ADR 0003). Until this lands, real artifacts false-reject; this is the single biggest blocker.
- **S1 — seed derivation** reconciled and bound to `inference_id`.
- **A1/S3 — canonical float string** pinned and shared by *one* function across executor, Python validator, and the Go chain path; proven by parity vectors.
- Zero observed Stage-1 false positives over a large honest sample.
- Cross-node / cross-arch reproducibility CI green, including Go parity.

**Should wait**
- Any executor `sampler.py` hot-path change beyond shadow mode (perf + correctness risk; GPU verification required).
- Turning Stage-1 replay failures into slashing.

---

## 6. Vulnerabilities / edge cases

1. **S1 — seed not bound to `inference_id`** (design): both branches derive `f"{seed}|{prompt_repr}"`. The seed component is executor-controllable, so an attacker can locally re-roll seeds until one makes a forged result pass replay; it also makes the check tokenizer-fragile → false fraud. *Highest priority security bug — blocks enforcement.* **Primitive fix in flight: `gonka-ai/vllm#56` (`derive_chain_bound_seed`), not yet wired into a call site (see §2).**
2. **E1 — executor (GPU float) vs validator (CPU decimal) weight paths are not bit-identical** (impl, ADR 0003): `(probs*2^16).round()` on float32 ≠ decimal HALF_EVEN pipeline. Zero-tolerance replay false-rejects real artifacts. *Biggest completeness blocker.*
3. **S3 — no Python↔Go parity implementation** (impl): the chain validator is Go; there is no Go implementation of the decimal pipeline / RNG, and cross-language bit-parity has never been tested. Divergence here = false fraud at scale. *Blocks enforcement.*
4. **A1 — float→string canonicalization** (design/impl): pinned to `repr(f)` on the validator in `_merged` (ADR 0001), but not yet shared with the executor or the Go side. Tied to E1/S3.
5. **S2 — global decimal context mutation** (impl): `_dump` mutates `getcontext()` at import; use `localcontext()` (ADR 0002 proposes this).
6. **Candidate-token ordering mismatch** (impl): one side sorts by token-ID string, another by numeric ID. Even with bit-identical weights, an order mismatch shifts the categorical index → false fraud. Must be pinned to one order on all three sides.
7. **Temperature = 0 (greedy)** bypasses the decimal pipeline and the replay check entirely; Stage 1 contributes *nothing* at temp 0 — only the distance check defends. Acceptable (argmax is deterministic and pre-fill still needs matching argmax), but it means a class of inferences has no sequence binding. Document explicitly or disallow temp-0 in validation.
8. **Top-K clamping** (`top_k` effectively `min(top_k, max_num_logprobs)`): if `top_logprobs` is unset the server must apply a fixed default, and the artifact must record it, or executor/validator reconstruct different distributions. `min_p` empty-set fallback (pick max) and residual tie-break (`(weight, token_id)` lexicographic) must be identical on all sides — no cross-language test yet.
9. **`sample_categorical_weights` total ≤ 0 → returns last index** silently. Consistent across sides, but in zero-tolerance validation a silent fallback can mask an upstream bug; prefer to raise or log.
10. **Distance check unchanged** as the sole defense against wrong-model/quantization; Stage 1 adds nothing there. Enforcement still hinges on distance-threshold calibration, which this work does not address.

---

## 7. Recommended next steps

1. **Land the executor decimal-weight path** (E1 / ADR 0003) behind the flag, first in shadow mode (log float-vs-decimal divergence), then as the artifact source. Requires GPU verification.
2. **Reconcile seed derivation** with the proposal — bind `run_seed` to chain `inference_id` (S1). Primitive already proposed in `gonka-ai/vllm#56`; converge it with PR #13, then **wire it into `gpu_model_runner.py`** and define how MLNode passes `inference_id_from_chain` into vLLM.
3. **Pin one candidate-token order and one float→string form** shared by executor, Python validator, and the Go chain path (A1/S3, ordering).
4. **Write the Go implementation + a Python↔Go parity vector test** (fixed inputs → expected weights + expected token), run in both CIs (S3). This is the gate that "cross-language reproducibility" has never actually been tested.
5. **Fix S2** (local decimal context, ADR 0002) and land the integer `deterministic_utils.py` + real unit tests.
6. **Retire the stale `test_sampler_interface.py`** (superseded by the merge).
7. **Continue consolidating on the `_merged` branch**; complete serving-layer orchestration + response fields (`deterministic_sampling_valid`, `distances`) non-enforcing.
8. **Ship the perplexity quick-fix as telemetry** in parallel (low risk, uses existing `get_metric`).
9. **Run the non-enforcing data-collection phase**; gate strict enforcement on the exit criteria in §5.

---

## 8. Requested summary answers

- **Matches the two-stage proposal?** Design yes (naming remap + a stronger replay mechanism); one seed-derivation divergence (S1) to reconcile.
- **Already implemented?** `v011` has the full skeleton + validator replay/distance (float sampling); `_dump` has the bit-stable integer algorithm (unwired); `_merged` unifies them and adds a pure-CPU validator replay with a passing smoke test. Not end-to-end runnable against real executor artifacts yet.
- **Still to modify/create?** Executor decimal-weight path (E1/ADR 0003), seed hardening (S1), Go parity implementation + tests (S3), shared token-ordering/float-string contract, serving orchestration + response fields.
- **Ready for soft MLNode integration?** Not yet — but the `_merged` branch is the correct consolidation and is validator-side runnable.
- **Keep non-enforcing:** all Stage-1 replay verdicts until E1/S1/S3 are closed and false-positive data is in.
- **Data before strict validation:** Stage-1 false-positive rate by model/quant/hardware, tokenizer determinism, realistic perf, Python↔Go parity.
- **Vulnerabilities/mismatches:** S1 (seed↔inference_id — primitive fix in flight, `vllm#56`), E1 (executor float vs validator decimal weights), S3 (no Go parity), A1 (float string), token-ordering, S2 (global decimal ctx), temp-0 gap, top-K/default handling.
- **Final recommendation:** **Needs additional review.** The integer primitive is adoptable as a library now; the `_merged` branch is the right base to continue on; but the executor hot-path conversion (E1), seed hardening (S1), and cross-language parity (S3) must land — all requiring GPU/protocol changes — before any enforcement.

</details>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/bonujel">@bonujel</a></span>
    <span class="issues-meta-item">commented 2026-07-14 01:16 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <h2>Follow-up — GPU evidence for the blockers, and the decisions that remain</h2>
<p>We took the review above as the frame and added the <strong>empirical layer</strong>: experiments on real model output that quantify <strong>E1</strong>, close <strong>S3</strong>, and fill part of the §5 data list — plus two findings the review did not anticipate, one of which changes the signed-artifact design.</p>
<p>These are review-level experiments (HuggingFace proxy, 64–128 positions per config, a single GPU architecture). They settle direction and prerequisites; they do not authorize enforcement. This follow-up adds the empirical layer to our #1199 review — the design analysis there stands unchanged.</p>
<p><strong>What the experiments add:</strong></p>
<ul>
<li><strong>Recompute is not reproducible — the logprobs must be signed</strong> <em>(new, design-level)</em>. Batch composition alone flips <strong>0–8%</strong> of honest positions, <strong>even after E1 is fixed</strong>. Stage-1 must replay the <strong>signed</strong> logprobs and can never reconstruct them by re-running the model. This constrains the contract, not just the implementation.</li>
<li><strong>S3 — validated.</strong> A Go validator (<code>detsample</code>: RNG, decimal pipeline, chain-bound seed, three-valued verdict) is now <strong>bit-identical to Python</strong> on shared conformance vectors — the "never actually been tested" item. Still needs to land in CI.</li>
<li><strong>E1 — quantified.</strong> The float executor false-rejects <strong>14–77%</strong> of honest positions; the decimal pipeline gives <strong>0/128 on every config × 2 models</strong>. <strong>E1 is a hard prerequisite for enforcement</strong> — enforcing before it lands would slash honest participants en masse.</li>
<li><strong>E1 confirmed live in vLLM</strong> — and it's entangled with token order. With the shadow flag on, the float executor diverges from the decimal validator on ~70% of positions in a real vLLM run (gpt2). That's higher than the offline 14–77% because the live float path also samples in numeric token-id order while the validator uses string order (§6.6). So the executor fix is E1 and the §6.6 ordering, together — adopting decimal weights alone won't make replay pass. This also closes the "requires GPU verification" caveat on §7 step 1.</li>
<li><strong>Stage-2's metric and threshold — measurable, and partly a policy call</strong> <em>(new)</em>. The distance check separates honest from a wrong model by <strong>~40–65×</strong>, but <strong>only as MAE/KL over the top-K support</strong>; the sampled-token delta overlaps and cannot gate. The distances also form a <strong>monotone ladder</strong> — quantizing the <em>same</em> model lands between honest noise and a genuinely different model:
  ```
  d_mae vs the fp16 reference   (Qwen2.5-1.5B, p50 — gpt2-large agrees)
  honest (fp16, batch noise): 0.006
  int8   (same model): 0.097 
  int4   (same model): 0.364<br />
  3×-smaller model: 0.817  </li>
</ul>
<p>threshold ~0.05  →  only fp16 passes
            ~0.25  →  int8 passes too
            ~0.75  →  int4 passes too
  ```</p>
<p><strong>int4 sits far enough out to be caught; int8 lands an order of magnitude above the honest floor but well below a genuinely different model</strong> — i.e. right where a natural threshold would fall. </p>
<p>So the threshold does not merely separate honest from fraud: it <strong>implicitly decides which quantizations still count as "the model."</strong> That placement is a policy decision, not a measurement.</p>
<p><strong>Open decisions.</strong> Consolidated from the review and from building the Go validator against the contract. These are <strong>questions, not settled answers</strong> — and they are decisions, a different kind of object from the review's finding codes.</p>
<ul>
<li><strong>A — the signed-artifact contract (keystone).</strong> Both sides must reconstruct a <strong>bit-identical</strong> distribution from the same signed data: which fields bind into <code>responseHash</code>; <strong>which tokens' logprobs are signed</strong> (the filter's kept set, not a fixed K); <strong>the logprobs themselves must be in it</strong>; float→string canonicalization, candidate ordering, filter-edge rules + resolved params; a version descriptor. 〔A1 / A2 / §6.6 / §6.8〕</li>
<li><strong>B — sampling/RNG semantics and the coverage boundary.</strong> One RNG stream across a sequence, or one seed per position? And which requests Stage-1 structurally cannot cover → <strong><em>Inconclusive</em></strong>, deferred to the distance check: <strong>temperature 0</strong>, and <strong>unbounded support</strong> (high-temp <code>top_p</code>, unfiltered). 〔§6.7〕</li>
<li><strong>C — seed binding and hardening.</strong> Chain-binding via <code>inference_id</code> (gonka-ai/vllm#56) still leaves <code>user_seed</code> request-controlled — bind inputs the executor cannot choose, or commit <code>user_seed</code> on-chain? How does <code>inference_id</code> reach vLLM? Invariant: the validator <strong>derives</strong> the seed and never trusts the payload's. 〔S1〕</li>
<li><strong>D — enforcement gating.</strong> Target false-reject rate, over how many epochs, which cross-arch/cross-node CI must be green — plus the <strong>Stage-2 metric and threshold</strong>, whose placement implicitly picks the accepted precision floor. Partly a <strong>policy</strong> decision. 〔gated by <strong>E1</strong>〕</li>
<li><strong>Integration — an action, not a decision:</strong> land Sampling-Replay as an <strong>additive shadow path</strong>, converge the two Python validators, put the Go implementation and parity vectors in CI. 〔S3〕</li>
</ul>
<p><strong>Only A and D block progress.</strong> A is the foundation — nothing downstream can be wired correctly until it is fixed. D cannot open until E1 lands.</p>
<p>Full experiment report below (setup + coverage against §5 + 7 experiments + mechanisms + next steps).</p>
<details>
<summary><b>Full experiment report (click to expand)</b></summary>

# GPU experiments — reproducible sampling (#1199)

**Setup:** 8×RTX-4090, fp16 (+ int8/int4 via `bitsandbytes`), `gpt2` / `gpt2-large` and `Qwen2.5-0.5B` / `Qwen2.5-1.5B`, 64–128 positions per config. **HuggingFace proxy — not vLLM's own kernels, except Experiment 8, which runs inside a real vLLM engine."** Scripts and raw logs: branch `bonujel/vllm@tg/deterministic_sampling_merged`, `dev_notes/reproduce_sampling/e1_experiment/`. Decision register: [gist](https://gist.github.com/bonujel/5bc8c21f7ca376de305b62b6f11a2e27).

---

## 1. Coverage against §5 "Data to collect before enabling strict enforcement"

| §5 item | Status |
|---|---|
| Stage-1 false-positive rate — **by model** | ✅ two models (Exp 1) |
| …**by quantization** | ⚠️ Stage-1 is precision-agnostic — it replays *signed* logprobs. Measured for **Stage-2** instead (Exp 5) |
| …**by hardware / arch** | ⚠️ same-arch **bit-identical** across 8 cards + repeat runs (Exp 6). **Cross-architecture not covered** |
| Distance distributions, det-mode on vs off | ⚠️ partial — recompute-noise floor (Exp 3) and honest-vs-fraud separation (Exp 4). The **penalty-reorder** comparison is not done |
| Tokenizer determinism across MLNode versions | ❌ not done |
| Realistic performance at production batch sizes | ❌ not done |
| Python↔Go bit-parity on shared vectors | ✅ done (**S3**) |

---

## 2. Experiments

| # | Question | Result | Bears on |
|---|---|---|---|
| **1** | Does the float executor path false-reject honest positions? | **14–77%**; **0%** with the decimal pipeline | **E1** → **D** |
| **2** | How large must the signed support set be? | a fixed top-256 distorts **7–33%** when the nucleus is unbounded → sign **the filter's kept set**, not a fixed K | A1/A2, §6.8 → **A** |
| **3** | Can the validator recompute logprobs instead of replaying signed ones? | **No** — batching alone flips **0–8%** of honest positions | → **A** |
| **4** | Does the Stage-2 distance check separate honest from fraud, and with which metric? | **~40–65×** with MAE/KL over top-K; the **sampled-token delta overlaps** and cannot gate | → **D** |
| **5** | Does a quantized *same* model look like fraud? | precision ladder: honest ≪ int8 < int4 < cheaper model. **int4 caught, int8 a gray zone** | → **D** |
| **6** | Is the drift from hardware or from batching? | 8 cards + repeat runs are **bit-identical** → drift is **entirely batch-shape**. Cross-arch untested | → **D** |
| **7** | Are the filter-edge rules load-bearing? | a token sits on the `top_p`/`min_p` edge on **5–46%** of positions → the rules fire constantly | §6.8 → **A** |
| **8** | Does E1 hold up *inside real vLLM*, not just the HF proxy? | **135/192 = 70.3%** float-vs-decimal divergence live (vs 14–77% offline) — higher because the executor samples in **numeric** token order while the validator uses **string** order (§6.6), so **E1 and §6.6 must be fixed together on the executor**; closes §7-step-1's "requires GPU verification" | **E1 + §6.6** → **A/D** |


---

## 3. Mechanisms

**Exp 1 — why the float path fails.** The float weights sum to `[65530, 65541]`, **never exactly 65536**. Since the sum ≠ 2^16, the same drawn u64 reduces (`u64 % sum`) to a value uncorrelated with the validator's `u64 % 65536`. Only the decimal pipeline guarantees an exact 2^16 total, so executor == validator.

**Exp 3 — why recompute is not reproducible.** Right-padding + a causal mask make a sequence's logits batch-independent in *exact* arithmetic; in float they are not, because batched-GEMM reduction order and kernel selection change with the batch dims. The effect is **~flat across batch size** (1+1 ≈ 1+16) — one co-batched sequence is enough. Magnitude is model-dependent (`gpt2` ≈ 4× `Qwen`).

**Exp 4 — why the sampled token alone is not enough.** A cheap model often agrees on the easy/obvious token, so `d_chosen` overlaps between honest and fraud (honest p95 `0.011` vs fraud p5 `0.006` on the Qwen pair). Fraud shows up in the **shape of the whole distribution** — which is why the metric must span the signed support set.

**Exp 5 — the precision ladder** (`d_mae` vs the fp16 reference, p50/p95): honest `0.006/0.011` ≪ int8 `0.097/0.200` < int4 `0.364/0.692` < a 3×-smaller model `0.82/2.26` (Qwen; `gpt2-large` agrees). A threshold near ~0.05 accepts only fp16, ~0.25 accepts int8, ~0.75 accepts int4.

**Exp 6 — determinism is exact within one architecture.** Across all 8 RTX-4090s and repeated runs, logits are **byte-identical** (0 max abs diff, 0 sample flips, both models). Run-to-run and card-to-card add **zero** drift, which isolates Exp 3's flips entirely to batch shape.

**Exp 7 — the boundary fires constantly.** Kept-set membership changes on 5–9% (`Qwen`) to 27–46% (`gpt2`) of positions under recompute noise. Since Stage-1 filters the *same* signed logprobs on both sides, they agree **only if the rule is identical** — a `<` vs `<=` cutoff, a different tie-break, a `top_k` clamp, or a `min_p` empty-set fallback would diverge on that same fraction.

---

## 4. Caveats

HF proxy — vLLM's chunked prefill / paged attention are untested and may drift differently. Small samples (64–128 positions per config). One GPU architecture (RTX 4090, one driver); **cross-architecture determinism is the single largest untested risk**. int4 = nf4 only; other schemes (gptq/awq) may land on different rungs. "Is int8 fraud?" is a protocol question, not a measurement.

---

## 5. Next steps

1. **Fix A** — the signed-artifact contract, with Exp 2 / 3 / 7 as inputs.
2. **Land the E1 patch** on the executor path, behind the flag, **in shadow first**.
3. **Close the untested gaps** before enforcement: cross-architecture determinism, real-vLLM-kernel behaviour, tokenizer drift, performance at production batch sizes.
4. Keep every Stage-1 verdict **non-enforcing** until D's criteria are met.

</details>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1199](https://github.com/gonka-ai/gonka/issues/1199) every hour.
