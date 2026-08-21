---
title: "#1619 — Phase out Kimi K2.6"
source: https://github.com/gonka-ai/gonka/discussions/1619
discussion_number: 1619
category: general
synced_at: 2026-08-21T19:32:26Z
---

> 🔄 **Auto-sync:** from [Discussion #1619](https://github.com/gonka-ai/gonka/discussions/1619) every hour. 

# Phase out Kimi K2.6

**Автор:** [@paranjko](https://github.com/paranjko) · **Категория:** :speech_balloon: General · **Создано:** 2026-08-21 01:09 UTC · **Обновлено:** 2026-08-21 10:42 UTC

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

## 💬 Комментарии (1)

### Комментарий 1 — [@theaungmyatmoe](https://github.com/theaungmyatmoe)

*2026-08-21 10:42 UTC*

Exactly and we could bring the Deepseek VL model too. 
