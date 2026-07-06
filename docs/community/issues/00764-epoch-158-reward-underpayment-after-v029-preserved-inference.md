---
title: "#764 — Epoch 158 reward underpayment after v0.2.9: preserved inference-slot weight was reset"
source: https://github.com/gonka-ai/gonka/issues/764
issue_number: 764
synced_at: 2026-07-06T09:52:49Z
template: issues-main.html
---

> 🔄 **Auto-synced:** from [Issue #764](https://github.com/gonka-ai/gonka/issues/764) every 6 hours. 

# 🔴 Epoch 158 reward underpayment after v0.2.9: preserved inference-slot weight was reset

**Author:** [@huxuxuya](https://github.com/huxuxuya) · **State:** Closed · **Created:** 2026-02-14 16:52 UTC · **Updated:** 2026-02-17 22:46 UTC

---

## 📝 Описание

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

---

## 💬 Comments (1)

### Комментарий 1 — [@AlexeySamosadov](https://github.com/AlexeySamosadov)

*2026-02-17 21:52 UTC*

PR with fix: #771 — removes resetPocSlotsInEpochGroupData from v0.2.9 upgrade handler. This function reset TimeslotAllocation[1] in EpochGroupData which is read during reward settlement, zeroing preservedWeight for all validators in epoch 158.

Note: this is a forward-fix for chain replay correctness. Compensation for epoch 158 affected validators requires a separate governance proposal.
