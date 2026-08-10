---
title: "#896 — `devshards`: Research aggregated BLS signatures"
source: https://github.com/gonka-ai/gonka/issues/896
issue_number: 896
synced_at: 2026-08-10T22:02:12Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    `devshards`: Research aggregated BLS signatures
    <span class="issues-number">#896</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/heitor-lassarote">@heitor-lassarote</a> opened 2026-03-16 15:10 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-04-29 21:30 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #95b500; color: #24292f; border-color: #95b500;">Priority: Low</span> <span class="issues-label" style="background-color: #aaaaaa; color: #24292f; border-color: #aaaaaa;">devshards</span></div>
</div>

<div class="issues-content" markdown="1">
Currently, the design for `devshards` requests a list of all hosts signatures for the settlement transaction. To reduce the transaction size, we'd like to investigate and implement an aggregated BLS signature (plus a bitset for which hosts signed).

To achieve this, one solution is to register the BLS `devshard` public key for each participant in the mainnet.

# Research

* [Applicability of Aggregated BLS Signatures](https://serokell.notion.site/Applicability-of-Aggregated-BLS-Signatures-31a6c9c166b380b49068d5574277dfd8)
</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/KKizilov">@KKizilov</a></span>
    <span class="issues-meta-item">commented 2026-03-26 15:16 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Will be done fast after finishing #913 </p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-04-29 21:15 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>postpone review after Upgrade v0.x.x-devshard2</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #896](https://github.com/gonka-ai/gonka/issues/896) every hour.
