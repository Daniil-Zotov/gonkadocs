---
title: "#791 — Automatic cleanup of old propagation proofs"
source: https://github.com/gonka-ai/gonka/issues/791
issue_number: 791
synced_at: 2026-07-06T09:52:16Z
template: issues-main.html
---

> 🔄 **Auto-synced:** from [Issue #791](https://github.com/gonka-ai/gonka/issues/791) every 6 hours. 

# 🔴 Automatic cleanup of old propagation proofs

**Author:** [@slandymani](https://github.com/slandymani) · **State:** Closed · **Created:** 2026-02-23 10:11 UTC · **Updated:** 2026-04-22 20:58 UTC

---

## 📝 Описание

Implement automatic cleanup of propagation data (bundles and proofs) from old epochs to prevent unbounded storage growth.

**Behavior:**
- When entering epoch N, delete all propagation data from epoch N-2
- Keep epoch N-1 data for potential validation recovery scenarios
- Cleanup triggers at the start of each new PoC phase

**Configuration:**
- Add `retain_all_proofs` flag to `poc_propagation` config section
- When `true`, disable cleanup (useful for debugging/testing)

---

## 💬 Comments (1)

### Комментарий 1 — [@slandymani](https://github.com/slandymani)

*2026-02-23 10:18 UTC*

https://github.com/gonka-ai/gonka/pull/792
