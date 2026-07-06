---
title: "#927 — [P1] Maintenance window for hosts"
source: https://github.com/gonka-ai/gonka/issues/927
issue_number: 927
synced_at: 2026-07-06T09:51:52Z
template: issues-main.html
---

> 🔄 **Auto-synced:** from [Issue #927](https://github.com/gonka-ai/gonka/issues/927) every 6 hours. 

# 🔴 [P1] Maintenance window for hosts

**Author:** [@tcharchian](https://github.com/tcharchian) · **State:** Closed · **Created:** 2026-03-20 23:39 UTC · **Updated:** 2026-06-22 01:35 UTC

**Labels:** `enhancement`

**Веха:** v0.2.14

---

## 📝 Описание

The proposal is described here https://github.com/gonka-ai/gonka/blob/22639fe25aada8090d971402e136714fa9c3b0e7/proposals/maintenance-windows/maintenance-windows.md

The preliminary implementation plan is outlined here https://github.com/gonka-ai/gonka/commit/219e975ae1b8a74d895e6a09ab5a26f629efd6f3, but it would be great if you could review it with a critical eye and suggest your own implementation approach based on your experience  

---

## 💬 Comments (3)

### Комментарий 1 — [@Ryanchen911](https://github.com/Ryanchen911)

*2026-03-30 08:54 UTC*

Hi @tcharchian ,

Thanks for the proposal! We've reviewed the preliminary implementation plan and noticed some gaps regarding the state transitions. Our feedback is as follows:

# D1 — Missing BeginBlocker state machine for reservation lifecycle

**Proposal says:** Reservations have four statuses: Scheduled, Active, Completed, Canceled.

**Problem:** The proposal never describes **who transitions reservations between states and when**. There is no description of a BeginBlocker (or EndBlocker) that:
- Transitions SCHEDULED → ACTIVE when `block_height >= start_height`
- Transitions ACTIVE → COMPLETED when `block_height >= start_height + duration_blocks`

The task plan also has no task for this state machine.

---

# D2 — Epoch-critical phase conflicts not addressed

**Proposal says:** Seven validation rules for `MsgScheduleMaintenance`. None mention epoch phase timing.

**Problem:** Two epoch phases are safety-critical and must not overlap with maintenance windows:

1. **PoC commit window [E+0, E+35]**: A participant in maintenance during this phase cannot submit their PoC commit, causing them to be silently excluded from the next epoch's `activeParticipants`. This directly violates Goal 4 ("Preserve participant participation in epoch structure without removing the participant from epoch groups").

2. **DKG phase [E+277, E+285]**: DKG has no recovery path. A participant missing DKG participation can cause the next epoch to fail to start — a consensus-level fault with no graceful fallback.

The restricted range is only 43 blocks out of a ~15,391 block epoch (~0.3%), so the operational cost is minimal.

**Recommendation:** Add two scheduling rejection rules:
- `ErrMaintenanceOverlapsPoCPhase`: Reject if window overlaps [E+0, E+35]
- `ErrMaintenanceOverlapsDKGPhase`: Reject if window overlaps [E+277, E+285]

---

# D3 — Credit storage: Participant record vs independent KV bucket

**Proposal says:** "Maintenance credit should be stored on the participant record itself as a field measured in blocks. This proposal prefers extending the existing participant record over introducing a separate maintenance-credit table."

**Divergence:** Use an independent `MaintenanceCreditPrefix` KV bucket, separate from `Participant`.

**Rationale:** `Participant` is the hottest object in the system — it is read and written on every status transition (`UpdateParticipantStatus`), every inference timeout (`handleExpiredInferenceWithContext`), and every epoch settlement. Coupling a low-frequency credit field to it means every credit update touches this hot object, and vice versa. An independent bucket decouples the two write paths, reduces write amplification, and allows independent testing. The cost is one additional store lookup per credit operation.

---

# D4 — Concurrency re-check at activation time

**Proposal says:** "The first version should evaluate concurrency only at scheduling time, not at activation time. This choice favors determinism and operator predictability."

**Divergence:** Re-check concurrency caps at activation time in the BeginBlocker.

**Rationale:** Governance can lower `max_concurrent_participants` or `max_concurrent_power_fraction` between scheduling and activation. Without a re-check, windows scheduled under old caps silently violate new parameters. The proposal itself flags this as "a possible attack surface or policy edge case" for later review.

**However**, hard cancellation at activation time creates a different problem: the operator has already arranged physical maintenance (host reboot, kernel upgrade). A last-minute cancellation forces them to either proceed with maintenance and accept penalties, or scramble to abort physical work.

**Recommendation:** Re-check at activation time, but on failure: **emit a warning event and activate anyway**, rather than cancel. This provides monitoring visibility for governance without breaking operator predictability. Hard cancellation should only be considered if a stronger safety argument emerges.

---

# D5 — Credit accrual during maintenance epochs

**Proposal says:** "Maintenance does not pause rewards or maintenance-credit earning." Listed as Open Issue #2: may create incentives to maximize maintenance usage.

**Divergence:** A `used_this_epoch` flag prevents credit accrual in any epoch where a maintenance window was activated.

**Rationale:** With `credit_per_epoch = 500` and `max_duration_blocks = 3000`, an operator using maximum windows has a net credit loss per use (spend 3000, earn 500, net −2500). However, if credit accrues during maintenance epochs, an operator using small windows can theoretically never deplete their credit — always staying under maintenance coverage. This is exactly the risk the proposal flags in Open Issue #2.

Blocking credit accrual in maintenance epochs closes this path: every maintenance use has a net credit cost, making the system self-balancing without requiring fine-tuning of duration caps. The trade-off is that legitimate operators lose one credit accrual opportunity per maintenance use, but this is arguably a fair cost for the exemption they receive.



### Комментарий 2 — [@patimen](https://github.com/patimen)

*2026-03-30 23:30 UTC*

# Maintenance Windows Proposal - Feedback Response Summary

Thanks for the review. We updated the proposal and task plan based on your feedback.

## Changes We Made

### D1: Reservation lifecycle state machine

Accepted.

We updated the proposal to make reservation lifecycle transitions explicit and block-driven:

1. `Scheduled -> Active` in `BeginBlock` when `block_height == start_height`
2. `Active -> Completed` in `BeginBlock` when `block_height == start_height + duration_blocks`

We also updated the task plan to add explicit lifecycle implementation work and called out that the lookup path must be fast enough for begin-block execution.

We also tightened the proposal to require exact-height `BeginBlock` transitions and bounded lookup behavior, while moving the concrete storage/index format into the task plan.

### D2: Epoch-critical phase conflicts

Accepted.

We added explicit scheduling rejection rules for windows that overlap:

1. The PoC commit / exchange phase
2. The DKG phase

We also updated the task plan to add explicit implementation work for these scheduling rejections and their corresponding query behavior.

### D3: Credit storage layout

Accepted.

We changed the proposal from storing maintenance credit on the participant record to using a dedicated per-participant `MaintenanceState`, keyed by participant address and separate from the hot participant object.

`MaintenanceState` now carries both:

1. Maintenance credit
2. The last epoch in which maintenance was activated
3. The active reservation reference, if any
4. The next scheduled reservation reference, if any

This keeps maintenance accounting decoupled from the participant record without splitting it into multiple fragmented per-participant maintenance buckets.

We also added a new rule that a participant may have at most one future scheduled maintenance window at a time.

### D4: Activation-time concurrency re-check

Accepted with a clarification.

We updated the proposal to re-check concurrency caps at activation time in `BeginBlock`, but we are not hard-canceling windows at activation.

If a reservation activates under current params that would now exceed caps:

1. The reservation still activates
2. A warning event is emitted
3. Advisory warning / violation metadata is stored on the reservation so it is queryable later

This preserves operator predictability while making governance drift visible.

### D5: Credit accrual during maintenance-used epochs

Accepted.

We updated the proposal so that:

1. Ordinary reward eligibility remains unchanged
2. Maintenance-credit accrual is suppressed in any epoch where a maintenance window was activated for that participant

This makes every maintenance use have a net credit cost and resolves the original self-replenishing-credit concern.

## Additional Notes

We also added the following clarifications while incorporating the feedback:

1. The `BeginBlock` lifecycle and lookup path must use direct keyed Cosmos SDK collections access rather than broad iteration.
2. Activation-time warnings are not event-only; they are also made queryable on the reservation itself.
3. The task plan now includes explicit work in both the maintained Cosmos SDK fork and the inference-chain repo.
4. The task plan now includes end-to-end coverage for the restricted PoC / DKG scheduling rules.
5. The proposal now states required performance properties at a high level, while the task plan carries the concrete storage and index layout.
6. The task plan now explicitly separates:
   - exact-height transition schedule for `BeginBlock`
   - start-height overlap index for scheduling-time range scans

## Updated Documents

The following documents were updated:

1. `proposals/maintenance-windows/maintenance-windows.md`
2. `proposals/maintenance-windows/maintenance-windows-todo.md`


### Комментарий 3 — [@Ryanchen911](https://github.com/Ryanchen911)

*2026-04-01 03:45 UTC*

works in progress
