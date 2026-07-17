---
title: "#772 — Slashed coins should not be burned"
source: https://github.com/gonka-ai/gonka/issues/772
issue_number: 772
synced_at: 2026-07-17T16:37:49Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Slashed coins should not be burned
    <span class="issues-number">#772</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-02-18 01:36 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-03-12 18:09 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Currently, slashed coins are burned.
This behavior should be changed.

Instead of burning slashed funds, they must be redirected to the Governance module account, consistent with how we handle rewards that are withheld from miners during penalties.

Expected behavior:

- [ ] Slashed coins must not be burned.
- [ ] Slashed coins must be transferred to the Governance module account.
- [ ] Implementation should reuse or mirror the existing logic that handles redistribution of miner rewards that are not paid out due to penalties
</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/x0152">@x0152</a></span>
    <span class="issues-meta-item">commented 2026-02-18 09:23 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <h1>775</h1>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/gmorgachev">@gmorgachev</a></span>
    <span class="issues-meta-item">commented 2026-02-26 18:29 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@patimen </p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #772](https://github.com/gonka-ai/gonka/issues/772) every hour.
