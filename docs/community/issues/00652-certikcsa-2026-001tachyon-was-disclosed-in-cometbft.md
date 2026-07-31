---
title: "#652 — Certik(CSA-2026-001:Tachyon, was disclosed in CometBFT)"
source: https://github.com/gonka-ai/gonka/issues/652
issue_number: 652
synced_at: 2026-07-31T12:23:03Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Certik(CSA-2026-001:Tachyon, was disclosed in CometBFT)
    <span class="issues-number">#652</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-01-27 19:04 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-03-12 18:29 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
A critical vulnerability — CSA-2026-001: Tachyon — was disclosed in CometBFT (Advisory: https://github.com/cometbft/cometbft/security/advisories/GHSA-c32p-wcqj-j677).

According to the disclosure, all versions of CometBFT are affected. The issue has been addressed in CometBFT versions v0.38.21 and v0.37.18.

As Gonka is a Cosmos-based project that uses CometBFT, Certik kindly recommends upgrading to a patched version as soon as possible to mitigate potential risks.
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/AlexeySamosadov">@AlexeySamosadov</a></span>
    <span class="issues-meta-item">commented 2026-02-08 14:14 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>PR created: https://github.com/gonka-ai/gonka/pull/675</p>
<p>Updates CometBFT to v0.38.21 to fix the Tachyon vulnerability (CSA-2026-001).</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #652](https://github.com/gonka-ai/gonka/issues/652) every hour.
