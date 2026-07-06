---
title: "#405 — [P0] Removing participants for inactivity"
source: https://github.com/gonka-ai/gonka/issues/405
issue_number: 405
synced_at: 2026-07-06T09:53:15Z
template: issues-main.html
---

> 🔄 **Auto-synced:** from [Issue #405](https://github.com/gonka-ai/gonka/issues/405) every 6 hours. 

# 🔴 [P0] Removing participants for inactivity

**Author:** [@tcharchian](https://github.com/tcharchian) · **State:** Closed · **Created:** 2025-10-23 19:48 UTC · **Updated:** 2026-01-16 05:33 UTC

**Веха:** v0.2.5

---

## 📝 Описание

Removing for inactivity

- Goal: to remove inactive/invalid participants faster, not send inference requests to them, not allow them to be TAs / Validators, and remove their voting power
- We need to check for missed inference not only once in an epoch, but more often. E.g., once in X blocks (X = 500?)
- if `missed_stat_signigicant([start_of_epoch, current_heigh])` => remove and jail
- if `invalid_stat_significant([start_of_epoch, current_heigh])` => remove and jail
- For invalid - we should check how it intercepts with the current check, but we check only for sequential invalidations.
- introduce additional `min_n_samples = 100` to make this regular check less strong
-  open question: we now allow being jailed but an active participant, there is some slashing for that, but the participant still receives most of the reward. It might be okay to leave it that way, but let's think if removing from active participants is better in that case

**All the details in that task are sketches, not exact solutions, and should be criticized accordingly.**
