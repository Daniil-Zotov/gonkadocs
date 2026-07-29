---
title: "#927 — [P1] Maintenance window for hosts"
source: https://github.com/gonka-ai/gonka/issues/927
issue_number: 927
synced_at: 2026-07-29T22:17:07Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-closed"><svg viewBox="0 0 16 16"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"/></svg></span>
    [P1] Maintenance window for hosts
    <span class="issues-number">#927</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Closed</span>
    <span class="issues-meta-item"><a href="https://github.com/tcharchian">@tcharchian</a> opened 2026-03-20 23:39 UTC</span>
    <span class="issues-meta-item">3 comments</span>
    <span class="issues-meta-item">Updated 2026-06-22 01:35 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"><span class="issues-label" style="background-color: #a2eeef; color: #24292f; border-color: #a2eeef;">enhancement</span></div>
</div>

<div class="issues-content" markdown="1">
The proposal is described here https://github.com/gonka-ai/gonka/blob/22639fe25aada8090d971402e136714fa9c3b0e7/proposals/maintenance-windows/maintenance-windows.md

The preliminary implementation plan is outlined here https://github.com/gonka-ai/gonka/commit/219e975ae1b8a74d895e6a09ab5a26f629efd6f3, but it would be great if you could review it with a critical eye and suggest your own implementation approach based on your experience  
</div>

---

## 💬 Comments (3)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Ryanchen911">@Ryanchen911</a></span>
    <span class="issues-meta-item">commented 2026-03-30 08:54 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Hi @tcharchian ,</p>
<p>Thanks for the proposal! We've reviewed the preliminary implementation plan and noticed some gaps regarding the state transitions. Our feedback is as follows:</p>
<h1>D1 — Missing BeginBlocker state machine for reservation lifecycle</h1>
<p><strong>Proposal says:</strong> Reservations have four statuses: Scheduled, Active, Completed, Canceled.</p>
<p><strong>Problem:</strong> The proposal never describes <strong>who transitions reservations between states and when</strong>. There is no description of a BeginBlocker (or EndBlocker) that:
- Transitions SCHEDULED → ACTIVE when <code>block_height &gt;= start_height</code>
- Transitions ACTIVE → COMPLETED when <code>block_height &gt;= start_height + duration_blocks</code></p>
<p>The task plan also has no task for this state machine.</p>
<hr />
<h1>D2 — Epoch-critical phase conflicts not addressed</h1>
<p><strong>Proposal says:</strong> Seven validation rules for <code>MsgScheduleMaintenance</code>. None mention epoch phase timing.</p>
<p><strong>Problem:</strong> Two epoch phases are safety-critical and must not overlap with maintenance windows:</p>
<ol>
<li>
<p><strong>PoC commit window [E+0, E+35]</strong>: A participant in maintenance during this phase cannot submit their PoC commit, causing them to be silently excluded from the next epoch's <code>activeParticipants</code>. This directly violates Goal 4 ("Preserve participant participation in epoch structure without removing the participant from epoch groups").</p>
</li>
<li>
<p><strong>DKG phase [E+277, E+285]</strong>: DKG has no recovery path. A participant missing DKG participation can cause the next epoch to fail to start — a consensus-level fault with no graceful fallback.</p>
</li>
</ol>
<p>The restricted range is only 43 blocks out of a ~15,391 block epoch (~0.3%), so the operational cost is minimal.</p>
<p><strong>Recommendation:</strong> Add two scheduling rejection rules:
- <code>ErrMaintenanceOverlapsPoCPhase</code>: Reject if window overlaps [E+0, E+35]
- <code>ErrMaintenanceOverlapsDKGPhase</code>: Reject if window overlaps [E+277, E+285]</p>
<hr />
<h1>D3 — Credit storage: Participant record vs independent KV bucket</h1>
<p><strong>Proposal says:</strong> "Maintenance credit should be stored on the participant record itself as a field measured in blocks. This proposal prefers extending the existing participant record over introducing a separate maintenance-credit table."</p>
<p><strong>Divergence:</strong> Use an independent <code>MaintenanceCreditPrefix</code> KV bucket, separate from <code>Participant</code>.</p>
<p><strong>Rationale:</strong> <code>Participant</code> is the hottest object in the system — it is read and written on every status transition (<code>UpdateParticipantStatus</code>), every inference timeout (<code>handleExpiredInferenceWithContext</code>), and every epoch settlement. Coupling a low-frequency credit field to it means every credit update touches this hot object, and vice versa. An independent bucket decouples the two write paths, reduces write amplification, and allows independent testing. The cost is one additional store lookup per credit operation.</p>
<hr />
<h1>D4 — Concurrency re-check at activation time</h1>
<p><strong>Proposal says:</strong> "The first version should evaluate concurrency only at scheduling time, not at activation time. This choice favors determinism and operator predictability."</p>
<p><strong>Divergence:</strong> Re-check concurrency caps at activation time in the BeginBlocker.</p>
<p><strong>Rationale:</strong> Governance can lower <code>max_concurrent_participants</code> or <code>max_concurrent_power_fraction</code> between scheduling and activation. Without a re-check, windows scheduled under old caps silently violate new parameters. The proposal itself flags this as "a possible attack surface or policy edge case" for later review.</p>
<p><strong>However</strong>, hard cancellation at activation time creates a different problem: the operator has already arranged physical maintenance (host reboot, kernel upgrade). A last-minute cancellation forces them to either proceed with maintenance and accept penalties, or scramble to abort physical work.</p>
<p><strong>Recommendation:</strong> Re-check at activation time, but on failure: <strong>emit a warning event and activate anyway</strong>, rather than cancel. This provides monitoring visibility for governance without breaking operator predictability. Hard cancellation should only be considered if a stronger safety argument emerges.</p>
<hr />
<h1>D5 — Credit accrual during maintenance epochs</h1>
<p><strong>Proposal says:</strong> "Maintenance does not pause rewards or maintenance-credit earning." Listed as Open Issue #2: may create incentives to maximize maintenance usage.</p>
<p><strong>Divergence:</strong> A <code>used_this_epoch</code> flag prevents credit accrual in any epoch where a maintenance window was activated.</p>
<p><strong>Rationale:</strong> With <code>credit_per_epoch = 500</code> and <code>max_duration_blocks = 3000</code>, an operator using maximum windows has a net credit loss per use (spend 3000, earn 500, net −2500). However, if credit accrues during maintenance epochs, an operator using small windows can theoretically never deplete their credit — always staying under maintenance coverage. This is exactly the risk the proposal flags in Open Issue #2.</p>
<p>Blocking credit accrual in maintenance epochs closes this path: every maintenance use has a net credit cost, making the system self-balancing without requiring fine-tuning of duration caps. The trade-off is that legitimate operators lose one credit accrual opportunity per maintenance use, but this is arguably a fair cost for the exemption they receive.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/patimen">@patimen</a></span>
    <span class="issues-meta-item">commented 2026-03-30 23:30 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <h1>Maintenance Windows Proposal - Feedback Response Summary</h1>
<p>Thanks for the review. We updated the proposal and task plan based on your feedback.</p>
<h2>Changes We Made</h2>
<h3>D1: Reservation lifecycle state machine</h3>
<p>Accepted.</p>
<p>We updated the proposal to make reservation lifecycle transitions explicit and block-driven:</p>
<ol>
<li><code>Scheduled -&gt; Active</code> in <code>BeginBlock</code> when <code>block_height == start_height</code></li>
<li><code>Active -&gt; Completed</code> in <code>BeginBlock</code> when <code>block_height == start_height + duration_blocks</code></li>
</ol>
<p>We also updated the task plan to add explicit lifecycle implementation work and called out that the lookup path must be fast enough for begin-block execution.</p>
<p>We also tightened the proposal to require exact-height <code>BeginBlock</code> transitions and bounded lookup behavior, while moving the concrete storage/index format into the task plan.</p>
<h3>D2: Epoch-critical phase conflicts</h3>
<p>Accepted.</p>
<p>We added explicit scheduling rejection rules for windows that overlap:</p>
<ol>
<li>The PoC commit / exchange phase</li>
<li>The DKG phase</li>
</ol>
<p>We also updated the task plan to add explicit implementation work for these scheduling rejections and their corresponding query behavior.</p>
<h3>D3: Credit storage layout</h3>
<p>Accepted.</p>
<p>We changed the proposal from storing maintenance credit on the participant record to using a dedicated per-participant <code>MaintenanceState</code>, keyed by participant address and separate from the hot participant object.</p>
<p><code>MaintenanceState</code> now carries both:</p>
<ol>
<li>Maintenance credit</li>
<li>The last epoch in which maintenance was activated</li>
<li>The active reservation reference, if any</li>
<li>The next scheduled reservation reference, if any</li>
</ol>
<p>This keeps maintenance accounting decoupled from the participant record without splitting it into multiple fragmented per-participant maintenance buckets.</p>
<p>We also added a new rule that a participant may have at most one future scheduled maintenance window at a time.</p>
<h3>D4: Activation-time concurrency re-check</h3>
<p>Accepted with a clarification.</p>
<p>We updated the proposal to re-check concurrency caps at activation time in <code>BeginBlock</code>, but we are not hard-canceling windows at activation.</p>
<p>If a reservation activates under current params that would now exceed caps:</p>
<ol>
<li>The reservation still activates</li>
<li>A warning event is emitted</li>
<li>Advisory warning / violation metadata is stored on the reservation so it is queryable later</li>
</ol>
<p>This preserves operator predictability while making governance drift visible.</p>
<h3>D5: Credit accrual during maintenance-used epochs</h3>
<p>Accepted.</p>
<p>We updated the proposal so that:</p>
<ol>
<li>Ordinary reward eligibility remains unchanged</li>
<li>Maintenance-credit accrual is suppressed in any epoch where a maintenance window was activated for that participant</li>
</ol>
<p>This makes every maintenance use have a net credit cost and resolves the original self-replenishing-credit concern.</p>
<h2>Additional Notes</h2>
<p>We also added the following clarifications while incorporating the feedback:</p>
<ol>
<li>The <code>BeginBlock</code> lifecycle and lookup path must use direct keyed Cosmos SDK collections access rather than broad iteration.</li>
<li>Activation-time warnings are not event-only; they are also made queryable on the reservation itself.</li>
<li>The task plan now includes explicit work in both the maintained Cosmos SDK fork and the inference-chain repo.</li>
<li>The task plan now includes end-to-end coverage for the restricted PoC / DKG scheduling rules.</li>
<li>The proposal now states required performance properties at a high level, while the task plan carries the concrete storage and index layout.</li>
<li>The task plan now explicitly separates:</li>
<li>exact-height transition schedule for <code>BeginBlock</code></li>
<li>start-height overlap index for scheduling-time range scans</li>
</ol>
<h2>Updated Documents</h2>
<p>The following documents were updated:</p>
<ol>
<li><code>proposals/maintenance-windows/maintenance-windows.md</code></li>
<li><code>proposals/maintenance-windows/maintenance-windows-todo.md</code></li>
</ol>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span><a href="https://github.com/Ryanchen911">@Ryanchen911</a></span>
    <span class="issues-meta-item">commented 2026-04-01 03:45 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>works in progress</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #927](https://github.com/gonka-ai/gonka/issues/927) every hour.
