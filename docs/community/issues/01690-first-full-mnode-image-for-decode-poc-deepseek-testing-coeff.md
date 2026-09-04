---
title: "#1690 — First full MNode image for Decode PoC (DeepSeek): testing + coefficients"
source: https://github.com/gonka-ai/gonka/issues/1690
issue_number: 1690
synced_at: 2026-09-04T14:24:40Z
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
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-09-03 05:17 UTC</span>
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

## 💬 Comments (2)

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

---

> 🔄 **Auto-synced** from [Issue #1690](https://github.com/gonka-ai/gonka/issues/1690) every hour.
