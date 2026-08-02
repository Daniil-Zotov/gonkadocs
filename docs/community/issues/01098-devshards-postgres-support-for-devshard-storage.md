---
title: "#1098 — `devshards` Postgres support for `devshard` storage"
source: https://github.com/gonka-ai/gonka/issues/1098
issue_number: 1098
synced_at: 2026-08-02T10:55:49Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    `devshards` Postgres support for `devshard` storage
    <span class="issues-number">#1098</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/akup">@akup</a> opened 2026-04-21 20:36 UTC</span>
    <span class="issues-meta-item">3 comments</span>
    <span class="issues-meta-item">Updated 2026-05-25 18:30 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
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
</div>

---

## 💬 Comments (3)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Mayveskii">@Mayveskii</a></span>
    <span class="issues-meta-item">commented 2026-04-24 20:22 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <blockquote>
<p>RE</p>
</blockquote>
<p>Hi, can i grab this one for couple of week ? </p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-04-29 21:21 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>https://github.com/gonka-ai/gonka/pull/1126</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/x0152">@x0152</a></span>
    <span class="issues-meta-item">commented 2026-05-07 08:41 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Closed by #1145 </p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1098](https://github.com/gonka-ai/gonka/issues/1098) every hour.
