---
title: "#419 — New Issue → Request Access to Inference Image"
source: https://github.com/gonka-ai/gonka/issues/419
issue_number: 419
synced_at: 2026-08-08T02:27:16Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    New Issue → Request Access to Inference Image
    <span class="issues-number">#419</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/rumirzayev-max">@rumirzayev-max</a> opened 2025-11-06 12:53 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2025-11-17 21:52 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Hi, I need access to the GHCR image to run inferenced nodes.

My GitHub username: rumirzayev-max

Please add me to the gonka-ai organization and grant "read" access to:
  ghcr.io/gonka-ai/inferenced

Thanks!

</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/DimaOrekhovPS">@DimaOrekhovPS</a></span>
    <span class="issues-meta-item">commented 2025-11-17 21:00 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>The images are public for everyone. One possible cause for failing to pull an image is using stale GH credentials, try using <code>docker logout ghcr.io</code> to clear the credentials, then login again with <code>docker login ghcr.io</code> and retry</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #419](https://github.com/gonka-ai/gonka/issues/419) every hour.
