---
title: "#935 — [P0] `devshards` fees"
source: https://github.com/gonka-ai/gonka/issues/935
issue_number: 935
synced_at: 2026-08-07T09:19:41Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    [P0] `devshards` fees
    <span class="issues-number">#935</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/dcastro">@dcastro</a> opened 2026-03-23 11:12 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-04-29 21:44 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #f86c7a; color: #24292f; border-color: #f86c7a;">Priority: High</span> <span class="issues-label" style="background-color: #aaaaaa; color: #24292f; border-color: #aaaaaa;">devshards</span></div>
</div>

<div class="issues-content" markdown="1">
Context: https://github.com/gonka-ai/gonka/issues/914#issuecomment-4090483233

* Calculate and charge fee for `devshards`
    * Initial impl: create_fee + max_nonce * fee_per_nonce
        * Reasoning: charging per nonce acts as a mechanism to deter from spamming the network with small inference requests
    * Ensure escrow amount covers the fee
    * Ensure the escrow balance never goes below the fee
    * Charge the fee upon settlement


</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/KKizilov">@KKizilov</a></span>
    <span class="issues-meta-item">commented 2026-03-26 15:06 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <blockquote>
<p>Calculate and charge fee for subnets
 Will be done by March 29th.</p>
</blockquote>
<p>All the remaining items will be done by April 5th</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #935](https://github.com/gonka-ai/gonka/issues/935) every hour.
