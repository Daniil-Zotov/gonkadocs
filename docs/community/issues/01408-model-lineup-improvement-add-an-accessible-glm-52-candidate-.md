---
title: "#1408 — Model lineup improvement: add an accessible GLM-5.2 candidate and reconsider MiniMax-M2.7 as default"
source: https://github.com/gonka-ai/gonka/issues/1408
issue_number: 1408
synced_at: 2026-07-22T03:51:52Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Model lineup improvement: add an accessible GLM-5.2 candidate and reconsider MiniMax-M2.7 as default
    <span class="issues-number">#1408</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/enonog">@enonog</a> opened 2026-07-06 12:31 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-07-16 19:56 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #a2eeef; color: #24292f; border-color: #a2eeef;">enhancement</span></div>
</div>

<div class="issues-content" markdown="1">
## Model lineup improvement: add an accessible GLM-5.2 candidate and reconsider the default model

### Problem

At the moment, the network appears to have very limited active capacity for `GLM-5.2`.

Most hosts are concentrated on `MiniMaxAI/MiniMax-M2.7`, while only a smaller number are serving `Kimi-K2.6`. GLM-5.2 adoption is still very low, even though GLM-5.2 is currently one of the most attractive open models for coding, long-context tasks, tool usage, and Chinese/English developer workloads.

The current official GLM-5.2 model is:

https://huggingface.co/zai-org/GLM-5.2-FP8

However, its resource requirements are high, which may reduce host willingness to serve it.

This creates a market mismatch:

- users may want GLM-5.2 inference
- but not enough hosts are willing or able to serve the current FP8 version
- as a result, the network cannot fully capture demand for this model

---

## Proposal 1: Add one quantized GLM-5.2 candidate

I suggest evaluating one of the following two non-GGUF, production-style GLM-5.2 quantized models.

### Option A: `canada-quant/GLM-5.2-W4A16-MTP`

https://huggingface.co/canada-quant/GLM-5.2-W4A16-MTP

Why it is interesting:

- vLLM-oriented
- non-GGUF production-style checkpoint
- W4A16 / INT4 quantization
- includes MTP / speculative decoding direction
- lower resource requirements than the current FP8 model
- may increase host willingness to serve GLM-5.2

### Option B: `PhalaCloud/GLM-5.2-W4AFP8`

https://huggingface.co/PhalaCloud/GLM-5.2-W4AFP8

Why it is interesting:

- non-GGUF production-style checkpoint
- based on `zai-org/GLM-5.2-FP8`
- much smaller than the FP8 release
- tested with SGLang
- keeps the full GLM-5.2 parameter count
- designed for long-context GLM-5.2 inference
- may provide strong practical throughput and user experience

Important note:

`PhalaCloud/GLM-5.2-W4AFP8` is currently documented mainly for SGLang. If Gonka requires vLLM for MLNode integration, vLLM compatibility should be tested before adding it to the active model lineup.

---

## Suggested implementation path

I do not suggest immediately replacing the current `zai-org/GLM-5.2-FP8`.

A safer path would be:

1. Add one quantized GLM-5.2 candidate as an optional model.
2. Give it a bootstrap period.
3. Measure:
   - host adoption
   - PoC stability
   - validation consistency
   - inference speed
   - long-context stability
   - real user demand
4. If the results are good, increase its role in the model lineup.

The goal is to make GLM-5.2 more accessible to hosts and increase real GLM-5.2 availability on the network.

---

## Proposal 2: Reconsider `MiniMaxAI/MiniMax-M2.7` as the default model

Currently, `MiniMaxAI/MiniMax-M2.7` is the default model / `initial_model_id`.

It may be useful as a low-barrier operational model, but it does not seem strong enough as the main default model for attracting real inference demand.

I suggest evaluating:

https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash

as a possible replacement or successor for `MiniMaxAI/MiniMax-M2.7` in the default / fallback model role.

Why `DeepSeek-V4-Flash` may be a better default candidate:

- lower resource requirements than many large MoE models
- strong DeepSeek brand recognition
- more attractive to developers than MiniMax-M2.7
- better fit for coding and agentic workloads
- likely to generate more real user demand
- can help keep the default model useful, not just easy to run

---

## Expected benefit

This would separate the model strategy into two layers:

1. A stronger default / fallback model:
   - consider `deepseek-ai/DeepSeek-V4-Flash` instead of `MiniMaxAI/MiniMax-M2.7`

2. A more accessible GLM-5.2 option:
   - choose between `canada-quant/GLM-5.2-W4A16-MTP` and `PhalaCloud/GLM-5.2-W4AFP8`

This may improve both sides of the network:

- more hosts willing to serve useful models
- more users willing to send real inference requests
- better utilization of the network
- stronger demand for GNK-based inference

---

## Request

Please consider:

1. Testing vLLM / MLNode compatibility for `canada-quant/GLM-5.2-W4A16-MTP`.
2. Testing vLLM / MLNode compatibility for `PhalaCloud/GLM-5.2-W4AFP8`.
3. Adding one of them as an optional GLM-5.2 candidate if validation is stable.
4. Evaluating `deepseek-ai/DeepSeek-V4-Flash` as a better default / fallback model than `MiniMaxAI/MiniMax-M2.7`.
</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/enonog">@enonog</a></span>
    <span class="issues-meta-item">commented 2026-07-06 12:33 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Additional note on <code>PhalaCloud/GLM-5.2-W4AFP8</code>:</p>
<p>This option may be especially promising. In practical use, its quality may be very close to, or in some cases even better than, the official FP8 release, while also providing very high token generation speed.</p>
<p>However, the main uncertainty is vLLM compatibility. The model card currently documents SGLang usage, but it is not fully clear whether it can run reliably under vLLM in Gonka's MLNode environment.</p>
<p>Since SGLang and vLLM share many important production inference capabilities, this model still seems worth testing. If it can be made compatible with Gonka's serving stack, it may be one of the best GLM-5.2 candidates for increasing host adoption and real user demand.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/enonog">@enonog</a></span>
    <span class="issues-meta-item">commented 2026-07-16 04:29 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p><img width="1705" height="794" alt="Image" src="https://github.com/user-attachments/assets/0b429965-059a-4e53-84d2-a71248f8b433" /></p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1408](https://github.com/gonka-ai/gonka/issues/1408) every hour.
