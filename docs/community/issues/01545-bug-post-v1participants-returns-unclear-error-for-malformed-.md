---
title: "#1545 — [BUG] POST /v1/participants returns unclear error for malformed JSON"
source: https://github.com/gonka-ai/gonka/issues/1545
issue_number: 1545
synced_at: 2026-10-10T13:50:19Z
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
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-09-28 19:18 UTC</span>
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

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/redstartechno">@redstartechno</a></span>
    <span class="issues-meta-item">commented 2026-09-28 19:18 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>There are now three open PRs for this issue, all changing the same line in <code>decentralized-api/internal/server/public/post_participant_handler.go</code>. Listing them side by side so one can be picked and the others closed:</p>
<table>
<thead>
<tr>
<th>PR</th>
<th>Opened</th>
<th>Handler change</th>
<th>Test</th>
</tr>
</thead>
<tbody>
<tr>
<td>#1546</td>
<td>2026-08-04</td>
<td><code>"Invalid request body"</code> + <code>.SetInternal(err)</code> (keeps the original error for logs)</td>
<td>Adds a malformed-JSON test, but it asserts only the status code and logs the body</td>
</tr>
<tr>
<td>#1678</td>
<td>2026-08-30</td>
<td><code>"Invalid request body"</code></td>
<td>None</td>
</tr>
<tr>
<td>#1865</td>
<td>2026-09-27</td>
<td><code>"Invalid request body"</code></td>
<td>Asserts the JSON body for malformed JSON and for missing fields</td>
</tr>
</tbody>
</table>
<h1>1546 does not reference this issue in its description, which is probably why the later two were opened.</h1>
<p>This is a comparison of the diffs only; I did not run the tests of #1865 or #1678.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1545](https://github.com/gonka-ai/gonka/issues/1545) every hour.
