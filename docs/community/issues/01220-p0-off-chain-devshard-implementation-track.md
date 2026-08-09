---
title: "#1220 — [P0] Off-chain / devshard implementation track"
source: https://github.com/gonka-ai/gonka/issues/1220
issue_number: 1220
synced_at: 2026-08-09T02:33:04Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    [P0] Off-chain / devshard implementation track
    <span class="issues-number">#1220</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-05-21 22:00 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-06-24 00:31 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #4cbc0f; color: #24292f; border-color: #4cbc0f;">up-for-grabs</span> <span class="issues-label" style="background-color: #f86c7a; color: #24292f; border-color: #f86c7a;">Priority: High</span></div>
</div>

<div class="issues-content" markdown="1">
Open for community contributors. Multiple parallel efforts in this direction are welcome to explore different approaches and accelerate progress.
</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/orvionx">@orvionx</a></span>
    <span class="issues-meta-item">commented 2026-06-22 23:37 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi, @tcharchian 
I’d like to work on this issue.</p>
<p>I reviewed the current <code>devshard</code> structure and would like to start with a scoped implementation pass rather than trying to cover the whole off-chain/devshard track at once.</p>
<p>My initial plan is:</p>
<ol>
<li>Review the existing <code>devshard</code> packages and current off-chain flow</li>
<li>Identify the smallest useful vertical slice that can be implemented and tested</li>
<li>Add or improve the missing devshard/off-chain logic</li>
<li>Include tests and documentation updates where needed</li>
<li>Open a focused PR linked to this issue</li>
</ol>
<p>Before I start the implementation, could you confirm whether there is a preferred first milestone or acceptance criteria for this track? If there is no strict preference, I can start by proposing a small PR around the current devshard flow and iterate from maintainer feedback.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/mtvnastya">@mtvnastya</a></span>
    <span class="issues-meta-item">commented 2026-06-23 21:31 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>hi @orvionx, thanks for you interest!</p>
<p>I'd say that these milestones are very broad to assess at this stage.
there are some important differences between inference off-chain logic (devshards) and requirements for training.</p>
<p>specifically, because inference is a very well-defined flow and all devshards are doing exactly the same work all the time. 
decentralized training, on the other hand, is a research direction with a lot of open questions regarding particular low-communication training methods, validation mechanisms etc. and it should allow researchers to run experiments, test these approaches and iterate quickly.</p>
<p>the first iteration of how communication with main net will work is proposed <a href="https://github.com/gonka-ai/gonka/issues/1219">here</a></p>
<p>I'd suggest to start with reviewing that issue and the corresponding PR with trainshard v0 plan and join the discussion from there.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1220](https://github.com/gonka-ai/gonka/issues/1220) every hour.
