---
title: "#1851 — `devshard`: It would be worth adding small tests asserting `pool.Config().MaxConns` for both payload storage constructors. `ConfigureMaxConns` itself is well tested, but the current tests wouldn’t catch the helper being accidentally removed from either constructor."
source: https://github.com/gonka-ai/gonka/issues/1851
issue_number: 1851
synced_at: 2026-09-26T07:51:05Z
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
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-09-25 16:19 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Looks good overall, approved. It would be worth adding small tests asserting `pool.Config().MaxConns` for both payload storage constructors. `ConfigureMaxConns` itself is well tested, but the current tests wouldn’t catch the helper being accidentally removed from either constructor.

_Originally posted by @aikuznetsov in https://github.com/gonka-ai/gonka/pull/1840#pullrequestreview-5312588423_
            
</div>

---

> 🔄 **Auto-synced** from [Issue #1851](https://github.com/gonka-ai/gonka/issues/1851) every hour.
