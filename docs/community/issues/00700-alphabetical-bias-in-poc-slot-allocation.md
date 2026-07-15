---
title: "#700 — Alphabetical Bias in PoC Slot Allocation"
source: https://github.com/gonka-ai/gonka/issues/700
issue_number: 700
synced_at: 2026-07-15T11:06:54Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Alphabetical Bias in PoC Slot Allocation
    <span class="issues-number">#700</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item">[@huxuxuya](https://github.com/huxuxuya) opened 2026-02-04 12:02 UTC</span>
    <span class="issues-meta-item">3 comments</span>
    <span class="issues-meta-item">Updated 2026-03-03 23:44 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
### Description
The current implementation of the ML node allocation logic in 
x/inference/module/model_assignment.go
 contains an alphabetical bias that affects the fairness of the network.

**Alphabetical Bias:** The allocation algorithm iterates through participants in deterministic alphabetical order. This allows participants with "vanity addresses" (lexicographical prefixes like gonka1aaa...) to have a significantly higher probability of receiving PoC slots, potentially starving honest participants with random addresses.

### Impact
Economic Injustice: Participants are incentivized to mine vanity addresses rather than focus on hardware quality/uptime to increase their selection chances.
Starvation: Honest hardware providers with random addresses receive fewer opportunities despite having equal or higher eligibility.
### Proposed Solution
Deterministic Shuffle: Implement a pseudo-random shuffle of the participant list using SHA256(EpochIndex + ModelID) as a seed. This ensures fair rotation across epochs and models, providing equal opportunity to all eligible participants regardless of their address prefix.
</div>

---

## 💬 Comments (3)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@AlexeySamosadov](https://github.com/AlexeySamosadov)</span>
    <span class="issues-meta-item">commented 2026-02-18 10:47 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Fix submitted in PR #777 — adds a deterministic SHA256-seeded Fisher-Yates shuffle to <code>allocateMLNodePerPoCForModel</code>, following the same pattern already used in <code>sampleEligibleParticipantsWithHistory</code>. All 27 tests pass.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@huxuxuya](https://github.com/huxuxuya)</span>
    <span class="issues-meta-item">commented 2026-03-02 12:26 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Assign to me plz. Task already done.</p>
<h1>701</h1>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@tcharchian](https://github.com/tcharchian)</span>
    <span class="issues-meta-item">commented 2026-03-03 23:44 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@akup, I believe you worked on PoC Slot attack. Do you want to review these issues and PRs? Thanks</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #700](https://github.com/gonka-ai/gonka/issues/700) every hour.
