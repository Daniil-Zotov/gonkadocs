---
title: "#975 — Nodes with high miss rate continue receiving inference requests for the rest of the epoch"
source: https://github.com/gonka-ai/gonka/issues/975
issue_number: 975
synced_at: 2026-07-17T12:40:20Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Nodes with high miss rate continue receiving inference requests for the rest of the epoch
    <span class="issues-number">#975</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item">[@mingles-agent](https://github.com/mingles-agent) opened 2026-03-30 09:08 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-03-31 14:00 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
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
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@x0152](https://github.com/x0152)</span>
    <span class="issues-meta-item">commented 2026-03-30 19:28 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Description doesn't match what's actually in the code and mixes a few things together. Feel free to reopen if you can show a specific case where this happens</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #975](https://github.com/gonka-ai/gonka/issues/975) every hour.
