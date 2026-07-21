---
title: "#381 — [P0] How to change `inference_url`"
source: https://github.com/gonka-ai/gonka/issues/381
issue_number: 381
synced_at: 2026-07-21T18:46:56Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    [P0] How to change `inference_url`
    <span class="issues-number">#381</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2025-09-30 16:43 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2025-12-08 21:16 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
1. Change `inference_url`. Probably, it should happen immediately and propagate everywhere.
2. Vefigy `inference_url`. Let's think on how can it be verified, at least asynchronousl,y whena  node with that URL is already running
Example: `api` container has a new endpoint /v1/verify, which returns:
```
{
    "requester_address": "gonka...",
    "timestamps": <timestamp in last Xmin>,
    "signature": <singature of timestamps by this node's warm key>
}
```
The signature should not be refreshed more than once within X minutes.
Such an endpoint should be enough to have voting for claiming the wrong address. Ideally, every `api` node should verify all `inference_url` once in an epoch automatically and initiate this voting, but it's hard to estimate it for now, it might be okay to leave it manual at the moment.
3. Add a check that a new participant can't be created if there is the same URL across active participants (are all?), and also a participant can't be edited to set the existing URL.
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2025-12-08 21:16 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>https://gonka.ai/FAQ/#how-to-change-inference_url</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #381](https://github.com/gonka-ai/gonka/issues/381) every hour.
