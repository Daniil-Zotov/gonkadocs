---
title: "#2308 — Proposal from Ancapex: Decision Models for Modest Hardware"
source: https://github.com/gonka-ai/gonka/discussions/2308
discussion_number: 2308
category: protocol-improvements
synced_at: 2026-11-26T14:59:55Z
---

> 🔄 **Auto-sync:** from [Discussion #2308](https://github.com/gonka-ai/gonka/discussions/2308) every hour. 

# Proposal from Ancapex: Decision Models for Modest Hardware

**Автор:** [@alancapex](https://github.com/alancapex) · **Категория:** :gear: Protocol Improvements · **Создано:** 2026-11-23 13:03 UTC · **Обновлено:** 2026-11-23 13:04 UTC

---

## 📝 Описание

The network is limited by hardware: powerful GPUs for modern LLMs are scarce. Decision models are a new class of in-demand models that needs only modest hardware, GPUs with 16 to 80 GB of memory.

They do not write text. They quickly choose one of the given answer options and report how confident they are. They are used for classifying and routing requests, checking the answers of other AI systems, and guardrails. About 6.7 trillion tokens a week already pass through OpenRouter for them.

We propose to bring this class to Gonka.

**Full draft:** https://github.com/alancapex/gonka/blob/proposal/decision-models/proposals/decision-models/README.md

Questions and feedback are welcome.

