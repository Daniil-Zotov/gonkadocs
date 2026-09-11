---
title: "#1721 — Community interest: adding GLM-5.3-Flash and Qwen3.8-Flash-Next to the lineup?"
source: https://github.com/gonka-ai/gonka/discussions/1721
discussion_number: 1721
category: protocol-improvements
synced_at: 2026-09-11T11:09:37Z
---

> 🔄 **Auto-sync:** from [Discussion #1721](https://github.com/gonka-ai/gonka/discussions/1721) every hour. 

# Community interest: adding GLM-5.3-Flash and Qwen3.8-Flash-Next to the lineup?

**Автор:** [@Ryanchen911](https://github.com/Ryanchen911) · **Категория:** :gear: Protocol Improvements · **Создано:** 2026-09-07 09:47 UTC · **Обновлено:** 2026-09-08 01:58 UTC

---

## 📝 Описание

Would the community be interested in adding these two models to Gonka?

- **GLM-5.3-Flash**
- **Qwen3.8-Flash-Next** (qwen4exp)

If so, which one would you want prioritized first?

---

## 💬 Комментарии (1)

### Комментарий 1 — [@paranjko](https://github.com/paranjko)

*2026-09-07 18:52 UTC*

I think we should have both models. From what I know from talking to hosts and contributor teams, **GLM 5.3 Flash is basically ready** for a vote, and we may see it as early as this week.

So let’s get GLM 5.3 Flash adopted first.

After that, I’d suggest moving straight to Qwen and phasing out MiniMax. That feels like the ideal setup: three relevant Flash models on the network.

So the order I’d propose is:
**GLM 5.3 Flash → adoption → Qwen 3.8 Flash → phase out MiniMax.**

**↳ Ответ от [@Ryanchen911](https://github.com/Ryanchen911)** · *2026-09-08 00:23 UTC*

> Sounds good, and I think the proportion of the running node weights of the Deepseek model can be increased.According to the statistics of gonka router in the recent half month, about 75% of the token consumption comes from the Deepseek model.

**↳ Ответ от [@paranjko](https://github.com/paranjko)** · *2026-09-08 01:58 UTC*

> Fully agree. I think once GLM 5.3F is adopted, we may want to put up another vote to adjust DeepSeek’s weight so it plays nicer on B200s.
