---
title: "#405 — [P0] Removing participants for inactivity"
source: https://github.com/gonka-ai/gonka/issues/405
issue_number: 405
synced_at: 2026-07-22T18:39:00Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    [P0] Removing participants for inactivity
    <span class="issues-number">#405</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2025-10-23 19:48 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-01-16 05:33 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Removing for inactivity

- Goal: to remove inactive/invalid participants faster, not send inference requests to them, not allow them to be TAs / Validators, and remove their voting power
- We need to check for missed inference not only once in an epoch, but more often. E.g., once in X blocks (X = 500?)
- if `missed_stat_signigicant([start_of_epoch, current_heigh])` => remove and jail
- if `invalid_stat_significant([start_of_epoch, current_heigh])` => remove and jail
- For invalid - we should check how it intercepts with the current check, but we check only for sequential invalidations.
- introduce additional `min_n_samples = 100` to make this regular check less strong
-  open question: we now allow being jailed but an active participant, there is some slashing for that, but the participant still receives most of the reward. It might be okay to leave it that way, but let's think if removing from active participants is better in that case

**All the details in that task are sketches, not exact solutions, and should be criticized accordingly.**
</div>

---

> 🔄 **Auto-synced** from [Issue #405](https://github.com/gonka-ai/gonka/issues/405) every hour.
