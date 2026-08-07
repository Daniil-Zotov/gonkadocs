---
title: "#893 — [P0] Remove float math from `devshards` consensus"
source: https://github.com/gonka-ai/gonka/issues/893
issue_number: 893
synced_at: 2026-08-07T04:05:34Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    [P0] Remove float math from `devshards` consensus
    <span class="issues-number">#893</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/Brgndy25">@Brgndy25</a> opened 2026-03-16 13:52 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-04-29 21:44 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #f86c7a; color: #24292f; border-color: #f86c7a;">Priority: High</span> <span class="issues-label" style="background-color: #aaaaaa; color: #24292f; border-color: #aaaaaa;">devshards</span></div>
</div>

<div class="issues-content" markdown="1">
DeterministicFloat, ShouldValidate, and penalizeUnrevealedSeeds use float64 and math.Ceil. 

Floating-point arithmetic is not deterministicacross architectures and can produce different results on different
machines, which can lead to state root divergence and consensus splits.

</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/KKizilov">@KKizilov</a></span>
    <span class="issues-meta-item">commented 2026-03-26 15:17 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Will be done by March 27th. </p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #893](https://github.com/gonka-ai/gonka/issues/893) every hour.
