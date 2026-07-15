---
title: "#1167 — `devshards` Optimizations for v0.2.13 db usage"
source: https://github.com/gonka-ai/gonka/issues/1167
issue_number: 1167
synced_at: 2026-07-15T20:29:23Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    `devshards` Optimizations for v0.2.13 db usage
    <span class="issues-number">#1167</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item">[@akup](https://github.com/akup) opened 2026-05-14 15:47 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-05-25 18:37 UTC</span>
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

> 🔄 **Auto-synced** from [Issue #1167](https://github.com/gonka-ai/gonka/issues/1167) every hour.
