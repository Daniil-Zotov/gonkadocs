---
title: "#803 — Punish TA on signature/component mismatch"
source: https://github.com/gonka-ai/gonka/issues/803
issue_number: 803
synced_at: 2026-07-26T00:17:20Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Punish TA on signature/component mismatch
    <span class="issues-number">#803</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/DimaOrekhovPS">@DimaOrekhovPS</a> opened 2026-02-25 20:47 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-05-25 19:10 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
When cross-message comparison detects a mismatch in TA-signed components (`prompt_hash`, `request_timestamp`, `transfer_agent`, `executor`), the Transfer Agent should be penalized.

### Context

Currently, mismatches in `compareStartTAComponents` / `compareFinishTAComponents` return an error and reject the message, but no slashing or reputation penalty is applied to the TA.

### Scenarios where TA is at fault

- **Start-first flow:** Finish arrives with a different `prompt_hash` than what start persisted. If TA signature on the finish message is valid, the TA signed a different prompt — TA is the cheater.
- **Finish-first flow:** Start arrives with a different `prompt_hash`. The TA submitted inconsistent data across messages — TA is the cheater.

### Requirements

- On TA component mismatch, re-verify the TA signature to confirm the TA actually signed the mismatched data (vs executor tampering).
- If TA signature is valid against the mismatched components, apply slashing/reputation penalty to the TA.
- If TA signature is invalid, the executor submitted forged data — penalize executor instead.

</div>

---

> 🔄 **Auto-synced** from [Issue #803](https://github.com/gonka-ai/gonka/issues/803) every hour.
