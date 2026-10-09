---
title: "#1852 — Decode PoC: move to vLLM 0.30.0 — one base for MiniMax, DeepSeek and GLM"
source: https://github.com/gonka-ai/gonka/issues/1852
issue_number: 1852
synced_at: 2026-10-09T16:19:36Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Decode PoC: move to vLLM 0.30.0 — one base for MiniMax, DeepSeek and GLM
    <span class="issues-number">#1852</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/baychak">@baychak</a> opened 2026-09-25 16:52 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-10-09 12:04 UTC</span>
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

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/baychak">@baychak</a></span>
    <span class="issues-meta-item">commented 2026-10-09 12:04 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p><strong>Status:</strong> done; closing.</p>
<p><strong>Delivered:</strong> the decode-PoC move to vLLM 0.30 landed through @vbgd0's PRs: <a href="https://github.com/gonka-ai/vllm/pull/116">gonka-ai/vllm#116</a> and <a href="https://github.com/gonka-ai/gonka-vllm-plugins/pull/21">gonka-ai/gonka-vllm-plugins#21</a> on 2026-09-29, with follow-ups <a href="https://github.com/gonka-ai/gonka-vllm-plugins/pull/25">gonka-ai/gonka-vllm-plugins#25</a> and <a href="https://github.com/gonka-ai/gonka-vllm-plugins/pull/26">gonka-ai/gonka-vllm-plugins#26</a> on 2026-10-06. Our <a href="https://github.com/gonka-ai/vllm/pull/114">gonka-ai/vllm#114</a> and <a href="https://github.com/gonka-ai/gonka-vllm-plugins/pull/19">gonka-ai/gonka-vllm-plugins#19</a> are closed as superseded.</p>
<p><strong>Limitations</strong></p>
<ul>
<li>GLM runs with <code>--language-model-only</code>. The GLM reference artifacts were re-taken on the release container on 2026-10-03: <a href="https://github.com/kaitakuai/experiments/tree/main/2026-10">kaitakuai/experiments/2026-10</a>.</li>
<li>A testnet run is not confirmed on this issue. The decode-PoC release goes out in v0.2.17 (<a href="https://github.com/gonka-ai/gonka/pull/1743">#1743</a>).</li>
</ul>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1852](https://github.com/gonka-ai/gonka/issues/1852) every hour.
