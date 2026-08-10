---
title: "#1570 — Devshard: timeout-vote threshold unreachable under skewed slot distribution — stranded nonce cannot be resolved (liveness)"
source: https://github.com/gonka-ai/gonka/issues/1570
issue_number: 1570
synced_at: 2026-08-10T12:03:10Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Devshard: timeout-vote threshold unreachable under skewed slot distribution — stranded nonce cannot be resolved (liveness)
    <span class="issues-number">#1570</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/kAIPraxisBot">@kAIPraxisBot</a> opened 2026-08-09 16:18 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-08-09 16:18 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

When a Devshard escrow's slots are distributed unevenly across participants, the **timeout-vote path can become structurally unable to reach its weight threshold**, leaving a stranded nonce permanently unresolved. This is a liveness issue: the escrow's inference cannot be timed out / resolved, and a single participant holding a large slot share can (deliberately or by going offline) deadlock timeout resolution for nonces it is involved in.

## Observed

```
nonce stranded            nonce=681  role=speculative
timeout_started           nonce=681  reason=refused
timeout_vote_requested    → mtd2v4zr, 9ulzldum
timeout_vote_result       9ulzldum  accept  weight=1  running=1  threshold=8
timeout_vote_result       mtd2v4zr  accept  weight=2  running=3  threshold=8
timeout_vote_tally        accept=2 weight=3 threshold=8 verifiers=2 sufficient=false
timeout_insufficient_votes
```

Two verifiers responded with combined weight 3; the threshold is 8; the remaining ~13 weight is held by the participant that does not vote → `sufficient=false` and the nonce stays stranded.

## Root cause

- A participant's timeout-vote weight equals its **slot count** in the escrow group (`devshard/state/machine.go` — `AddressSlotCount` / `addressToSlotCount`). Slot distribution across participants can be highly skewed (e.g. `1 / 2 / 13` across three participants of a 16-slot group).
- The timeout threshold is a **fixed fraction of the total group slot weight**: `ComputeVoteThreshold(groupSize, VoteThresholdFactor)` with `VoteThresholdFactor = 50` → `groupSize/2` (for a 16-slot group, threshold = 8). (Finalize quorum separately uses `QuorumThreshold() = 2*totalSlots/3 + 1`, `devshard/state/machine.go:1424`.)
- The tally (`devshard/user/session.go`, ~L2147) accumulates only the weight of verifiers that actually respond/accept and requires `accWeight > voteThreshold`; on failure it emits `timeout_insufficient_votes` (`session.go:1904`) and the nonce remains stranded.

**The structural gap:** the denominator is the *full* group weight, but the participant whose nonce is being timed out (or any absent large-share participant) is exactly the one not contributing votes. If that participant holds a slot share ≥ `total − threshold` (here 13 ≥ 16 − 8), the honest, reachable remainder holds ≤ threshold weight and **can never reach it**, regardless of correctness. Timeout resolution is then impossible.

## Impact

- **Liveness:** a stranded/refused nonce that needs a timeout vote can never be resolved → the escrow's progress stalls on that nonce.
- **Griefing vector:** a participant assigned a large slot share can strand nonces it is involved in simply by not voting (or going offline), and the remaining verifiers cannot meet the threshold to time it out.

## Suggested direction

- Compute the timeout threshold relative to the **eligible/responsive verifier weight for that specific nonce**, excluding the subject (timed-out) participant's slots from the denominator; or
- add a **fallback resolution** when the reachable verifier set cannot structurally reach the threshold (so a single large-share or absent participant cannot deadlock timeout resolution); and/or
- bound slot-share skew at escrow creation so no single participant can hold ≥ `total − threshold` of the slots.

</div>

---

> 🔄 **Auto-synced** from [Issue #1570](https://github.com/gonka-ai/gonka/issues/1570) every hour.
