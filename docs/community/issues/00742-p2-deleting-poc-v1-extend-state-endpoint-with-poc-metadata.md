---
title: "#742 — [P2] Deleting PoC v1 + Extend state endpoint with PoC metadata"
source: https://github.com/gonka-ai/gonka/issues/742
issue_number: 742
synced_at: 2026-07-30T12:09:46Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    [P2] Deleting PoC v1 + Extend state endpoint with PoC metadata
    <span class="issues-number">#742</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/IgnatovFedor">@IgnatovFedor</a> opened 2026-02-12 15:06 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-03-25 19:10 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #95b500; color: #24292f; border-color: #95b500;">Priority: Low</span></div>
</div>

<div class="issues-content" markdown="1">
We want the main state endpoint to also expose PoC-related information required by the next vLLM PoC, so that vLLM can rely on a single source of truth.
Also poc v1 should be removed.
</div>

---

> 🔄 **Auto-synced** from [Issue #742](https://github.com/gonka-ai/gonka/issues/742) every hour.
