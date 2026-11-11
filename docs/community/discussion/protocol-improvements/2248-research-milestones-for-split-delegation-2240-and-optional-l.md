---
title: "#2248 — Research milestones for split delegation (#2240) and optional launch-time intents (#2243)"
source: https://github.com/gonka-ai/gonka/discussions/2248
discussion_number: 2248
category: protocol-improvements
synced_at: 2026-11-11T21:24:22Z
---

> 🔄 **Auto-sync:** from [Discussion #2248](https://github.com/gonka-ai/gonka/discussions/2248) every hour. 

# Research milestones for split delegation (#2240) and optional launch-time intents (#2243)

**Автор:** [@startupcompliancekit](https://github.com/startupcompliancekit) · **Категория:** :gear: Protocol Improvements · **Создано:** 2026-11-08 07:42 UTC · **Обновлено:** 2026-11-08 07:42 UTC

---

## 📝 Описание

I propose two bounded research milestones for #2240 and #2243, with designs, compatibility analysis and reproducible local simulations. These would establish implementation requirements before changing protocol behavior.

For #2240, the deliverable would distinguish governance voting authorization, fractional voting choices and stake delegation; trace the current implementation; specify fractional allocation, per-node caps, deterministic failover and Guardian exclusion; and document migration and enforcement requirements. Local cases would cover four equal allocations, rounding, insufficient eligible capacity, failed fallback targets, Guardian status changes, revocation, duplicate votes and conservation of voting power. The design would explicitly identify which behavior requires a protocol upgrade rather than existing authz grants.

For #2243, the deliverable would trace the intent lifecycle and compare automatic creation against opt-in creation, preserving the existing interest-first, launch-later workflow. It would recommend defaults and configuration, with local cases for pre-existing intents, restart, concurrent launches, failed transactions, delayed confirmation, cancellation and unavailable signing authority. Launching a process must not silently overwrite or duplicate an existing intent.

Proposed ETA: #2240 within five calendar days of scope alignment; #2243 within three calendar days after the first milestone, or within three days of alignment if taken independently. Each milestone includes one review revision. Production implementation and mainnet transactions are outside this research scope.

Before claiming the work, please confirm whether these design-and-simulation milestones are eligible for contributor rewards without a production implementation, who will review them, and the proposed stablecoin reward for each milestone, including asset/network and expected Host-approval process and timing. I understand that a proposed reward is not a guaranteed payout and that on-chain Host approval remains required.
