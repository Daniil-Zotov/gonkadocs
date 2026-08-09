---
title: "#1219 — [P0] Basic primitives for training"
source: https://github.com/gonka-ai/gonka/issues/1219
issue_number: 1219
synced_at: 2026-08-09T11:49:28Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    [P0] Basic primitives for training
    <span class="issues-number">#1219</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-05-21 21:56 UTC</span>
    <span class="issues-meta-item">6 comments</span>
    <span class="issues-meta-item">Updated 2026-07-29 18:02 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #f86c7a; color: #24292f; border-color: #f86c7a;">Priority: High</span></div>
</div>

<div class="issues-content" markdown="1">
The framing is simple: you can prepare any container, it will run across different GPUs in the network, a protocol layer will coordinate interaction between nodes, they will perform training, and then use a protocol-level voting mechanism to determine which participants behaved correctly.

We intentionally ignore the automatic redeployment problem for now. 
This should be a small-scoped task on mainnet.
Put together a lightweight training flow without the heavy logic we have in devshards
</div>

---

## 💬 Comments (6)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/x0152">@x0152</a></span>
    <span class="issues-meta-item">commented 2026-06-23 19:38 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Here's the draft plan and draft of the first-stage PR:</p>
<p>Plan (draft): https://docs.google.com/document/d/1LLZngQ7VoIL3DVT8St40XLE8HcRcxyNXZueyzoQfWuE/edit?usp=sharing
PR (stage 1): #1350 </p>
<p>Any help is welcome, from shaping the plan to implementation and reviews</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/orvionx">@orvionx</a></span>
    <span class="issues-meta-item">commented 2026-06-23 21:44 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi @mtvnastya , I’d like to help with this if there is still an open sub-scope.</p>
<p>My understanding is that this should be a lightweight mainnet training primitive, not a full devshards port: define/register a training workload, dispatch it to ML nodes, track basic execution state/result metadata, and leave redeployment/heavy orchestration out of scope.</p>
<p>I can start with a small PR around the training task/request model + API flow + minimal tests, then follow up with ML-node execution hooks if that direction works.</p>
<p>Could you confirm which part you’d prefer contributors to start with?</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/x0152">@x0152</a></span>
    <span class="issues-meta-item">commented 2026-06-24 22:54 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi @orvionx, I've already started working on this and opened a draft PR for the first stage: #1350. There's also a draft plan here: https://docs.google.com/document/d/1LLZngQ7VoIL3DVT8St40XLE8HcRcxyNXZueyzoQfWuE/edit?tab=t.0</p>
<p>I'd be happy if you could join. Could you take a look at the plan and share your thoughts? Stage 2 can be implemented in parallel with stage 1</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/orvionx">@orvionx</a></span>
    <span class="issues-meta-item">commented 2026-06-24 23:03 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi @x0152 Thanks for the mention — I’d be happy to join and help with this.</p>
<p>I reviewed the Stage 1 direction from PR #1350. My understanding is that Stage 1 mainly covers the on-chain reservation/release lifecycle, while Stage 2 can focus more on the actual training execution layer and coordination flow between reserved nodes.</p>
<p>My initial thoughts:</p>
<ul>
<li>Stage 2 should be kept clearly separated from Stage 1 by relying on stable interfaces/events from the reservation lifecycle.</li>
<li>It would be useful to define the exact state machine for a training run: reserved → container prepared → training started → progress/heartbeat → result submitted → validation/voting → settled/released.</li>
<li>I think we should pay special attention to failure handling: node timeout, container startup failure, partial participant failure, researcher cancellation, and result mismatch.</li>
<li>For parallel development, I can work against mocked Stage 1 events/interfaces first, then wire it to the real chain implementation after Stage 1 stabilizes.</li>
<li>I can also help with tests around edge cases and documentation for how hosts/researchers should use the flow.</li>
</ul>
<p>I’ll continue reviewing the plan in more detail, but overall I agree that Stage 2 looks suitable to implement in parallel with Stage 1 if the interface boundary is defined clearly.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/x0152">@x0152</a></span>
    <span class="issues-meta-item">commented 2026-07-21 20:49 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi @orvionx ! Just checking in - how are you doing? Were you able to make any progress on this?</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/orvionx">@orvionx</a></span>
    <span class="issues-meta-item">commented 2026-07-21 23:07 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@x0152 Hi, I didn't make any progress yet</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1219](https://github.com/gonka-ai/gonka/issues/1219) every hour.
