---
title: "#1264 — logprobs, top_logprobs conditional stripping"
source: https://github.com/gonka-ai/gonka/issues/1264
issue_number: 1264
synced_at: 2026-08-04T14:45:07Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    logprobs, top_logprobs conditional stripping
    <span class="issues-number">#1264</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/a-kuprin">@a-kuprin</a> opened 2026-05-27 17:29 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-07-20 05:41 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #a2eeef; color: #24292f; border-color: #a2eeef;">enhancement</span></div>
</div>

<div class="issues-content" markdown="1">
The gateway forces logprobs upstream for validation, but clients who never asked for logprobs should not see them in the response (OpenAI-compatible default).
Clients who explicitly set `logprobs: true` or `top_logprobs` should get them back.

Now we always strip them even if client asked this fields in request

Recommendation: Adopt conditional stripping for logprobs and top_logprobs on the client-facing proxy path. Keep unconditional stripping for token_ids, prompt_token_ids, and prompt_logprobs.
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/a-kuprin">@a-kuprin</a></span>
    <span class="issues-meta-item">commented 2026-07-20 05:41 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Merged to v4 https://github.com/gonka-ai/gonka/commit/4a8eb85af061c94e8f572d42bb5ee5f1c267fa2f</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1264](https://github.com/gonka-ai/gonka/issues/1264) every hour.
