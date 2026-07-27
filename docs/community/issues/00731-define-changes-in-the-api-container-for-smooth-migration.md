---
title: "#731 — Define changes in the API container for smooth migration"
source: https://github.com/gonka-ai/gonka/issues/731
issue_number: 731
synced_at: 2026-07-27T17:14:09Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Define changes in the API container for smooth migration
    <span class="issues-number">#731</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-02-11 01:28 UTC</span>
    <span class="issues-meta-item">3 comments</span>
    <span class="issues-meta-item">Updated 2026-03-11 19:54 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
*(empty)*
</div>

---

## 💬 Comments (3)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tamazgadaev">@tamazgadaev</a></span>
    <span class="issues-meta-item">commented 2026-03-02 01:18 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <ul>
<li>Fix the 400/422 issue in API container</li>
<li>Adjust thresholds a little bit (onchain, not API)</li>
<li>Do one of the two: a) ignore -9999 logprobs in validation b) enforce top_p and top_k in requests (a) preferred)</li>
</ul>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tamazgadaev">@tamazgadaev</a></span>
    <span class="issues-meta-item">commented 2026-03-03 03:06 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Actually, we don't strictly need any of these 3 for smooth migration. 1 is desirable, 2 nice to have (and we'll get the threshold values), 3 is not needed</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/gmorgachev">@gmorgachev</a></span>
    <span class="issues-meta-item">commented 2026-03-11 19:54 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>i think we need to close this one. fix 400/422 is independent bug to fix</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #731](https://github.com/gonka-ai/gonka/issues/731) every hour.
