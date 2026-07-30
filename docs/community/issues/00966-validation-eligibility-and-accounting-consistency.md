---
title: "#966 — Validation Eligibility and Accounting Consistency"
source: https://github.com/gonka-ai/gonka/issues/966
issue_number: 966
synced_at: 2026-07-30T09:46:58Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    Validation Eligibility and Accounting Consistency
    <span class="issues-number">#966</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/akup">@akup</a> opened 2026-03-27 13:43 UTC</span>
    <span class="issues-meta-item">1 comment</span>
    <span class="issues-meta-item">Updated 2026-04-03 10:10 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #d73a4a; color: #ffffff; border-color: #d73a4a;">bug</span> <span class="issues-label" style="background-color: #a2eeef; color: #24292f; border-color: #a2eeef;">enhancement</span></div>
</div>

<div class="issues-content" markdown="1">
# Validation Eligibility and Accounting Consistency

Work on Inferences and Validations on current version is now legacy. All future work will be concentrated on devnets (shardchains). This PR shouldn't be high priority or probably should be closed in nearest future.
It was useful to see issues that should be handled in devchains

## Summary

This branch fixes a cumulative protocol issue across validation lifecycle, validator eligibility, and claim accounting. Before these changes, a non-settled participant could still attempt validation/revalidation, multi-address participants could bypass intent of own-inference restrictions, already-decided inferences could be re-processed in edge cases, and claim accounting around invalidation/revalidation was vulnerable to expensive or inconsistent handling.

## Motivation

This matters now because revalidation is expensive, and stricter status guards (`VALIDATED` / `VOTING`) require strict eligibility enforcement to avoid unauthorized heavy paths. At the same time, claim checks must remain both correct and performant under epoch-scale load.

## Impact

- Affected components: `x/inference/keeper/msg_server_validation.go`, `x/inference/keeper/msg_server_claim_rewards.go`, revalidation collections in keeper, seed-based settlement checks.
- Who is impacted (developers, hosts): core protocol developers, validators/hosts, node operators, and participants whose rewards depend on correct claim accounting.
- Which metric is expected to improve and how much: unauthorized validation/revalidation acceptance is expected to drop to zero for post-rollout strict mode; claim-path overhead is reduced by avoiding per-inference `GetInference(...)` scans in the hot validation-credit path.

## Detailed description

- How issue impact was measured/confirmed:
  - Validation flow analysis showed eligibility was not always tied to settled validator evidence.
  - Multi-address threat analysis showed own-inference protection can be bypassed without eligibility binding.
  - Runtime behavior and tests confirm status-guard semantics and claim-path behavior.
- Links to evidence:
  - [PR #832: VALIDATED/VOTING status guard logic and discussion](https://github.com/gonka-ai/gonka/pull/832)

UPDATE:
  [PR #829: INVALIDATED-related claim accounting discussion](https://github.com/gonka-ai/gonka/pull/829/changes) was referenced but it was my mistake. It seams it should be handled in other way. See discussion on that PR

## Expected outcome

When done:

- Only settled, eligible validators can validate or revalidate.
- Unauthorized revalidation initiation is blocked.
- Already-decided inference states are protected from duplicate first-time processing.
- Compatibility expectations: backward compatible with staged rollout. Behavior tightening for missing-seed eligibility checks becomes strict in stage 2.

## Proposed approach

- High-level plan:
  - Keep status guards for finalized states from [#832](https://github.com/gonka-ai/gonka/pull/832).
  - Enforce eligibility via chain-level seed settlement evidence.
- Migration or rollout plan:
  - Stage 1: transition epoch post-upgrade, seeds may be absent, temporary skip path exists in validation eligibility check.
  - Stage 2: after seed population, missing seed becomes hard error and strict eligibility is enforced.

## External feedback (optional but recommended)

- Community reviewer(s): references from [#832](https://github.com/gonka-ai/gonka/pull/832).

</div>

---

## 💬 Comments (1)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/akup">@akup</a></span>
    <span class="issues-meta-item">commented 2026-04-03 10:10 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Issue should be closed, because now all focus is moving to devshards. Moreover here seed is revealed, but current protocol version doesn't protect from seed early revealing, and some party can cheat with inferenceIds</p>
<p>@0xMayoor let's accept your PR https://github.com/gonka-ai/gonka/pull/832</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #966](https://github.com/gonka-ai/gonka/issues/966) every hour.
