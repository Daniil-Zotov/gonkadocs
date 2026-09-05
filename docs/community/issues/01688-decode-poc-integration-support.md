---
title: "#1688 — Decode PoC: integration support"
source: https://github.com/gonka-ai/gonka/issues/1688
issue_number: 1688
synced_at: 2026-09-05T01:04:07Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Decode PoC: integration support
    <span class="issues-number">#1688</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-08-31 20:15 UTC</span>
    <span class="issues-meta-item">3 comments</span>
    <span class="issues-meta-item">Updated 2026-09-04 20:16 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
Integration of Decode PoC with the current chain and MLNode path. Design and seeding questions stay on this issue. Verification of the current MiniMax implementation on a full image is #1689. DeepSeek thresholds and the DeepSeek seeding scheme are #1690.

**Integration**
— Current Decode PoC path is written up (what is in production shape, what is still experimental)
— Integration points with MLNode and the epoch cycle are listed
— Open questions on the Decode PoC design are listed in notes on this issue, not only off-thread

**DeepSeek expert seeding**
DeepSeek seeding is more complex than MiniMax. This issue covers the integration discussion; the scheme fix itself is #1690.
— Expert seeding for DeepSeek is described (how experts are chosen, what the current scheme does)
— Weight distribution across seeded experts is measured
— A closer-to-uniform distribution across seeded experts is proposed, with notes if uniform is not possible

**Experiments (when the checklist on this issue is enough to run them)**
- [ ] Нardware used is written up
- [ ] Models used are written up
- [ ] What passed / what did not is written up, with links to notebooks or logs
</div>

---

## 💬 Comments (3)

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
    <span class="issues-meta-item">commented 2026-08-31 20:26 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>ty</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/baychak">@baychak</a></span>
    <span class="issues-meta-item">commented 2026-09-04 20:07 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p><strong>Status:</strong> in progress. The code lives on our forks as a residual/plugin pair; the design questions were still off-thread, and this comment moves them here.</p>
<p><strong>Where the work is</strong></p>
<table>
<thead>
<tr>
<th></th>
<th>branch on our fork</th>
<th>PR</th>
<th>lands in</th>
</tr>
</thead>
<tbody>
<tr>
<td>residual</td>
<td><code>kaitakuai/vllm : mixed-poc-vllm-0.25.1-dev</code></td>
<td>gonka-ai/vllm#100</td>
<td><code>release/v0.25.1-decode-int</code></td>
</tr>
<tr>
<td>plugin</td>
<td><code>kaitakuai/gonka-vllm-plugins : mixed-poc-vllm-0.25.1-dev</code></td>
<td>gonka-ai/gonka-vllm-plugins#8</td>
<td><code>decode-poc-int</code></td>
</tr>
</tbody>
</table>
<p>Development is easier on the forks, so both intake branches @vbgd0 created are still where they were on 2026-08-13.</p>
<p><strong>Since last</strong></p>
<ul>
<li>@vbgd0 has been pushing directly into both PR branches: 6 commits on the residual, 14 on the plugin, latest 2026-09-02. Not only cleanup — the PoC artifact payload gained <code>n_nan_steps</code> and the max mismatch margin, and decode validation gained a nonce-level snap-margin stat test.</li>
<li>gonka-ai/vllm#100 points at exactly our working residual branch — no divergence. gonka-ai/gonka-vllm-plugins#8 is 41 commits behind our working plugin branch; nothing of his work is lost, ours is a strict superset. We will refresh it.</li>
<li>Zero review comments on either PR.</li>
</ul>
<p><strong>Open design questions</strong></p>
<ol>
<li>Backward compatibility — keep the old prefill PoC untouched behind a flag, or accept that artifacts stop being cross-verifiable.</li>
<li>How DeepSeek seeding should treat the hash-routed layers.</li>
<li>Sign-off on the new consensus constants — @axeltec-gonka owns them; not given.</li>
</ol>
<p><strong>Next:</strong> refresh gonka-ai/gonka-vllm-plugins#8 onto the current plugin branch — update here by 2026-09-05.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1688](https://github.com/gonka-ai/gonka/issues/1688) every hour.
