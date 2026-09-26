---
title: "#1852 — Decode PoC: move to vLLM 0.30.0 — one base for MiniMax, DeepSeek and GLM"
source: https://github.com/gonka-ai/gonka/issues/1852
issue_number: 1852
synced_at: 2026-09-26T01:39:55Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Decode PoC: move to vLLM 0.30.0 — one base for MiniMax, DeepSeek and GLM
    <span class="issues-number">#1852</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/baychak">@baychak</a> opened 2026-09-25 16:52 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-09-25 18:13 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
One decode-PoC base for all three models: vLLM 0.30.0, which carries GLM-5.3-Flash upstream. Integration and design stay on [#1688](https://github.com/gonka-ai/gonka/issues/1688). The decode-PoC release ships on 0.30.0 (@vbgd0, 2026-09-23). Out of scope: A100 (none on chain) and a new settings search.

**Done when**

- [x] residual on v0.30.0: [gonka-ai/vllm#114](https://github.com/gonka-ai/vllm/pull/114) into `release/v0.30-decode-int`
- [x] plugin on v0.30.0: [gonka-ai/gonka-vllm-plugins#19](https://github.com/gonka-ai/gonka-vllm-plugins/pull/19) into `decode/vlm030`
- [x] all three models on B300 and H100: start, validate against the previous reference artifacts, throughput measured. GLM runs with two prefill-kernel flags that keep the 0.28.1 references valid
- [ ] PRs merged, testnet built

**Needs:** @vbgd0 — review and testnet build.

**Estimate:** done on our side; waiting for review.

**Handover:** treated as delivered when the checklist above is complete. Anything skipped is listed here with the reason before handover.
</div>

---

> 🔄 **Auto-synced** from [Issue #1852](https://github.com/gonka-ai/gonka/issues/1852) every hour.
