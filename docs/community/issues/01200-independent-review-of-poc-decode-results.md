---
title: "#1200 — Independent review of PoC-decode results"
source: https://github.com/gonka-ai/gonka/issues/1200
issue_number: 1200
synced_at: 2026-07-28T12:17:33Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Independent review of PoC-decode results
    <span class="issues-number">#1200</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-05-19 23:36 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-05-19 23:36 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #4cbc0f; color: #24292f; border-color: #4cbc0f;">up-for-grabs</span></div>
</div>

<div class="issues-content" markdown="1">
Independently review and re-check the PoC-decode approach from https://github.com/gonka-ai/gonka/issues/1135 and the Axel-T experiments.

Current PoC correlates reasonably well with inference compute, but memory-usage coverage can be improved. The concern is that specialized versions could significantly accelerate PoC without equivalently improving real inference.

PoC-decode proposes extending Proof-of-Compute from prefill to decode steps.

Context

Relevant materials:

* Main issue: https://github.com/gonka-ai/gonka/issues/1135
* Presentation: https://docs.google.com/presentation/d/11zXgKd8q3t7SZ_wqfiMvCqTWqiKxJw65AFmAWDnMcL8/edit
* Experiment artifacts: https://drive.google.com/drive/folders/1tVh6mTsazMfjtSz-J0MTN8KYD5B9g1Bq
* Implementation branch: https://github.com/axeltec-software/vllm/tree/axeltec/poc-decode-proposal

Please use these materials as the source of truth.

## Task

Review the PoC-decode proposal and independently re-check the results.

The task should be treated as a critical review, not just a confirmation that the implementation runs.

## Review scope

Please check:

1. Whether the results from #1135 are reproducible.
2. Whether the hypothesis is confirmed beyond the initial experiments.
3. Whether the method should be tested on different models.
4. Whether the implementation can be integrated into the current vLLM path if the results are confirmed.
5. What makes migration painful and how to reduce that pain.
6. Whether a safer rollout can start only with new models.

## Review points

1. Re-check the reported results

Review the experiments from #1135 and the linked Axel-T materials.

Confirm whether the reported PoC-decode results hold under independent review.

2. Validate on different models

The current experiments provide the first confirmation of the hypothesis, but independent confirmation on different models is required before integration decisions.

Please identify and run, or define, the minimum additional model checks needed.

3. Review the implementation branch

Review the Axel-T vLLM branch:

https://github.com/axeltec-software/vllm/tree/axeltec/poc-decode-proposal

Check whether the implementation matches the method described in #1135 and whether it can be prepared for integration into the current vLLM path if the hypothesis is confirmed.

4. Review migration impact

Migration may be painful.

Please identify:

* what makes migration difficult;
* what can be done to reduce migration pain;
* whether rollout can start only with new models;
* what should be avoided during initial rollout.

5. Critical risk review

Risk level is medium: there is an initial positive signal, but the method still needs an honest critical review.

Please document:

* what is confirmed;
* what is not confirmed yet;
* what requires more experiments;
* what could block integration.

## Notes

This task is about independent verification and critical review.
If the results are confirmed on different models, the next step can be integration into the current vLLM path.
</div>

---

> 🔄 **Auto-synced** from [Issue #1200](https://github.com/gonka-ai/gonka/issues/1200) every hour.
