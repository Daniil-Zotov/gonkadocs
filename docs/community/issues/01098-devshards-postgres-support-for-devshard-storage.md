---
title: "#1098 — `devshards` Postgres support for `devshard` storage"
source: https://github.com/gonka-ai/gonka/issues/1098
issue_number: 1098
synced_at: 2026-07-06T09:52:00Z
template: issues-main.html
---

> 🔄 **Auto-synced:** from [Issue #1098](https://github.com/gonka-ai/gonka/issues/1098) every 6 hours. 

# 🔴 `devshards` Postgres support for `devshard` storage

**Author:** [@akup](https://github.com/akup) · **State:** Closed · **Created:** 2026-04-21 20:36 UTC · **Updated:** 2026-05-25 18:30 UTC

**Веха:** v0.2.13

---

## 📝 Описание

## Problem

`devshard/storage` is sqlite-only today (`storage/sqlite.go`,
`modernc.org/sqlite`). Running production devshards on embedded sqlite is
the wrong default:

- Every `devshardd` instance holds its own file, so nothing aggregates
  across hosts or across versions managed by `versiond`.
- A production operator already runs Postgres for
  `decentralized-api` (see `decentralized-api/payloadstorage/`,
  `decentralized-api/statsstorage/`); forcing a second on-box database
  in sqlite duplicates backup, monitoring, and retention setups.
- Integration tests and CI, by contrast, benefit from sqlite: zero
  dependencies, per-test cleanup, in-memory mode, fast startup.

We want both backends behind a single interface, chosen at runtime the
same way `decentralized-api/payloadstorage` does it.

Also we should prune the old epoch's devshard data

## Goals

- Keep `devshard/storage.Storage` as the sole interface consumed by
  `devshard/host` and the rest of the module; do not leak backend
  specifics into callers.
- Add a Postgres backend alongside the existing sqlite backend. It should be default db
- Prune data related to devshards created at epochs `< currentEpoch - 2`

---

## 💬 Comments (3)

### Комментарий 1 — [@Mayveskii](https://github.com/Mayveskii)

*2026-04-24 20:22 UTC*

>RE

Hi, can i grab this one for couple of week ? 

### Комментарий 2 — [@tcharchian](https://github.com/tcharchian)

*2026-04-29 21:21 UTC*

https://github.com/gonka-ai/gonka/pull/1126

### Комментарий 3 — [@x0152](https://github.com/x0152)

*2026-05-07 08:41 UTC*

Closed by #1145 
