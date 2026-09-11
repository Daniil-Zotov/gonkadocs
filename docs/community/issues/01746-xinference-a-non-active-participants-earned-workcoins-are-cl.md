---
title: "#1746 — x/inference: a non-ACTIVE participant's earned WorkCoins are cleared at settlement with no claim record and no governance transfer"
source: https://github.com/gonka-ai/gonka/issues/1746
issue_number: 1746
synced_at: 2026-09-11T09:49:34Z
template: issues-main.html
---

<div class="issues-detail-header">
  <h1 class="issues-detail-title">
    <span class="issues-status issues-status-open"><svg viewBox="0 0 16 16"><path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z"/></svg></span>
    x/inference: a non-ACTIVE participant's earned WorkCoins are cleared at settlement with no claim record and no governance transfer
    <span class="issues-number">#1746</span>
  </h1>
  <div class="issues-detail-meta">
    <span class="issues-meta-item">Open</span>
    <span class="issues-meta-item"><a href="https://github.com/vitaly-andr">@vitaly-andr</a> opened 2026-09-10 11:45 UTC</span>
    <span class="issues-meta-item">0 comments</span>
    <span class="issues-meta-item">Updated 2026-09-10 11:45 UTC</span>
  </div>
  <div class="issues-labels" style="margin-top: 8px;"></div>
</div>

<div class="issues-content" markdown="1">
While measuring the devshard settlement path I ran into a case where earned funds leave the ledger with no on-chain record of where they went. I'm filing this as a question rather than a bug report, because the code and the tokenomics documents point in opposite directions and I can't tell which one you meant.

At settlement, `participant.CoinBalance` is cleared unconditionally (`accountsettle.go:272-273`). The same amount reaches the claimable total only for ACTIVE:

```go
// bitcoin_rewards.go:918-923
workCoins := uint64(0)
if participant.CoinBalance > 0 && participant.Status == types.ParticipantStatus_ACTIVE {
    workCoins = uint64(participant.CoinBalance)  // "UNCHANGED from current system - direct user fees"
}
```

For any other status the amount is not just withheld. With `WorkCoins == 0 && RewardCoins == 0` the "no payment needed" branch at `accountsettle.go:298-321` skips writing a `SettleAmount` at all. `MsgClaimRewards` pays only against an existing record (`msg_server_claim_rewards.go:31-36, 83-104`), and the expired-claim sweep iterates existing records (`settle_amount.go:108-119`). Nothing can find the amount later. It shows up once in an application log through `SafeLogSubAccountTransaction(..., "settling")` and nowhere in state.

What makes me read this as an oversight rather than a penalty is that the same function treats the other coin type differently under the same status. A non-ACTIVE participant's RewardCoins share is zeroed, their weight deliberately stays in the denominator, and the undistributed remainder goes to the governance account (`bitcoin_rewards.go:869-903, 982-999`; `accountsettle.go:248-261`). WorkCoins never reach `totalDistributed` or any remainder, so those coins stay in the module account with nobody entitled to them.

The documents disagree with each other as well. `proposals/tokenomics-v2/bitcoin-reward.md:7-20, 29-61` calls WorkCoins user fees for work actually delivered and says they stay unchanged, `bitcoin-reward-todo.md:63-73` asks for a 1:1 mapping from CoinBalance, and `bitcoin-reward-todo.md:99-109` says an invalid participant gets zero of both.

On reachability: `UpdateParticipantStatus` (`participant_status.go:55-73`) can move a participant to INVALID or INACTIVE mid-epoch. Both handlers end in `removeFromEpochGroups` (`:126-132`), which only drops them from the epoch group object, while the persisted `ActiveParticipants` set that settlement reads (`accountsettle.go:49-58`) stays as it was. Status returns to ACTIVE when the next epoch becomes effective (`module.go:1296-1304, 1335-1356`), and that happens after settlement runs at the end of PoC validation (`module.go:647-671`).

I reproduced it with one participant and one epoch, `CoinBalance` 1000, state set through `SetParticipant` / `SetEpochGroupData` / `SetActiveParticipants`, then real `SettleAccounts`, varying only the status:

| Status | CoinBalance after | EarnedCoins | SettleAmount |
|---|---|---|---|
| ACTIVE | 0 | 1000 | present, WorkCoins=1000 |
| INVALID | 0 | 0 | absent |
| INACTIVE | 0 | 0 | absent |

<details>
<summary>The test, if you want to run it (drop into x/inference/keeper/, go test -run 'TestSettleAccounts_(Active|Invalid|Inactive)Participant')</summary>

```go
package keeper_test

// Does a participant who becomes non-ACTIVE mid-epoch (INVALID or INACTIVE) lose the CoinBalance
// they already earned when the epoch settles?
//
// SettleAccounts zeroes CoinBalance unconditionally (accountsettle.go:272-273), while the carry-over
// into the claimable amount is gated on Status == ACTIVE (bitcoin_rewards.go:919-921). A non-ACTIVE
// participant can still be in the settled set: UpdateParticipantStatus (participant_status.go:62)
// flips a participant mid-epoch, and both paths end in removeFromEpochGroups
// (participant_status.go:126-132), which removes them only from the epoch GROUP object. The
// ActiveParticipants set that settlement reads (accountsettle.go:49-58) is left untouched.
//
// Participant state is raised entirely through keeper methods (SetParticipant, SetEpochGroupData,
// SetActiveParticipants), the same ones the existing settlement tests in this package use, never by
// writing store keys directly.
//
// TestSettleAccounts_ActiveParticipant_EarnedBalanceIsClaimable is the control: identical fixture,
// Status = ACTIVE. It must be green, otherwise red on the non-ACTIVE cases proves nothing.

import (
	"testing"

	"github.com/productscience/inference/testutil"
	keeper2 "github.com/productscience/inference/testutil/keeper"
	"github.com/productscience/inference/x/inference/types"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"go.uber.org/mock/gomock"
)

const (
	probeEpochIndex          = uint64(10)
	probeStartingCoinBalance = int64(1000)
)

// settleSingleParticipant sets up exactly one participant with the given status and
// CoinBalance = probeStartingCoinBalance, in the ActiveParticipants set for probeEpochIndex, then
// runs SettleAccounts for that epoch. It returns the participant's CoinBalance after settlement, the
// EarnedCoins recorded in its EpochPerformanceSummary for the epoch, and whatever SettleAmount record
// (if any) exists for it afterwards.
//
// This is the only state-construction path used by every test in this file: SetParticipant,
// SetEpochGroupData, and SetActiveParticipants are all keeper methods, the same ones
// TestActualSettle/TestActualSettleWithManyParticipants (accountsettle_test.go) already use.
func settleSingleParticipant(t *testing.T, status types.ParticipantStatus) (coinBalanceAfter int64, earnedCoins uint64, settleAmount types.SettleAmount, settleFound bool) {
	t.Helper()

	participant := types.Participant{
		Index:       testutil.Executor,
		Address:     testutil.Executor,
		CoinBalance: probeStartingCoinBalance,
		Status:      status,
		CurrentEpochStats: &types.CurrentEpochStats{
			InferenceCount: 100,
			MissedRequests: 0,
		},
	}

	k, ctx, mocks := keeper2.InferenceKeeperReturningMocks(t)

	k.SetParticipant(ctx, participant)
	k.SetEpochGroupData(ctx, types.EpochGroupData{
		EpochIndex: probeEpochIndex,
		ValidationWeights: []*types.ValidationWeight{
			{
				MemberAddress:      participant.Address,
				Weight:             1000,
				Reputation:         100,
				ConfirmationWeight: 1000,
			},
		},
	})
	k.SetActiveParticipants(ctx, types.ActiveParticipants{
		EpochId: probeEpochIndex,
		Participants: []*types.ActiveParticipant{
			{Index: participant.Address},
		},
	})

	// The reward-pool minting and governance transfer are not what this checks; only the
	// CoinBalance -> WorkCoins -> EarnedCoins path is. Accept any amounts there, the same relaxation
	// the existing grace-epoch tests use for the downtime side of settlement.
	mocks.BankKeeper.EXPECT().MintCoins(gomock.Any(), types.ModuleName, gomock.Any(), gomock.Any()).Return(nil)
	mocks.BankKeeper.EXPECT().LogSubAccountTransaction(gomock.Any(), gomock.Any(), gomock.Any(), gomock.Any(), gomock.Any(), gomock.Any()).AnyTimes()
	mocks.BankKeeper.EXPECT().SendCoinsFromModuleToModule(gomock.Any(), gomock.Any(), gomock.Any(), gomock.Any(), gomock.Any()).Return(nil).AnyTimes()

	err := k.SettleAccounts(ctx, probeEpochIndex, 0)
	require.NoError(t, err, "SettleAccounts itself must not error for any status")

	updated, found := k.GetParticipant(ctx, participant.Address)
	require.True(t, found, "participant must still exist after settlement")

	summary, found := k.GetEpochPerformanceSummary(ctx, probeEpochIndex, participant.Address)
	require.True(t, found, "EpochPerformanceSummary is written for every participant in the settlement loop regardless of status (accountsettle.go:276-290)")

	amount, found := k.GetSettleAmount(ctx, participant.Address)

	return updated.CoinBalance, summary.EarnedCoins, amount, found
}

// Control case: identical fixture to the two tests below, Status = ACTIVE. Must be green.
func TestSettleAccounts_ActiveParticipant_EarnedBalanceIsClaimable(t *testing.T) {
	coinBalanceAfter, earnedCoins, settleAmount, settleFound := settleSingleParticipant(t, types.ParticipantStatus_ACTIVE)

	require.Equal(t, int64(0), coinBalanceAfter,
		"CoinBalance is always zeroed at settlement (accountsettle.go:273), ACTIVE included")
	require.Equal(t, uint64(probeStartingCoinBalance), earnedCoins,
		"ACTIVE control: the earned %d must be claimable as EpochPerformanceSummary.EarnedCoins -- got %d", probeStartingCoinBalance, earnedCoins)
	require.True(t, settleFound, "ACTIVE control: a SettleAmount record must exist for the earned balance")
	require.Equal(t, uint64(probeStartingCoinBalance), settleAmount.WorkCoins,
		"ACTIVE control: SettleAmount.WorkCoins must carry the earned balance")
}

// Status = INVALID. EXPECTED RED on current development: CoinBalance is zeroed to 0
// unconditionally, but bitcoin_rewards.go:920 gates the carry-over on Status == ACTIVE, so
// EarnedCoins comes out 0 and no SettleAmount record is written at all (WorkCoins == 0 and
// RewardCoins == 0 for a non-ACTIVE participant -> the "no payment needed" branch at
// accountsettle.go:305-309 skips the write entirely). The assertions below state what SHOULD hold if
// the earned balance were preserved; on current code they fail, and the failure output shows the
// zeroed balance against the zero claimable amount in numbers.
func TestSettleAccounts_InvalidParticipant_LosesEarnedBalance(t *testing.T) {
	coinBalanceAfter, earnedCoins, settleAmount, settleFound := settleSingleParticipant(t, types.ParticipantStatus_INVALID)

	require.Equal(t, int64(0), coinBalanceAfter,
		"CoinBalance is zeroed unconditionally at settlement, INVALID included -- got %d", coinBalanceAfter)

	// Both facts below are asserted with `assert`, not `require`, so a run against current
	// development code reports BOTH numbers in one go instead of stopping at the first mismatch.
	assert.Equal(t, uint64(probeStartingCoinBalance), earnedCoins,
		"INVALID: CoinBalance dropped from %d to 0, but EarnedCoins is %d, not %d -- the earned balance is lost, not carried forward",
		probeStartingCoinBalance, earnedCoins, probeStartingCoinBalance)
	assert.True(t, settleFound, "INVALID: no SettleAmount record exists for the earned %d either -- it is unclaimed nowhere", probeStartingCoinBalance)
	if settleFound {
		assert.Equal(t, uint64(probeStartingCoinBalance), settleAmount.WorkCoins)
	}
}

// Status = INACTIVE. Same expectation and same EXPECTED RED as the INVALID case above:
// deactiveParticipant follows the identical removeFromEpochGroups path (participant_status.go:76-83).
func TestSettleAccounts_InactiveParticipant_LosesEarnedBalance(t *testing.T) {
	coinBalanceAfter, earnedCoins, settleAmount, settleFound := settleSingleParticipant(t, types.ParticipantStatus_INACTIVE)

	require.Equal(t, int64(0), coinBalanceAfter,
		"CoinBalance is zeroed unconditionally at settlement, INACTIVE included -- got %d", coinBalanceAfter)

	assert.Equal(t, uint64(probeStartingCoinBalance), earnedCoins,
		"INACTIVE: CoinBalance dropped from %d to 0, but EarnedCoins is %d, not %d -- the earned balance is lost, not carried forward",
		probeStartingCoinBalance, earnedCoins, probeStartingCoinBalance)
	assert.True(t, settleFound, "INACTIVE: no SettleAmount record exists for the earned %d either -- it is unclaimed nowhere", probeStartingCoinBalance)
	if settleFound {
		assert.Equal(t, uint64(probeStartingCoinBalance), settleAmount.WorkCoins)
	}
}
```

</details>

On scale: in mainnet epoch 388, 13.33 GNK moved through `CoinBalance` across 25 of the 28 seated participants over 311 escrows, median 0.19 and max 2.39 per participant. Two of 29 seats turned over going into 389. That is small today, but devshard settlement (`msg_server_settle_devshard_escrow.go:155-164`) is the only writer of `CoinBalance` left, so it follows devshard volume. Neither line changed in the 0.2.16 train, so this is not a regression.

Which behaviour did you intend? If forfeiture, the amount could follow the RewardCoins precedent and go to governance with a record instead of sitting unattributed. If preservation, the clearing needs the same status guard the carry-over already has. I haven't sent a patch because those are two different fixes and the answer decides which one is right.

</div>

---

> 🔄 **Auto-synced** from [Issue #1746](https://github.com/gonka-ai/gonka/issues/1746) every hour.
