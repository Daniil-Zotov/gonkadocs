---
title: "#1198 — Re-validate VLM inference and validation results from #1026"
source: https://github.com/gonka-ai/gonka/issues/1198
issue_number: 1198
synced_at: 2026-07-06T15:05:12Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Re-validate VLM inference and validation results from #1026
    <span class="issues-number">#1198</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item">[@tcharchian](https://github.com/tcharchian) opened 2026-05-19 23:03 UTC</span>
    <span class="issues-meta-item">7 comments</span>
    <span class="issues-meta-item">Updated 2026-06-11 09:07 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #4cbc0f; color: #24292f; border-color: #4cbc0f;">up-for-grabs</span></div>
</div>

<div class="issues-content">
Independent re-check of the VLM inference and validation results reported in #1026 before they are used for protocol, model onboarding, or host-facing decisions.

The goal is not to redo the full research from scratch, but to verify that the reported methodology, scripts, artifacts, thresholds, and conclusions are reproducible and technically sound.

## Context

Issue https://github.com/gonka-ai/gonka/issues/1026 proposes adding VLM serving and validation support to Gonka.
Current reported results, related PRs, Notebooks, raw validation data, and scripts are in the parent issue. 
 
## Task

Independently verify the results reported in https://github.com/gonka-ai/gonka/issues/1026
Please check:
1. Reproducibility
    * Can the provided notebooks and scripts be run from a clean environment?
    * Are all dependencies, model versions, dataset preparation steps, and runtime assumptions documented clearly enough?
    * Are there any hidden assumptions that are not captured in the issue, notebook, README, or scripts?
2. Dataset and artifacts
    * Confirm that the Flickr8K test split preparation is correct.
    * Confirm that the same images are used consistently between inference and validation.
    * Check that generated inference artifacts have the expected format and contain all fields required for validation.
    * Check whether artifact paths, image IDs, prompts, and outputs are aligned correctly.
3. Threshold calculation
    * Re-run or inspect the threshold calibration procedure.
    * Confirm that the reported thresholds 0.0214 / 0.0224 are produced by the documented method.
    * Verify that thresholds were not overfit to the specific fraud scenario or test split.
    * Check whether the threshold choice is robust enough for protocol use, or only suitable for the specific experiment.
4. Fraud / honest scenario design
    * Review how “honest” and “fraud” scenarios are constructed.
    * Confirm that the fraud scenario is realistic enough for Gonka validation assumptions.
    * Check whether the tested fraud case covers only one type of model mismatch, or whether more scenarios are needed.
    * In particular, verify the comparison between:
        * Qwen/Qwen3-VL-235B-A22B-Instruct-FP8
        * Qwen3-VL-235B-A22B-Instruct-AWQ
5. Metrics
    * Recompute the reported fraud detection accuracy / F1-score.
    * Confirm the reported approximately 99% accuracy for the large model.
    * Check false positives and false negatives separately.
    * Identify whether any failures are systematic, for example tied to image type, prompt type, output length, or model behavior.
6. Operational assumptions
    * Check whether the suggested deployment parameters are sufficient:

additional_args=[
    '--max-model-len', '128000',
    '--gpu-memory-utilization', '0.95'
]

* Verify whether the example setup of approximately 320GB VRAM is realistic for serving and validation.
* Note any risks around model loading, image preprocessing, context length, memory pressure, latency, batching, or logprobs support.

7. Integration readiness
    * Confirm whether the current scripts are suitable only for research benchmarking or are close to production integration into MLNode.
    * Identify what is still missing before VLM validation can be used in Gonka:
        * tests
        * docs
        * deterministic artifact format
        * validation pipeline integration
        * host deployment instructions
        * dashboard / monitoring implications
        * model proposal parameters

Please provide a short report in this issue with:

* Whether the results from #1026 are reproducible.
* Whether the reported thresholds and accuracy are correct.
* Any discrepancies found.
* Any assumptions that need to be documented.
* Any additional tests that should be run before accepting the VLM validation approach.
* A recommendation:
    * ready to proceed
    * proceed after minor fixes
    * needs more validation
    * not ready
</div>

---

## 💬 Comments (7)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@Ryanchen911](https://github.com/Ryanchen911)</span>
    <span class="issues-meta-item">commented 2026-05-22 08:30 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    hi Tania ,i plan to take this one
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@Ryanchen911](https://github.com/Ryanchen911)</span>
    <span class="issues-meta-item">commented 2026-05-25 09:34 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    cc @fedor-konovalenko @tcharchian
# Independent Re-Check of VLM Inference/Validation Results (#1026, PR #1150)

**Reviewer:** @Ryanchen911
**Scope:** Static methodology review of PR #1150 and the Qwen3-VL-235B-FP8 threshold calibration in `qwen3-VL-235B_thresholds-new.ipynb`, plus the companion `qwen2-2B-VL_thresholds.ipynb`. I did not re-run inference/validation on GPUs (no access to 4×A100/H100), and the raw `validation_results.jsonl` files live in GDrive rather than in the PR, so the numerical results themselves were not independently regenerated. Findings below come from reading the scripts, notebooks, committed configs, and comparing against the existing text-validation flow.

First — thank you @fedor-konovalenko for the substantial amount of work in this PR. The artifact format, config probing, and end-to-end inference/validation pipeline are all carefully designed and well-organized. The points below are suggestions and questions raised in the spirit of getting the model ready for protocol-level acceptance, not criticisms of the engineering effort.

---

## Summary recommendation

**Proceed after addressing a few clarifications.** The methodology is sound in shape and the headline numbers are internally consistent (I confirmed `Best F1-Score: 0.9935` and `Share of fraud found = 0.987` from the committed notebook outputs). There are a few areas where I'd suggest tightening before the threshold is used to gate host onboarding — listed below in rough order of how much they could affect the final number.

---

## Key questions / areas worth clarifying

### Q1. Were inference and validation actually run on different hosts?

Looking at the committed configs, both `mlnode/packages/benchmarks/data/235b-inference_results-new/inference/fp8-free_h100/inference_config.json` and `.../validation/fp8-enf_h100-h100/validation_config.json` record `url = http://localhost:8801/`. The only visible difference is the model load path (`/home/ubuntu/Qwen3-VL-...` vs `/dev/shm/Qwen3-VL-...`).

If both endpoints were on the same physical machine for the calibration data, that's worth noting because production validators will run on hosts the executor doesn't control, and the cross-host setup could introduce additional distance drift from:

- different CUDA / driver / vLLM builds across hosts
- different GPU kernel paths (TF32 vs FP16)
- continuous-batching nondeterminism across separate vLLM instances

Could you confirm whether the two endpoints were on different physical hosts? If they were on the same host, it might be worth running one more honest h100→h100 pair across two separate machines and checking whether the distance distribution sits visibly higher — that would tell us whether 0.0214 needs to be widened for the production scenario.

### Q2. F1 = 0.9935 — is the calibration set the same as the evaluation set?

Reading `find_optimal_bounds_parallel` in `validation/analysis.py`, the search range and the F1 computation both use the same `distances_val` / `distances_quant` arrays. The constraint `np.any(distances_val > lower) → reject` effectively pins `lower ≈ max(honest_distances)`, so the threshold is shaped by the 1–2 most extreme honest samples in the calibration set.

The number itself is correct as a description of the calibration data, but it would be very helpful to also have a held-out estimate (e.g. fit on 80% of the calibration set, evaluate on the remaining 20%, repeat a few times and report mean ± std). That way the protocol decision can be based on an out-of-sample number, which is what production-time fraud rate will actually look like.

### Q3. Coverage of fraud strategies

The fraud set in `qwen3-VL-235B_thresholds-new.ipynb` is `int4-enf_h100-h100` (INT4 AWQ as the dishonest executor, FP8 as the validator) — a single configuration. It might be worth adding one or two more plausible adversary patterns before the threshold is treated as a production safeguard, e.g.:

- a different quantization (INT2 / Marlin / GGUF Q4_K_M)
- a different sibling model (e.g. Qwen2.5-VL-7B passed off as Qwen3-VL-235B)
- the base (non-instruct) checkpoint

This isn't about chasing every possible attack, but covering more than one fraud configuration would make the 99% number much more meaningful for the "Gonka network will be safe from fraud" conclusion.

### Q4. The `upper` bound — is it intended to be active?

In `evaluate_bound()`:
```python
labels_pred = np.where(all_distances < lower, 0, 1)
labels_pred[(all_distances >= lower) & (all_distances <= upper)] = 1
```
The second assignment doesn't change any label, because `np.where` has already set all positions where `d >= lower` to 1. So `upper` doesn't affect F1, and `classify_data()` also only reads `lower`. Per cell 11 the printed "thresholds 0.0214 / 0.0224" come out of this loop, but only the first one is actually doing work.

Two possible directions:
- If the intent is a single-threshold gate, the `upper` could be dropped from the API and from the README so it's clear there's one threshold.
- If a two-stage gate was intended (e.g. `< lower` → accept, `lower–upper` → flag-for-review, `> upper` → reject), the optimizer could be reworked to fit `upper` against a metric that depends on it (e.g. minimize the review queue while keeping recall above target).

Either way, just wanted to flag that the README and the code currently don't agree on this.

---

## Additional observations

### O1. Notebook narrative is a bit out of sync with the actual outputs

In `qwen3-VL-235B_thresholds-new.ipynb`, the markdown above the fraud classification plot (cell 14) says *"with 54% of fraud samples falling in the 'fraud' classification zone."* The actual code output two cells later (cell 17) says `Share of fraud found = 0.987`. Looks like the 54 % text is left over from an earlier configuration. Worth a quick edit so the narrative matches the numerical result.

### O2. `_compare_configs` includes the URL, which always trips on the cross-host case

When inference and validation are intentionally on different hosts, the URLs differ and the comparison reports a warning. That makes it harder to spot a *real* config drift (e.g. mismatched request_params) buried in the same warning. One small improvement would be comparing just model `name` and `request_params`, and reporting URL difference at info level only.

### O3. Text-mismatch rows are kept then dropped silently

If the validation backend doesn't honor `enforced_tokens` (e.g. an older vLLM build without the patch), every row would mismatch on text, the validation script keeps the row with a warning, and `process_data` later drops it via `distance == -1`. In the worst case the user could end up with an empty distance set and no clear signal of *why*. A "first row mismatched — fail fast" check at the top of validation would catch this category much earlier.

### O4. No tests in the PR

The PR adds substantial new code (514 LOC for `vlm_inference.py`, 416 LOC for `vlm_validation.py`, plus changes in `analysis.py` / `utils.py`) without accompanying tests. Even a small fixture-based test of `distance2()` would help guard against silent regressions, and a CI check that the notebook's `Share of fraud found` cell output matches a value declared in the README would catch O1-type drift automatically going forward.

### O5. Distance metric has a length floor

`distance2()` divides by `max(100, len(results)) * top_k`. For Flickr8K image captions (mostly short responses), all rows hit the 100-token denominator. That implies the calibrated threshold is specifically for short-caption-style outputs. If the same model is later used for longer-form VLM tasks (multi-paragraph descriptions, document OCR), the threshold may need to be recalibrated. Worth mentioning in the deployment notes.

### O6. Top-k choice affects the threshold

Comparing the old proposal README (top-k = 20: threshold 0.0169, top-k = 5: threshold 0.0323) with the new one (top-k = 5: threshold 0.0214), the threshold is clearly sensitive to `top_logprobs`. If hosts deploy with a different value, the calibrated threshold no longer applies. Recommend documenting `top_logprobs = 5` as a hard deployment constraint, or recalibrating per supported value.

### O7. vLLM version

`validation_config.json` shows `0.8.2.dev8106+g9a6d76e05`, which is the custom build supporting `enforced_tokens`. The proposal README says "MLNode v0.1.0" — pinning the exact gonka-vllm commit alongside it would make the result independently reproducible.

### O8. System prompt difference between text and VLM paths

`utils.py:_prepare_messages` adds `"You are a helpful assistant…"` for the text path; the VLM path sends `[{"role": "user", "content": [text + image_url]}]` with no system prompt. Production traffic will likely include user-supplied system prompts, which the calibration doesn't cover. A small honest-set re-run with a representative system prompt would let us confirm the threshold doesn't drift much.

---

## Companion notebook: `qwen2-2B-VL_thresholds.ipynb`

The 2B notebook shares the same template as the 235B-new one, so Q1–Q4 apply analogously (one honest + one fraud config, same threshold methodology, same `upper` no-op). Two stale-text observations specific to it:

- **O1 is more pronounced in the 2B notebook**: cell 14 still says "54% of fraud samples falling in the 'fraud' classification zone", but cell 17's actual output is `Share of fraud found = 1.0`. The gap is larger than in the 235B notebook.
- **Additional**: cell 4's markdown says "validation uses the correct FP8 model", but cell 18's conclusion (and the old proposal README) confirm the 2B honest baseline is GPTQ-Int8, not FP8. Looks like text left over from the 235B template.

Both seem to be artifacts of template duplication. Since the proposal currently targets the 235B model rather than the 2B, this isn't on the critical path — but if future model proposals reuse this notebook template, it'd be helpful to fix the source so the boilerplate doesn't propagate.

---

## What I was able to confirm

| Issue's review point | Status | Notes |
|---|---|---|
| Notebooks reproducible from clean env | Partial | `gonka_path` is hard-coded; raw data on GDrive; vLLM build not pinned. Working through the pipeline from scratch would take some setup work. |
| Same Flickr8K test split between inference and validation | Mostly yes | Inference writes `metadata.image_paths`; validation reuses them. Falls back to sorted-dir alignment in the absence of metadata, which could misalign across hosts — worth adding a hash check (see L below). |
| Threshold calibration produces 0.0214 / 0.0224 | Yes | Confirmed via committed notebook outputs. |
| Threshold not overfit | Open question | See Q2 — no holdout reported. |
| Fraud scenario realistic | Could be broader | See Q3 — single fraud config. |
| ~99 % accuracy reproducible | Numerically yes | Cell outputs match the README's 0.9935 F1 / 98.7 % recall. Caveats from Q1–Q4 apply. |
| Operational params (320 GB VRAM, max-model-len 128000, gpu-mem-util 0.95) | Plausible | The 0.95 utilization is on the aggressive side and could OOM under input-length spikes; recommend documenting 0.85–0.90 as a safer baseline that operators can raise. |
| Integration readiness | Needs a few items | Tests, vLLM commit pin, narrative cleanup, ideally cross-host validation. |

---

## Minor / housekeeping notes

- `download_test_set.py`: line 39 has a Russian docstring; the script downloads all three Flickr8K splits (~8000 images) when only 1000 are used; lines 58–60 execute at module-import time. Wrapping the download in `if __name__ == "__main__":` and filtering to the test split would make this safer to import as a library.
- The notebook's `gonka_path = '/home/konovalenko_f/projects/gonka'` is hard-coded — easy to miss for someone reproducing the analysis. A `os.environ.get("GONKA_PATH", ...)` would help.
- `metadata.image_paths` stores absolute paths only. A SHA-256 of each image alongside the path would catch silent file-content drift between inference and validation hosts.
- F1 is computed on a 2:1 honest:fraud sample mix (2000 honest + 1000 fraud). Production base rate is much closer to 99:1, where F1 transfers poorly. PR-AUC or precision at a fixed FPR would translate more cleanly to the operational regime.
- PR base branch is `tg/benchamrk_scripts_update`, not `main`. Worth making the merge order explicit for anyone reviewing the chain.

---

## Suggested items before protocol-level acceptance

In rough priority order:

1. **Q1** — confirm/redo one honest run across two physical hosts and compare the distance distribution.
2. **Q2** — report a held-out F1 (e.g. 3 random 80/20 splits, mean ± std).
3. **Q3** — add at least one more fraud configuration (different quantization or sibling model).
4. **Q4** — either drop `upper` from the reported thresholds, or implement a real two-stage gate.
5. **O1** — update the notebook narrative in cell 14 (in both the 235B and 2B notebooks) to match the cell 17 output.
6. **O7** — pin the gonka-vllm commit that provides `enforced_tokens` in the README.
7. **O4** — add a small fixture-based test for `distance2()`, plus a CI check that the notebook's printed fraud share matches a value declared in the README.

Once Q1–Q4 are addressed, an updated headline number from a held-out evaluation would be the right basis for the onboarding decision. Happy to help review any follow-up changes.

  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@fedor-konovalenko](https://github.com/fedor-konovalenko)</span>
    <span class="issues-meta-item">commented 2026-06-06 22:43 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    First of all, thank you very much for such detailed, valuable, and helpful comments and feedback. I will do my best to take them into account.


**Q1. Were inference and validation actually run on different hosts?**
**Answer 1:** 
Yes, inference and validation were performed on physically different hosts.

**Q2. F1 = 0.9935 — is the calibration set the same as the evaluation set?**
**Answer 2:**
I add scripts and results for several validation runs experiments. New notebook is here `mlnode/packages/benchmarks/notebooks/qwen3-VL-235B_thresholds-new-holdout.ipynb`


**Q3. Coverage of fraud strategies**
**Answer 3:** 
A comparison with a small model presented as a large one will be added to the notebook; I'll attach the link below.

**Q4. The upper bound — is it intended to be active?**
**Answer 4**
Okay, I agree that it is better to drop `upper` from notebook

O1 - fixed
O2 - fixed
O3 - Yes, I was aiming for the latest version of the inference engine. The mentioned check can be added later if necessary.
O4 - Yes, the comment is certainly fair, the necessary tests will be added at the integration stage, which was discussed with the Gonka team.
O5 - fixed
O6 - The value 5 was taken as a currently unsupported value (according to the discussions with Gonka team). A note about this has been added to the readme.
O7 - fixed
O8 - The proposed verification will require additional experiments with larger models. I will discuss its feasibility and priority separately with the Gonka team.

**Minor issues**

- download_test_set.py - fixed
- The notebook's gonka_path - fixed
- PR base branch is tg/benchamrk_scripts_update - the choice of this particular branch as the baseline was agreed upon by the team
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@Ryanchen911](https://github.com/Ryanchen911)</span>
    <span class="issues-meta-item">commented 2026-06-08 01:55 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    Thanks for the thorough turnaround — this addresses almost everything, and the deferral of O3/O4/O8 to the integration stage is fine by me.
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@fedor-konovalenko](https://github.com/fedor-konovalenko)</span>
    <span class="issues-meta-item">commented 2026-06-10 13:28 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    Thanks! 

And here are results of fraud detection scenario: 7B VLM as 235B VLM.
F1 score = 100%

[notebook](https://github.com/machine-intelligence-laboratory/gonka/blob/32975b57567bcf09e8c858e5bd57259cba773943/mlnode/packages/benchmarks/notebooks/qwen3-VL-235B-vs-7B_thresholds.ipynb)
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@Ryanchen911](https://github.com/Ryanchen911)</span>
    <span class="issues-meta-item">commented 2026-06-11 08:42 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    Overall this looks good to me. Thanks for the thorough iterations.

One tiny carryover in qwen3-VL-235B-vs-7B_thresholds.ipynb: the fraud cell still says "99% of fraud samples" (output is 1.0) and the honest cell says "INT8 on both sides" though the set here is FP8 — leftover template text, same as O1. Easy fix whenever.
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@fedor-konovalenko](https://github.com/fedor-konovalenko)</span>
    <span class="issues-meta-item">commented 2026-06-11 09:07 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    Sorry, I really used old template :(
Fixed
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1198](https://github.com/gonka-ai/gonka/issues/1198) every 6 hours.
