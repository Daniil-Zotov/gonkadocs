---
title: "#1269 — x/inference: revalidation vote fails when voter absent from epoch x/group"
source: https://github.com/gonka-ai/gonka/issues/1269
issue_number: 1269
synced_at: 2026-08-02T21:13:35Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    x/inference: revalidation vote fails when voter absent from epoch x/group
    <span class="issues-number">#1269</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/vitaly-andr">@vitaly-andr</a> opened 2026-05-28 12:45 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-05-28 16:52 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
# x/inference: revalidation vote fails when voter absent from epoch x/group

## Summary

`MsgValidation{Revalidation:true}` for an inference whose VOTING window
is still open fails with `voter address: <bech32>: not found` when the
submitter is in `ActiveParticipantsSet[inference.EpochId]` but is NOT a
member of the x/group that owns
`inference.ProposalDetails.ReValidatePolicyId` **at the moment the
second of two sequential votes is dispatched**.

The handler issues two `k.group.Vote` calls back-to-back (Invalidate
then Revalidate). Either vote can hit a state where the voter is
missing from the group. Two independent mechanisms can produce that
state — one demonstrated by sim, one plausible from code inspection.

Related to #1265 (manifestation #1: VOTING-stuck escrow on timeout,
narrow fix already discussed there).

## Reproduction (simulation)

Two prerequisites:

1. **Sim infrastructure** — check out PR #1228 (Phase 3 of #982; adds
   `make sim-full-test`, simsx wiring, first-wave `x/inference`
   operations):

   ```bash
   gh pr checkout 1228
   ```

2. **Manifestation #1 production fix** — apply this local patch. Without
   it sim-full fails earlier on the timeout-stuck path (#1265) and
   never reaches the vote race below:

   ```diff
   --- a/inference-chain/x/inference/module/module.go
   +++ b/inference-chain/x/inference/module/module.go
   @@ -228,6 +228,11 @@ func (am AppModule) expireInferences(
    		if inference.Status == types.InferenceStatus_STARTED {
    			am.handleExpiredInferenceWithContext(ctx, inference, expiryCtx)
   +		} else if inference.Status == types.InferenceStatus_VOTING {
   +			// VOTING inferences whose x/group proposals missed quorum
   +			// would otherwise be silently dropped here, stranding client
   +			// escrow in the inference module account.
   +			am.expireInferenceAndIssueRefund(ctx, inference)
    		}
    	}
    	return nil
   ```

Then from `inference-chain/`, run sim-full in canonical Docker per
`docs/simulation.md` **with `-Verbose=true`** so the intra-tx trace is
captured:

```bash
go test -mod=readonly -tags "sims muslc" ./app/ \
  -run "TestFullAppSimulation" \
  -Enabled=true -Commit=true -Verbose=true \
  -NumBlocks=500 -BlockSize=200 -Seed=99 -GenesisTime=1700000000 \
  -v -timeout 180m
```

On seed=99 the run terminates at block 39/500, op 222. The verbose
trace within the failing `MsgValidation` tx shows the full sequence:

```
INF Voting               vote="proposal_id:170 voter:gonka1acqhn... Invalidate ..."
INF Voted on validation  vote="proposal_id:170 ..."         ← first vote succeeds
INF Inference invalidated
INF Participant status updated  new=INVALID original=ACTIVE
                                reason=statistical_invalidations
WRN Participant invalidated
INF Slashing participant        slash_fraction=0.2          ← voter removed from group here
INF Voting               vote="proposal_id:171 voter:gonka1acqhn... Revalidate ..."
ERR Error voting   error="voter address: gonka1acqhn...: not found"
                   vote="proposal_id:171 ..."               ← second vote fails
simulate.go:346: error on block 39/500, operation (222/236) ...
```

## Root cause

The handler `revalidateInferenceVote`
(`x/inference/keeper/msg_server_validation.go:226`) calls
`k.voteValidationProposal` twice in sequence — first on
`InvalidatePolicyId`, then on `ReValidatePolicyId`
(`msg_server_validation.go:246`, `:253`). Both calls bottom out at
`k.group.Vote` (`msg_server_validation.go:304`), which suppresses one
exact error string only — `"proposal not open for voting: invalid
value"` (`msg_server_validation.go:306`); every other error
propagates as `DeliverTx` failure.

Two independent mechanisms can leave the voter absent from the group:

**Mechanism A — self-invalidation cascade between the two votes
(DEMONSTRATED by sim verbose trace above).** The first vote on
`InvalidatePolicyId` can succeed and immediately trigger the
inference-invalidation handler. That handler updates participant
statistics; if `statistical_invalidations` thresholds are breached
(in the seed=99 trace, after `invalidated_inferences=24`), the voter
themselves is marked `INVALID`, slashed, and removed from the epoch
sub-group. The handler then proceeds to the second `k.group.Vote` on
`ReValidatePolicyId` — voter is no longer a member, vote
hard-errors. The entire tx then reverts (atomicity preserves funds
but discards both votes, the invalidation, and the slash — see
Consequences).

**Mechanism B — permissive `addEpochMembers` leaves
`ActiveParticipantsSet ⊆ group members` invariant unmaintained
(plausible from code inspection; not separately demonstrated here).**
`SetActiveParticipants` writes `ActiveParticipantsSet` first
(`x/inference/keeper/module.go:757`, `:785`), then `addEpochMembers`
adds those participants to the epoch x/group
(`module.go:1119`, `x/inference/keeper/epoch_group.go:391`).
`addEpochMembers` is permissive:

- skips participants whose seed is nil (`module.go:1134`, logged as
  `ILLEGAL STATE`);
- continues after an `AddMember` error rather than rolling back
  (`module.go:1143`, `:1145`).

Both paths leave `ActiveParticipantsSet` populated while the x/group
for that epoch is missing those members. A later `MsgValidation`
picking such a participant as voter would then fail on the **first**
vote, before the cascade above is even reached.

A correct fix has to cover both: the voter may be absent at handler
entry (mechanism B) or become absent between the two sequential votes
(mechanism A).

## Production consequences

- **Atomicity preserves funds**: a handler error reverts the entire
  tx. The first vote, the invalidation, the slash, and any partial
  refund all roll back together with the failed second vote. Net
  effect: nothing happens, voter remains ACTIVE, inference status
  unchanged.
- **Fee impact**: `MsgValidation` is fee-exempt via
  `NetworkDutyFeeBypassDecorator` (`app/ante_fee.go::isNetworkDuty`).
  No fee is deducted on the failed delivery.
- **Silent retry trap**: the cascade is deterministic from the same
  state, so a validator that retries the same `MsgValidation` will
  hit the same failure. Stuck only escapes via state change from
  other validators' votes or eventual timeout.
- **Quorum impact**: this validator's votes do not count on either
  proposal. If multiple validators reach the cascade independently,
  the `ReValidatePolicyId` proposal can miss quorum and expire.
  Liveness for the inference is bounded by the manifestation #1
  timeout fix (#1265) — client refunded, inference marked EXPIRED.
- **Frequency**:
  - Mechanism A triggers whenever a validator voting YES on
    `InvalidatePolicyId` breaches the statistical-invalidation
    threshold via that same tx. Reproducible: any validator near the
    threshold who lands on a will-invalidate inference.
  - Mechanism B depends on the rate of nil-seed participants and of
    `AddMember` failures during epoch construction. Lower frequency,
    but each occurrence persists for the rest of the epoch.

## Suggested fix (narrow)

Structural membership precheck in `revalidateInferenceVote`, applied
**before each `k.group.Vote` call** — not once at the top. Mechanism A
specifically requires a recheck between the two votes; checking only
at handler entry mirrors the state in which the voter is still a
member and is not sufficient.

Sketch:

```go
isMember := func() bool {
    sg, err := k.GetEpochGroup(ctx, inference.EpochId, inference.Model)
    if err != nil || sg == nil || sg.GroupData == nil || sg.GroupData.EpochGroupId == 0 {
        return false
    }
    members, mErr := sg.GetGroupMembers(ctx)
    if mErr != nil {
        return false
    }
    for _, m := range members {
        if m.Member != nil && m.Member.Address == voter {
            return true
        }
    }
    return false
}

if !isMember() {
    // log + no-op return; do not reach k.group.Vote
    return &types.MsgValidationResponse{}, nil
}
// ... first vote on InvalidatePolicyId ...

if !isMember() {
    // voter removed mid-tx (mechanism A); skip second vote
    return &types.MsgValidationResponse{}, nil
}
// ... second vote on ReValidatePolicyId ...
```

`GroupMessageKeeper.GroupMembers` is already exposed
(`x/inference/types/expected_keepers.go:46`) and
`epochgroup.EpochGroup.GetGroupMembers` paginates correctly
(`x/inference/epochgroup/epoch_group.go:464`). No interface
extension required.

Out of scope for this issue (deferred):

- Whether the second vote *should* still be cast in some form when
  mechanism A fires (e.g. the inference is already invalidated by
  the first vote, so the revalidate proposal is moot anyway). That
  is a design question for `revalidateInferenceVote` semantics.
- Tightening `addEpochMembers` itself (rollback on `AddMember`
  failure vs the current continue-and-log) — separate behavioural
  change that touches epoch transition semantics.
- Re-vote semantics for inferences whose voting window closes without
  quorum — covered by the broader hybrid-revote discussion mentioned
  on #1265.

## How discovered

Surfaced by the x/inference simulation work in #982 (Phase 3-B
invariants + custom decoders, follow-up to PR #1228). Initial
hypothesis from code inspection (mechanism B above) was filed first;
running sim with `-Verbose=true` produced the intra-tx trace that
demonstrates mechanism A is the actual failure mode on seed=99
b39/op 222.

## References

- Manifestation #1 (related): #1265 (VOTING-stuck escrow on timeout)
- Sim infrastructure prerequisite: PR #1228 (Phase 3 of #982)
- Handler: `x/inference/keeper/msg_server_validation.go:226`, `:246`,
  `:253`, `:304`, `:306`
- Permissive epoch-build path (mechanism B):
  `x/inference/keeper/module.go:1119`, `:1134`, `:1143`, `:1145`
- Group member API: `x/inference/types/expected_keepers.go:46`,
  `x/inference/epochgroup/epoch_group.go:464`

</div>

---

> 🔄 **Auto-synced** from [Issue #1269](https://github.com/gonka-ai/gonka/issues/1269) every hour.
