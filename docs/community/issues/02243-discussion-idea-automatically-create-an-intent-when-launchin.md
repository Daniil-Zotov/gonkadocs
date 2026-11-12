---
title: "#2243 — Discussion idea: automatically create an intent when launching a node"
source: https://github.com/gonka-ai/gonka/issues/2243
issue_number: 2243
synced_at: 2026-11-12T20:06:06Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Discussion idea: automatically create an intent when launching a node
    <span class="issues-number">#2243</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-11-06 22:57 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-11-06 22:57 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #c2e0c6; color: #24292f; border-color: #c2e0c6;">Priority: Low</span></div>
</div>

<div class="issues-content" markdown="1">
A community member suggested automatically creating an intent when a new node is launched, since launching a node typically implies that the host intends to make it available.

Alternatively, we could add a configuration flag that lets hosts enable or disable this behavior.

One thing to consider: Currently, hosts often create an intent before switching nodes to check whether enough participants are interested. They only bring the node online once the required number of participants is reached.

Open question: Would automatic intent creation improve the hosting experience, or would it interfere with the existing workflow? Should we make this behavior optional?
</div>

---

> 🔄 **Auto-synced** from [Issue #2243](https://github.com/gonka-ai/gonka/issues/2243) every hour.
