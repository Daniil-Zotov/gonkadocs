---
title: "#1404 — Add a lower-barrier GLM-5.2 option and consider DeepSeek-V4-Flash as the default model"
source: https://github.com/gonka-ai/gonka/discussions/1404
discussion_number: 1404
category: proposals
synced_at: 2026-07-26T04:35:03Z
---

> 🔄 **Auto-sync:** from [Discussion #1404](https://github.com/gonka-ai/gonka/discussions/1404) every hour. 

# Add a lower-barrier GLM-5.2 option and consider DeepSeek-V4-Flash as the default model

**Автор:** [@enonog](https://github.com/enonog) · **Категория:** :bulb: Proposals · **Создано:** 2026-07-05 23:32 UTC · **Обновлено:** 2026-07-16 04:40 UTC

---

## 📝 Описание

At the moment, the network has very limited active capacity for `GLM-5.2`. Most hosts are concentrated on `MiniMaxAI/MiniMax-M2.7`, while only a smaller number are serving `Kimi-K2.6`, and GLM-5.2 host adoption is still very low.

The current official GLM-5.2 model is `zai-org/GLM-5.2-FP8`, but its resource requirements are high. This makes it harder for more hosts to choose GLM-5.2, even though GLM-5.2 is one of the most attractive open models for coding, long-context tasks, tool usage, and Chinese/English developer workloads.

## Proposal 1: Add one quantized GLM-5.2 candidate

I suggest evaluating one of the following two GLM-5.2 quantized models:

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

Important note: this model is currently tested with SGLang only, so vLLM compatibility should be evaluated separately if Gonka requires vLLM for MLNode integration.

## Suggested approach

Do not replace the current GLM-5.2-FP8 immediately. A safer path would be:

1. Add one quantized GLM-5.2 candidate as an optional model.
2. Give it a bootstrap period.
3. Measure host adoption, PoC stability, validation consistency, inference speed, and user demand.
4. If results are good, increase its role in the model lineup.

The goal is to make GLM-5.2 more accessible to hosts and increase real GLM-5.2 availability on the network.

## Proposal 2: Consider replacing MiniMax-M2.7 as the default model

Currently, `MiniMaxAI/MiniMax-M2.7` is the default model (`initial_model_id`). It is useful as a low-barrier operational model, but it does not seem strong enough as the main default model for attracting real inference demand.

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

## Summary

I think Gonka should separate the model strategy into two layers:

1. A stronger default / fallback model:
   - consider `deepseek-ai/DeepSeek-V4-Flash` instead of `MiniMaxAI/MiniMax-M2.7`

2. A more accessible GLM-5.2 option:
   - choose between `canada-quant/GLM-5.2-W4A16-MTP` and `PhalaCloud/GLM-5.2-W4AFP8`

This would help the network improve both sides of the market:

- more hosts willing to serve useful models
- more users willing to send real inference requests

---

## 💬 Комментарии (2)

### Комментарий 1 — [@enonog](https://github.com/enonog)

*2026-07-06 11:35 UTC*

https://huggingface.co/PhalaCloud/GLM-5.2-W4AFP8

This model looks especially interesting because it is not just smaller than the official FP8 release, but may also provide very strong practical serving performance. According to the model card, it is optimized for SGLang and can fit on a wider range of host setups while still preserving long-context capability.

In some real workloads, quantized models are not necessarily worse than the official FP8 version. Depending on the quantization method and serving stack, they can sometimes preserve quality very well, and in certain scenarios such as long-context reasoning, coding, instruction following, and agentic workloads, the practical user experience may even be better because of higher throughput and lower latency.

The only unclear point is vLLM compatibility. The PhalaCloud model card mainly documents SGLang usage, so it would need to be tested inside Gonka’s current inference stack. However, since SGLang and vLLM share many important production-serving capabilities, this model still seems worth evaluating.

### Комментарий 2 — [@enonog](https://github.com/enonog)

*2026-07-16 04:40 UTC*

<img width="1703" height="775" alt="image" src="https://github.com/user-attachments/assets/757ff3b5-ed8b-4b87-8855-d586a2bd4b2c" />

