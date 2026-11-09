---
title: "#2234 — Maintenance window: Review & activation"
source: https://github.com/gonka-ai/gonka/issues/2234
issue_number: 2234
synced_at: 2026-11-09T08:06:26Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Maintenance window: Review & activation
    <span class="issues-number">#2234</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-11-06 06:14 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-11-06 22:45 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #c2e0c6; color: #24292f; border-color: #c2e0c6;">Priority: Low</span></div>
</div>

<div class="issues-content" markdown="1">
*(empty)*
</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/cyberdelamain">@cyberdelamain</a></span>
    <span class="issues-meta-item">commented 2026-11-06 22:24 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <h1>1850 is relevant here. With current params the confirmation PoC trigger comes 281 blocks before evaluation, and the schedule lead is only 100 blocks, so a host that sees the trigger can still put a 1-block window on the evaluation block and be skipped by it. The PR rejects any window that covers an in-progress evaluation.</h1>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/maksimenkoff">@maksimenkoff</a></span>
    <span class="issues-meta-item">commented 2026-11-06 22:45 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>One thing to fix first, in ClaimRewards: a window touching an epoch at all (a single block at its end is enough) currently skips the missed-validation check for the entire epoch. Once claim_validation_enabled is on as well, default credit params let a host validate in just 1 epoch out of 21. My PR #2212 limits the waiver to inferences created inside the window.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2234](https://github.com/gonka-ai/gonka/issues/2234) every hour.
