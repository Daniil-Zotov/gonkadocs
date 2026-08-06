---
title: "#976 — [P0] `devshards`: Distribute `WorkCoins` at the end of the epoch"
source: https://github.com/gonka-ai/gonka/issues/976
issue_number: 976
synced_at: 2026-08-06T00:14:38Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    [P0] `devshards`: Distribute `WorkCoins` at the end of the epoch
    <span class="issues-number">#976</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/dcastro">@dcastro</a> opened 2026-03-30 11:10 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-04-21 23:43 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #a2eeef; color: #24292f; border-color: #a2eeef;">enhancement</span> <span class="issues-label" style="background-color: #aaaaaa; color: #24292f; border-color: #aaaaaa;">devshards</span></div>
</div>

<div class="issues-content" markdown="1">
As described in https://github.com/gonka-ai/gonka/issues/914#issuecomment-4090483233, we want to:

* Distribute `WorkCoins` at the end of the epoch, instead of upon settlement.
* Take `devshards` stats into account when 
    * calculating punishments `WorkCoins`/`RewardCoins` (see `bitcoin_rewards.go`)
    * participant's inactivity status (see `status.go` -> `ComputeStatus`)

</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-04-21 23:42 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Very close logic is implemented and merged in https://github.com/gonka-ai/gonka/pull/1087 &amp; https://github.com/gonka-ai/gonka/pull/1069</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #976](https://github.com/gonka-ai/gonka/issues/976) every hour.
