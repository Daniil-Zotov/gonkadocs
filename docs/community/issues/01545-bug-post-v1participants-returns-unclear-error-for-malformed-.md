---
title: "#1545 — [BUG] POST /v1/participants returns unclear error for malformed JSON"
source: https://github.com/gonka-ai/gonka/issues/1545
issue_number: 1545
synced_at: 2026-08-09T11:49:25Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    [BUG] POST /v1/participants returns unclear error for malformed JSON
    <span class="issues-number">#1545</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/Parikalp-Bhardwaj">@Parikalp-Bhardwaj</a> opened 2026-08-04 19:19 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-08-04 19:19 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span></div>
</div>

<div class="issues-content" markdown="1">
## Description

`POST /v1/participants` returns a nested parser error when the request body contains malformed JSON.

## Current behavior

```json
{"error":{"message":"unexpected EOF"}}
```

## Expected behavior
```
{"error":"Invalid request body"}
```
</div>

---

> 🔄 **Auto-synced** from [Issue #1545](https://github.com/gonka-ai/gonka/issues/1545) every hour.
