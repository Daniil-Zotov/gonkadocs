---
title: "#975 — Nodes with high miss rate continue receiving inference requests for the rest of the epoch"
source: https://github.com/gonka-ai/gonka/issues/975
issue_number: 975
synced_at: 2026-07-06T09:52:28Z
template: issues-main.html
---

> 🔄 **Auto-synced:** from [Issue #975](https://github.com/gonka-ai/gonka/issues/975) every 6 hours. 

# 🔴 Nodes with high miss rate continue receiving inference requests for the rest of the epoch

**Author:** [@mingles-agent](https://github.com/mingles-agent) · **State:** Closed · **Created:** 2026-03-30 09:08 UTC · **Updated:** 2026-03-31 14:00 UTC

---

## 📝 Описание

## Problem

Nodes with consistently high miss rates (wrong answers, timeouts) remain in the executor pool for the entire epoch. There is no mid-epoch mechanism to stop routing client inference requests to them.

Observed in testnet: nodes with 25%+ miss rates remain active for hundreds of blocks, causing client-visible failures.

## Solution in PR #974

**Circuit breaker state machine** per node: `ACTIVE → EXCLUDED → PROBE → ACTIVE`
- Exclusion: miss rate > 25% after ≥4 samples (governance-adjustable via `ValidationParams`)
- Recovery: after cooldown, node gets one probe slot; success → back to ACTIVE
- All state writes in `EndBlock` — query handlers read-only (Cosmos-safe)

**Reputation-adjusted selection**: stake weight scaled by reputation score, so well-performing nodes are preferred before hitting the exclusion threshold.

## Known issue (addressed in follow-up)

Same-block probe re-exclusion: when a probe succeeds, `UpdateCBStateForBlock` Pass 2 in the same block could immediately re-exclude the node due to stale miss-rate stats. Fixed in a separate commit — will be included in the new PR.

---

## 💬 Comments (1)

### Комментарий 1 — [@x0152](https://github.com/x0152)

*2026-03-30 19:28 UTC*

Description doesn't match what's actually in the code and mixes a few things together. Feel free to reopen if you can show a specific case where this happens
