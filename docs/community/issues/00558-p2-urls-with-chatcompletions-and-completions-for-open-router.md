---
title: "#558 — [P2] URLs with `/chat/completions` and `/completions` for Open Router"
source: https://github.com/gonka-ai/gonka/issues/558
issue_number: 558
synced_at: 2026-07-30T03:36:56Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    [P2] URLs with `/chat/completions` and `/completions` for Open Router
    <span class="issues-number">#558</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-01-14 20:40 UTC</span>
    <span class="issues-meta-item">3 comments</span>
    <span class="issues-meta-item">Updated 2026-04-08 16:51 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Provide a minimal but verifiable example that demonstrates Gonka’s inference capability via standard OpenAI-compatible endpoints, suitable for validation and review by openrouter.ai. We need to run a simple inference and provide publicly accessible URLs for the following endpoints:
- `/completions`
- `/chat/completions`

These endpoints are required for listing Gonka as an inference vendor on openrouter.ai.

Requirements
- The inference should be very simple (e.g. a basic prompt like asking about the weather).
- The URLs must return real inference results, not mock data.

Inference logs for the provided URLs must:
- Be readable
- Remain accessible for a reasonably long period of time
- Just a minimal, clear demonstration of how to query the API

**Must be openAI-compliant and return usage for both stream and non-stream**

+ include pricing models endpoint

Before implementation, please review OpenRouter documentation and any relevant provider integration requirements.
This will help ensure full compatibility and avoid iteration during validation.
</div>

---

## 💬 Comments (3)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-01-23 01:14 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@x0152 feel free to ask @kotelnikova any questions here as well </p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/libermans">@libermans</a></span>
    <span class="issues-meta-item">commented 2026-02-18 01:17 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Should it work with no "request signing" needed? With "api key" requests? Do we have requirements from them? @kotelnikova @tcharchian </p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-02-19 03:20 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>After review https://github.com/gonka-ai/gonka/pull/614, the merge is temporarily paused. A community broker must be identified to serve as an intermediary between OpenRouter and Gonka. Once that structure is defined, the required adjustments on the integration side will become clearer.</p>
<p>In particular, this will determine whether separate endpoints (for example, with /openrouter in the address) are necessary, or whether a different architectural approach would be more appropriate.</p>
<p>Further feedback and next steps will be shared once the broker setup is clarified.</p>
<p>cc: @libermans @kotelnikova @x0152 </p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #558](https://github.com/gonka-ai/gonka/issues/558) every hour.
