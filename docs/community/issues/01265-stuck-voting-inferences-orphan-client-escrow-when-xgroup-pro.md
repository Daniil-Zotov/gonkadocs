---
title: "#1265 — Stuck VOTING inferences orphan client escrow when x/group proposals miss quorum"
source: https://github.com/gonka-ai/gonka/issues/1265
issue_number: 1265
synced_at: 2026-07-09T18:14:25Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    Stuck VOTING inferences orphan client escrow when x/group proposals miss quorum
    <span class="issues-number">#1265</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item">[@vitaly-andr](https://github.com/vitaly-andr) opened 2026-05-27 19:50 UTC</span>
    <span class="issues-meta-item">5 comments</span>
    <span class="issues-meta-item">Updated 2026-05-30 17:17 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
## Summary

`expireInferences` (`inference-chain/x/inference/module/module.go:226-234`) filters by `Status == STARTED` only. When a failing `MsgValidation` transitions an inference to `VOTING` and the resulting x/group proposals don't reach quorum, the inference is silently skipped by the timeout cleanup, the timeout entry is removed unconditionally at line 391, and the client's escrow is permanently held in the inference module account.

Surfaced 2026-05-27 by a multi-seed sim sweep (related to #982 Phase 3 work) — seed 99 triggered a custom `NoStuckVoting` invariant: an inference from epoch 0 was still in `Status=VOTING` at epoch 10.

## Reproducer

A black-box test driving the real `expireInferences` is in #1275:
`TestExpireInferences_VotingInferenceRefundedOnTimeout`
(`inference-chain/x/inference/module/expire_voting_stuck_test.go`).

It seeds a `VOTING` inference plus a matching `InferenceTimeout`, then calls the
real (unexported) `expireInferences` through an `export_test.go` wrapper with a
mocked bank keeper. On current `main` it fails — the refund is never issued and
the inference stays `VOTING`; with the fix in #1275 it passes (inference marked
`EXPIRED`, client escrow refunded).

## Failure mode

1. Client calls `MsgStartInference` — escrow ngonka to inference module account, `Status=STARTED`, `InferenceTimeout` queued at `start_block + ExpirationBlocks`.
2. Executor calls `MsgFinishInference` — `Status=FINISHED`.
3. Validator submits failing `MsgValidation` (`msg_server_validation.go:178`) — `Status=VOTING`, two x/group proposals (invalidate, revalidate) created via `submitValidationProposalsWithPolicy` at line 280.
4. x/group voting window closes without quorum. Neither proposal reaches majority. x/group `EndBlock` tallies and prunes but does not auto-execute — execution requires `MsgExec` or a vote with `Exec_EXEC_TRY` (`cosmos-sdk/x/group/keeper/msg_server.go:771-777`).
5. Block reaches `InferenceTimeout.ExpirationHeight`. EndBlocker calls `expireInferences` (`module.go:208`).
6. Filter at `module.go:231` only handles `Status == STARTED`:

   ```go
   if inference.Status == types.InferenceStatus_STARTED {
       am.handleExpiredInferenceWithContext(...)
   }
   ```

   VOTING falls through. No refund.
7. `RemoveInferenceTimeout` (`module.go:391`) unconditionally removes the timeout entry.
8. Inference now permanently `VOTING`, client escrow stuck in inference module account.

## Severity

Liveness for client funds. Not a chain halt — block processing continues. But on every failing `MsgValidation` that misses x/group quorum within the voting window, the client's escrow is lost permanently. The trigger (validators not reaching majority within the voting window) is a routine production condition — network lag, validator restart, split votes — not an exotic edge case.

## Minimal recommended fix

Extend the filter at `module.go:231` to also handle `VOTING`:

```go
switch inference.Status {
case types.InferenceStatus_STARTED:
    am.handleExpiredInferenceWithContext(ctx, inference, expiryCtx)
case types.InferenceStatus_VOTING:
    // Voting window expired without consensus. Refund client, mark
    // EXPIRED, leave x/group proposals to be pruned by x/group EndBlock.
    am.expireInferenceAndIssueRefund(ctx, inference)
}
```

Smallest change that restores liveness. Implements default-to-refund semantics on quorum miss: when validators don't reach consensus, client gets escrow back, executor receives no payment, no slashing.

## Alternative semantics (for separate discussion)

The minimal fix picks one of several reasonable semantics. The following alternatives are worth considering as a separate design discussion (not bundled with this fix):

- **Re-vote on quorum miss.** Open a new proposal pair with current epoch members; retry up to N times; fall back to refund if still no quorum. Maximizes consensus chance but introduces new state (retry counter), a new governance param, proposer-identity handling on retry (the invalidate proposer is the invalidator; the revalidate proposer is the executor, who may have been dropped from the active set), and would require a proposal-close API not currently in the inference module's group interface.
- **Default-to-invalidate.** Quorum miss = treat as invalidated. Protects client but penalizes executor for validators' technical failures (offline, network lag).

Not recommended: default-to-validate (passive non-voting becomes implicit approval — attack vector); slash non-voting validators (DoS vector via spurious failing validations).

## Open questions for maintainers

- Is default-to-refund acceptable on quorum miss, or do you prefer a different fallback (re-vote, default-to-invalidate)?
- If re-vote is preferred, that probably belongs in a separate design issue — happy to draft it once the immediate liveness gap is closed.

---

@patimen — touching code you originally wrote (`module.go:231`, commit `2f33567dd7`). Flagging directly since you'd have the most context on the intended semantics here.

</div>

---

## 💬 Comments (5)

<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@vitaly-andr](https://github.com/vitaly-andr)</span>
    <span class="issues-meta-item">commented 2026-05-28 12:46 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Quick follow-up: applied the filter extension from the body of this issue locally (<code>module.go:231</code> → also handle <code>Status=VOTING</code> via <code>expireInferenceAndIssueRefund</code>) and reran sim. The timeout-stuck path is no longer reachable on seed=99 — sim-full now progresses past the previous failure point.</p>
<p>What surfaced next is a distinct mechanism in the revalidation vote path: validators present in <code>ActiveParticipantsSet[epoch]</code> can be absent from the corresponding x/group, and <code>voteValidationProposal</code> hard-errors with <code>voter not found</code> instead of treating non-member as no-op. Root cause is the permissive <code>addEpochMembers</code> (skip on nil-seed, continue on <code>AddMember</code> error — <code>module.go:1134</code>, <code>:1143</code>) which leaves the <code>ActiveParticipantsSet ⊆ group members</code> invariant unmaintained.</p>
<p>Filed separately as #1269 with the sim reproduction (seed=99, block 39/500) and a suggested structural pre-check using <code>GroupMessageKeeper.GroupMembers</code>. Liveness for that path is now bounded by the timeout cleanup proposed in this issue, so it's a correctness/quorum issue rather than fund-loss.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@a-kuprin](https://github.com/a-kuprin)</span>
    <span class="issues-meta-item">commented 2026-05-30 05:18 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>I think we should focus now on devshard inference flow.
Anyway legacy inference flow will not be supported in the future.</p>
<p>Also do we really have such issue in production environment?</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@vitaly-andr](https://github.com/vitaly-andr)</span>
    <span class="issues-meta-item">commented 2026-05-30 08:13 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>Thanks for the steer — both points taken.</p>
<p><strong>On "do we really have this in production?"</strong> — honestly, I can't confirm it from chain state. I scanned ~40k inferences on a mainnet node and found none in <code>VOTING</code>, but that's not evidence either way: inferences that enter the epoch-group validation path get a real <code>epoch_id</code> and are pruned after <code>InferencePruningEpochThreshold</code> epochs (<code>keeper/pruning.go</code>), while only the <code>epoch_id=0</code> start/finish/expire residue persists. So state inspection structurally can't answer this — it'd need tx history (the public node has <code>tx_index=off</code>) or your internal telemetry. Do you have a way to see whether a failing <code>MsgValidation</code> → quorum-miss has actually occurred?</p>
<p>My case for the fix isn't "it happens a lot in prod" — it's that the gap is real in the code (<code>expireInferences</code> silently skips <code>VOTING</code> and still removes the timeout entry, stranding client escrow), the fix is minimal (one <code>VOTING</code> branch → refund), and it's required for the #982 sim-full run to stay green (the <code>no-stuck-voting</code> invariant catches it deterministically). If the legacy validation flow is genuinely being retired, I'm happy to defer or close #1275 — your call.</p>
<p><strong>On devshard</strong> — point taken, and I'd like to follow it. The simsx infrastructure from #982 (#1228) is flow-agnostic plumbing; it currently carries only the legacy factories, but it's the natural place to add devshard coverage. I'm happy to write the sim factories + invariants for the escrow/settlement path (<code>MsgCreateDevshardEscrow</code> / <code>MsgSettleDevshardEscrow</code>). The one open question is how to treat <code>VerifyDevshardSettlement</code>'s signature check under simulation — would welcome a hint on the intended approach.</p>
<p><strong>One ask:</strong> #1228 (the #982 simsx infrastructure) hasn't had a review yet. Could you take a look? It's the foundation everything above builds on, and a first pass from you would help me aim the next round (legacy vs devshard) correctly.</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@a-kuprin](https://github.com/a-kuprin)</span>
    <span class="issues-meta-item">commented 2026-05-30 15:37 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <blockquote>
<p>it's the natural place to add devshard coverage</p>
</blockquote>
<p>Validation logic of devshard is subject to change in future releases</p>
  </div>
</div>
<div class="issues-comment">
  <div class="issues-comment-header">
    <span>[@vitaly-andr](https://github.com/vitaly-andr)</span>
    <span class="issues-meta-item">commented 2026-05-30 17:17 UTC</span>
  </div>
  <div class="issues-comment-body issues-content">
    <p>@patimen — pulling you in, since you authored #982 and own the original scope.</p>
<p>I want to make sure I'm putting effort where it's actually useful. a-kuprin's steer here is clear, and I agree with it: legacy validation is being retired, and devshard's validation logic is still in flux — so I'll hold off on adding devshard sim coverage until it stabilizes (no point simming a moving target).</p>
<p>What I'm unsure about is the disposition of the work already done on this accepted issue. Two honest questions:</p>
<ol>
<li><strong>Is the #982 simulation work (#1228) still wanted</strong> as merged infrastructure? It's flow-agnostic and would be the natural place to add devshard coverage later, once that logic settles.</li>
<li>Along the way the sim surfaced two concrete bugs in the <strong>current</strong> flow — stranded client escrow on a quorum-missed timeout (#1265 → #1275) and a revalidation-vote failure when the voter isn't in the epoch group (#1269 → #1276). Both are small fixes on code live in <code>main</code> today. <strong>Even if focus shifts to devshard, is there a reason not to land them now?</strong></li>
</ol>
<p>If this whole area is being superseded and the fixes aren't worth merging, that's completely fine — I'd just like to know, so I can close things out cleanly rather than leave them open. Whatever fits your roadmap.</p>
  </div>
</div>

---

> 🔄 **Auto-synced** from [Issue #1265](https://github.com/gonka-ai/gonka/issues/1265) every hour.
