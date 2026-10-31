---
title: "#2182 — OpenBroker registration fails: POST /api/auth/send-code → 500 failed to send email"
source: https://github.com/gonka-ai/gonka/issues/2182
issue_number: 2182
synced_at: 2026-10-31T07:04:53Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    OpenBroker registration fails: POST /api/auth/send-code → 500 failed to send email
    <span class="issues-number">#2182</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/ludmilavasilievna3-cmd">@ludmilavasilievna3-cmd</a> opened 2026-10-30 07:56 UTC</span>
    <span class="issues-meta-item">3 comments</span>
    <span class="issues-meta-item">Updated 2026-10-30 21:15 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Reproduced 2026-10-29 and 2026-10-30 with three different addresses, including a freshly created working mailbox:

Nothing delivered — inbox stays at 0 messages after 24 h. Validation itself works ({"email":"notanemail"} → 400 valid email is required), and the rest of the API is healthy (status operational, error_rate 0.2 %), so the mail sender is the only broken part.

Side note: gonka.gg has no DMARC record — _dmarc.gonka.gg returns nothing.
</div>

---

## 💬 Comments (3)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/ludmilavasilievna3-cmd">@ludmilavasilievna3-cmd</a></span>
    <span class="issues-meta-item">commented 2026-10-30 07:57 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Adding the missing reproduction — the code block was stripped on submit.</p>
<p>Request (2026-10-29 13:31 UTC and 2026-10-30 07:46 UTC, identical result):</p>
<pre><code>curl -s -D - -X POST https://api.openbroker.gonka.gg/api/auth/send-code \
  -H "content-type: application/json" \
  -d '{"email":"&lt;valid working inbox&gt;","purpose":"register"}'

HTTP/1.1 500 Internal Server Error
Server: Caddy
Content-Type: application/json
Content-Length: 33

{"error":"failed to send email"}
</code></pre>
<p>Recipients tested: a disposable but fully working mailbox (mail.tm),
probe@example.com, probe@invalid.invalid — all 500, nothing delivered
(0 messages in the inbox after 35 s, and again after 24 h).</p>
<p>Control requests on the same endpoint, proving the request format is fine:</p>
<ul>
<li>{"email":"notanemail","purpose":"register"} → 400 {"error":"valid email is required"}</li>
<li>{"email":"x@example.com","purpose":"login"} → 400 {"error":"purpose must be register or reset"}</li>
<li>POST /v1/chat/completions without key → 401 {"error":"missing or invalid OpenBroker API key"}</li>
</ul>
<p>Related: #1405 — accounts lost after the infrastructure migration.
This looks like the same migration leaving the mail sender down on
api.openbroker.gonka.gg.</p>
<p>Impact: registration is impossible — no verification code, no account, no obk- key.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-10-30 21:11 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@gonkalabs</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/gonkalabs">@gonkalabs</a></span>
    <span class="issues-meta-item">commented 2026-10-30 21:15 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hey @ludmilavasilievna3-cmd , thank you for reaching out!</p>
<p>Can you please retry now? Issue was transient and was related to mailing server issues, not core OpenBroker features.</p>
<p>Best regards,
Gonka Labs team</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #2182](https://github.com/gonka-ai/gonka/issues/2182) every hour.
