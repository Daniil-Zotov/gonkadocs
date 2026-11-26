---
title: "#2308 — Proposal from Ancapex: Decision Models for Modest Hardware"
source: https://github.com/gonka-ai/gonka/discussions/2308
discussion_number: 2308
category: protocol-improvements
synced_at: 2026-11-26T23:44:44Z
---

> 🔄 **Auto-sync:** from [Discussion #2308](https://github.com/gonka-ai/gonka/discussions/2308) every hour. 

# Proposal from Ancapex: Decision Models for Modest Hardware

**Автор:** [@alancapex](https://github.com/alancapex) · **Категория:** :gear: Protocol Improvements · **Создано:** 2026-11-23 13:03 UTC · **Обновлено:** 2026-11-26 19:33 UTC

---

## 📝 Описание

The network is limited by hardware: powerful GPUs for modern LLMs are scarce. Decision models are a new class of in-demand models that needs only modest hardware, GPUs with 16 to 80 GB of memory.

They do not write text. They quickly choose one of the given answer options and report how confident they are. They are used for classifying and routing requests, checking the answers of other AI systems, and guardrails. About 6.7 trillion tokens a week already pass through OpenRouter for them.

We propose to bring this class to Gonka.

**Full draft:** https://github.com/alancapex/gonka/blob/proposal/decision-models/proposals/decision-models/README.md

Questions and feedback are welcome.


---

## 💬 Комментарии (2)

### Комментарий 1 — [@alancapex](https://github.com/alancapex)

*2026-11-26 17:43 UTC*

This proposal is now on-chain as **#121**. Voting is open until 28 November, 17:38 UTC.

### Комментарий 2 — [@akamitch](https://github.com/akamitch)

*2026-11-26 19:33 UTC*

A new type of model is a great experiment.
Even if a vulnerability is found in the implementation, a new cheating method appears, and these models have to be disabled the way Qwen 2.5 had to be, Gonka needs experiments like this. They're good for the protocol's development.

The Ancapex team has already made a useful improvement to the protocol, making it possible to mine to a different wallet, and as a mining service they've delivered with no complaints. To me, that already looks like enough of a reputation to justify allocating the funds.
The amount looks reasonable too.
