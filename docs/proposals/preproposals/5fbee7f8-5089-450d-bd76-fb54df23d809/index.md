---
title: "Add DeepSeek V4 Pro and Qwen3.8-27B Models"
template: proposals-main.html
---

# Add DeepSeek V4 Pro and Qwen3.8-27B Models

<div class="preproposal-header" markdown="1">

<div class="preproposal-status">🔴 Expired</div>

**Author:** Aung Myat Moe
**Created:** 2026-08-19 06:34 UTC
**Closes:** 2026-08-27 06:34 UTC
**Language:** EN
**Votes:** 2
**Avg. Bid:** 0.00 GNK

</div>

Expedited Update Params (Inference), Register Model

---

## Full Proposal

Motivation
The Gonka network relies on offering top-tier, high-demand AI models to remain competitive and attract a steady stream of inference requests. The recent advancements in open-weight models have brought two standout performers to the forefront:

DeepSeek V4 Pro: DeepSeek's latest iteration offers state-of-the-art reasoning, coding, and mathematical capabilities, often rivaling or exceeding proprietary counterparts at a fraction of the parameter cost. There is significant developer demand for DeepSeek models, as evidenced by the success of our recent addition of DeepSeek V4 Flash 0731.

Qwen3.8-27B: The Qwen series continues to excel in multilingual proficiency, robust context handling, and high-efficiency inference. The 27B parameter size is the "sweet spot" for decentralized inference, offering excellent capabilities while remaining hardware-friendly enough to ensure a broad distribution of capable nodes within our network.

Adding these two models will directly increase the network's utility, expand our user base, and drive higher computational volume through the network.

# 2. High-Level Solution
We propose registering both DeepSeek V4 Pro and Qwen3.8-27B to the Gonka model registry. This involves updating the network parameters to formally accept inference workloads for these models.

Register Model: Formally add the model identifiers and configurations to the chain.

Update Params (Inference): Adjust the inference parameters to allocate appropriate weight_scale_factor multipliers for these models based on their computational requirements.

# 3. Implementation Details
If this proposal passes, the following on-chain actions will be executed:

Register deepseek-v4-pro: Add the official DeepSeek model architecture configurations.

Register qwen3.8-27b: Add the official Qwen architecture configurations.

Set Weight Scale Factors:

Set the weight_scale_factor for deepseek-v4-pro to reflect its heavy computational demands relative to smaller models.

Set the weight_scale_factor for qwen3.8-27b to appropriately reward nodes processing this medium-to-large model. (Exact parameter multipliers to be finalized during community discussion prior to the final on-chain vote).

# 4. Open Questions for the Community Call
What should the exact weight_scale_factor be for these models to ensure fair compensation for node operators without pricing out end-users?

Should we gradually phase out any older, underutilized models (similar to the removal of older Kimi models) to free up bandwidth and storage for node operators?

---

## Comments (7)

### 💬 Slava MyGonka
*2026-08-19 08:25* · 👍 1 · 👎 0

Активное участие в добавлении новых моделей принимают эти ребята:
https://registry.kaitaku.ai/

https://t.me/baridoka

Думаю, тебе было бы интересно с ними пообщаться.

Именно они разрабатывали коэффициент для добавления Deep Seek.

---

### 💬 Aung Myat Moe
*2026-08-19 08:30* · 👍 1 · 👎 0

Yup I send message to them and I checked their images and most of them are optimized properly and new ds is just putting the entry

---

### 💬 Slava MyGonka
*2026-08-19 08:34* · 👍 1 · 👎 0

Я не могу найти их расчеты. Они где-то есть на GitHub. Перед добавлением подели они тестировали эту модель на разном оборудовании. Результаты тестов есть в отчете на GitHub.

Коэффициенты при добавлении модели  очень важны.

---

### 💬 Slava MyGonka
*2026-08-19 08:38* · 👍 1 · 👎 0

https://github.com/kaitakuai/experiments вот, ребята подсказали из Комьюнити.
Ты это читал?

---

### 💬 Slava MyGonka
*2026-08-19 07:14* · 👍 0 · 👎 0

Я считаю, что сеть пока не готова к приему моделей, которые не помещаются на 8*Н100.
Ты видел, что было с GLM?
То же самое ждет и DeepSeek V4 Pro, т.к. она слишком большая для доступных GPU.

А модель Qwen3.8-27B помещается на 1×H100 80 GB

Мы уже это проходили. Слишком маленькие модели позволяют заниматься читингом. Поэтому от них отказались.

---

### 💬 Aung Myat Moe
*2026-08-19 08:05* · 👍 0 · 👎 0

Nvx version can accept and it’s acceptable at performance and accuracy bro.

And the small model is dense qwen is at opus level and competing with Fabel .

To fix cheating governance need to update like TAO and make sure to put devshard as validate 

I am planning to make llm as verifier with new proposal before the research is done it should be able to do it

---

### 💬 Aung Myat Moe
*2026-08-19 23:11* · 👍 0 · 👎 0

Ok

---


---

<div class="preproposal-link" markdown="1">

[View on gonka.vote](https://gonka.vote/proposal/5fbee7f8-5089-450d-bd76-fb54df23d809)

</div>
