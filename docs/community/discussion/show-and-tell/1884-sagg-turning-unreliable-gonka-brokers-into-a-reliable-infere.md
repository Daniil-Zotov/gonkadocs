---
title: "#1884 — SAGG — turning unreliable Gonka brokers into a reliable inference API (cascading failover, real data)"
source: https://github.com/gonka-ai/gonka/discussions/1884
discussion_number: 1884
category: show-and-tell
synced_at: 2026-09-30T23:41:29Z
---

> 🔄 **Auto-sync:** from [Discussion #1884](https://github.com/gonka-ai/gonka/discussions/1884) every hour. 

# SAGG — turning unreliable Gonka brokers into a reliable inference API (cascading failover, real data)

**Автор:** [@privatedeskai](https://github.com/privatedeskai) · **Категория:** :raised_hands: Show and Tell · **Создано:** 2026-09-30 18:07 UTC · **Обновлено:** 2026-09-30 18:07 UTC

---

## 📝 Описание

The core idea: any single Gonka broker can have rough periods, but a cascade across several of them doesn't have to. That's the whole premise behind SAGG — take inherently volatile, individually unreliable brokers and turn them into a consistently reliable API on the output side, by holding several at once and switching automatically the moment one degrades.

We didn't just build this and claim it works — we measured it properly, on real, sustained production traffic:

Real, measured numbers (thousands of requests, sequential realistic traffic, not synthetic):

Standard line: 100% success (1000/1000 requests)
Super Deal line: 98.9% success (989/1000 requests)
TTFT p50: ~190ms, p95 under 3s

Full methodology, raw data, and a reproduction script: github.com/privatedeskai/sagg-benchmark-data

Why this isn't trivial: the hard part wasn't picking a backup broker — it was streaming responses specifically. Once a provider starts sending content to the client, you can't silently switch mid-stream without breaking the output. We solved this with buffered commit (hold the first content chunk before committing to the client) plus a reconnect mechanism that splices in a backup provider's continuation if a stream breaks partway through.

We also found and fixed a structural bug where the gateway reached its most reliable fallback tier far less often than it should have — the kind of thing that only shows up under sustained real traffic, not short tests.

If you're building on Gonka and dealing with broker instability yourself — happy to compare notes, or share more on the architecture. Live reference: api.privatedeskai.com (pricing) and api.privatedeskai.com/benchmarks (full reliability data, live).
