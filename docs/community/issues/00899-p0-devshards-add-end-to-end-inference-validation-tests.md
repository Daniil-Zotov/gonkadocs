---
title: "#899 — [P0] `devshards`: Add end-to-end inference validation tests"
source: https://github.com/gonka-ai/gonka/issues/899
issue_number: 899
synced_at: 2026-07-19T22:13:11Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    [P0] `devshards`: Add end-to-end inference validation tests
    <span class="issues-number">#899</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/heitor-lassarote">@heitor-lassarote</a> opened 2026-03-16 18:50 UTC</span>
    <span class="issues-meta-item">3 comments</span>
    <span class="issues-meta-item">Updated 2026-04-07 16:10 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #f86c7a; color: #24292f; border-color: #f86c7a;">Priority: High</span> <span class="issues-label" style="background-color: #aaaaaa; color: #24292f; border-color: #aaaaaa;">devshards</span></div>
</div>

<div class="issues-content" markdown="1">
We should write testermint tests to ensure that inference validations in `devshards` work as expected. Such tests already exist for mainnet, but we should reimplement them according to the `devshards` design and implementation.
</div>

---

## 💬 Comments (3)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/heitor-lassarote">@heitor-lassarote</a></span>
    <span class="issues-meta-item">commented 2026-03-19 17:46 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Note: I took a little detour from this task to see if I can make the development loop with testermint a bit quicker, by writing a small REPL to interact with the <code>devshard</code>.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/KKizilov">@KKizilov</a></span>
    <span class="issues-meta-item">commented 2026-03-26 15:14 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Will be done by March 27th.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/heitor-lassarote">@heitor-lassarote</a></span>
    <span class="issues-meta-item">commented 2026-03-26 15:31 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>I've written a couple of Testermint tests and added an endpoint to get the inference from the proxy server.</p>
<p>Recently I've been trying to see about changing the session configuration for tests. Although not sure yet if that's the best path forward.</p>
<p>I expect to push a PR with these tests very soon.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #899](https://github.com/gonka-ai/gonka/issues/899) every hour.
