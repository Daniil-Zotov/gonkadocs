---
title: "#631 — Add message to transfer amount with vesting"
source: https://github.com/gonka-ai/gonka/issues/631
issue_number: 631
synced_at: 2026-07-10T18:52:09Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Add message to transfer amount with vesting
    <span class="issues-number">#631</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item">[@tcharchian](https://github.com/tcharchian) opened 2026-01-23 23:58 UTC</span>
    <span class="issues-meta-item">4 comments</span>
    <span class="issues-meta-item">Updated 2026-02-10 22:49 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
When the community distributes funds to miners, the transferred tokens should vest over a fixed 180-epoch period, rather than being fully available at the time of transfer.

</div>

---

## 💬 Comments (4)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@AlexeySamosadov](https://github.com/AlexeySamosadov)</span>
    <span class="issues-meta-item">commented 2026-01-24 21:29 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Implemented in PR #641 - adds MsgTransferWithVesting message with 180 epoch default vesting, validation, CLI support, and unit tests.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@tcharchian](https://github.com/tcharchian)</span>
    <span class="issues-meta-item">commented 2026-01-29 23:47 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi @AlexeySamosadov can I kindly ask you to contact me on Discord? <code>tatianacharchian_07833</code></p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@AlexeySamosadov](https://github.com/AlexeySamosadov)</span>
    <span class="issues-meta-item">commented 2026-01-31 15:18 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p><img width="554" height="402" alt="Image" src="https://github.com/user-attachments/assets/51108f38-eff7-45b9-8114-d9e71c754913" /> Hi @tcharchian i texted you in Discord :)</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@AlexeySamosadov](https://github.com/AlexeySamosadov)</span>
    <span class="issues-meta-item">commented 2026-02-08 14:14 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>PR created: https://github.com/gonka-ai/gonka/pull/641</p>
<p>Adds MsgTransferWithVesting for vesting transfers.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #631](https://github.com/gonka-ai/gonka/issues/631) every hour.
