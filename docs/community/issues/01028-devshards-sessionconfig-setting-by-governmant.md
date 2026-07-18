---
title: "#1028 — `devshards` `SessionConfig` setting by governmant"
source: https://github.com/gonka-ai/gonka/issues/1028
issue_number: 1028
synced_at: 2026-07-18T09:49:58Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    `devshards` `SessionConfig` setting by governmant
    <span class="issues-number">#1028</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/akup">@akup</a> opened 2026-04-07 18:44 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-06-26 22:40 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #95b500; color: #24292f; border-color: #95b500;">Priority: Low</span></div>
</div>

<div class="issues-content" markdown="1">
Currently devshard `SessionConfig` has a lot of hardcoded values. They should be settable on new escrow start from mainnet, and should be configurable by governance.

For example https://github.com/gonka-ai/gonka/pull/1005 introduces `MaxInferencesPerSubnet` that is also used for checking at `‎inference-chain/x/inference/keeper/subnet_settlement.go` that is breaking single source of truth rule
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/unameisfine">@unameisfine</a></span>
    <span class="issues-meta-item">commented 2026-04-20 16:35 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Starting work on this. PR to follow — threading RefusalTimeout, ExecutionTimeout, and ValidationRate through SubnetEscrowParams -&gt; SubnetEscrow -&gt; subnet SessionConfig, same pattern as TokenPrice. ETA: done.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1028](https://github.com/gonka-ai/gonka/issues/1028) every hour.
