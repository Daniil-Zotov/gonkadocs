---
title: "#1067 — bug: ClaimRewards error handling — payout path silently continues on failure"
source: https://github.com/gonka-ai/gonka/issues/1067
issue_number: 1067
synced_at: 2026-07-06T09:52:09Z
template: issues-main.html
---

> 🔄 **Авто-синхронизация:** из [Issue #1067](https://github.com/gonka-ai/gonka/issues/1067) каждые 6 часов. 

# 🔴 bug: ClaimRewards error handling — payout path silently continues on failure

**Автор:** [@Mayveskii](https://github.com/Mayveskii) · **Состояние:** Closed · **Создано:** 2026-04-15 19:40 UTC · **Обновлено:** 2026-04-28 20:55 UTC

**Метки:** `enhancement`

---

## 📝 Описание

## Summary
In `msg_server_claim_rewards.go`, when `PayParticipantFromEscrow` or `PayParticipantFromModule` returns an error, the function logs the error and continues processing instead of returning the error. This can result in partial payouts or silent fund loss when the payment path fails.
## Motivation
This was identified during audit of payout error handling in the inference escrow claims path. The current behavior allows settlement records to be finalized even when underlying payments have failed, making the loss non-recoverable. PR #948 (v0.2.12 upgrade) introduces `CacheContext` to make payouts atomic, confirming the maintainers are aware of this class of issue.
## Impact
- Affected components: `x/inference/keeper/msg_server_claim_rewards.go`
- Who is impacted: Validators and delegators who claim rewards from inference escrow
- Which metric is expected to improve: payout success rate — errors that should halt the transaction are logged and swallowed, resulting in settlements marked complete without actual payment
## Detailed description
- `ClaimRewards` calls `PayParticipantFromEscrow` and `PayParticipantFromModule` to distribute work and reward coins. When either returns an error:
  1. Work payment failure: `k.LogError("Error paying participant from escrow", ...)` is logged, but `finishSettle` is still called, marking the settlement complete even though the participant was never paid.
  2. Reward payment failure: `k.LogError("Error paying participant for rewards", ...)` is logged, but the function continues, potentially completing a partial settlement.
- In both cases, the settlement is finalized regardless of payment success. There is no mechanism to retry failed payments.
- Evidence: PR #948 (CacheContext atomic payouts) addresses this pattern. PR #1013 (escrow fund loss prevention) addresses a related class. PR #1016 (this fix) was previously opened but closed without merge. Сheck it out - https://github.com/gonka-ai/gonka/commit/ec5e453e03b0970ce6c4db1ca4243d0843f57989
## Expected outcome
- `ClaimRewards` should use `CacheContext` to wrap all payout mutations atomically
- If any payment fails, the entire transaction should be rolled back
- The settlement record should persist for retry, not be finalized as complete
- Backward compatible: settlement records that were partially paid remain claimable
## Proposed approach
- Use `CacheContext` for atomic payouts (aligned with PR #948 approach):
  1. Wrap all payment operations in `cacheCtx`
  2. Call `writeFn()` only after all payments succeed
  3. On failure, settlement persists with pending status for retry
- Alternatives considered:
  - Return error immediately on first payment failure (simpler but doesn't allow partial recovery)
  - Add a retry queue for failed payments (over-engineered for this scope)
## External feedback
- Discord thread link: https://discord.com/channels/1336477374442770503/1425189436748206171/1492754655170662431
- Community reviewer(s): Mayveskii

---

## 💬 Комментарии (5)

### Комментарий 1 — [@Doog-bot534](https://github.com/Doog-bot534)

*2026-04-16 03:08 UTC*

This issue aligns with the finding in our security audit (#1053, finding #3) and the fix submitted in PR #1051.

Our PR #1051 takes the simpler approach (return error without calling `finishSettle`), while the `CacheContext` approach described here is more comprehensive and aligned with the pattern in PR #948. Happy to update #1051 to use `CacheContext` if the maintainers prefer that approach.

### Комментарий 2 — [@Mayveskii](https://github.com/Mayveskii)

*2026-04-16 03:37 UTC*

> This issue aligns with the finding in our security audit ([#1053](https://github.com/gonka-ai/gonka/issues/1053), finding [#3](https://github.com/gonka-ai/gonka/pull/3)) and the fix submitted in PR [#1051](https://github.com/gonka-ai/gonka/pull/1051).
> 
> Our PR [#1051](https://github.com/gonka-ai/gonka/pull/1051) takes the simpler approach (return error without calling `finishSettle`), while the `CacheContext` approach described here is more comprehensive and aligned with the pattern in PR [#948](https://github.com/gonka-ai/gonka/pull/948). Happy to update [#1051](https://github.com/gonka-ai/gonka/pull/1051) to use `CacheContext` if the maintainers prefer that approach.



Thanks for the context and the alignment with #1053 finding #3.
For the maintainers' visibility: the fix proposed in this issue and the approach in PR #1051 were already proposed and implemented in commit ec5e453 (https://github.com/gonka-ai/gonka/commit/ec5e453) and PR #1016 (https://github.com/gonka-ai/gonka/pull/1016) (opened Apr 5, closed without merge). It is closed cause of terms of visibily bugs finding that the team set in contrib proccess. That commit predates PR #1051 by 10 days and includes both the error propagation fix and a unit test (TestClaimRewards_PayoutRewardFailure_RollsBackState).
The approach in ec5e453 goes further than just removing finishSettle:
1. ClaimRewards: return payoutResponse, nil → return nil, payoutErr — the critical line that enables full TX rollback
2. payoutClaim reward failure: finishSettle removed, response changed to Amount: 0, Result: "Claim payout failed, no funds moved." — no partial success signal
3. handleUnderfundedWork: finishSettle removed — Cosmos SDK rollback preserves SettleAmount for retry
4. Unit test: verifies error propagation and that SettleAmount remains in store after failure
Happy to re-submit as a new PR from Mayveskii/gonka if the maintainers prefer the full approach.
Regarding the label — this is a bug (fund loss on payment failure), not an enhancement. Could a maintainer update the label from enhancement to bug?

### Комментарий 3 — [@Doog-bot534](https://github.com/Doog-bot534)

*2026-04-16 12:09 UTC*

Good catch on the timeline — I wasn't aware of PR #1016 and commit ec5e453 when I filed #1051. My fix came independently from the audit in #1053 (finding #3), but yours clearly predates it and covers more ground (full TX rollback + unit test). Happy to defer to whichever approach the maintainers prefer. Agreed this should be labeled as bug, not enhancement.

### Комментарий 4 — [@Mayveskii](https://github.com/Mayveskii)

*2026-04-28 19:09 UTC*

@x0152 watch out this one , please 

### Комментарий 5 — [@x0152](https://github.com/x0152)

*2026-04-28 20:55 UTC*

There were additional non-atomic paths, and they were fully addressed in #789

Closing as resolved
