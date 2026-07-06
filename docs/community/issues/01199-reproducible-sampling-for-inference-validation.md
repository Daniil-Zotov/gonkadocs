---
title: "#1199 — Reproducible sampling for inference validation"
source: https://github.com/gonka-ai/gonka/issues/1199
issue_number: 1199
synced_at: 2026-07-06T15:59:12Z
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
    <span class="issues-meta-item">[@tcharchian](https://github.com/tcharchian) opened 2026-05-19 23:17 UTC</span>
    <span class="issues-meta-item">5 comments</span>
    <span class="issues-meta-item">Updated 2026-07-06 02:53 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #4cbc0f; color: #24292f; border-color: #4cbc0f;">up-for-grabs</span></div>
</div>

<div class="issues-content">
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
    <span>[@Ryanchen911](https://github.com/Ryanchen911)</span>
    <span class="issues-meta-item">commented 2026-06-26 11:33 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    hi @tcharchian , does this issue need help? If yes, maybe we  can take this one.
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@tcharchian](https://github.com/tcharchian)</span>
    <span class="issues-meta-item">commented 2026-06-30 00:53 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    @Ryanchen911, yes please! 
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@neuron7xLab](https://github.com/neuron7xLab)</span>
    <span class="issues-meta-item">commented 2026-07-02 13:28 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    I ran an adversarial pass on the deterministic sampling dump against the inference-validation proposal.

**Finding:** the deterministic replay seed was not chain-bound — it was derived from request-controlled material (`f"{user_seed}|{prompt_token_ids}"`), so Stage-1 replay could be detached from the chain inference instance. The proposal requires `run_seed = SHA256(user_seed || inference_id_from_chain)`.

I opened a focused PR against `gonka-ai/vllm:tg/detemrinistic_sampling_dump` — gonka-ai/vllm#56 — with a chain-bound seed primitive + tests.

Scope note (updated as review tightened it to match vLLM's actual API):
- `user_seed` is **`int`-only** (vLLM `SamplingParams.seed` / OpenAI `seed` are `Optional[int]`); `bool`/non-`int` fail closed, so a str `"7"` can't collide with int `7`.
- the chain id must be a non-empty `str`, hashed **byte-exact** (no stripping); missing/empty/whitespace-only/non-`str` fail closed.
- framing is **byte-length-prefixed SHA256 over UTF-8** (portable to Go/Rust/JS), not raw concatenation.

Honest status: reproducible from `pull/56/head`; 10 invariant tests + a golden vector verified locally (isolated harness — full `pytest` needs a built vLLM env); CI is `action_required` (fork approval gate), so not green yet. Complementary to @Ryanchen911's review, not a takeover.
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@Ryanchen911](https://github.com/Ryanchen911)</span>
    <span class="issues-meta-item">commented 2026-07-06 01:30 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    @neuron7xLab thanks for the focused pass and PR — this lands squarely on the highest-priority item in our‘s review. We flagged the same seed-domain issue: the _dump/v011 derivation f"{user_seed}|{prompt_token_ids}" is request-controlled on both components, so Stage-1 replay can be ground/detached from the chain inference instance. Binding to inference_id_from_chain per the proposal is exactly right.

  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@Ryanchen911](https://github.com/Ryanchen911)</span>
    <span class="issues-meta-item">commented 2026-07-06 02:53 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    ## Review summary — reproducible sampling for inference validation

We reviewed the two-stage validation design (proposal §"Proper Fix") against the actual code on all three vllm branches (`_dump`, `v011`, `_merged`) plus the gonka chain-side validator, with an eye on a safe soft-rollout path.

**Final recommendation: needs additional review — not ready for soft MLNode integration yet.** The design is sound and matches the two-stage proposal; the implementation is real but split across two branches (each ~half) and not yet end-to-end runnable against real executor artifacts.

**Three blockers gate enforcement:**
- **S1 — seed not chain-bound.** Both branches seed from `f"{user_seed}|{prompt_token_ids}"` (executor-controllable → grindable + tokenizer-fragile). The proposal requires `SHA256(user_seed ‖ inference_id_from_chain)`. Primitive fix now in flight: `gonka-ai/vllm#56` (`derive_chain_bound_seed`) — should converge with #13 and get wired into a call site.
- **E1 — executor (GPU float) vs validator (CPU decimal) weights aren't bit-identical.** Zero-tolerance replay will false-reject real artifacts until the executor path adopts the decimal pipeline (ADR 0003; needs GPU verification).
- **S3 — no Python↔Go parity.** The chain validator is Go; there is no Go implementation of the decimal pipeline/RNG and cross-language bit-parity has never been tested.

**Safe now / non-enforcing:** the integer `deterministic_utils.py` as a torch-free library (after the S2 local-decimal-context fix, ADR 0002); the perplexity quick-fix as telemetry (gonka's `get_metric` ≈ 1/PPL); everything behind `VLLM_DETERMINISTIC_SAMPLING`, recording verdicts without slashing while collecting Stage-1 false-positive data (target: zero, by model/quant/hardware).

Full report below (findings S1/E1/S3/A1/A2/S2 + edge cases + rollout data + next steps).

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

---

> 🔄 **Auto-synced** from [Issue #1199](https://github.com/gonka-ai/gonka/issues/1199) every 6 hours.
