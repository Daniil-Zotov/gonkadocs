---
title: "#744 — [P1] Don’t require developers to register as Participants to run inference"
source: https://github.com/gonka-ai/gonka/issues/744
issue_number: 744
synced_at: 2026-08-10T22:02:34Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    [P1] Don’t require developers to register as Participants to run inference
    <span class="issues-number">#744</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-02-13 01:16 UTC</span>
    <span class="issues-meta-item">4 comments</span>
    <span class="issues-meta-item">Updated 2026-03-30 23:52 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Currently, the chain requires a Participant record not only to host, but also to send inference requests. There is no real reason for this, since the public key is available in the Account record after the first on-chain transaction signed by that account is executed. That should be sufficient.

- [ ] Remove the requirement to create a Participant record.
- [ ] Fix `/v1/participants/gonka...` to query Participant data, not just the Account (as it does now).
- [ ] Determine how to preserve per-developer statistics in this case.
- [ ] Update the documentation accordingly.
</div>

---

## 💬 Comments (4)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-02-13 01:19 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@x0152, would you like to work on this issue?</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/x0152">@x0152</a></span>
    <span class="issues-meta-item">commented 2026-02-13 06:15 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>I'll take it</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/gmorgachev">@gmorgachev</a></span>
    <span class="issues-meta-item">commented 2026-03-11 20:03 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@tcharchian the PR itself is marked for milestone 0.2.11. what is valid?</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-03-11 20:23 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <blockquote>
<p><a href="https://github.com/tcharchian">@tcharchian</a> the PR itself is marked for milestone 0.2.11. what is valid?</p>
</blockquote>
<p>Per @patimen, let's move it to v0.2.12. https://github.com/gonka-ai/gonka/pull/750#issuecomment-3938311002
cc: @x0152  </p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #744](https://github.com/gonka-ai/gonka/issues/744) every hour.
