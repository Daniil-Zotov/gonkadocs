---
title: "#630 — Research: Ephemeral port exhaustion"
source: https://github.com/gonka-ai/gonka/issues/630
issue_number: 630
synced_at: 2026-07-07T04:29:20Z
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
    <span class="issues-meta-item">[@tcharchian](https://github.com/tcharchian) opened 2026-01-23 20:09 UTC</span>
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
    <span>[@AlexeySamosadov](https://github.com/AlexeySamosadov)</span>
    <span class="issues-meta-item">commented 2026-01-24 21:13 UTC</span>
  </div>
  <div class="issues-comment-body issues-content" markdown="1">
    ## Ephemeral Port Exhaustion Analysis

### Summary
Found several patterns that can cause ephemeral port exhaustion due to improper HTTP client usage and missing connection pooling configuration.

---

### Critical Issues Found

#### 1. `http.DefaultClient` usage without pooling config
**File:** `internal/server/public/post_chat_handler.go:367`
```go
resp, err := http.DefaultClient.Do(req)
```
- DefaultClient has no MaxIdleConns/MaxIdleConnsPerHost limits
- Called in critical inference request path (`handleTransferRequest`)

#### 2. `http.Post()` calls create new connections each time
**Files:**
- `internal/server/public/post_chat_handler.go:443` - tokenization
- `internal/server/public/post_chat_handler.go:525` - executor requests  
- `internal/validation/inference_validation.go:897` - validation

#### 3. `NewHttpClient()` lacks Transport config
**File:** `utils/http.go:14-18`
```go
func NewHttpClient(timeout time.Duration) *http.Client {
    return &http.Client{
        Timeout: timeout,
    }
}
```
Only sets timeout, no connection pooling configuration.

#### 4. mlnodeclient creates Client without pooling
**File:** `mlnodeclient/client.go:38-40`
```go
client: http.Client{
    Timeout: 15 * time.Minute,
}
```

#### 5. New clients created per health check
**File:** `internal/server/admin/setup_report.go:549,567`
Creates new `http.Client` for each health check call.

#### 6. No timeout in participant registration
**File:** `participant/participant_registration.go:160`
```go
client := &http.Client{}  // No timeout!
```

---

### Recommended Fix

Create a shared HTTP client with proper Transport configuration:

```go
var sharedHTTPClient = &http.Client{
    Transport: &http.Transport{
        MaxIdleConns:        100,
        MaxIdleConnsPerHost: 10,
        MaxConnsPerHost:     20,
        IdleConnTimeout:     90 * time.Second,
    },
    Timeout: 30 * time.Second,
}
```

### Files Requiring Changes
1. `utils/http.go` - Update `NewHttpClient()` with Transport config
2. `internal/server/public/post_chat_handler.go` - Replace `http.DefaultClient` and `http.Post()`
3. `mlnodeclient/client.go` - Add Transport configuration
4. `internal/server/admin/setup_report.go` - Reuse single client
5. `participant/participant_registration.go` - Use configured client with timeout
6. `internal/validation/inference_validation.go` - Replace `http.Post()`
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@tcharchian](https://github.com/tcharchian)</span>
    <span class="issues-meta-item">commented 2026-01-29 00:21 UTC</span>
  </div>
  <div class="issues-comment-body issues-content" markdown="1">
    Hello @AlexeySamosadov, thank you for your contribution. However, I'd suggest waiting for @libermans or @gmorgachev to give a detailed description of the task and expected results.  
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@AlexeySamosadov](https://github.com/AlexeySamosadov)</span>
    <span class="issues-meta-item">commented 2026-02-08 14:14 UTC</span>
  </div>
  <div class="issues-comment-body issues-content" markdown="1">
    PR created: https://github.com/gonka-ai/gonka/pull/656

Adds HTTP client connection pooling to prevent ephemeral port exhaustion.
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #630](https://github.com/gonka-ai/gonka/issues/630) every hour.
