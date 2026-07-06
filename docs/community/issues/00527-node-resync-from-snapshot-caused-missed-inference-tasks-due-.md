---
title: "#527 — Node resync from snapshot caused missed inference tasks due to large application.db"
source: https://github.com/gonka-ai/gonka/issues/527
issue_number: 527
synced_at: 2026-07-06T09:53:09Z
template: issues-main.html
---

> 🔄 **Auto-synced:** from [Issue #527](https://github.com/gonka-ai/gonka/issues/527) every 6 hours. 

# 🔴 Node resync from snapshot caused missed inference tasks due to large application.db

**Author:** [@bingcongxihaha](https://github.com/bingcongxihaha) · **State:** Closed · **Created:** 2026-01-06 16:35 UTC · **Updated:** 2026-01-22 00:08 UTC

---

## 📝 Описание

Hi,

I encountered an issue with my node where the application.db grew too large.
Because of this, I had to stop the node and resync it from a snapshot.

However, during the resync period, the node missed a significant number of inference tasks. I would like to ask:

Is there any way to recover or compensate for the missed inference tasks?

Or is there a recommended approach to avoid losing inference tasks when a resync is required due to a large application.db?

Any guidance or best practices would be greatly appreciated.
Thanks in advance for your help.

---

## 💬 Comments (1)

### Комментарий 1 — [@tcharchian](https://github.com/tcharchian)

*2026-01-22 00:08 UTC*

Hi @bingcongxihaha! Unfortunately, no inference tasks that are missed while a node is offline (e.g. during resync) cannot be recovered or compensated retroactively. Inference assignment and PoC are performed in real time. If a node is not running and serving requests during that period, those inference opportunities are simply lost.  

The goal is to prevent forced resyncs by controlling database growth and disk usage.

Cosmovisor creates a full backup of the .`inference/data` directory during upgrades. Make sure sufficient disk space is available. If disk usage is high, older backups in `.inference` [can be safely removed. ](https://gonka.ai/FAQ/#how-much-free-disk-space-is-required-for-a-cosmovisor-update-and-how-can-i-safely-remove-old-backups-from-the-inference-directory)
Large `application.db` files can be reduced using [these techniques.](https://gonka.ai/FAQ/#why-is-my-applicationdb-growing-so-large-and-how-do-i-fix-it)
