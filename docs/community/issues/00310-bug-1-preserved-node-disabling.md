---
title: "#310 — BUG-1: Preserved node disabling"
source: https://github.com/gonka-ai/gonka/issues/310
issue_number: 310
synced_at: 2026-08-11T04:46:12Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    BUG-1: Preserved node disabling
    <span class="issues-number">#310</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/gmorgachev">@gmorgachev</a> opened 2025-09-01 18:19 UTC</span>
    <span class="issues-meta-item">3 comments</span>
    <span class="issues-meta-item">Updated 2026-02-12 15:34 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span> <span class="issues-label" style="background-color: #4cbc0f; color: #24292f; border-color: #4cbc0f;">up-for-grabs</span></div>
</div>

<div class="issues-content" markdown="1">
# Description

When MLNodes are disabled `POST 9200/admin/v1/nodes/<id>/disable`

MLNodes have to work till next PoC according to schedule:
```
enum TimeslotType {
  PRE_POC_SLOT = 0;
  POC_SLOT = 1;
}
```

Essentially:  
- work till end of current 
- serve inference during next PoC if POC_SLOT is set to true (on-duty nodes)

It supposed that after end of next PoC, all disabled MLNodes will be have weight 0 and not used anymore. 

Currently, the MLNode which was on-duty has the same weight as in previous epoch and scheduled for the next epoch (can be checked in `/v1/epochs/10/participants`).  
At the same time it's not presented in HardwareNodes (can be checked in: `./inferenced query inference hardware-nodes-all`)


</div>

---

## 💬 Comments (3)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-01-28 22:35 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>up-tp-grabs, but needs to be rechecked</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/AlexeySamosadov">@AlexeySamosadov</a></span>
    <span class="issues-meta-item">commented 2026-02-08 14:14 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>PR created: https://github.com/gonka-ai/gonka/pull/682</p>
<p>Skips disabled nodes from governance model population.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/AlexeySamosadov">@AlexeySamosadov</a></span>
    <span class="issues-meta-item">commented 2026-02-12 15:34 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>I have a PR for this: #682 — skips disabled nodes from governance model population. Would appreciate a review when you get a chance.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #310](https://github.com/gonka-ai/gonka/issues/310) every hour.
