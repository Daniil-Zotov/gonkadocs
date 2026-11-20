---
title: "#2272 — [BUG] PoC v2 vectors of a bf16 KV cache node change with the validation batch, so honest nodes fail validation"
source: https://github.com/gonka-ai/gonka/issues/2272
issue_number: 2272
synced_at: 2026-11-20T13:09:31Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    [BUG] PoC v2 vectors of a bf16 KV cache node change with the validation batch, so honest nodes fail validation
    <span class="issues-number">#2272</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/yaUrich">@yaUrich</a> opened 2026-11-16 16:43 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-11-16 18:24 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

With `--kv-cache-dtype auto` (bf16), an ML node does not reproduce its own PoC v2 vectors when it recomputes them in a different batch. Generated in one batch of 32 nonces and validated in a batch of 20, the same node mismatched on 5 of 20 nonces, always the same ones, with either attention backend. With `--kv-cache-dtype fp8` the same node reproduces its vectors bit for bit in any batch. Chain validation recomputes a sample of nonces in its own batch, so bf16 KV cache nodes are flagged as fraud.

## Motivation

On Community DevNet, switching every Qwen2.5-7B ML node from `fp8` to `auto` made PoC reject all of them, even in self-validation. The model group lost its weight for about 10 hours. We moved to `auto` because `fp8` degrades Qwen2.5-7B inference: its hosts vote invalid on a fifth of each other's answers. So for this model neither KV cache mode works today.

#1716 reports the same direction on Kimi-K2.6: 8.3 % self-validation mismatch on bf16 KV cache against 1.3 % on fp8.

## Impact

- Who is affected: hosts that run a model on bf16 KV cache, which is the vLLM default when node config sets no `--kv-cache-dtype`.
- Network-wide or limited: per model; every host of the model is affected the same way.
- Likelihood: reproducible on every run, on the same nonces.
- Affected components: MLNode PoC v2 generation and validation, `/api/v1/inference/pow/generate`.

## Detailed description

Setup: chain 0.2.16, `ghcr.io/gonka-ai/mlnode:3.0.16`, vLLM 0.25.1, Qwen/Qwen2.5-7B-Instruct `a09a35458c702b33eeacc393d103063234e8bc28`, RTX A5000 (sm86), `--kv-cache-memory-bytes 1073741824`. The node took no inference or PoC during the run.

Reproduction with `mlnode/packages/benchmarks/scripts/poc_validation` at `9e663130755ec60cd8c3f2be24c328353883a06c`:

1. Serve the model with `--kv-cache-dtype fp8`.
2. `make_artifact.py --seq-len 256 --num-nonces 32 --batch-size 32` with a fixed block hash, height and public key.
3. `validate.py --skip-download --skip-deploy --skip-throughput --threshold 0.4 --p-mismatch 0.1 --fraud-threshold 0.01` against that artifact, once with `--validation-batch-size 32`, once against an artifact cut to 20 evenly spread nonces.
4. Repeat 1–3 with `--kv-cache-dtype auto`, then with `--kv-cache-dtype auto --attention-backend FLASHINFER`, then with `fp8` again.

Mismatches of a node validating its own vectors:

| KV cache | Attention backend | All 32 in one batch | Sample of 20 |
|---|---|---|---|
| `fp8` | FlashInfer | 0 | 0 |
| `auto` | FlashAttention | 0 | 5 (nonces 0, 1, 3, 4, 6), p 0.043 |
| `auto` | FlashInfer | 0 | 5 (nonces 0, 1, 3, 4, 6), p 0.043 |
| `fp8`, after restart | FlashInfer | 0 | 0 |

- With `fp8` the vectors before and after the restart are identical, L2 distance 0 on all 32 nonces.
- When an `fp8` node validates the `auto` vectors, the sample mismatches only where the batch of 32 also does. The extra mismatches on nonces 0, 1, 3, 4 and 6 appear only when the validating node runs `auto`.
- At the chain's `p_value_threshold` of 0.05 the `auto` self-validation on the sample is `fraud_detected`. It passes only at the MLNode default of 0.01, which 0.2.16 applies because the chain value does not reach MLNode (fixed in v0.2.17, #2116).
- The attention backend changes the distance between `fp8` and `auto` vectors, median 0.275 with FlashAttention and 0.194 with FlashInfer, but not the batch dependence.

Full report with the per-mode table: paranjko/external-test-lab#327. How `fp8` degrades Qwen2.5-7B inference: paranjko/external-test-lab#315.

Question: for Qwen2.5-7B, `fp8` breaks inference and bf16 breaks PoC. Is there a supported setup for this model?

</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/yaUrich">@yaUrich</a></span>
    <span class="issues-meta-item">commented 2026-11-16 18:24 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Closing as fixed in newer MLNode images. The measurements above are from <code>mlnode:3.0.16</code>. The current images also run on chain 0.2.16:</p>
<ul>
<li>CUDA 13: <code>ghcr.io/gonka-ai/mlnode:4.0.0-sigma3@sha256:ce449de9545b55a8c55d495eaa512beebb72cd29478d4f4b672a1c231ce89d1f</code></li>
<li>CUDA 12: <code>ghcr.io/gonka-ai/mlnode:4.0.0-sigma3-cu12@sha256:3e4588d1dc33f4a09a1d099cb491348cdc80849ad7bad883da184ccf055f9aca</code></li>
</ul>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2272](https://github.com/gonka-ai/gonka/issues/2272) every hour.
