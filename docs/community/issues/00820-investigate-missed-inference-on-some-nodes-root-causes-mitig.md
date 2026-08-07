---
title: "#820 — Investigate missed inference on some nodes (root causes + mitigation)"
source: https://github.com/gonka-ai/gonka/issues/820
issue_number: 820
synced_at: 2026-08-07T20:04:42Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Investigate missed inference on some nodes (root causes + mitigation)
    <span class="issues-number">#820</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-02-27 21:13 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-03-06 14:25 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span> <span class="issues-label" style="background-color: #008672; color: #ffffff; border-color: #008672;">help wanted</span> <span class="issues-label" style="background-color: #4cbc0f; color: #24292f; border-color: #4cbc0f;">up-for-grabs</span> <span class="issues-label" style="background-color: #f86c7a; color: #24292f; border-color: #f86c7a;">Priority: High</span></div>
</div>

<div class="issues-content" markdown="1">

### Discussed in https://github.com/gonka-ai/gonka/discussions/817

<div type='discussions-op-text'>

<sup>Originally posted by **tcharchian** February 27, 2026</sup>

Task: Some nodes experience missed inference events. Likely multi-cause, needs community participation.
</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/AlexeySamosadov">@AlexeySamosadov</a></span>
    <span class="issues-meta-item">commented 2026-03-03 10:27 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>PR: https://github.com/gonka-ai/gonka/pull/843</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Mayveskii">@Mayveskii</a></span>
    <span class="issues-meta-item">commented 2026-03-06 14:25 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Measured data from live network may help narrow root causes here.</p>
<p>Epochs 161–191, 2,503,595 inferences:
Miss rate: 3.25% (81,360 misses)
Completion rate: mean 90.4%, σ=7.4%, range 72–99%</p>
<p>The σ=7.4% variance is the signal — not the mean.
Some nodes miss 28% of assigned inferences while others miss 1%.
GetRandomExecutor routes to both equally regardless.</p>
<p>Phase 4 of GiP #860 proposes GetQualityWeightedExecutor — routes traffic 
proportional to L9 completion rate. Projection: σ ↓40% as high-miss nodes 
receive less traffic and face economic incentive to improve.</p>
<p>Design + data: docs/specs/inference-quality-protocol.md (PR #859 branch)
Discussion: #860 </p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #820](https://github.com/gonka-ai/gonka/issues/820) every hour.
