---
title: "#977 — [P0] `devshards`: Limit amount of inferences"
source: https://github.com/gonka-ai/gonka/issues/977
issue_number: 977
synced_at: 2026-07-21T09:44:53Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    [P0] `devshards`: Limit amount of inferences
    <span class="issues-number">#977</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/dcastro">@dcastro</a> opened 2026-03-30 11:17 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-06-01 22:04 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #a2eeef; color: #24292f; border-color: #a2eeef;">enhancement</span> <span class="issues-label" style="background-color: #aaaaaa; color: #24292f; border-color: #aaaaaa;">devshards</span></div>
</div>

<div class="issues-content" markdown="1">
As described in https://github.com/gonka-ai/gonka/issues/914#issuecomment-4090483233, we want to limit the amount of inferences that can be done in a `devshard`, as a way of limiting the amount of damage a hijacked `devshard` can cause on the network.

For now, let's say each `devshard` can run up to 2k inferences.

Upon settlement, the protocol should verify "Missed inferences + Invalidated inferences" does not exceed 2k, for the whole group.

</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/a-kuprin">@a-kuprin</a></span>
    <span class="issues-meta-item">commented 2026-05-26 21:49 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>At 0.2.13 nonce limit was introduced. Inference count could be limited by nonces limit and there is no need in extra parameter.
Handling on devshard side is implemented at https://github.com/gonka-ai/gonka/pull/1258 </p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #977](https://github.com/gonka-ai/gonka/issues/977) every hour.
