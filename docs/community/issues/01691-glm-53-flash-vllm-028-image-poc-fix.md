---
title: "#1691 — GLM 5.3 Flash: vLLM 0.28 image + PoC fix"
source: https://github.com/gonka-ai/gonka/issues/1691
issue_number: 1691
synced_at: 2026-09-03T18:45:05Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    GLM 5.3 Flash: vLLM 0.28 image + PoC fix
    <span class="issues-number">#1691</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-08-31 20:23 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-09-03 05:07 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Pitstop’s main track is MLNode images, experiments, and evaluations for bringing new models onto the network.

The current piece of work is GLM 5.3 Flash: a vLLM 0.28 image plus a PoC fix. PoC currently exceeds the allowed memory budget; that needs to be resolved before handover.

This issue also sets a public bar for how MLNode image work is specified and accepted, so anyone taking an image can see what was checked and what the limitations are.

Confirm the live on-chain set from poc_params.models if the list below has drifted.

---

### Process

- [ ] Experiments completed and written up (hardware, models, what passed, what did not)
- [ ] MLNode starts and reaches a working state (does not crash)
- [ ] Write-up reviewed (review does not have to block image built; once the two items above are done, the image can be built and backward compatibility can be checked in parallel)
- [ ] Image rechecked against the model list below before handover
- [ ] If the image is intentionally for a specific model: notes published before handover, listing which models are supported and which are not

---

### Per-model checks

For every model below: both PoC and inference must pass. Installing this image must not break models already on chain unless that is stated in the notes before handover.

`MiniMaxAI/MiniMax-M2.7` — base model, active

- [ ] PoC starts, finishes, and stays within the allowed memory budget
- [ ] Inference works
- [ ] Supported on this image, or unsupported and called out in notes before handover

`moonshotai/Kimi-K2.6` — active

- [ ] PoC starts, finishes, and stays within the allowed memory budget
- [ ] Inference works
- [ ] Supported on this image, or unsupported and called out in notes before handover

`deepseek-ai/DeepSeek-V4-Flash-0731` — active

- [ ] PoC starts, finishes, and stays within the allowed memory budget
- [ ] Inference works
- [ ] Supported on this image, or unsupported and called out in notes before handover

`zai-org/GLM-5.2-FP8` — registered on chain, not bootstrapped (penalty_start_epoch = 500)

- [ ] PoC starts, finishes, and stays within the allowed memory budget
- [ ] Inference works
- [ ] Supported on this image, or unsupported and called out in notes before handover

GLM 5.3 Flash — target of this image (vLLM 0.28)

- [ ] vLLM 0.28 image builds and runs
- [ ] PoC starts, finishes, and no longer exceeds the allowed memory budget
- [ ] Inference works
- [ ] Experiment notes attached (hardware, memory, PoC, inference)

---

### Handover

- [ ] Image tag published
- [ ] Checklist above filled for each model
- [ ] Limitations, if any, written in notes before handover

The image is treated as delivered when this checklist is complete.
</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/baychak">@baychak</a></span>
    <span class="issues-meta-item">commented 2026-08-31 20:26 UTC</span>
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

---

> 🔄 **Auto-synced** from [Issue #1691](https://github.com/gonka-ai/gonka/issues/1691) every hour.
