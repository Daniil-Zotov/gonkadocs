---
title: "#804 — [P0?] Extend dev and TA signature payloads"
source: https://github.com/gonka-ai/gonka/issues/804
issue_number: 804
synced_at: 2026-07-26T11:39:46Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    [P0?] Extend dev and TA signature payloads
    <span class="issues-number">#804</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/DimaOrekhovPS">@DimaOrekhovPS</a> opened 2026-02-25 20:49 UTC</span>
    <span class="issues-meta-item">2 comments</span>
    <span class="issues-meta-item">Updated 2026-05-21 21:05 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
### Dev signature

Currently signs: `original_prompt_hash + timestamp + ta_address`.

Add `model` to prevent a TA or executor from redirecting the inference to a different model after the developer signed. The cross-message comparison catches model mismatches today, but the first message accepts any model without cryptographic proof of developer intent.

New payload: `original_prompt_hash + timestamp + ta_address + model`.

### TA signature

Currently signs: `prompt_hash + timestamp + ta_address + executor_address`.

Add `inferenceId` and `original_prompt_hash` to bind the TA signature to a specific inference request. Without these, an executor could replay a valid TA signature from one inference onto a different inference that shares the same `prompt_hash`, `timestamp`, and addresses.

New payload: `prompt_hash + timestamp + ta_address + executor_address + inferenceId + original_prompt_hash`.

### Changes required

- Update `getDevSignatureComponents` / `getFinishDevSignatureComponents`
- Update `getTASignatureComponents` / `getFinishTASignatureComponents`
- Update corresponding comparison functions
- Coordinate with off-chain signing code (TA and dev) to match new payload formats

</div>

---

## 💬 Comments (2)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/tcharchian">@tcharchian</a></span>
    <span class="issues-meta-item">commented 2026-03-21 00:13 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Per discussion with @DimaOrekhovPS, this issue may become irrelevant after v0.2.12 and depends on whether we fully switch to the new inference system in the next upgrade or not, wdyt @0xgonka @gmorgachev?</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/0xgonka">@0xgonka</a></span>
    <span class="issues-meta-item">commented 2026-03-21 07:45 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>security-wise it is important someone can't just use a dev signature from another inference. I am not sure what PR in 0.2.12 makes this irrelevant but would be happy to take a look if someone can point me in that direction</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #804](https://github.com/gonka-ai/gonka/issues/804) every hour.
