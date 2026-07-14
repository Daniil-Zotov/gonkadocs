---
title: "#985 — [P0] Bug: unsupported OpenAI type input for the inference requests"
source: https://github.com/gonka-ai/gonka/issues/985
issue_number: 985
synced_at: 2026-07-14T09:21:08Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    [P0] Bug: unsupported OpenAI type input for the inference requests
    <span class="issues-number">#985</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item">[@tamazgadaev](https://github.com/tamazgadaev) opened 2026-03-31 15:15 UTC</span>
    <span class="issues-meta-item">4 comments</span>
    <span class="issues-meta-item">Updated 2026-04-03 22:36 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
decentralized-api rejects valid Cursor/OpenAI chat requests where messages[].content is an array of text parts instead of a plain string. The request fails during request parsing on TA/executor because Message.Content is typed as string, producing 500 {"error":"json: cannot unmarshal array into Go struct field ... content of type string"} even though the payload is valid modern chat-completions format.
</div>

---

## 💬 Comments (4)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@tamazgadaev](https://github.com/tamazgadaev)</span>
    <span class="issues-meta-item">commented 2026-03-31 15:16 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Check David's thoughts on this in the branch: https://github.com/gonka-ai/gonka/compare/main...codex/dl/diagnose-multimodal-content-parsing</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@tamazgadaev](https://github.com/tamazgadaev)</span>
    <span class="issues-meta-item">commented 2026-03-31 15:16 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@tcharchian FYI
@patimen @DimaOrekhovPS Can you take a look? </p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@x0152](https://github.com/x0152)</span>
    <span class="issues-meta-item">commented 2026-03-31 16:31 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hey! If we're talking about the current /v1/chat/completions endpoint then #614 covers this</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@tcharchian](https://github.com/tcharchian)</span>
    <span class="issues-meta-item">commented 2026-04-01 03:09 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@x0152 thanks! @DimaOrekhovPS will be working on merging David's changes first. And then will ask you @x0152  to merge them in David's branch. Hope that works for you</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #985](https://github.com/gonka-ai/gonka/issues/985) every hour.
