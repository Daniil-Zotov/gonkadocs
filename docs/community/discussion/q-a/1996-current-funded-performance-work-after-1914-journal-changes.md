---
title: "#1996 — Current funded performance work after #1914 journal changes"
source: https://github.com/gonka-ai/gonka/discussions/1996
discussion_number: 1996
category: q-a
synced_at: 2026-10-25T18:57:42Z
---

> 🔄 **Auto-sync:** from [Discussion #1996](https://github.com/gonka-ai/gonka/discussions/1996) every hour. 

# Current funded performance work after #1914 journal changes

**Автор:** [@zileria354-ship-it](https://github.com/zileria354-ship-it) · **Категория:** :interrobang: Q&A · **Создано:** 2026-10-14 06:04 UTC · **Обновлено:** 2026-10-14 06:05 UTC

---

## 📝 Описание

Before posting a funding proposal around #1914, I checked the release branches and found that #1930 and #1932 already implement the mutation-journal work that would have formed its central scope. I will not claim or propose compensation for that existing implementation.

There is a narrower `TurnTracker.Clone` / `heartbeatAt` copying path in the reviewed v5/v6 branches, but v4.2 lacks it, and [on-chain governance proposal 114](https://gonka.gg/network/proposals/114) was described as approving v4.2 and removing v5. A benchmark of main's earlier path would not justify work on the replacement release.

Is there an unclaimed, current-release performance task that the maintainers want addressed under an explicitly agreed USDT milestone budget? I had prepared a 15,000-USDT engineering scope, but am holding it until the target, overlap, acceptance tests, governance sponsor, payment asset/network and funding process are confirmed. The amount is a proposed negotiation budget, not a demand or an existing reward.

I can provide a reproducible baseline, a reviewed implementation, differential correctness checks and before/after measurements once those conditions are agreed. Please identify any existing owner or funded assignment first. No live-network changes, expenses, or contract acceptance are proposed by this message.
