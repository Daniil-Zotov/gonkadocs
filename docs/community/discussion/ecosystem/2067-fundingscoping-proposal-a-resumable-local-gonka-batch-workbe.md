---
title: "#2067 — Funding/scoping proposal: a resumable local Gonka batch workbench"
source: https://github.com/gonka-ai/gonka/discussions/2067
discussion_number: 2067
category: ecosystem
synced_at: 2026-10-29T20:12:28Z
---

> 🔄 **Auto-sync:** from [Discussion #2067](https://github.com/gonka-ai/gonka/discussions/2067) every hour. 

# Funding/scoping proposal: a resumable local Gonka batch workbench

**Автор:** [@brodyga45](https://github.com/brodyga45) · **Категория:** :jigsaw: Ecosystem · **Создано:** 2026-10-20 10:21 UTC · **Обновлено:** 2026-10-20 10:21 UTC

---

## 📝 Описание

## Motivation
The roadmap's developer-access and demand-activation tracks call for usable reference applications. I propose a local, resumable batch workbench for running an agreed JSONL workload through a Gonka community broker. This is a funding/scoping proposal, not an implemented product or claim of existing users.

## High-level solution
A standalone Apache-2.0 Python CLI, using the broker's documented OpenAI-compatible chat endpoint. Input rows have stable job IDs; results and failures are checkpointed in SQLite and exported as JSONL. A small synthetic support-ticket classification example demonstrates a real end-to-end workflow. It would reuse standard HTTP libraries, not create another thin SDK wrapper or modify protocol/fees/settlement. No Genesis Code would be copied.

The useful behavior is local job recovery: restart the JSONL queue without re-running jobs whose completed results are durably recorded, bounded concurrency, explicit handling of 429/Retry-After, user-controlled attempts, separate malformed-result failures, and a review queue for requests whose server outcome is uncertain after a lost connection. This does not promise reconnecting an interrupted token stream or resuming model generation. Without a documented broker idempotency/recovery contract, a client cannot guarantee exactly-once inference or billing; uncertain requests must not be silently replayed. Any SDK or transport retries must follow that agreed contract. Users control prompt/result retention; keys must never enter logs or result exports.

## Proposed milestones and budget
Total proposed: USD3,500, subject to a useful agreed scope and actual funding route.
1. USD500: maintainer/Host-approved acceptance matrix, endpoint and supported-model baseline, an agreed synthetic workload, and a paid implementation plan. Review the existing broker, SDK and batch/benchmark tools for reuse first; agree whether a new CLI adds enough value. The matrix must specify retry limits, durable job states, interruption/uncertain-outcome handling, and whether this broker exposes stable request IDs or documented cached-result lookup. Existing native devshard recovery does not automatically establish that public broker contract. If existing tools already satisfy the workflow, recommend reuse and stop or re-scope rather than duplicating them. No substantial build before this agreement.
2. USD1,800: working CLI and fault-controlled local fixtures; planted rate limits, interrupted responses, process restart, malformed JSON and cancellation covered. Demonstrate retained completed-job IDs and explicit uncertain states.
3. USD1,200: agreed broker acceptance run and reproducible report, public release, installation/maintenance handoff, plus four weeks of bounded stabilization (one triage pass per week, fixes within agreed scope; no round-the-clock operational SLA).

Proposed duration: three weeks to release after agreement and test access, then the included four-week stabilization period. Live inference needs sponsor-provided approved test capacity or an agreed Host-run acceptance procedure. Local mocks alone would not prove live compatibility. No GPU hosting, paid API purchase, deposit, signing key, wallet operation or mainnet transaction is assumed for our preparation.

## Competition and boundaries
Existing OpenAI-compatible broker access and SDKs should be reused. Discussion869 covers semantic quality/routing and includes a planned SDK;1085 covers node observability. The current devshard stream-resume pre-proposal describes completed-response replay and distinguishes that from reconnecting a token stream; the offchain-payloads batching note concerns chain transaction throughput. This proposal concerns an end-user local batch queue with durable job records. It does not establish that no equivalent generic or Gonka tool exists: please identify overlap before implementation, and make reuse part of the first milestone. API-level batch endpoints, token-stream replay, model-quality claims, semantic routing, protocol transaction batching, chain security work, token economics and escrow management are outside this scope.

## Open questions before commitment
- Is this workflow useful enough to fund, and who would accept the milestones? Which existing effort should it complement?
- Can milestone funding be agreed in advance rather than retrospectively hoping for a reward? Every actual on-chain payout remains subject to governance; a suggested budget is not approval.
- Is an invoiced contract with an existing organization available for a Serbian sole proprietor? If only a stablecoin payout is available, what counterparty, denomination, payment evidence and fees would apply for the owner's review? No wallet setup or deposit is requested or authorized by this post.
- Who can sponsor approved test access or perform the live acceptance run?

## Who would do the work
brodyga45, through a Serbian sole proprietorship. Development uses Codex automation; no prior Gonka deployment, specialized blockchain history, existing batch-product users or completed human review is claimed. This is an invitation to agree a paid public deliverable; applicable contract/onboarding terms would receive owner review before acceptance.
