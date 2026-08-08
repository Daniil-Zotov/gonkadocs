---
title: "#1167 — `devshards` Optimizations for v0.2.13 db usage"
source: https://github.com/gonka-ai/gonka/issues/1167
issue_number: 1167
synced_at: 2026-08-08T16:57:10Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    `devshards` Optimizations for v0.2.13 db usage
    <span class="issues-number">#1167</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/akup">@akup</a> opened 2026-05-14 15:47 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-07-20 04:54 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
During review of https://github.com/gonka-ai/gonka/pull/1143 there was found optimization points for db usage:

1. Do not lock around `createSession` (https://github.com/gonka-ai/gonka/pull/1143#discussion_r3200794751)

2. Add migration point to remove CREATE TABLE IF NOT EXIST from hot paths (https://github.com/gonka-ai/gonka/pull/1143#discussion_r3200930890, https://github.com/gonka-ai/gonka/pull/1143#discussion_r3205286743)

3. Neat like this: https://github.com/gonka-ai/gonka/pull/1143#discussion_r3201178940, https://github.com/gonka-ai/gonka/pull/1143#discussion_r3205419993

4. Optimize pruning (do not call every 30 seconds): https://github.com/gonka-ai/gonka/pull/1143#discussion_r3212576442

5. Do not create SQLite base for each session when Postgres is available (https://github.com/gonka-ai/gonka/pull/1143#discussion_r3205241993)

6. Snapshots in protobuf instead of json (https://github.com/gonka-ai/gonka/pull/1143#discussion_r3202629755)

It could be added in one PR for devshard realease. Should be merged with https://github.com/gonka-ai/gonka/pull/1162

</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/a-kuprin">@a-kuprin</a></span>
    <span class="issues-meta-item">commented 2026-07-20 04:54 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Closing by https://github.com/gonka-ai/gonka/pull/1482</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1167](https://github.com/gonka-ai/gonka/issues/1167) every hour.
