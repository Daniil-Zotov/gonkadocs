---
title: "#742 — [P2] Deleting PoC v1 + Extend state endpoint with PoC metadata"
source: https://github.com/gonka-ai/gonka/issues/742
issue_number: 742
synced_at: 2026-07-06T09:52:30Z
template: issues-main.html
---

> 🔄 **Авто-синхронизация:** из [Issue #742](https://github.com/gonka-ai/gonka/issues/742) каждые 6 часов. 

# 🔴 [P2] Deleting PoC v1 + Extend state endpoint with PoC metadata

**Автор:** [@IgnatovFedor](https://github.com/IgnatovFedor) · **Состояние:** Closed · **Создано:** 2026-02-12 15:06 UTC · **Обновлено:** 2026-03-25 19:10 UTC

**Метки:** `Priority: Low`

**Веха:** v0.2.12

---

## 📝 Описание

We want the main state endpoint to also expose PoC-related information required by the next vLLM PoC, so that vLLM can rely on a single source of truth.
Also poc v1 should be removed.
