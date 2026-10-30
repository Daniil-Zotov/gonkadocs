---
title: "#1884 — SAGG — an OpenAI-compatible gateway over several Gonka providers, with measured results"
source: https://github.com/gonka-ai/gonka/discussions/1884
discussion_number: 1884
category: show-and-tell
synced_at: 2026-10-30T06:59:52Z
---

> 🔄 **Auto-sync:** from [Discussion #1884](https://github.com/gonka-ai/gonka/discussions/1884) every hour. 

# SAGG — an OpenAI-compatible gateway over several Gonka providers, with measured results

**Автор:** [@privatedeskai](https://github.com/privatedeskai) · **Категория:** :raised_hands: Show and Tell · **Создано:** 2026-09-30 18:07 UTC · **Обновлено:** 2026-10-26 20:32 UTC

---

## 📝 Описание

SAGG is an OpenAI-compatible gateway (`https://api.privatedeskai.com/v1`). It keeps several independent providers behind one endpoint and switches automatically when one of them degrades.

**Measured results**: one 24-hour test of version R1, 23–24 October 2026, synthetic mix of five request classes, nothing excluded.

**Standard line**: 99.94 % of requests served (4,769 of 4,772); time to first text median 1.4 s, 95th percentile 7.7 s.

**Super Deal line** (economical tariff, Gonka network only, no insurance outside it): 98.82 % served (4,782 of 4,839); median 1.4 s, 95th percentile 6.9 s.

No stream ended without an end signal; billing matched delivery for every served request.

One day is a measurement of that day, not a promise. Method, limits and raw data: https://api.privatedeskai.com/benchmarks and https://github.com/privatedeskai/sagg-benchmark-data. Earlier figures in this thread's first version (September, older gateway version) are replaced by the above.

Questions: support@privatedeskai.com.
