---
title: "#2308 — Proposal from Ancapex: Decision Models for Modest Hardware"
source: https://github.com/gonka-ai/gonka/discussions/2308
discussion_number: 2308
category: protocol-improvements
synced_at: 2026-11-28T10:12:48Z
---

> 🔄 **Auto-sync:** from [Discussion #2308](https://github.com/gonka-ai/gonka/discussions/2308) every hour. 

# Proposal from Ancapex: Decision Models for Modest Hardware

**Автор:** [@alancapex](https://github.com/alancapex) · **Категория:** :gear: Protocol Improvements · **Создано:** 2026-11-23 13:03 UTC · **Обновлено:** 2026-11-27 16:13 UTC

---

## 📝 Описание

The network is limited by hardware: powerful GPUs for modern LLMs are scarce. Decision models are a new class of in-demand models that needs only modest hardware, GPUs with 16 to 80 GB of memory.

They do not write text. They quickly choose one of the given answer options and report how confident they are. They are used for classifying and routing requests, checking the answers of other AI systems, and guardrails. About 6.7 trillion tokens a week already pass through OpenRouter for them.

We propose to bring this class to Gonka.

**Full draft:** https://github.com/alancapex/gonka/blob/proposal/decision-models/proposals/decision-models/README.md

Questions and feedback are welcome.


---

## 💬 Комментарии (3)

### Комментарий 1 — [@alancapex](https://github.com/alancapex)

*2026-11-26 17:43 UTC*

This proposal is now on-chain as **#121**. Voting is open until 28 November, 17:38 UTC.

### Комментарий 2 — [@akamitch](https://github.com/akamitch)

*2026-11-26 19:33 UTC*

A new type of model is a great experiment.
Even if a vulnerability is found in the implementation, a new cheating method appears, and these models have to be disabled the way Qwen 2.5 had to be, Gonka needs experiments like this. They're good for the protocol's development.

The Ancapex team has already made a useful improvement to the protocol, making it possible to mine to a different wallet, and as a mining service they've delivered with no complaints. To me, that already looks like enough of a reputation to justify allocating the funds.
The amount looks reasonable too.

### Комментарий 3 — [@sysmanalex](https://github.com/sysmanalex)

*2026-11-27 16:13 UTC*

Let me break down the arguments regarding this proposal from a practical standpoint:
- If the market is already occupied, three questions arise:
a) How—and by virtue of what—do you plan to enter an already saturated market, competing against a large, powerful incumbent? What is the specific competitive advantage that will lead to success? How will this be executed, and what are the projected timelines and costs?

b) Who are the initial target clients, and how will they be acquired? Are there any existing agreements or proven demand? What are the projections for sales and monetization?

c) What is the timeline for market entry and the procurement of the necessary 16–80GB GPU cards? Who are the leading suppliers—do you have access to at least 5–7–15 major vendors capable of providing thousands of units? Are there any formal agreements in place? Who, specifically, will handle the implementation?

d) What is the experience and assessment regarding the deployment of "decision models"?
Consider the implementation timeline, pricing strategy, cost estimation, and the overall economic model. Does a market for this even exist? Who has researched it, and what are the profit margins for small-scale models?

- Furthermore, how do you intend to explain to your current investors that the project is undergoing a complete change in direction?

Decision models (classifiers, rerankers, reward models, guardrails) have a completely different workload and verification profile compared to generative LLMs:
Small models typically involve long input sequences (prefill) followed by only 1–5 output tokens, with strict latency requirements (in the tens of milliseconds; otherwise, the router slows down the entire request).
Classification, routing, and guardrail models—even those requiring 16–80GB of VRAM—are considered "ultra-light" tasks. In a real-world production environment, these are not run over decentralized P2P networks for two key reasons:
- The criticality of latency: Routers and guardrails sit in front of the primary LLM. If the classifier adds a network hop to a random node in a P2P network (plus the overhead of consensus/verification), it destroys the UX of the entire pipeline—and, incidentally, renders the use of high-end hardware like H200s, B200s, or B300s completely pointless.

More importantly, the profit margins are razor-thin: these models have minimal production costs, yet face intense competition. Given the overheads inherent in a decentralized protocol—coordination, verification, transaction fees, and rewards—the network simply cannot compete with centralized providers on a price-per-million-tokens basis.

Not to mention the sales challenge: clients for these models don’t want to pay in GNK tokens; they want to pay in their own local currency. This complicates the sales process—B2B inference traffic doesn’t just magically appear the moment code is merged into a GitHub repository. It requires a dedicated sales effort—integrations, SDKs, billing systems, technical support, uptime guarantees, and a robust go-to-market strategy (sales, developer relations, and partnerships) planned months in advance. This isn't something you can just improvise.

I don’t want to clutter this thread with overly long comments—the core points are summarized above—but if there’s interest, I can provide a much deeper, more detailed analysis of the practical aspects. I have a concrete understanding of how to execute each step and what the downstream consequences of those decisions would be.
