---
title: "#1474 — Security/hardening: Executor signature verification disabled; token counts self-reported on Finish"
source: https://github.com/gonka-ai/gonka/issues/1474
issue_number: 1474
synced_at: 2026-07-31T23:26:24Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Security/hardening: Executor signature verification disabled; token counts self-reported on Finish
    <span class="issues-number">#1474</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/Aphelios01-sdk">@Aphelios01-sdk</a> opened 2026-07-18 03:05 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-07-18 03:08 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

On-chain policy disables **executor** signature verification on both Start-first and Finish-first paths. Payment-critical `CompletionTokenCount` / `PromptTokenCount` come from `MsgFinishInference` and drive escrow payouts up to reserved max.

Integrity then relies on peer validation / invalidation. That residual control is weaker when `ClaimValidationEnabled` is false (related issue).

Source also notes a TODO: TA signature should include `inferenceId` to prevent modified-prompt substitution.

## Paths

- `inference-chain/x/inference/keeper/msg_server_start_inference.go`
- `inference-chain/x/inference/keeper/msg_server_finish_inference.go`
- `inference-chain/x/inference/calculations/inference_state.go`

## Suggested remediation

1. Re-enable executor signatures over response/prompt hashes + token counts + inferenceId
2. Bind TA signature to inferenceId (resolve TODO)
3. Cross-check tokens during validation against payloads when available

## Disclosure

May be intentional design — filing for visibility / defense-in-depth. Happy to discuss on HackerOne if preferred.
</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Aphelios01-sdk">@Aphelios01-sdk</a></span>
    <span class="issues-meta-item">commented 2026-07-18 03:08 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Closing to focus disclosure on the highest-priority finding: https://github.com/gonka-ai/gonka/issues/1470 (SSRF via InferenceUrl). Other items can be re-opened or filed via HackerOne if needed.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1474](https://github.com/gonka-ai/gonka/issues/1474) every hour.
