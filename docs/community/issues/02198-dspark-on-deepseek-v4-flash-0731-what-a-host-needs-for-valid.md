---
title: "#2198 — DSpark on DeepSeek-V4-Flash-0731: what a host needs for valid answers and votes"
source: https://github.com/gonka-ai/gonka/issues/2198
issue_number: 2198
synced_at: 2026-11-10T17:57:36Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    DSpark on DeepSeek-V4-Flash-0731: what a host needs for valid answers and votes
    <span class="issues-number">#2198</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/redstartechno">@redstartechno</a> opened 2026-11-02 05:22 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-11-05 19:27 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
### Summary

DSpark speeds up decode on DeepSeek-V4-Flash-0731: on real Gonka traffic we measured about 1.5x median and 2x p90 per stream at K=5, with a mean accepted length of 2.86. A plain setup, however, fails in ways that cost a host its answers, its votes or a whole epoch. We hit each of these on mainnet between 2026-10-17 and 10-20, then ran DSpark in production with the fixes below.

This issue proposes a documented, opt-in way to run DSpark on Gonka. It needs one code change, gonka-ai/vllm#124. The default stays as it is: V1 runner, no DSpark. Questions for maintainers are at the end.

### What a host needs

| # | Without it | Cause | What to do |
|---|---|---|---|
| 1 | The host's validator votes INVALID on nearly everything | The V2 runner, which DSpark requires, ignores `enforced_token_ids` during replay | Code fix: gonka-ai/vllm#124. The stock image also refuses V2 (`mlnode/packages/api/Dockerfile:44`) |
| 2 | The host's own answers are invalidated unless temperature is 0 | On V2 the logprobs mode is deployment-wide (`vllm/v1/worker/gpu/sample/sampler.py` and `spec_decode/rejection_sampler.py` read only the engine setting), the default is `raw_logprobs`, and the chain's `validation_params.logprobs_mode` is `processed_logprobs`. The `deploy/join` DeepSeek configs do not set the flag; the V1 path honours the per-request mode | `--logprobs-mode processed_logprobs` |
| 3 | The engine dies with `torch.OutOfMemoryError` on long prefills | The draft stages add 5.44 GiB per card in our setup, plus activation memory the startup estimate undercounts. At utilization 0.96 and chunk 8192 we had five engine deaths on 57K-108K prompts in one morning | Leave real headroom. `--max-model-len 400000` must still fit, or vLLM refuses to start, so utilization alone cannot solve it |
| 4 | A confirmation PoC produces 0 nonces and the host is excluded for the rest of the epoch | Lowering the chunk to avoid those OOMs breaks PoC: one forward is `batch x 1024` tokens and the buffer is sized by `--max-num-batched-tokens` (`assert buffer.shape[0] >= num_output_tokens`, `vllm/v1/attention/backend.py:509`) | Keep `POC_BATCH_SIZE_DEFAULT x 1024 <= --max-num-batched-tokens`, and smoke-test PoC after any chunk change. Chunk 2048 with batch 8 cost us epoch 431 |
| 5 | Startup hangs before any engine line (15 minutes in our case) | The API server blocks on an idle HTTPS socket to the HF CDN during the draft config lookup, with no read timeout | `HF_HUB_OFFLINE=1`, with the pinned revision in the local cache |
| 6 | Speculative config errors | `num_speculative_tokens` is validated before the block-size default applies (seen on a vLLM 0.32 nightly) | Set it explicitly. 5 is the DSpark block size, and K=7 measured no faster for us |

### A reference setup

Tested on 2 x RTX PRO 6000 (SM120) with tensor parallel 2, on top of the usual DeepSeek-V4-Flash args from `deploy/join`. Other GPUs will need different memory numbers.

```
VLLM_USE_V2_MODEL_RUNNER=1
POC_BATCH_SIZE_DEFAULT=4
HF_HUB_OFFLINE=1

--tensor-parallel-size 2
--gpu-memory-utilization 0.94
--max-model-len 400000
--max-num-batched-tokens 4096
--max-num-seqs 16
--kv-cache-dtype fp8
--logprobs-mode processed_logprobs
--speculative-config {"method":"dspark","num_speculative_tokens":5}
```

Measured with this setup on 2026-10-23: ready after 322 s; 168 requests in 21 minutes at concurrency 16 (up to about 370K tokens) with 0 drops and 0 preemptions; PoC golden vectors at batch 4 passed (12/1000 mismatches, p 1.0).

Costs against V1 on the same cards: PoC about 7% slower (642 against 690 nonces/min, because of batch 4) and KV memory about 35% smaller (8.02 against 12.41 GiB per card).

This exact setup has not served a full mainnet epoch. The later field data below comes from a build with the same code and requirements 1 and 2, but with host-specific tuning that is left out here, so it is not a sizing guide.

### Evidence

**Validator votes on other hosts' answers** (one host, all escrows in each window; the windows judge different answers, and sample sizes vary):

| Build | Valid | Invalid |
|---|---|---|
| V2 + DSpark, `raw_logprobs` | 1 | 119 |
| V2 + DSpark, `processed_logprobs`, no vLLM fix | 0 | 10 |
| V1, no DSpark | 330 | 60 |
| V2 + DSpark, `processed_logprobs`, vLLM fix | 206 | 17 |

**The host's own answers:** with `raw_logprobs`, 31 of 33 judged answers were invalidated (10-20). In an earlier sample from that window, the 2 valid answers had temperature 0 and all 29 invalid ones had temperature 0.2-0.6 or `top_p` 0.95. With all requirements in place, in epoch 437:

| Measure | This host | Reference |
|---|---|---|
| Challenged or invalidated, including cleared ones (10-25 23:06 to 10-26 12:48 UTC) | 15 / 2,127 (0.71%) | Other executors in the same 11 escrows: 172 / 18,047 (0.95%) |
| Whole epoch at a 10-26 19:35 UTC database copy | 6,234 sealed, 5 invalidated, 14 timed out; votes on our answers 938 valid / 84 invalid | |
| Tracker `slow_decode` / `slow_chunks` | 20% / 11% | Epoch 435 on this host, V1: 54% / 44%. Host tuning also differed, so not all of this is DSpark |
| Mean accepted tokens per step (K=5) | 3.45 | 2.86 in the first DSpark run, 10-17 to 10-20 |

Over about 22 hours of that epoch: no OOM, EngineDead, traceback or restart, and 7 preemptions. In epoch 439 the tracker showed `protocol_invalid` at 11 / 687 (1.6%, partial epoch), against 2.05% for epoch 435 on V1.

**Mixed network, controlled:** 18 synthetic prompts per cell (input 0.5K to 129K tokens; temperature 0, 0.7, and 0.6 with `top_p` 0.95), all 18/18 (10-23):

| Answers x validator | Min similarity | Median |
|---|---|---|
| V1 x V1 (control) | 0.964 | 0.972 |
| V1 x DSpark | 0.960 | 0.968 |
| DSpark x DSpark | 0.959 | 0.972 |
| DSpark x V1 | 0.959 | 0.969 |

**PoC on V2 + DSpark** (current prefill scheme): confirmation stage 10-18 with 13 validators, 0 invalid; cPoC 6,622,222 on 10-19 with 12 validators, 0 invalid; start PoC of epoch 439 with 16 validations, 0 invalid.

**Stored answers:** a scan of 2,082 DSpark answers found `usage.completion_tokens` equal to the logprob tokens in every complete answer, 0 duplicate `top_logprobs` in about 1.2M positions, and 0 NaN or missing logprobs. Every empty answer in those windows matched a logged engine death or PoC event.

### What this does not solve

- **Decode PoC.** The decode-PoC hooks exist only in the V1 runner (`vllm/v1/worker/gpu_model_runner.py`), and gonka-ai/vllm#116 reports batch-shape-dependent artifacts on V2. A DSpark host cannot serve the DECODE scheme, so this setup is only usable while the prefill scheme is live. The public chain params have no `poc_scheme` field today.
- **Coverage.** One host, one GPU type. Nothing here has run on H100, H200, B200 or B300, and we do not know their memory numbers.
- **DSpark answers under V1 validators.** The controlled cell passes, but the field votes are not split by validator build, so the judged sample for this combination is small.
- **vLLM changes and reports not specifically tested.** vllm-project/vllm#47616 (trims tokens left past a stop string under speculative decoding, merged 10-09) is not in the 0.30 fork's history, and no stored request in our scan set stop strings. vllm-project/vllm#62417 (DSpark output corruption, closed 10-27) was reported on V4.1-Flash-1017 on vLLM 0.32; we did not test for it on 0731 on 0.30.

### Questions for maintainers

1. Is an opt-in V2 + DSpark setup acceptable on the 0.30 line, with V1 staying the default? On gonka-ai/vllm#81 (July) a maintainer described V2 as a runner not offered yet; gonka-ai/vllm#92 then added V2 replay on 0.25.1, and gonka-ai/vllm#116 kept V1 as the 0.30 default.
2. What is the plan for decode PoC on V2? If no V2 hooks are planned, the docs should say a DSpark host has to return to V1 before a `poc_scheme` change.
3. If 1 is yes, we can follow up with: a capability check in `mlnode/packages/api/Dockerfile` (the `vllm.validation.V2_ENFORCED_TOKENS` marker from the vLLM PR, in place of the V1 assert); a section under "Deployment requirements" in `docs/chat-api/deepseek-v4-flash-0731.md`; and an opt-in node-config in `deploy/join/`. Would you want these?
4. Would you take a plugin change that passes `chunk` to `compute_prefill_artifacts` (`gonka_poc/poc/prefill_path.py`)? It already accepts the argument but its caller does not pass it. Splitting PoC batches would remove the coupling in requirement 4 for every host, with or without DSpark.

</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/redstartechno">@redstartechno</a></span>
    <span class="issues-meta-item">commented 2026-11-05 19:27 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>An update to this issue: a correction, a plan, and three questions. @vbgd0, it touches decode PoC and #2215, so you may be the right person to answer.</p>
<p><strong>Correction.</strong> "What this does not solve" says a DSpark host is usable while the prefill scheme is live. That is incomplete. From v0.2.17 the first confirmation PoC of each epoch runs decode as a trial (#2036; <code>ConfirmationRecipe</code> in <code>inference-chain/x/inference/types/poc_scheme.go</code>). Decode PoC runs only on the V1 runner (gonka-ai/vllm#116), and DSpark runs only on V2 (<code>vllm/config/vllm.py</code>: "DSpark is implemented only by the V2 GPU model runner").</p>
<p><strong>Why it is worth solving.</strong> The profile doc leaves speculative decoding off because its gain depends on the traffic (<code>docs/release-candidate-gpu-profile.md</code>): 1.4x to 3.9x on 20K to 45K prompts, 0.58x to 1.32x on 2K prompts at concurrency 30, PoC unchanged. On our host's real traffic we measured about 1.5x median and 2x p90 per stream. The losing case is the one vLLM's adaptive verification targets; in the fork's config checks it needs Hopper or B200/B300 and no pipeline parallelism, and we have not tested it. As an opt-in, each host can decide for its own traffic.</p>
<p><strong>What a DSpark host has to pass, as we read the code</strong> (not tested on a GPU unless stated):</p>
<table>
<thead>
<tr>
<th>Check</th>
<th>Status</th>
</tr>
</thead>
<tbody>
<tr>
<td>Today's logprob validation</td>
<td>Works with gonka-ai/vllm#124 and <code>processed_logprobs</code> (evidence above)</td>
</tr>
<tr>
<td>Decode PoC on V2</td>
<td>Missing; gonka-ai/vllm#115 measured batch-shape-dependent artifacts on V2</td>
</tr>
<tr>
<td>Decode PoC under pipeline parallelism</td>
<td>Missing for every pipeline-parallel host (<code>docs/mlnode-configs.md</code>). Each decode step's input embedding is seeded by the previous step's snap (<code>gonka_poc/mixed/runtime.py</code>), the snap comes from the final hidden states on the last rank, and the mixed path has no transfer back to the first rank</td>
</tr>
<tr>
<td>#2215 echo validation</td>
<td>Two gaps. V2 draws seeded noise with its own Triton Gumbel layout (<code>vllm/v1/worker/gpu/sample/gumbel.py</code>), while #2215 recomputes torch's V1 exponential draw, so we expect any V2 host to fail it, with or without DSpark. And DSpark's verification is a probability-ratio test, so its tokens leave the seed's sequence</td>
</tr>
</tbody>
</table>
<p><strong>What we plan to build</strong>, each as its own PR with tests, with GPU evidence on RTX PRO 6000 where we can get it:</p>
<ol>
<li>Decode PoC under pipeline parallelism: pass the previous step's snap from the last rank to the first, following the prefill PoC's pipeline-parallel path. Unless someone is already on this, we will take it.</li>
<li>An exact-match verification mode for DSpark: the draft proposes with the target's per-position noise, and a draft token is kept only if it equals the token the seeded draw picks at that position. Given the same logits, the output then equals the non-speculative output for the same seed.</li>
<li>After your answer on #2215: V2 drawing the same seeded noise as V1, so V2 answers land on the echo tape.</li>
<li>After your answer on decode PoC: the decode PoC hooks on V2, once the batch-shape cause is understood.</li>
<li>Last: the opt-in package (image capability check, node-config, docs).</li>
</ol>
<p><strong>Questions</strong></p>
<ol>
<li>Is an opt-in DSpark path wanted, with V1 and no speculation staying the default?</li>
<li>Is the cause of the V2 batch-shape dependence in gonka-ai/vllm#115 known?</li>
<li>For #2215: would you accept V2 matching V1's seeded noise, plus the exact-match mode above, as the way a host running speculative decoding passes the echo check?</li>
</ol>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2198](https://github.com/gonka-ai/gonka/issues/2198) every hour.
