---
title: "#2231 — Multi-Model Scheduling"
source: https://github.com/gonka-ai/gonka/issues/2231
issue_number: 2231
synced_at: 2026-11-13T01:12:12Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Multi-Model Scheduling
    <span class="issues-number">#2231</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-11-06 01:18 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-11-06 11:58 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Improvement of the economic model for how multi-model support works  
Each model will likely have a quota, dynamically determined by demand.
Consider community review in upgrdae 0.2.12, including: https://github.com/gonka-ai/gonka/pull/948#issuecomment-4256362213

https://github.com/gonka-ai/gonka/blob/e9b6e47d97cfbc6e7d3777dcc3726faf9e8f5f7f/proposals/multi-model-scheduling/README.md
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/zpoken">@zpoken</a></span>
    <span class="issues-meta-item">commented 2026-11-06 11:58 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>I suggest revisiting the design first:</p>
<ul>
<li><strong>Layer 2 targets a deprecated field.</strong> <code>weight_scale_factor</code> is null on mainnet. The GIP needs to say whether it replaces or extends the v0.2.16 controller, including bounds, dilution and snapshots.</li>
<li><strong>The agent's EV isn't protocol income.</strong> §3.2 uses a per-model pot, but reward coins follow overall weight. In epoch 444, on 24 of 26 hosts, work coins were ~65 GNK against ~147k GNK of rewards.</li>
<li><strong>The bootstrap subsidy doesn't work as specified.</strong> Zero paid value gives zero EV at any coefficient, and a higher learning ceiling doesn't raise <code>base × demand_factor</code> under neutral demand.</li>
<li><strong>Demand manipulation is unresolved.</strong> Under the proposed bands, bought traffic could move DeepSeek from 17.6% to 46.1% of reward weight in the current snapshot (~74k GNK/epoch gross). This is a conditional calculation.</li>
<li><strong>Overloading INTENT is risky.</strong> It clears a stored delegation, so an unfulfilled announcement can lead to the 15% reward-only penalty. Intent state also has no epoch or quantity and is cleared each epoch, so the announcement history doesn't exist as described.</li>
<li><strong>The simulations don't validate this.</strong> They omit block rewards, penalties and eligibility, and bluffs never enter other agents' predictions. When bluffs are modeled, 80% liars drop served demand from 0.932 to 0.697 even with the 5-epoch cooldown. Random 10% staggering with no announcements served 0.936 in the same toy model.</li>
</ul>
<p>Spec fixes also needed: the two-block switch window in §3.7, the clamp vs. zero coefficient on retirement, late devshard settlement in demand accounting, auto-deprecation of LEARNING models, and an x/group path for parameter tuning. The issue (#2231) also still links the May 6 revision.</p>
<p>Suggested direction: specify Layer 2 as a change to the existing controller, have the agent optimize real income including penalties and eligibility, test random staggering instead of reusing INTENT, and keep retirement governance-reviewed. Automatic demand-driven targets need their own manipulation analysis first.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2231](https://github.com/gonka-ai/gonka/issues/2231) every hour.
