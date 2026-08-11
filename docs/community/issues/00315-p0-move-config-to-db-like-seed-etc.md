---
title: "#315 — [P0] Move config to DB (like seed, etc)"
source: https://github.com/gonka-ai/gonka/issues/315
issue_number: 315
synced_at: 2026-08-11T15:20:58Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    [P0] Move config to DB (like seed, etc)
    <span class="issues-number">#315</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2025-09-03 22:44 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-01-15 22:00 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
- [ ] The `api-config.yml` file often goes missing, and this part is needs to be rewritten: https://github.com/gonka-ai/gonka/blob/bacddd41f257b459d85b04786bee06b49a084dff/decentralized-api/apiconfig/config_manager.go#L302
- [ ] The `api-config` should be split into two parts:
      - a static configuration file
      - some kind of state (either in MySQL or a JSON file, but one that is updated strictly atomically). Consider leaning toward using MySQL right away, as it remains a standard and straightforward option, yet allows for the safe storage of as much data as needed. For debugging, a human-readable export is fine.
</div>

---

> 🔄 **Auto-synced** from [Issue #315](https://github.com/gonka-ai/gonka/issues/315) every hour.
