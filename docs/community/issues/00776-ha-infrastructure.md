---
title: "#776 — HA infrastructure"
source: https://github.com/gonka-ai/gonka/issues/776
issue_number: 776
synced_at: 2026-08-04T14:46:42Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    HA infrastructure
    <span class="issues-number">#776</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/Laboltus">@Laboltus</a> opened 2026-02-18 09:41 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-03-03 23:52 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
I'm trying to figure out how to create a highly available node. My understanding at the time is following
1. Full-node can be started in multiple instances and we can use some LB for balance and failover
2. Validator - with tmkms we can have only one active validator to avoid double-sign. For multiple active validators we need to adapt horcrux
3. Decentralized API - There can only be one active instance, and we should use custom scripts to synchronize SQLite database from the active instance to the standby one.

Am I right ? Is there some guide on this that I missed ?
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/blizko">@blizko</a></span>
    <span class="issues-meta-item">commented 2026-03-03 08:44 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>This topic is raised as discussion https://github.com/gonka-ai/gonka/discussions/837</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #776](https://github.com/gonka-ai/gonka/issues/776) every hour.
