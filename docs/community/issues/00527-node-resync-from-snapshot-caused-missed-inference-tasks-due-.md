---
title: "#527 — Node resync from snapshot caused missed inference tasks due to large application.db"
source: https://github.com/gonka-ai/gonka/issues/527
issue_number: 527
synced_at: 2026-08-03T19:02:05Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Node resync from snapshot caused missed inference tasks due to large application.db
    <span class="issues-number">#527</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/bingcongxihaha">@bingcongxihaha</a> opened 2026-01-06 16:35 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-01-22 00:08 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Hi,

I encountered an issue with my node where the application.db grew too large.
Because of this, I had to stop the node and resync it from a snapshot.

However, during the resync period, the node missed a significant number of inference tasks. I would like to ask:

Is there any way to recover or compensate for the missed inference tasks?

Or is there a recommended approach to avoid losing inference tasks when a resync is required due to a large application.db?

Any guidance or best practices would be greatly appreciated.
Thanks in advance for your help.
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-01-22 00:08 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi @bingcongxihaha! Unfortunately, no inference tasks that are missed while a node is offline (e.g. during resync) cannot be recovered or compensated retroactively. Inference assignment and PoC are performed in real time. If a node is not running and serving requests during that period, those inference opportunities are simply lost.  </p>
<p>The goal is to prevent forced resyncs by controlling database growth and disk usage.</p>
<p>Cosmovisor creates a full backup of the .<code>inference/data</code> directory during upgrades. Make sure sufficient disk space is available. If disk usage is high, older backups in <code>.inference</code> <a href="https://gonka.ai/FAQ/#how-much-free-disk-space-is-required-for-a-cosmovisor-update-and-how-can-i-safely-remove-old-backups-from-the-inference-directory">can be safely removed. </a>
Large <code>application.db</code> files can be reduced using <a href="https://gonka.ai/FAQ/#why-is-my-applicationdb-growing-so-large-and-how-do-i-fix-it">these techniques.</a></p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #527](https://github.com/gonka-ai/gonka/issues/527) every hour.
