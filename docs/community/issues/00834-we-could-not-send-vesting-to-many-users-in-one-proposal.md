---
title: "#834 — We could not send vesting to many users in one proposal"
source: https://github.com/gonka-ai/gonka/issues/834
issue_number: 834
synced_at: 2026-07-18T13:54:54Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    We could not send vesting to many users in one proposal
    <span class="issues-number">#834</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/huxuxuya">@huxuxuya</a> opened 2026-03-01 22:24 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-03-12 20:29 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
  **Problem**
  We had only single-recipient vesting transfer.
  So if we needed to vest tokens to many addresses, we had to add many separate messages
  into one governance proposal.

  **Main limitation**
  Governance proposals have practical size/count limits.
  With many recipients, the proposal became too large (too many messages), and
  distribution could not be done in one clean operation.

  **Why we solved it**
  We needed a simple way to send vesting to many addresses at once, in one proposal, to
  avoid splitting into multiple proposals and reduce operational risk.

  **Target result**
  Add one batch vesting message so one proposal can include many recipients and execute
  the distribution in a single run.

Assign this task to me plz.
</div>

---

> 🔄 **Auto-synced** from [Issue #834](https://github.com/gonka-ai/gonka/issues/834) every hour.
