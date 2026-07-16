---
title: "#924 — [P0] Make sure Bitfury community sale works: IBC"
source: https://github.com/gonka-ai/gonka/issues/924
issue_number: 924
synced_at: 2026-07-16T20:15:02Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    [P0] Make sure Bitfury community sale works: IBC
    <span class="issues-number">#924</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item">[@tcharchian](https://github.com/tcharchian) opened 2026-03-20 23:20 UTC</span>
    <span class="issues-meta-item">3 comments</span>
    <span class="issues-meta-item">Updated 2026-04-11 04:34 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #f86c7a; color: #24292f; border-color: #f86c7a;">Priority: High</span></div>
</div>

<div class="issues-content" markdown="1">
*(empty)*
</div>

---

## 💬 Comments (3)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@tcharchian](https://github.com/tcharchian)</span>
    <span class="issues-meta-item">commented 2026-03-20 23:21 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@maria-mitina said that Community Sale contract tested with IBC, worked well.
@GLiberman @0xgonka do we have other scenarios to try?</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@maria-mitina](https://github.com/maria-mitina)</span>
    <span class="issues-meta-item">commented 2026-03-25 09:11 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>it will be great to confirm/decide whether bridge is needed for the Bitfury scenario.
If yes, we will work this scenario out and test.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@maria-mitina](https://github.com/maria-mitina)</span>
    <span class="issues-meta-item">commented 2026-03-25 17:15 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@mtvnastya and I had a discussion about it, and bridge is needed for the Bitfury contract. We need to fix the hardcoded chainId and rebuild the binary. Happy to test after that 
@GLiberman - any chance you could update us on the bridge fix? </p>
<p>FYI, @tcharchian </p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #924](https://github.com/gonka-ai/gonka/issues/924) every hour.
