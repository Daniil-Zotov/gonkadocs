---
title: "#791 — Automatic cleanup of old propagation proofs"
source: https://github.com/gonka-ai/gonka/issues/791
issue_number: 791
synced_at: 2026-07-29T22:17:40Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Automatic cleanup of old propagation proofs
    <span class="issues-number">#791</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/slandymani">@slandymani</a> opened 2026-02-23 10:11 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-04-22 20:58 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Implement automatic cleanup of propagation data (bundles and proofs) from old epochs to prevent unbounded storage growth.

**Behavior:**
- When entering epoch N, delete all propagation data from epoch N-2
- Keep epoch N-1 data for potential validation recovery scenarios
- Cleanup triggers at the start of each new PoC phase

**Configuration:**
- Add `retain_all_proofs` flag to `poc_propagation` config section
- When `true`, disable cleanup (useful for debugging/testing)
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/slandymani">@slandymani</a></span>
    <span class="issues-meta-item">commented 2026-02-23 10:18 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>https://github.com/gonka-ai/gonka/pull/792</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #791](https://github.com/gonka-ai/gonka/issues/791) every hour.
