---
title: "#700 — Alphabetical Bias in PoC Slot Allocation"
source: https://github.com/gonka-ai/gonka/issues/700
issue_number: 700
synced_at: 2026-07-06T09:52:46Z
template: issues-main.html
---

> 🔄 **Auto-synced:** from [Issue #700](https://github.com/gonka-ai/gonka/issues/700) every 6 hours. 

# 🟢 Alphabetical Bias in PoC Slot Allocation

**Author:** [@huxuxuya](https://github.com/huxuxuya) · **State:** Open · **Created:** 2026-02-04 12:02 UTC · **Updated:** 2026-03-03 23:44 UTC

---

## 📝 Описание

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

---

## 💬 Comments (3)

### Комментарий 1 — [@AlexeySamosadov](https://github.com/AlexeySamosadov)

*2026-02-18 10:47 UTC*

Fix submitted in PR #777 — adds a deterministic SHA256-seeded Fisher-Yates shuffle to `allocateMLNodePerPoCForModel`, following the same pattern already used in `sampleEligibleParticipantsWithHistory`. All 27 tests pass.

### Комментарий 2 — [@huxuxuya](https://github.com/huxuxuya)

*2026-03-02 12:26 UTC*

Assign to me plz. Task already done.
#701 

### Комментарий 3 — [@tcharchian](https://github.com/tcharchian)

*2026-03-03 23:44 UTC*

@akup, I believe you worked on PoC Slot attack. Do you want to review these issues and PRs? Thanks
