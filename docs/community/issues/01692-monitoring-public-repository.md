---
title: "#1692 — Monitoring: public repository"
source: https://github.com/gonka-ai/gonka/issues/1692
issue_number: 1692
synced_at: 2026-09-06T21:26:07Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Monitoring: public repository
    <span class="issues-number">#1692</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-08-31 20:24 UTC</span>
    <span class="issues-meta-item">5 comments</span>
    <span class="issues-meta-item">Updated 2026-09-04 20:31 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Public Grafana repo (Pitstop): https://github.com/kaitakuai/gonka-grafana
Pasha @clanster has it ready for review.  
When it is out:
- [ ] the stack actually works
- [ ] Grafana shows what is really happening on the node
</div>

---

## 💬 Comments (5)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/baychak">@baychak</a></span>
    <span class="issues-meta-item">commented 2026-08-31 20:27 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>TY!</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/clanster">@clanster</a></span>
    <span class="issues-meta-item">commented 2026-08-31 20:27 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>ty</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/baychak">@baychak</a></span>
    <span class="issues-meta-item">commented 2026-09-04 14:12 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p><strong>Status:</strong> in progress</p>
<p><strong>Since last</strong></p>
<ul>
<li>Repo is ready and was renamed: <code>kaitakuai/gonka-grafana</code> → <code>kaitakuai/gonka-monitoring</code>. The link in the description still points to the old name.</li>
<li>Configuration only — compose file, two dashboards, scrape config. No code to build.</li>
</ul>
<p><strong>Next:</strong> switching it to public after confirming with @clanster on today's sync — by 2026-09-05.</p>
<p><strong>Q:</strong> the two boxes are a review, not a self-check — do you want someone on your side to run the stack, or should we verify and tick them ourselves?</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/clanster">@clanster</a></span>
    <span class="issues-meta-item">commented 2026-09-04 16:13 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p><strong>Status:</strong> done
<strong>Delivered:</strong> https://github.com/kaitakuai/gonka-monitoring (<code>c88f04f</code>). Hosted instance of the same stack, open to anyone: https://monitoring.kaitaku.ai/. Clean deploy on a fresh host: <code>docker compose up -d</code>, overview populated in ~3 min; 30 epoch participants discovered, 26 scraped, all panels on the three dashboards return data.
<strong>Limitations:</strong> repo flips to public once @baychak switches visibility (org owner) — by 2026-09-05; 4 participants return 503 on <code>/v1/mlnodes/metrics</code> on their side; the link in the description points to the old repo name.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/baychak">@baychak</a></span>
    <span class="issues-meta-item">commented 2026-09-04 20:31 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p><strong>Status:</strong> done
<strong>Delivered:</strong> repo is public now — https://github.com/kaitakuai/gonka-monitoring. Whole-network view via epoch auto-discovery landed today, so the stack is no longer limited to our own nodes.
<strong>Limitations:</strong> the link in the description still points to the old repo name.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1692](https://github.com/gonka-ai/gonka/issues/1692) every hour.
