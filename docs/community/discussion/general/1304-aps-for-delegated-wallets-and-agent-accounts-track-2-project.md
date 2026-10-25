---
title: "#1304 — APS for delegated wallets and agent accounts (Track 2, Project 3)"
source: https://github.com/gonka-ai/gonka/discussions/1304
discussion_number: 1304
category: general
synced_at: 2026-10-25T18:57:41Z
---

> 🔄 **Auto-sync:** from [Discussion #1304](https://github.com/gonka-ai/gonka/discussions/1304) every hour. 

# APS for delegated wallets and agent accounts (Track 2, Project 3)

**Автор:** [@aeoess](https://github.com/aeoess) · **Категория:** :speech_balloon: General · **Создано:** 2026-06-04 01:38 UTC · **Обновлено:** 2026-10-20 23:36 UTC

---

## 📝 Описание

Track 2, Project 3 is close to what APS was built for: an agent acting within scoped authority, without exposing the owner's main key and without manual approval on every call. That authorization and audit layer is what APS implements today, open and Apache-2.0, on npm.

The primitives map to the project directly:

- **Predefined limits without exposing the main key:** the agent acts under a delegated key with a scoped grant. The owner's main key never leaves them. Limits can cover scope, spend cap, time window, and allowed actions.
- **No manual confirmation per action:** the scope authorizes a class of calls up front. Each request is checked against the delegation before it executes, with no human in the loop.
- **Owner keeps control:** sub-delegations can only narrow authority, and revoking a grant cascades to everything downstream.
- **Audit-trail review:** every authorized action emits a signed receipt that verifies offline, so the trail does not depend on trusting the gateway that produced it.

Project 3 also covers agents buying compute, not only calling inference. The same model extends to payment: one rail-agnostic interface carrying the same scoped authorization, spend limits, and signed receipts. Reference adapters ship for x402 (USDC on Base) and Nano, with bindings to AP2 (Google's Agent Payments Protocol), Stripe Issuing, and ACP. A Gonka-token rail would implement the same interface and inherit the limits, revocation, and receipts without new machinery.

To be clear on the boundary, APS is not a wallet, custody, or settlement. It sits in front of whatever holds funds and calls inference, decides whether a given agent action is authorized, and leaves a verifiable record that it happened. It runs as a library or an opt-in sidecar and needs no protocol change.

I'd rather show this than describe it, so I'm happy to put up a small reference implementation against the delegated-wallet path. Two questions to target it:

1. Is there a current branch or interface for the delegated-wallet / agent-account work, or is Project 3 still at the roadmap level?
2. Do you expect the authorization check to live closer to the wallet/account layer or the inference gateway? That decides where the check sits.

Repo: github.com/aeoess/agent-passport-system · npm: npmjs.com/package/agent-passport-system


---

## 💬 Комментарии (1)

### Комментарий 1 — [@aeoess](https://github.com/aeoess)

*2026-10-20 23:36 UTC*

@tcharchian, this thread came back up in today's triage, so here is a more concrete version of the proposal above. Gonka's roadmap describes this exact problem in Track 2, Project 3, "Delegated wallets and agent accounts", which asks for agents that "buy compute and run inference within predefined limits without exposing the main key", with the owner keeping "control through limits, delegation revocation, and audit-trail review".

In #1185, akamitch and gmorgachev suggested starting on the broker side, and a-kuprin said devshard should get authentication. Here is the narrower version, built on those suggestions.

OpenBroker already revokes individual API keys and records usage per request. What it does not cover yet, as far as I can see, is an owner giving an agent a bounded compute budget that the agent can split with sub-agents, with the limits holding across all of them. An owner lets a research agent use one model until a deadline. That agent hands a task to a second agent with a smaller allowance. Both draw from the owner's ceiling, two concurrent requests can't spend the same remaining budget, and revoking the parent stops every later call under either delegation.

Agent Passport System already has delegation chains that only narrow, revocation, and signed decision records. The Gonka inference adapter and the link to real charges would be new work.

The pilot I'd build, open source, broker side, one model, non-streaming:

- narrowed delegation, expiry and revocation checked before dispatch
- concurrent requests against a shared budget
- a signed record for every admission and refusal, linked to Gonka's own request and usage records, with estimated and settled cost kept apart

These are the same properties I work on in agent security standards. I wrote the denied-before-dispatch example vector in the OWASP Agentic Skills Top 10 (AST09), and I co-lead the candidate conformance cases for CoSAI's evidence sufficiency RFC-189. The pilot would be tested against those public cases, so you can check the results yourselves instead of trusting mine.

One call can involve several billable inference attempts, so a hard spend cap has to reserve the maximum charge before dispatch and hold it until the charge settles. If the broker can't bound the charge, the first version would limit calls or tokens and say so.

The roadmap says critical infrastructure "should not depend by default on a closed SaaS controlled exclusively by a single external team". I share that. APS is Apache 2.0, and anyone can check its records without trusting us. I'm also working with independent open source projects on a federation proposal for this kind of infrastructure (aeoess/agent-governance-vocabulary#177), where each project keeps its own code and keys. Gonka could be the compute layer there. The pilot stands on its own either way.

Which broker would be the best place to test this, and who should review the scope for Project 3?

**AI use:** drafted with AI assistance (Claude and Codex) under my direction. I reviewed it and take responsibility for the text.

