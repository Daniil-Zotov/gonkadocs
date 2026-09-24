---
title: "#1823 — Under PoC challenge load the host accepts inference and returns an empty stream instead of rejecting it"
source: https://github.com/gonka-ai/gonka/issues/1823
issue_number: 1823
synced_at: 2026-09-24T19:16:35Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Under PoC challenge load the host accepts inference and returns an empty stream instead of rejecting it
    <span class="issues-number">#1823</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-09-23 01:05 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-09-23 01:05 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
During the long-running PoC test #1811 by @maria-mitina, a host under challenge load stayed responsive to inference: it confirmed a receipt (`has_receipt=true` on `race_completed`) and then returned an empty stream. The attempt never won the race. Other hosts won with real content, so clients still received answers. The expected behavior is that a host under challenge load rejects the inference and does not take the receipt.

</div>

---

> 🔄 **Auto-synced** from [Issue #1823](https://github.com/gonka-ai/gonka/issues/1823) every hour.
