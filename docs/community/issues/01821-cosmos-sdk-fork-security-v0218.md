---
title: "#1821 — Cosmos SDK / fork security v0.2.18"
source: https://github.com/gonka-ai/gonka/issues/1821
issue_number: 1821
synced_at: 2026-09-24T19:16:36Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Cosmos SDK / fork security v0.2.18
    <span class="issues-number">#1821</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-09-22 02:35 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-09-22 16:24 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #f86c7a; color: #24292f; border-color: #f86c7a;">Priority: High</span></div>
</div>

<div class="issues-content" markdown="1">
Cosmos SDK fork security for v0.2.18. Nothing huge: targeted fork patches first, full rebase only if it stays in scope.

Chain-halt fixes can ship on the current `v0.53.3-ps19` fork without waiting for v0.53.8. The rebase is a second, state-breaking step and needs its own test pass.

Needs thorough testing before merge.

## Sub-issues

- #1708 chain-halt: `ValidatorByConsAddr` returns `ErrNoValidatorFound` (gonka-ai/cosmos-sdk#19)
- #1205 chain-halt: `markValidatorForDeletion` jailed-delete race (gonka-ai/cosmos-sdk#16)
- #1719 ECIES: restore curve validation, reject short ciphertexts (gonka-ai/cosmos-sdk#20)
- #1671 rebase fork onto upstream v0.53.8

## Related fork PRs  

- gonka-ai/cosmos-sdk#14 stale consensus-key conflicts
- gonka-ai/cosmos-sdk#17 skip tombstoned validators in epoch recompute
- gonka-ai/cosmos-sdk#10 snapshot chunk deletion during state sync (see also #632)
</div>

---

> 🔄 **Auto-synced** from [Issue #1821](https://github.com/gonka-ai/gonka/issues/1821) every hour.
