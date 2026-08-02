---
title: "#764 — Epoch 158 reward underpayment after v0.2.9: preserved inference-slot weight was reset"
source: https://github.com/gonka-ai/gonka/issues/764
issue_number: 764
synced_at: 2026-08-02T12:18:33Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Epoch 158 reward underpayment after v0.2.9: preserved inference-slot weight was reset
    <span class="issues-number">#764</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/huxuxuya">@huxuxuya</a> opened 2026-02-14 16:52 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-02-17 22:46 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
After upgrade v0.2.9, part of epoch 158 rewards appears to be distributed incorrectly.
  Validators that had ML nodes in preserved inference slot (POC_SLOT, TimeslotAllocation[1]) were not paid.

  Suspected root cause:
  - upgrade migration reset TimeslotAllocation[1] for effective-epoch data;
  - reward settlement uses preserved weight from this slot (effectiveWeight = preservedWeight +
    confirmationWeight);
  - as a result, preserved weight was reduced to zero for affected participants during settlement.

  Impact:
  - epoch 158 reward shares are skewed;
  - validators with significant preserved/inference-slot weight are affected most.

  Requested actions:

  1. Reconstruct historical slot allocation for epoch 158 at effective block height.
  2. Recalculate expected rewards with the same chain formula and filters.
  3. Prepare and execute compensation distribution via upgrade/governance proposal.
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/AlexeySamosadov">@AlexeySamosadov</a></span>
    <span class="issues-meta-item">commented 2026-02-17 21:52 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>PR with fix: #771 — removes resetPocSlotsInEpochGroupData from v0.2.9 upgrade handler. This function reset TimeslotAllocation[1] in EpochGroupData which is read during reward settlement, zeroing preservedWeight for all validators in epoch 158.</p>
<p>Note: this is a forward-fix for chain replay correctness. Compensation for epoch 158 affected validators requires a separate governance proposal.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #764](https://github.com/gonka-ai/gonka/issues/764) every hour.
