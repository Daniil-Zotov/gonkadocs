---
title: "#791 — Automatic cleanup of old propagation proofs"
source: https://github.com/gonka-ai/gonka/issues/791
issue_number: 791
synced_at: 2026-07-06T09:52:16Z
---

> 🔄 **Авто-синхронизация:** из [Issue #791](https://github.com/gonka-ai/gonka/issues/791) каждые 6 часов. 

# 🔴 Automatic cleanup of old propagation proofs

**Автор:** [@slandymani](https://github.com/slandymani) · **Состояние:** Closed · **Создано:** 2026-02-23 10:11 UTC · **Обновлено:** 2026-04-22 20:58 UTC

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

## 💬 Комментарии (1)

### Комментарий 1 — [@slandymani](https://github.com/slandymani)

*2026-02-23 10:18 UTC*

https://github.com/gonka-ai/gonka/pull/792
