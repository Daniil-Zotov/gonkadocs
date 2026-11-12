---
title: "#2240 — Explore delegation across multiple nodes"
source: https://github.com/gonka-ai/gonka/issues/2240
issue_number: 2240
synced_at: 2026-11-12T03:08:14Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Explore delegation across multiple nodes
    <span class="issues-number">#2240</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-11-06 22:42 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-11-06 22:42 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Investigate whether delegation can be split across multiple nodes to diversify risk.

For example, instead of delegating 100% to a single node, a user could allocate 25% to each of four nodes. This would be similar to fractional voting, where voting power can be divided across multiple options rather than choosing only “Yes” or “No.”

This functionality is not supported in the current setup, but it may be useful for reducing concentration risk and improving delegation flexibility.

Additional options:

1. Set a delegation cap per node so that no single node can receive more than 30% of the total delegation.
2. Can we implement failover delegation? For example, if our node becomes unavailable, could our voting weight be automatically delegated to the 6Blocks node?
3. Do not delegate to Guardian nodes in the future. This is critically important and may be worth enforcing at the protocol level.
</div>

---

> 🔄 **Auto-synced** from [Issue #2240](https://github.com/gonka-ai/gonka/issues/2240) every hour.
