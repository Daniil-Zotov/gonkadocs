---
title: "#706 — Inference Slot Hogging"
source: https://github.com/gonka-ai/gonka/issues/706
issue_number: 706
synced_at: 2026-08-01T15:33:55Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Inference Slot Hogging
    <span class="issues-number">#706</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/huxuxuya">@huxuxuya</a> opened 2026-02-05 18:52 UTC</span>
    <span class="issues-meta-item">4 comments</span>
    <span class="issues-meta-item">Updated 2026-03-02 12:27 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
**Vulnerability:** Inference Slot Hogging
**Severity:** Medium 
**Component:** model_assignment.go

### Description
The system always picks the node with the smallest weight for the "safe" inference slot. If a validator has multiple nodes, the same small node will keep getting the safe slot every single epoch, avoiding PoC verification indefinitely.

### The Problem
Verification Avoidance: The smallest node is never checked because it stays in the safe slot.
Guaranteed Rewards: This node earns rewards every epoch without risk, while the other nodes of the same validator are always forced to undergo PoC checks.

### Example
Validator has: Node A (weight 10) and Node B (weight 20).

Epoch 1: Node A is smallest -> Safe Slot.
Epoch 2: Node A is smallest -> Safe Slot.
Result: Node A never performs PoC, but always gets paid.

### Fix
A mandatory rotation. If a node was in the safe slot in the previous epoch, it is moved to the end of the queue for the next epoch. This forces the validator's other nodes to take turns in the safe slot and undergo verification.
</div>

---

## 💬 Comments (4)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/AlexeySamosadov">@AlexeySamosadov</a></span>
    <span class="issues-meta-item">commented 2026-02-08 14:13 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>PR created: https://github.com/gonka-ai/gonka/pull/718</p>
<p>Implements rotation logic to prevent the same node from always getting the safe inference slot.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/AlexeySamosadov">@AlexeySamosadov</a></span>
    <span class="issues-meta-item">commented 2026-02-12 15:26 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>I have a PR for this: #718 — implements deterministic rotation for PoC slot allocation to prevent hogging. Would appreciate a review when you get a chance.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/huxuxuya">@huxuxuya</a></span>
    <span class="issues-meta-item">commented 2026-02-24 19:31 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>This task was created in parallel with this PR #707</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/huxuxuya">@huxuxuya</a></span>
    <span class="issues-meta-item">commented 2026-03-02 12:27 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Assign to me plz. Task already done.</p>
<h1>707</h1>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #706](https://github.com/gonka-ai/gonka/issues/706) every hour.
