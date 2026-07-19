---
title: "#672 — gRPC always falls back to RPC"
source: https://github.com/gonka-ai/gonka/issues/672
issue_number: 672
synced_at: 2026-07-19T21:11:37Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    gRPC always falls back to RPC
    <span class="issues-number">#672</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/x0152">@x0152</a> opened 2026-01-30 16:21 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-02-12 15:26 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
gRPC is enabled, but requests still use RPC (#685 )
</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/AlexeySamosadov">@AlexeySamosadov</a></span>
    <span class="issues-meta-item">commented 2026-02-08 14:13 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>PR created: https://github.com/gonka-ai/gonka/pull/694</p>
<p>Enables gRPC for chain queries instead of RPC fallback.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/AlexeySamosadov">@AlexeySamosadov</a></span>
    <span class="issues-meta-item">commented 2026-02-12 15:26 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>I have a PR for this: #694 — adds optional gRPC transport for chain queries. Would appreciate a review when you get a chance.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #672](https://github.com/gonka-ai/gonka/issues/672) every hour.
