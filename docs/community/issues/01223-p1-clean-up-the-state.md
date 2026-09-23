---
title: "#1223 — [P1] Clean up the state"
source: https://github.com/gonka-ai/gonka/issues/1223
issue_number: 1223
synced_at: 2026-09-23T00:41:17Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    [P1] Clean up the state
    <span class="issues-number">#1223</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-05-21 22:34 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-09-17 06:52 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #12a6e8; color: #24292f; border-color: #12a6e8;">Priority: Medium</span></div>
</div>

<div class="issues-content" markdown="1">
Review what’s currently stored, identify any leftovers, and remove them.
</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Ryanchen911">@Ryanchen911</a></span>
    <span class="issues-meta-item">commented 2026-05-28 02:09 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>hi @tcharchian ,I will take this one, thank you!</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Ryanchen911">@Ryanchen911</a></span>
    <span class="issues-meta-item">commented 2026-09-17 06:52 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Developer-stats scope is now resolved: the pre-devshard <code>DeveloperStatsByTime</code>, <code>DeveloperStatsByEpoch</code>, embedded <code>InferenceStats</code>, and supporting <code>stats/...</code> indexes do not need to be retained. They must be removed gradually rather than from an upgrade handler.</p>
<p>I opened #1793 for that cleanup. It sweeps all four prefixes (~10.4 GiB / ~34.7M keys in the measured snapshot) with a shared 1,000-key per-block budget, while limiting the large <code>DeveloperStatsByEpoch</code> aggregate values to one deletion per block. It also reclaims stale by-model entries that cannot be reached through the other indexes.</p>
<p>Current split and merge order:
- #1773: generic pruner correctness fixes
- #1499: gradual <code>InferenceValidationDetails</code> cleanup (~4 GiB), stacked on #1773
- #1793: gradual legacy developer-stats cleanup (~10.4 GiB), stacked on #1499
- #1287: independent v0.2.16 bounded legacy cleanup + state analysis tooling</p>
<p>Relevant keeper/types/upgrade tests pass locally.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1223](https://github.com/gonka-ai/gonka/issues/1223) every hour.
