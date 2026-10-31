---
title: "#2194 — Track LFM3 support in MLNode and Gonka PoC"
source: https://github.com/gonka-ai/gonka/issues/2194
issue_number: 2194
synced_at: 2026-10-31T18:38:08Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Track LFM3 support in MLNode and Gonka PoC
    <span class="issues-number">#2194</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/ilyar">@ilyar</a> opened 2026-10-31 15:48 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-10-31 15:52 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
LFM3-1.7B cannot start in MLNode through the vLLM Transformers backend, so its Gonka PoC compatibility cannot yet be tested

## Observed behaviour

Tested `LiquidAI/LFM3-1.7B` at [this pinned revision](https://huggingface.co/LiquidAI/LFM3-1.7B/tree/ac2586a34f1a1c03329dbdcdefabd8b6478ddaa7) on a Tesla T4, FP16, with MLNode `4.0.0-sigma2`

```text
ghcr.io/gonka-ai/mlnode@sha256:e45bae55f11c9d72291dd075af781d5b7cf0b1bdb030fb611a937c8d7685b496
vLLM 0.30.0
Transformers 5.17.0
PyTorch 2.13.0+cu130
gonka-poc 0.2.0
```

The stock runtime fails while processing the model configuration with `KeyError: 'conv'` in `standardize_rope_params`

An isolated experiment using Transformers 5.22.0 advances beyond configuration loading, then vLLM rejects the convolution layer

```text
ValueError: Layer 0 (conv) does not dispatch through the Transformers attention interface and vLLM has no other way to handle it.
```

No Gonka or model source was modified, the dependency override was experimental and is not an official MLNode qualification result

## Reproduction

Download the pinned model snapshot including its custom Python files, mount it read-only at `/models/lfm3`, then send this payload to `POST /api/v1/inference/up/async`

```json
{
  "model": "/models/lfm3",
  "dtype": "float16",
  "additional_args": [
    "--tensor-parallel-size", "1",
    "--max-num-seqs", "1",
    "--gpu-memory-utilization", "0.26",
    "--max-model-len", "1024",
    "--max-num-batched-tokens", "1024",
    "--served-model-name", "LiquidAI/LFM3-1.7B",
    "--enforce-eager",
    "--model-impl", "transformers",
    "--trust-remote-code"
  ]
}
```

The original experiment reserved other GPU memory to leave approximately 4 GiB free before startup, neither failure was an OOM and this reservation is not required to explain the unsupported-layer error

## Required behaviour and integration scope

Track a supported path for LFM3 inference and Gonka PoC once a native vLLM implementation is available, startup or direct Transformers generation alone must not count as PoC support

The same checkpoint generated complete short responses through standalone Transformers 5.22.0 in FP16 within the experimental 4 GiB free-memory budget, that result does not qualify MLNode or PoC

Upstream work already exists in [the LFM3 support issue](https://github.com/vllm-project/vllm/issues/64645) and [the width-7 convolution PR](https://github.com/vllm-project/vllm/pull/64647), this issue tracks the Gonka integration boundary rather than duplicating the native model implementation

The integration needs verification of convolution-state isolation, repeated and reordered nonce checks, and inference after PoC, these are proposed acceptance requirements and have not yet been executed for LFM3

</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/ilyar">@ilyar</a></span>
    <span class="issues-meta-item">commented 2026-10-31 15:52 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Sorry, this is my personal experiment; I created it by accident</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2194](https://github.com/gonka-ai/gonka/issues/2194) every hour.
