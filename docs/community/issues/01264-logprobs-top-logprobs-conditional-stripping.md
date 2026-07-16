---
title: "#1264 — logprobs, top_logprobs conditional stripping"
source: https://github.com/gonka-ai/gonka/issues/1264
issue_number: 1264
synced_at: 2026-07-16T09:32:48Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    logprobs, top_logprobs conditional stripping
    <span class="issues-number">#1264</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item">[@a-kuprin](https://github.com/a-kuprin) opened 2026-05-27 17:29 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-07-01 06:06 UTC</span>
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

> 🔄 **Auto-synced** from [Issue #1264](https://github.com/gonka-ai/gonka/issues/1264) every hour.
