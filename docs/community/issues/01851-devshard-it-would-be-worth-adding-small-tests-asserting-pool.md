---
title: "#1851 — `devshard`: It would be worth adding small tests asserting `pool.Config().MaxConns` for both payload storage constructors. `ConfigureMaxConns` itself is well tested, but the current tests wouldn’t catch the helper being accidentally removed from either constructor."
source: https://github.com/gonka-ai/gonka/issues/1851
issue_number: 1851
synced_at: 2026-10-06T10:30:51Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    `devshard`: It would be worth adding small tests asserting `pool.Config().MaxConns` for both payload storage constructors. `ConfigureMaxConns` itself is well tested, but the current tests wouldn’t catch the helper being accidentally removed from either constructor.
    <span class="issues-number">#1851</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-09-25 16:19 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-09-30 14:48 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Looks good overall, approved. It would be worth adding small tests asserting `pool.Config().MaxConns` for both payload storage constructors. `ConfigureMaxConns` itself is well tested, but the current tests wouldn’t catch the helper being accidentally removed from either constructor.

_Originally posted by @aikuznetsov in https://github.com/gonka-ai/gonka/pull/1840#pullrequestreview-5312588423_
            
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/zpoken">@zpoken</a></span>
    <span class="issues-meta-item">commented 2026-09-30 14:48 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Added in #1883 : tests for both payload constructors, <code>newPostgresStorage</code> (<code>common/storage/payloads</code>) and <code>NewPostgresStorage</code> (<code>decentralized-api/payloadstorage</code>).</p>
<ul>
<li>An invalid <code>PG_POOL_MAX_CONNS</code> must fail the constructor with the helper's error before any connection is made. Runs in <code>-short</code>, no Docker.</li>
<li>testcontainers: <code>pool.Config().MaxConns</code> is the default when the variable is unset and <code>3</code> when it is set. <code>3</code> is below pgx's floor of 4, so the check does not depend on the CPU count.</li>
</ul>
<p>Verified by removing the <code>ConfigureMaxConns</code> call from both constructors: every new test fails, on hosts pinned to 3, 4 and 8 CPUs.</p>
<p>@akup </p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1851](https://github.com/gonka-ai/gonka/issues/1851) every hour.
