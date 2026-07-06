---
title: "#820 — Investigate missed inference on some nodes (root causes + mitigation)"
source: https://github.com/gonka-ai/gonka/issues/820
issue_number: 820
synced_at: 2026-07-06T09:52:44Z
template: issues-main.html
---

> 🔄 **Авто-синхронизация:** из [Issue #820](https://github.com/gonka-ai/gonka/issues/820) каждые 6 часов. 

# 🟢 Investigate missed inference on some nodes (root causes + mitigation)

**Автор:** [@tcharchian](https://github.com/tcharchian) · **Состояние:** Open · **Создано:** 2026-02-27 21:13 UTC · **Обновлено:** 2026-03-06 14:25 UTC

**Метки:** `bug` `help wanted` `up-for-grabs` `Priority: High`

---

## 📝 Описание


### Discussed in https://github.com/gonka-ai/gonka/discussions/817

<div type='discussions-op-text'>

<sup>Originally posted by **tcharchian** February 27, 2026</sup>

Task: Some nodes experience missed inference events. Likely multi-cause, needs community participation.

---

## 💬 Комментарии (2)

### Комментарий 1 — [@AlexeySamosadov](https://github.com/AlexeySamosadov)

*2026-03-03 10:27 UTC*

PR: https://github.com/gonka-ai/gonka/pull/843

### Комментарий 2 — [@Mayveskii](https://github.com/Mayveskii)

*2026-03-06 14:25 UTC*

Measured data from live network may help narrow root causes here.

Epochs 161–191, 2,503,595 inferences:
Miss rate: 3.25% (81,360 misses)
Completion rate: mean 90.4%, σ=7.4%, range 72–99%

The σ=7.4% variance is the signal — not the mean.
Some nodes miss 28% of assigned inferences while others miss 1%.
GetRandomExecutor routes to both equally regardless.

Phase 4 of GiP #860 proposes GetQualityWeightedExecutor — routes traffic 
proportional to L9 completion rate. Projection: σ ↓40% as high-miss nodes 
receive less traffic and face economic incentive to improve.

Design + data: docs/specs/inference-quality-protocol.md (PR #859 branch)
Discussion: #860 
