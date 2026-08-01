---
title: "#1198 — Re-validate VLM inference and validation results from #1026"
source: https://github.com/gonka-ai/gonka/issues/1198
issue_number: 1198
synced_at: 2026-08-01T14:00:55Z
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
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-05-19 23:03 UTC</span>
    <span class="issues-meta-item">7 comments</span>
    <span class="issues-meta-item">Updated 2026-06-11 09:07 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #4cbc0f; color: #24292f; border-color: #4cbc0f;">up-for-grabs</span></div>
</div>

<div class="issues-content" markdown="1">
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
    <span><a href="https://github.com/Ryanchen911">@Ryanchen911</a></span>
    <span class="issues-meta-item">commented 2026-05-22 08:30 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>hi Tania ,i plan to take this one</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Ryanchen911">@Ryanchen911</a></span>
    <span class="issues-meta-item">commented 2026-05-25 09:34 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>cc @fedor-konovalenko @tcharchian</p>
<h1>Independent Re-Check of VLM Inference/Validation Results (#1026, PR #1150)</h1>
<p><strong>Reviewer:</strong> @Ryanchen911
<strong>Scope:</strong> Static methodology review of PR #1150 and the Qwen3-VL-235B-FP8 threshold calibration in <code>qwen3-VL-235B_thresholds-new.ipynb</code>, plus the companion <code>qwen2-2B-VL_thresholds.ipynb</code>. I did not re-run inference/validation on GPUs (no access to 4×A100/H100), and the raw <code>validation_results.jsonl</code> files live in GDrive rather than in the PR, so the numerical results themselves were not independently regenerated. Findings below come from reading the scripts, notebooks, committed configs, and comparing against the existing text-validation flow.</p>
<p>First — thank you @fedor-konovalenko for the substantial amount of work in this PR. The artifact format, config probing, and end-to-end inference/validation pipeline are all carefully designed and well-organized. The points below are suggestions and questions raised in the spirit of getting the model ready for protocol-level acceptance, not criticisms of the engineering effort.</p>
<hr />
<h2>Summary recommendation</h2>
<p><strong>Proceed after addressing a few clarifications.</strong> The methodology is sound in shape and the headline numbers are internally consistent (I confirmed <code>Best F1-Score: 0.9935</code> and <code>Share of fraud found = 0.987</code> from the committed notebook outputs). There are a few areas where I'd suggest tightening before the threshold is used to gate host onboarding — listed below in rough order of how much they could affect the final number.</p>
<hr />
<h2>Key questions / areas worth clarifying</h2>
<h3>Q1. Were inference and validation actually run on different hosts?</h3>
<p>Looking at the committed configs, both <code>mlnode/packages/benchmarks/data/235b-inference_results-new/inference/fp8-free_h100/inference_config.json</code> and <code>.../validation/fp8-enf_h100-h100/validation_config.json</code> record <code>url = http://localhost:8801/</code>. The only visible difference is the model load path (<code>/home/ubuntu/Qwen3-VL-...</code> vs <code>/dev/shm/Qwen3-VL-...</code>).</p>
<p>If both endpoints were on the same physical machine for the calibration data, that's worth noting because production validators will run on hosts the executor doesn't control, and the cross-host setup could introduce additional distance drift from:</p>
<ul>
<li>different CUDA / driver / vLLM builds across hosts</li>
<li>different GPU kernel paths (TF32 vs FP16)</li>
<li>continuous-batching nondeterminism across separate vLLM instances</li>
</ul>
<p>Could you confirm whether the two endpoints were on different physical hosts? If they were on the same host, it might be worth running one more honest h100→h100 pair across two separate machines and checking whether the distance distribution sits visibly higher — that would tell us whether 0.0214 needs to be widened for the production scenario.</p>
<h3>Q2. F1 = 0.9935 — is the calibration set the same as the evaluation set?</h3>
<p>Reading <code>find_optimal_bounds_parallel</code> in <code>validation/analysis.py</code>, the search range and the F1 computation both use the same <code>distances_val</code> / <code>distances_quant</code> arrays. The constraint <code>np.any(distances_val &gt; lower) → reject</code> effectively pins <code>lower ≈ max(honest_distances)</code>, so the threshold is shaped by the 1–2 most extreme honest samples in the calibration set.</p>
<p>The number itself is correct as a description of the calibration data, but it would be very helpful to also have a held-out estimate (e.g. fit on 80% of the calibration set, evaluate on the remaining 20%, repeat a few times and report mean ± std). That way the protocol decision can be based on an out-of-sample number, which is what production-time fraud rate will actually look like.</p>
<h3>Q3. Coverage of fraud strategies</h3>
<p>The fraud set in <code>qwen3-VL-235B_thresholds-new.ipynb</code> is <code>int4-enf_h100-h100</code> (INT4 AWQ as the dishonest executor, FP8 as the validator) — a single configuration. It might be worth adding one or two more plausible adversary patterns before the threshold is treated as a production safeguard, e.g.:</p>
<ul>
<li>a different quantization (INT2 / Marlin / GGUF Q4_K_M)</li>
<li>a different sibling model (e.g. Qwen2.5-VL-7B passed off as Qwen3-VL-235B)</li>
<li>the base (non-instruct) checkpoint</li>
</ul>
<p>This isn't about chasing every possible attack, but covering more than one fraud configuration would make the 99% number much more meaningful for the "Gonka network will be safe from fraud" conclusion.</p>
<h3>Q4. The <code>upper</code> bound — is it intended to be active?</h3>
<p>In <code>evaluate_bound()</code>:</p>
<pre><code class="language-python">labels_pred = np.where(all_distances &lt; lower, 0, 1)
labels_pred[(all_distances &gt;= lower) &amp; (all_distances &lt;= upper)] = 1
</code></pre>
<p>The second assignment doesn't change any label, because <code>np.where</code> has already set all positions where <code>d &gt;= lower</code> to 1. So <code>upper</code> doesn't affect F1, and <code>classify_data()</code> also only reads <code>lower</code>. Per cell 11 the printed "thresholds 0.0214 / 0.0224" come out of this loop, but only the first one is actually doing work.</p>
<p>Two possible directions:
- If the intent is a single-threshold gate, the <code>upper</code> could be dropped from the API and from the README so it's clear there's one threshold.
- If a two-stage gate was intended (e.g. <code>&lt; lower</code> → accept, <code>lower–upper</code> → flag-for-review, <code>&gt; upper</code> → reject), the optimizer could be reworked to fit <code>upper</code> against a metric that depends on it (e.g. minimize the review queue while keeping recall above target).</p>
<p>Either way, just wanted to flag that the README and the code currently don't agree on this.</p>
<hr />
<h2>Additional observations</h2>
<h3>O1. Notebook narrative is a bit out of sync with the actual outputs</h3>
<p>In <code>qwen3-VL-235B_thresholds-new.ipynb</code>, the markdown above the fraud classification plot (cell 14) says <em>"with 54% of fraud samples falling in the 'fraud' classification zone."</em> The actual code output two cells later (cell 17) says <code>Share of fraud found = 0.987</code>. Looks like the 54 % text is left over from an earlier configuration. Worth a quick edit so the narrative matches the numerical result.</p>
<h3>O2. <code>_compare_configs</code> includes the URL, which always trips on the cross-host case</h3>
<p>When inference and validation are intentionally on different hosts, the URLs differ and the comparison reports a warning. That makes it harder to spot a <em>real</em> config drift (e.g. mismatched request_params) buried in the same warning. One small improvement would be comparing just model <code>name</code> and <code>request_params</code>, and reporting URL difference at info level only.</p>
<h3>O3. Text-mismatch rows are kept then dropped silently</h3>
<p>If the validation backend doesn't honor <code>enforced_tokens</code> (e.g. an older vLLM build without the patch), every row would mismatch on text, the validation script keeps the row with a warning, and <code>process_data</code> later drops it via <code>distance == -1</code>. In the worst case the user could end up with an empty distance set and no clear signal of <em>why</em>. A "first row mismatched — fail fast" check at the top of validation would catch this category much earlier.</p>
<h3>O4. No tests in the PR</h3>
<p>The PR adds substantial new code (514 LOC for <code>vlm_inference.py</code>, 416 LOC for <code>vlm_validation.py</code>, plus changes in <code>analysis.py</code> / <code>utils.py</code>) without accompanying tests. Even a small fixture-based test of <code>distance2()</code> would help guard against silent regressions, and a CI check that the notebook's <code>Share of fraud found</code> cell output matches a value declared in the README would catch O1-type drift automatically going forward.</p>
<h3>O5. Distance metric has a length floor</h3>
<p><code>distance2()</code> divides by <code>max(100, len(results)) * top_k</code>. For Flickr8K image captions (mostly short responses), all rows hit the 100-token denominator. That implies the calibrated threshold is specifically for short-caption-style outputs. If the same model is later used for longer-form VLM tasks (multi-paragraph descriptions, document OCR), the threshold may need to be recalibrated. Worth mentioning in the deployment notes.</p>
<h3>O6. Top-k choice affects the threshold</h3>
<p>Comparing the old proposal README (top-k = 20: threshold 0.0169, top-k = 5: threshold 0.0323) with the new one (top-k = 5: threshold 0.0214), the threshold is clearly sensitive to <code>top_logprobs</code>. If hosts deploy with a different value, the calibrated threshold no longer applies. Recommend documenting <code>top_logprobs = 5</code> as a hard deployment constraint, or recalibrating per supported value.</p>
<h3>O7. vLLM version</h3>
<p><code>validation_config.json</code> shows <code>0.8.2.dev8106+g9a6d76e05</code>, which is the custom build supporting <code>enforced_tokens</code>. The proposal README says "MLNode v0.1.0" — pinning the exact gonka-vllm commit alongside it would make the result independently reproducible.</p>
<h3>O8. System prompt difference between text and VLM paths</h3>
<p><code>utils.py:_prepare_messages</code> adds <code>"You are a helpful assistant…"</code> for the text path; the VLM path sends <code>[{"role": "user", "content": [text + image_url]}]</code> with no system prompt. Production traffic will likely include user-supplied system prompts, which the calibration doesn't cover. A small honest-set re-run with a representative system prompt would let us confirm the threshold doesn't drift much.</p>
<hr />
<h2>Companion notebook: <code>qwen2-2B-VL_thresholds.ipynb</code></h2>
<p>The 2B notebook shares the same template as the 235B-new one, so Q1–Q4 apply analogously (one honest + one fraud config, same threshold methodology, same <code>upper</code> no-op). Two stale-text observations specific to it:</p>
<ul>
<li><strong>O1 is more pronounced in the 2B notebook</strong>: cell 14 still says "54% of fraud samples falling in the 'fraud' classification zone", but cell 17's actual output is <code>Share of fraud found = 1.0</code>. The gap is larger than in the 235B notebook.</li>
<li><strong>Additional</strong>: cell 4's markdown says "validation uses the correct FP8 model", but cell 18's conclusion (and the old proposal README) confirm the 2B honest baseline is GPTQ-Int8, not FP8. Looks like text left over from the 235B template.</li>
</ul>
<p>Both seem to be artifacts of template duplication. Since the proposal currently targets the 235B model rather than the 2B, this isn't on the critical path — but if future model proposals reuse this notebook template, it'd be helpful to fix the source so the boilerplate doesn't propagate.</p>
<hr />
<h2>What I was able to confirm</h2>
<table>
<thead>
<tr>
<th>Issue's review point</th>
<th>Status</th>
<th>Notes</th>
</tr>
</thead>
<tbody>
<tr>
<td>Notebooks reproducible from clean env</td>
<td>Partial</td>
<td><code>gonka_path</code> is hard-coded; raw data on GDrive; vLLM build not pinned. Working through the pipeline from scratch would take some setup work.</td>
</tr>
<tr>
<td>Same Flickr8K test split between inference and validation</td>
<td>Mostly yes</td>
<td>Inference writes <code>metadata.image_paths</code>; validation reuses them. Falls back to sorted-dir alignment in the absence of metadata, which could misalign across hosts — worth adding a hash check (see L below).</td>
</tr>
<tr>
<td>Threshold calibration produces 0.0214 / 0.0224</td>
<td>Yes</td>
<td>Confirmed via committed notebook outputs.</td>
</tr>
<tr>
<td>Threshold not overfit</td>
<td>Open question</td>
<td>See Q2 — no holdout reported.</td>
</tr>
<tr>
<td>Fraud scenario realistic</td>
<td>Could be broader</td>
<td>See Q3 — single fraud config.</td>
</tr>
<tr>
<td>~99 % accuracy reproducible</td>
<td>Numerically yes</td>
<td>Cell outputs match the README's 0.9935 F1 / 98.7 % recall. Caveats from Q1–Q4 apply.</td>
</tr>
<tr>
<td>Operational params (320 GB VRAM, max-model-len 128000, gpu-mem-util 0.95)</td>
<td>Plausible</td>
<td>The 0.95 utilization is on the aggressive side and could OOM under input-length spikes; recommend documenting 0.85–0.90 as a safer baseline that operators can raise.</td>
</tr>
<tr>
<td>Integration readiness</td>
<td>Needs a few items</td>
<td>Tests, vLLM commit pin, narrative cleanup, ideally cross-host validation.</td>
</tr>
</tbody>
</table>
<hr />
<h2>Minor / housekeeping notes</h2>
<ul>
<li><code>download_test_set.py</code>: line 39 has a Russian docstring; the script downloads all three Flickr8K splits (~8000 images) when only 1000 are used; lines 58–60 execute at module-import time. Wrapping the download in <code>if __name__ == "__main__":</code> and filtering to the test split would make this safer to import as a library.</li>
<li>The notebook's <code>gonka_path = '/home/konovalenko_f/projects/gonka'</code> is hard-coded — easy to miss for someone reproducing the analysis. A <code>os.environ.get("GONKA_PATH", ...)</code> would help.</li>
<li><code>metadata.image_paths</code> stores absolute paths only. A SHA-256 of each image alongside the path would catch silent file-content drift between inference and validation hosts.</li>
<li>F1 is computed on a 2:1 honest:fraud sample mix (2000 honest + 1000 fraud). Production base rate is much closer to 99:1, where F1 transfers poorly. PR-AUC or precision at a fixed FPR would translate more cleanly to the operational regime.</li>
<li>PR base branch is <code>tg/benchamrk_scripts_update</code>, not <code>main</code>. Worth making the merge order explicit for anyone reviewing the chain.</li>
</ul>
<hr />
<h2>Suggested items before protocol-level acceptance</h2>
<p>In rough priority order:</p>
<ol>
<li><strong>Q1</strong> — confirm/redo one honest run across two physical hosts and compare the distance distribution.</li>
<li><strong>Q2</strong> — report a held-out F1 (e.g. 3 random 80/20 splits, mean ± std).</li>
<li><strong>Q3</strong> — add at least one more fraud configuration (different quantization or sibling model).</li>
<li><strong>Q4</strong> — either drop <code>upper</code> from the reported thresholds, or implement a real two-stage gate.</li>
<li><strong>O1</strong> — update the notebook narrative in cell 14 (in both the 235B and 2B notebooks) to match the cell 17 output.</li>
<li><strong>O7</strong> — pin the gonka-vllm commit that provides <code>enforced_tokens</code> in the README.</li>
<li><strong>O4</strong> — add a small fixture-based test for <code>distance2()</code>, plus a CI check that the notebook's printed fraud share matches a value declared in the README.</li>
</ol>
<p>Once Q1–Q4 are addressed, an updated headline number from a held-out evaluation would be the right basis for the onboarding decision. Happy to help review any follow-up changes.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/fedor-konovalenko">@fedor-konovalenko</a></span>
    <span class="issues-meta-item">commented 2026-06-06 22:43 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>First of all, thank you very much for such detailed, valuable, and helpful comments and feedback. I will do my best to take them into account.</p>
<p><strong>Q1. Were inference and validation actually run on different hosts?</strong>
<strong>Answer 1:</strong> 
Yes, inference and validation were performed on physically different hosts.</p>
<p><strong>Q2. F1 = 0.9935 — is the calibration set the same as the evaluation set?</strong>
<strong>Answer 2:</strong>
I add scripts and results for several validation runs experiments. New notebook is here <code>mlnode/packages/benchmarks/notebooks/qwen3-VL-235B_thresholds-new-holdout.ipynb</code></p>
<p><strong>Q3. Coverage of fraud strategies</strong>
<strong>Answer 3:</strong> 
A comparison with a small model presented as a large one will be added to the notebook; I'll attach the link below.</p>
<p><strong>Q4. The upper bound — is it intended to be active?</strong>
<strong>Answer 4</strong>
Okay, I agree that it is better to drop <code>upper</code> from notebook</p>
<p>O1 - fixed
O2 - fixed
O3 - Yes, I was aiming for the latest version of the inference engine. The mentioned check can be added later if necessary.
O4 - Yes, the comment is certainly fair, the necessary tests will be added at the integration stage, which was discussed with the Gonka team.
O5 - fixed
O6 - The value 5 was taken as a currently unsupported value (according to the discussions with Gonka team). A note about this has been added to the readme.
O7 - fixed
O8 - The proposed verification will require additional experiments with larger models. I will discuss its feasibility and priority separately with the Gonka team.</p>
<p><strong>Minor issues</strong></p>
<ul>
<li>download_test_set.py - fixed</li>
<li>The notebook's gonka_path - fixed</li>
<li>PR base branch is tg/benchamrk_scripts_update - the choice of this particular branch as the baseline was agreed upon by the team</li>
</ul>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Ryanchen911">@Ryanchen911</a></span>
    <span class="issues-meta-item">commented 2026-06-08 01:55 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Thanks for the thorough turnaround — this addresses almost everything, and the deferral of O3/O4/O8 to the integration stage is fine by me.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/fedor-konovalenko">@fedor-konovalenko</a></span>
    <span class="issues-meta-item">commented 2026-06-10 13:28 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Thanks! </p>
<p>And here are results of fraud detection scenario: 7B VLM as 235B VLM.
F1 score = 100%</p>
<p><a href="https://github.com/machine-intelligence-laboratory/gonka/blob/32975b57567bcf09e8c858e5bd57259cba773943/mlnode/packages/benchmarks/notebooks/qwen3-VL-235B-vs-7B_thresholds.ipynb">notebook</a></p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Ryanchen911">@Ryanchen911</a></span>
    <span class="issues-meta-item">commented 2026-06-11 08:42 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Overall this looks good to me. Thanks for the thorough iterations.</p>
<p>One tiny carryover in qwen3-VL-235B-vs-7B_thresholds.ipynb: the fraud cell still says "99% of fraud samples" (output is 1.0) and the honest cell says "INT8 on both sides" though the set here is FP8 — leftover template text, same as O1. Easy fix whenever.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/fedor-konovalenko">@fedor-konovalenko</a></span>
    <span class="issues-meta-item">commented 2026-06-11 09:07 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Sorry, I really used old template :(
Fixed</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1198](https://github.com/gonka-ai/gonka/issues/1198) every hour.
