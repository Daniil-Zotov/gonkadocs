---
title: "#839 — LogInfo tests on testnet for StartInference and FinishInference"
source: https://github.com/gonka-ai/gonka/issues/839
issue_number: 839
synced_at: 2026-07-07T21:46:37Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    LogInfo tests on testnet for StartInference and FinishInference
    <span class="issues-number">#839</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item">[@maria-mitina](https://github.com/maria-mitina) opened 2026-03-02 15:50 UTC</span>
    <span class="issues-meta-item">3 comments</span>
    <span class="issues-meta-item">Updated 2026-03-19 06:35 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
To investigate the impact of log_format = "json" vs log_format = "plain" on node performance, a [number of experiments were executed on Testnet](https://docs.google.com/spreadsheets/d/1GkV6tn5tgQ3eL7VgAF4JaBWerqsN-fGHc6KEKNigFog/edit?pli=1&gid=586520582#gid=586520582). This is not compared to [mainnet performance](https://github.com/gonka-ai/gonka/issues/780#issuecomment-3972000833), however in isolation supports the same conclusion.  
We could achieve around 3x improvement under inference to performance of LogInfo, when switching to log_format = "json".



<img width="1237" height="470" alt="Image" src="https://github.com/user-attachments/assets/dc9b7e25-3562-4f70-b058-2c6fe8ed52ac" />
</div>

---

## 💬 Comments (3)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@maria-mitina](https://github.com/maria-mitina)</span>
    <span class="issues-meta-item">commented 2026-03-02 15:51 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Should we continue with the log_level=info and log_level=error?</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@hleb-albau](https://github.com/hleb-albau)</span>
    <span class="issues-meta-item">commented 2026-03-02 16:34 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>x3 for start/finish inference, or x3 for logging?</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@maria-mitina](https://github.com/maria-mitina)</span>
    <span class="issues-meta-item">commented 2026-03-03 08:44 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@hleb-albau 3x improvement under inference to performance of LogInfo</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #839](https://github.com/gonka-ai/gonka/issues/839) every hour.
