---
title: "#630 — Research: Ephemeral port exhaustion"
source: https://github.com/gonka-ai/gonka/issues/630
issue_number: 630
synced_at: 2026-07-26T04:03:23Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Research: Ephemeral port exhaustion
    <span class="issues-number">#630</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-01-23 20:09 UTC</span>
    <span class="issues-meta-item">3 comments</span>
    <span class="issues-meta-item">Updated 2026-03-21 19:24 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
This is a future task. A detailed description will be provided in the near future.

Please do not start working on this task without the detailed specification, as it may turn out to be a different direction than expected, which could reduce the chances of receiving a reward.

If you are interested in completing this task, please leave a comment here.
After that, feel free to contact me on Discord: `tatianacharchian_07833`.
</div>

---

## 💬 Comments (3)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/AlexeySamosadov">@AlexeySamosadov</a></span>
    <span class="issues-meta-item">commented 2026-01-24 21:13 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <h2>Ephemeral Port Exhaustion Analysis</h2>
<h3>Summary</h3>
<p>Found several patterns that can cause ephemeral port exhaustion due to improper HTTP client usage and missing connection pooling configuration.</p>
<hr />
<h3>Critical Issues Found</h3>
<h4>1. <code>http.DefaultClient</code> usage without pooling config</h4>
<p><strong>File:</strong> <code>internal/server/public/post_chat_handler.go:367</code></p>
<pre><code class="language-go">resp, err := http.DefaultClient.Do(req)
</code></pre>
<ul>
<li>DefaultClient has no MaxIdleConns/MaxIdleConnsPerHost limits</li>
<li>Called in critical inference request path (<code>handleTransferRequest</code>)</li>
</ul>
<h4>2. <code>http.Post()</code> calls create new connections each time</h4>
<p><strong>Files:</strong>
- <code>internal/server/public/post_chat_handler.go:443</code> - tokenization
- <code>internal/server/public/post_chat_handler.go:525</code> - executor requests<br />
- <code>internal/validation/inference_validation.go:897</code> - validation</p>
<h4>3. <code>NewHttpClient()</code> lacks Transport config</h4>
<p><strong>File:</strong> <code>utils/http.go:14-18</code></p>
<pre><code class="language-go">func NewHttpClient(timeout time.Duration) *http.Client {
    return &amp;http.Client{
        Timeout: timeout,
    }
}
</code></pre>
<p>Only sets timeout, no connection pooling configuration.</p>
<h4>4. mlnodeclient creates Client without pooling</h4>
<p><strong>File:</strong> <code>mlnodeclient/client.go:38-40</code></p>
<pre><code class="language-go">client: http.Client{
    Timeout: 15 * time.Minute,
}
</code></pre>
<h4>5. New clients created per health check</h4>
<p><strong>File:</strong> <code>internal/server/admin/setup_report.go:549,567</code>
Creates new <code>http.Client</code> for each health check call.</p>
<h4>6. No timeout in participant registration</h4>
<p><strong>File:</strong> <code>participant/participant_registration.go:160</code></p>
<pre><code class="language-go">client := &amp;http.Client{}  // No timeout!
</code></pre>
<hr />
<h3>Recommended Fix</h3>
<p>Create a shared HTTP client with proper Transport configuration:</p>
<pre><code class="language-go">var sharedHTTPClient = &amp;http.Client{
    Transport: &amp;http.Transport{
        MaxIdleConns:        100,
        MaxIdleConnsPerHost: 10,
        MaxConnsPerHost:     20,
        IdleConnTimeout:     90 * time.Second,
    },
    Timeout: 30 * time.Second,
}
</code></pre>
<h3>Files Requiring Changes</h3>
<ol>
<li><code>utils/http.go</code> - Update <code>NewHttpClient()</code> with Transport config</li>
<li><code>internal/server/public/post_chat_handler.go</code> - Replace <code>http.DefaultClient</code> and <code>http.Post()</code></li>
<li><code>mlnodeclient/client.go</code> - Add Transport configuration</li>
<li><code>internal/server/admin/setup_report.go</code> - Reuse single client</li>
<li><code>participant/participant_registration.go</code> - Use configured client with timeout</li>
<li><code>internal/validation/inference_validation.go</code> - Replace <code>http.Post()</code></li>
</ol>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-01-29 00:21 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hello @AlexeySamosadov, thank you for your contribution. However, I'd suggest waiting for @libermans or @gmorgachev to give a detailed description of the task and expected results.  </p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/AlexeySamosadov">@AlexeySamosadov</a></span>
    <span class="issues-meta-item">commented 2026-02-08 14:14 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>PR created: https://github.com/gonka-ai/gonka/pull/656</p>
<p>Adds HTTP client connection pooling to prevent ephemeral port exhaustion.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #630](https://github.com/gonka-ai/gonka/issues/630) every hour.
