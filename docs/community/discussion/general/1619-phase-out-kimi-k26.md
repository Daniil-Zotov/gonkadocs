---
title: "#1619 — Phase out Kimi K2.6"
source: https://github.com/gonka-ai/gonka/discussions/1619
discussion_number: 1619
category: general
synced_at: 2026-09-03T05:41:15Z
---

> 🔄 **Auto-sync:** from [Discussion #1619](https://github.com/gonka-ai/gonka/discussions/1619) every hour. 

# Phase out Kimi K2.6

**Автор:** [@paranjko](https://github.com/paranjko) · **Категория:** :speech_balloon: General · **Создано:** 2026-08-21 01:09 UTC · **Обновлено:** 2026-09-02 07:39 UTC

---

## 📝 Описание

DeepSeek v4 Flash 0731 has quickly become one of the most in-demand models on Gonka. Demand has been strong from day one, and at times it exceeds our current capacity. To increase Gonka’s capacity for DeepSeek v4 Flash and meet this demand, we need to encourage more hosts to allocate suitable hardware to the model.

That is why I propose phasing out Kimi K2.6.

There are several reasons for choosing Kimi:

- Demand for Kimi inference has been declining.
- Phasing out Kimi would free up B200 capacity that can be reallocated to DeepSeek v4 Flash.
- MiniMax M2.6 still sees meaningful demand and mostly runs on Hopper-class GPUs, so phasing it out would do less to free the Blackwell capacity DeepSeek needs.

You can track current inference demand by model, including token volume and requests, on the [inference dashboard](https://inference.dahl.global/gonka-network/).

You can also see the model and gateway distribution over time [here](https://inference.dahl.global/gonka-network/?view=pairs).

Instead of waiting for Kimi K2.6 to fade out on its own, I think a planned phase-out would make the transition more predictable. A predefined transition period would give hosts, gateways, and their clients time to adjust.

The goal is simple: move Gonka’s GPU capacity toward models with stronger demand and make better use of the hardware already in the network.

I suggest keeping this discussion about Kimi's fate open until August 30. Unless there are any objections, I’ll put the proposal to phase out Kimi K2.6 to a vote after that.

---

## 💬 Комментарии (6)

### Комментарий 1 — [@theaungmyatmoe](https://github.com/theaungmyatmoe)

*2026-08-21 10:42 UTC*

Exactly and we could bring the Deepseek VL model too. 

### Комментарий 2 — [@theaungmyatmoe](https://github.com/theaungmyatmoe)

*2026-08-23 09:40 UTC*

When will this progress start? can we get the date?

**↳ Ответ от [@paranjko](https://github.com/paranjko)** · *2026-08-24 21:34 UTC*

> I think I will put the proposal to phase out Kimi to a vote after August 30. There don’t seem to be many objections.

**↳ Ответ от [@theaungmyatmoe](https://github.com/theaungmyatmoe)** · *2026-08-25 11:15 UTC*

> ok pls put it i am ready to vote

### Комментарий 3 — [@mtvnastya](https://github.com/mtvnastya)

*2026-08-25 18:17 UTC*

the choice is ultimately for the hosts to make but I think this is a good idea to discuss this ahead.

Gonka should aim to support best models based on quality and demand.
both Kimi and Minimax are dropping from that list.
freeing up capacity for DeepSeek makes total sense.

with the current hardware distribution in the network it also makes more sense to start with substituting Kimi.

**↳ Ответ от [@theaungmyatmoe](https://github.com/theaungmyatmoe)** · *2026-08-25 19:47 UTC*

> this is the best news

**↳ Ответ от [@sysmanalex](https://github.com/sysmanalex)** · *2026-08-25 20:01 UTC*

> small remark & correction here. High demand for a model - or any network resource - cannot be treated as an objective measure of true value or economic utility if it is decoupled from cost.
>
> When users select a resource without facing its actual cost, high usage reflects artificially inflated consumer surplus, not a balanced market preference. This dynamic creates economic and operational distortions.
> right now it's most expensive model to run for network, but with discount pricing - this will be highly probably changed after real price forming/expenses re-evaluation. 
>
> **Price Distortions Hide the "Tragedy of the Commons"**
> In economics, when a valuable or resource-heavy asset is offered for free or well below its cost to serve, consumers use it up to the point where their marginal utility approaches zero.The Distortion: If DeepSeek Flash V4 consumes significant compute (e.g., active GPU memory, dense routing, or speculative execution compute) but users face flat, subsidized, or zero pricing, they will route mundane tasks to it simply because "it is the best available option for free."  
>
> **The Reality: This creates artificial demand. Users are not making a value-based choice or tradeoff (e.g., "Is this prompt worth $0.02 of compute?"); they are simply grabbing the maximum capability & best possible mode at zero marginal cost.**

**↳ Ответ от [@mtvnastya](https://github.com/mtvnastya)** · *2026-08-25 20:14 UTC*

> @sysmanalex I think these are two separate questions - which models to serve vs how the cost of inference for the users should be determined

**↳ Ответ от [@sysmanalex](https://github.com/sysmanalex)** · *2026-08-25 20:21 UTC*

> sorry to say, they are fundamentally linked and that's basic's of real economy. 
> - that's not questions, not guess, that's answer:
> You cannot separate which model to serve from how you price inference, because without price signals, you have no real demand data.
> - Free/Subsidized usage creates fake demand: If a heavy model is offered at zero or flat cost, users will over-consume it for simple tasks, creating artificial "high demand"
> - Prices reveal true economic value: Only when real pricing (reflecting compute/OpEx) is applied do users make rational trade-offs.
> - The feedback loop: Cost-reflective pricing filters out low-value traffic, which directly dictates which models are actually economically viable to keep serving on the network.
> p.s. This is not my opinion, not a guess, these are facts. I am writing this not to irritate you, but only to help and protect you from making mistakes through experience.

**↳ Ответ от [@mtvnastya](https://github.com/mtvnastya)** · *2026-08-26 22:40 UTC*

> agree these are deeply related, but they're of very different orders of magnitude in how they affect the network.
>
> phasing out kimi can be discussed, proposed and voted on within a week or two. updating the pricing model is a much bigger change that's already being discussed in many other threads, and it shouldn't block a smaller decision.
>
> pricing alone also doesn't solve this case: with per-model coefficients unchanged, a b200 serving deepseek at full capacity, even at openrouter prices, would earn less in total (inference + bitcoin-style reward) than it earns on kimi from the bitcoin-style reward alone. that's why a separate decision makes sense here.
>
> and by that logic we shouldn't have added deepseek, or any new model, in the first place, since picking initial coefficients carries the same distortion.

### Комментарий 4 — [@gmorgachev](https://github.com/gmorgachev)

*2026-08-26 06:30 UTC*

I agree that our demand data is noisy in some way

I support kimi -> deepseek replacement as:
1. deepseek is much cheaper to compute (total throughtput on the same server is much higher, 8xH100 with deepseek handles ~the same thoughtput as 8xB300 on kimi)
=> chain will be able to process much more client requests and it'll be more stable 
2. in public benchmarks latest deepseek flash beats kimi k2.6 clearly 

Overall, think Kimi has no real benefits



**↳ Ответ от [@theaungmyatmoe](https://github.com/theaungmyatmoe)** · *2026-08-26 06:39 UTC*

> at that server card it can get much more request and can handle it, i even tested with ds flash 0831 with rtx 4090 and get 100 tps so that at data center level cards it will be much more 

**↳ Ответ от [@sysmanalex](https://github.com/sysmanalex)** · *2026-08-27 21:57 UTC*

> check - qwen3.8-flash-next 
> @gmorgachev 

### Комментарий 5 — [@Username14345](https://github.com/Username14345)

*2026-09-01 12:23 UTC*

I'd say goodbye to the Minimax first; here, on the contrary, people actively use the Kimi. As for the Minimax, nobody uses it at all.

Especially since the new GLM Flash model requires the H100 and H200, which the Minimax has.

**↳ Ответ от [@theaungmyatmoe](https://github.com/theaungmyatmoe)** · *2026-09-01 13:45 UTC*

> GlM 5.3 Flash is dumb but it's better than MinMax ofc 
>
> I like to host both dsv4flash and Glm5.3 flash 

**↳ Ответ от [@paranjko](https://github.com/paranjko)** · *2026-09-02 00:25 UTC*

> I think we should definitely consider phasing out MiniMax as well, but I’d do it sequentially rather than all at once.
>
> Right now, MiniMax has a relatively large host base, while Kimi has much less capacity allocated to it. I think the better first step is to introduce GLM 5.3 Flash and phase out Kimi.
>
> This gives Hopper hosts time to adopt GLM 5.3 Flash organically, instead of forcing a large group of hosts to move at once. The relatively small number of B200 hosts currently on Kimi should be able to switch to DeepSeek Flash fairly easily.
>
> Then, as a next step, once GLM 5.3 Flash has been adopted by a meaningful share of hosts, we can look at phasing out MiniMax as well.

### Комментарий 6 — [@Ryanchen911](https://github.com/Ryanchen911)

*2026-09-02 07:39 UTC*

I agree, and we can add GLM 5.3 flash and Qwen 3.8 flash later.
