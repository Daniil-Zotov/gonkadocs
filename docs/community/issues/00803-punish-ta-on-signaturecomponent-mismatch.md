---
title: "#803 — Punish TA on signature/component mismatch"
source: https://github.com/gonka-ai/gonka/issues/803
issue_number: 803
synced_at: 2026-07-06T09:51:58Z
template: issues-main.html
---

> 🔄 **Auto-synced:** from [Issue #803](https://github.com/gonka-ai/gonka/issues/803) every 6 hours. 

# 🔴 Punish TA on signature/component mismatch

**Author:** [@DimaOrekhovPS](https://github.com/DimaOrekhovPS) · **State:** Closed · **Created:** 2026-02-25 20:47 UTC · **Updated:** 2026-05-25 19:10 UTC

---

## 📝 Описание

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

