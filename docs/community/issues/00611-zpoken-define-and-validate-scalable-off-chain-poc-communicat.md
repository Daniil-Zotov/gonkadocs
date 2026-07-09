---
title: "#611 — [zpoken] Define and validate scalable off-chain PoC communication beyond Merkle-based commits"
source: https://github.com/gonka-ai/gonka/issues/611
issue_number: 611
synced_at: 2026-07-09T21:51:17Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    [zpoken] Define and validate scalable off-chain PoC communication beyond Merkle-based commits
    <span class="issues-number">#611</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item">[@tcharchian](https://github.com/tcharchian) opened 2026-01-20 21:32 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-04-23 01:38 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
**Problem**
The Merkle tree–based off-chain PoC commit approach is already being implemented as an urgent, short-term solution. 

- https://github.com/gonka-ai/gonka/blob/dl/v0.2.8-poc-v2-offchain/proposals/poc-v2/poc-v2-offchain.md
- https://github.com/gonka-ai/gonka/blob/gm/poc-offchain/proposals/poc/offchain.md

However, it is understood that this approach does not scale to large participant counts on its own.

Because of this, a second approach https://zpoken.notion.site/Andrii-2ea9506ab1488027b6d5e72df66d8654 is proposed as a scalability solution

**Goal**
Formally define, evaluate, and validate the Mesh / Turbine-based off-chain PoC communication approach as the scalable solution, given that Merkle-based commits are already accepted as a non-scalable but necessary interim step.

</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@akup](https://github.com/akup)</span>
    <span class="issues-meta-item">commented 2026-01-23 11:21 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Why gossip is just overlooked?</p>
<p>While it will have more latency (this 100ms are neglectable compared to block finalization time), it consumes much less resources and bandwidth.
In article, in comparison it is stated that gossip needs 12 connections, while turbine tree 32 connections.
But to have good protection against nodes control attack, we need to have up to 8 trees, and this is 256 connections, that is 20 times more then gossip.
This multiple connections even with Solomon-reed (additional encoding/decoding resources) will increase bandwidth consumption as well.
Moreover gossip is more adaptive and selfheeling and always will find the route.</p>
<p>I think this points should be taken into account on protocol selection</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #611](https://github.com/gonka-ai/gonka/issues/611) every hour.
