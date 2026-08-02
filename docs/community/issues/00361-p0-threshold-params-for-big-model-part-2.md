---
title: "#361 — [P0] Threshold + Params for big model. Part 2."
source: https://github.com/gonka-ai/gonka/issues/361
issue_number: 361
synced_at: 2026-08-02T06:50:41Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    [P0] Threshold + Params for big model. Part 2.
    <span class="issues-number">#361</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2025-09-16 22:31 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2025-12-05 22:18 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
1. Threshold + Params for big model; 
2. Scripts to compute, re-check for existing; 
3. New Models 

- [ ] `gpt-oss-120b`
- [x] `DeepSeek-R1-0528`
- [x] `gemma-3-27b-it`
- [x] `Qwen3-30B-A3B-Instruct-2507`
- [ ] `gpt-oss-20b`
- [x] `Qwen3-235B`

4. Instruction to do it
5. Inference Validation finetuning;
6. Fine-tuning Qwen 235 
</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2025-12-05 22:16 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>GPT-OSS can be implemented after the vLLM update. Right now, it is being handled by community contributors from the bounty program  https://discord.com/channels/1336477374442770503/1425189436748206171/1446142256900997152</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2025-12-05 22:18 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>The threshold-calculation task is completed for the models listed above (except GTP-OSS). They haven’t deployed it to the chain yet. They will most likely be deployed after the vLLM update  </p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #361](https://github.com/gonka-ai/gonka/issues/361) every hour.
