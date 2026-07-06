---
title: "#1167 — `devshards` Optimizations for v0.2.13 db usage"
source: https://github.com/gonka-ai/gonka/issues/1167
issue_number: 1167
synced_at: 2026-07-06T09:51:59Z
template: issues-main.html
---

> 🔄 **Авто-синхронизация:** из [Issue #1167](https://github.com/gonka-ai/gonka/issues/1167) каждые 6 часов. 

# 🟢 `devshards` Optimizations for v0.2.13 db usage

**Автор:** [@akup](https://github.com/akup) · **Состояние:** Open · **Создано:** 2026-05-14 15:47 UTC · **Обновлено:** 2026-05-25 18:37 UTC

**Веха:** v0.2.14-devshard3

---

## 📝 Описание

During review of https://github.com/gonka-ai/gonka/pull/1143 there was found optimization points for db usage:

1. Do not lock around `createSession` (https://github.com/gonka-ai/gonka/pull/1143#discussion_r3200794751)

2. Add migration point to remove CREATE TABLE IF NOT EXIST from hot paths (https://github.com/gonka-ai/gonka/pull/1143#discussion_r3200930890, https://github.com/gonka-ai/gonka/pull/1143#discussion_r3205286743)

3. Neat like this: https://github.com/gonka-ai/gonka/pull/1143#discussion_r3201178940, https://github.com/gonka-ai/gonka/pull/1143#discussion_r3205419993

4. Optimize pruning (do not call every 30 seconds): https://github.com/gonka-ai/gonka/pull/1143#discussion_r3212576442

5. Do not create SQLite base for each session when Postgres is available (https://github.com/gonka-ai/gonka/pull/1143#discussion_r3205241993)

6. Snapshots in protobuf instead of json (https://github.com/gonka-ai/gonka/pull/1143#discussion_r3202629755)

It could be added in one PR for devshard realease. Should be merged with https://github.com/gonka-ai/gonka/pull/1162

