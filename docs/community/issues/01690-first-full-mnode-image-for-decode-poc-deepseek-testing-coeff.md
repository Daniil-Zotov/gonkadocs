---
title: "#1690 — First full MNode image for Decode PoC (DeepSeek): testing + coefficients"
source: https://github.com/gonka-ai/gonka/issues/1690
issue_number: 1690
synced_at: 2026-09-07T00:01:34Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    First full MNode image for Decode PoC (DeepSeek): testing + coefficients
    <span class="issues-number">#1690</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-08-31 20:21 UTC</span>
    <span class="issues-meta-item">3 comments</span>
    <span class="issues-meta-item">Updated 2026-09-04 23:33 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Decode PoC thresholds and expert seeding for DeepSeek. DeepSeek seeding is more complex than MiniMax; the scheme needs a fix before coefficients alone are useful.
Kimi Decode PoC thresholds stay on hold (unclear future of Kimi on this path).
MiniMax image verification of the current implementation is #1689. Integration / design questions are #1688.
Confirm the live on-chain id from poc_params.models if it has drifted. Target: deepseek-ai/DeepSeek-V4-Flash-0731.

**Process**
— Experiments completed and written up (hardware, models, what passed, what did not)
— Seeding scheme for DeepSeek is described (how it differs from MiniMax)
— Scheme fix is written up before threshold collection is treated as done
— If work is DeepSeek-only: notes before handover, stating that Kimi is out of scope

**Expert seeding (DeepSeek)**
— Current seeding scheme is documented
— Why MiniMax seeding is not sufficient for DeepSeek is written up
— Scheme is fixed or a concrete proposal is on this issue
— Weight distribution across seeded experts is measured
— Closer-to-uniform weights across seeded experts are shown, with notes if uniform is not possible

**Thresholds (DeepSeek)**
— Decode PoC thresholds for DeepSeek are collected after the seeding scheme is stable
— How thresholds were measured is written up (hardware, setup, logs / notebooks)
— Thresholds are not treated as acceptance of a MiniMax-style full image — that bar is #1689

**Kimi**
— Kimi Decode PoC thresholds are explicitly out of scope on this issue (on hold)

**Handover**
- [ ] Seeding scheme notes published
- [ ] DeepSeek thresholds published, or listed as blocked on the scheme fix

</div>

---

## 💬 Comments (3)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/baychak">@baychak</a></span>
    <span class="issues-meta-item">commented 2026-08-31 20:26 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>TY!</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/clanster">@clanster</a></span>
    <span class="issues-meta-item">commented 2026-08-31 20:27 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>ty</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/baychak">@baychak</a></span>
    <span class="issues-meta-item">commented 2026-09-04 23:19 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p><strong>Dependency:</strong> not blocked by <a href="https://github.com/gonka-ai/gonka/issues/1688">#1688</a>. @tcharchian — for the ordering.</p>
<ul>
<li>The DeepSeek seeding scheme lives on this issue. <a href="https://github.com/gonka-ai/gonka/issues/1688">#1688</a> says so: <code>the scheme fix itself is #1690</code>.</li>
<li>Blocking this issue on it would be circular: <a href="https://github.com/gonka-ai/gonka/issues/1689">#1689</a> waits on the algorithm freeze, and that freeze includes this scheme.</li>
<li>The work is not blocked; publishing the numbers is. The scheme change for the hash-routed layers (pseudo token ids for the seeded decode steps, natural gate logits on those layers) and the tau-grid thresholds on vLLM 0.25.1 are measured on our forks.</li>
<li>Thresholds are posted here after the scheme note is written and the constants are signed off. They are consensus parameters, and we do not publish them before they are on chain.</li>
</ul>
<p>Ordering inside this issue is unchanged: thresholds count as done only after the seeding scheme is fixed and written up.</p>
<p><strong>Next:</strong> scheme note for the hash-routed layers, on this issue by 2026-09-08. Status update every Monday, next 2026-09-07.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1690](https://github.com/gonka-ai/gonka/issues/1690) every hour.
