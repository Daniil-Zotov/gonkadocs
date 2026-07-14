# Gonka Withheld Rewards Redistribution

This directory contains a reference computation for redistributing the
withheld-reward balance accumulated in the `gov` module account back to the
miners who participated in epochs `132..247`.

The output is a single CSV that maps each historical participant to the
exact amount of `ngonka` they should receive. The numbers are deterministic
and verifiable against the on-chain state of any gonka full node.

## TL;DR

- Withheld rewards (≈ **3 053 801 GNK**) sit in the gov module account
  (`gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33`).
- These are unpaid earnings that belong to miners, not community-pool funds.
- The proposal redistributes them proportionally to each miner's actual
  rewarded share in each affected epoch.
- The computation is fully reproducible from a single Python script and any
  gonka node.

## Background — How We Got Here

Two upgrades changed the lifecycle of unpaid rewards on chain. Together they
moved miner-earned coins that were not paid out for performance reasons from
the participant set into a single pool — the gov module account. This
proposal addresses what should happen to that pool now that it has grown
substantial.

### Upgrade v0.2.9 — Withheld rewards routed to gov

Before v0.2.9, when a participant was penalized during cPoC validation
(e.g. for missed validations or invalid inferences), the unpaid portion of
their epoch reward was redistributed *among the remaining participants* in
the same epoch. v0.2.9 changed this: the unaccounted portion is now
**transferred to the gov module account** instead.

From the v0.2.9 release notes (proposal **#26**, passed 2026-02-01,
executed at block 2 451 000):

> **Reward flow correction for cPoC cases.** In cases where rewards are
> reduced or excluded due to cPoC penalties, the unaccounted portion is
> transferred to the Community pool. Previously, such rewards were
> redistributed among other participants.

Although the announcement says "Community pool", on chain the destination is
the gov module account (`auth/gov`), not the community pool managed by
`auth/distribution`. That distinction is not cosmetic — see the section
"Why these are miner funds, not community funds" below.

### Upgrade v0.2.11 — Slashed collateral routed to gov

v0.2.11 (proposal **#31**, passed 2026-03-20) extended the same policy to
slashed collateral. PR
[#775](https://github.com/gonka-ai/gonka/pull/775) replaced
`BurnCoins(...)` with `SendCoinsFromModuleToModule(..., govtypes.ModuleName, ...)`,
making the rule consistent across all forms of forfeited miner funds.

The motivation is captured in the issue
[#772](https://github.com/gonka-ai/gonka/issues/772) that PR #775 closed:

> Slashed coins must be transferred to the Governance module account,
> consistent with how we handle rewards that are withheld from miners
> during penalties. Implementation should reuse or mirror the existing
> logic that handles redistribution of miner rewards that are not paid out
> due to penalties.

### Earliest evidence of the mechanism

The earliest observed `inference → gov` transfer is at block 2 058 543
(epoch 132, 2026-01-08), so for redistribution purposes epoch 132 is the
practical start. Epochs 1..131 show zero gov inflow.

## Why These Are Miner Funds, Not Community Funds

A common misconception is that the gov module balance is "community money"
and can be spent on grants, marketing, ecosystem initiatives, etc. It is
not.

- The **community pool** is a separate on-chain account
  (`gonka1jv65s3grqf6v6jl3dp4t6c9t9rk99cd8h2rzwa`, the `auth/distribution`
  module). It is funded by an explicit fraction of inflation and is
  designed to be spent through `MsgCommunityPoolSpend`. At time of writing
  it holds approximately **102 972 832 GNK + 10 000 IBC USDT**, more than
  enough capital for community initiatives.
- The **gov module account** (this proposal's subject) holds two distinct
  things: temporary deposits attached to live governance proposals
  (returned to depositors when voting ends), and the withheld /
  slashed coins introduced by v0.2.9 and v0.2.11.

The withheld coins entered the gov account specifically because the
mechanic that previously redistributed them inside the epoch was disabled.
At the time of the v0.2.9 change there was no follow-up rule defined for
how those funds should ultimately be returned. This proposal is that rule.

These coins were never minted as community subsidy — they were minted as
miner reward. The participants who *did* perform their epoch duties were
the ones who would have received those coins under the pre-v0.2.9 rule.
Returning the balance to them by their proportional share of actually-paid
rewards is the most direct restoration of the pre-v0.2.9 economic outcome,
modulo the original intent of the v0.2.9 change (no longer giving an extra
bonus to in-epoch peers).

## Prior Art — Proposals #32 and #33

Two narrow predecessors already used the gov balance to compensate
miners who had documented losses:

- **Proposal #32** (passed 2026-03-24): paid 30 538 GNK to compensate
  participants for lost preserved weights specific to epoch 158, computed
  individually from a snapshot of historical preserved weight at block
  2 443 438. The batch was sent from gov via
  `MsgBatchTransferWithVesting`.
- **Proposal #33** (passed 2026-03-27): paid 27 906 GNK to compensate
  participants affected by a cPoC bug in epochs 132–133, again via batch
  vesting from gov, with smaller community-pool payments to proposal
  authors.

Both proposals confirm two things relevant to the present design:

1. The gov balance is a legitimate source for miner compensation
   (precedent established and ratified by governance).
2. Past compensations were targeted by ad-hoc methodology (per-incident
   loss models). The present proposal does not retroactively adjust those
   payouts; it simply redistributes the *current* balance proportionally.

The script does not subtract the #32/#33 amounts from any specific
recipient's share. Some addresses in those proposals will receive a small
additional amount under this distribution — at the order of 1.7% of the
total wallet balance (~55 000 GNK out of 3 156 941 GNK), which is well
below the typical per-epoch noise.

## Algorithm

The computation is a deterministic 7-step pipeline implemented in
`taxreturn.py`. Inputs come exclusively from a gonka full node via standard
Cosmos REST and Tendermint RPC endpoints; no off-chain data is used.

### Step 1 — Resolve module addresses dynamically

Read `/cosmos/auth/v1beta1/module_accounts` and look up the addresses of
the `gov` and `inference` modules. No chain-specific addresses are
hardcoded; the script will work on any gonka network (mainnet, testnet,
devnet) that exposes these standard module accounts.

### Step 2 — Discover all blocks where `inference → gov` happened

Tendermint RPC `block_search` indexes both `transfer.sender` and
`transfer.recipient` event keys. Combining them with an `AND` query
returns exactly the blocks where the inference module sent coins into the
gov account, and excludes proposal deposits, refunds, slashed-collateral
transfers, etc.

```
block_search?query="transfer.sender='<inference>' AND transfer.recipient='<gov>'"
```

This yields ~116 blocks for the entire history covered by the proposal — a
5× reduction relative to a naïve `recipient='<gov>'` query, with no loss
of relevant data.

### Step 3 — Sum the per-block ngonka inflow

For each block from step 2, fetch `block_results?height=H` and sum every
`transfer` event whose `sender` is the inference module and whose
`recipient` is the gov module. This works because `block_results` returns
events as plain JSON; it does not decode tx bodies, so the post-v0.2.12
REST tx-decoding bug (`errUnknownField "*types.TokenomicsParams"`) does
not affect this path.

End-block events (the actual payout mechanism) are not transactions and
therefore are invisible to `tx_search` and to the Cosmos REST tx
endpoints. `block_results` is the canonical source for them.

### Step 4 — Read real epoch boundaries

For every epoch in `[132..247]`, fetch
`/inference/inference/epoch_group_data/{n}` to obtain:

- `effective_block_height` and `last_block_height` — the real block range
  the epoch occupies. Epoch length is governance-controlled and has
  changed over the chain's history, so derived formulas are unsafe; the
  on-chain values are the ground truth.
- `validation_weights[*].member_address` — the participant set for the
  epoch.

### Step 5 — Per-participant rewards

For every (epoch, participant) pair, fetch
`/inference/inference/epoch_performance_summary/{epoch}/{addr}` and read
`rewarded_coins`. This field is the canonical "how much the participant
actually received from this epoch's reward pool" and matches the
`vest_reward.amount` event attribute observed in on-chain
`MsgClaimRewards` transactions (verified empirically; spot-checked on top
recipients).

### Step 6 — Map inflow to epoch and aggregate

Each inflow block height is mapped to its epoch using the boundary table
from step 4 (`eff ≤ h ≤ last`). The per-epoch inflow is the sum of
ngonka observed in step 3 for that epoch's blocks.

Result: a vector `inflow[epoch] → ngonka` covering epochs 132..247.

### Step 7 — Apportionment

The total amount to distribute is

```
T = sum(inflow[epoch]) for epoch in 132..247
```

This is the historical inflow, not the current wallet balance. The
current balance contains residual amounts from epochs the proposal does
not address (in particular, withheld coins from epochs >247 that have
arrived since the snapshot, plus a few small pre-132 entries). Choosing
`T = total in-range inflow` ensures that participants of epochs 132..247
receive exactly the funds that originated from those epochs — no more, no
less.

Apportionment is performed in two nested levels using **Hamilton's
largest-remainder method** in pure integer ngonka arithmetic:

1. Apportion `T` across epochs in proportion to `inflow[epoch]`. The sum
   of per-epoch budgets equals `T` exactly.
2. For each epoch, apportion that epoch's budget across its participants
   in proportion to `rewarded_coins`. Participants with zero
   `rewarded_coins` (those who were penalized in that epoch and whose
   share was withheld) receive nothing from that epoch's budget — they
   are exactly the participants for whom the funds were withheld in the
   first place.

Both steps use the same Hamilton procedure: compute floor shares, then
distribute the leftover (target minus sum of floors) one ngonka at a
time to the shares with the largest fractional remainders. This produces
an integer allocation whose total equals the target exactly, with no
rounding error and no privileged participant.

The final per-recipient amount is the sum of their per-epoch shares
across epochs 132..247.

### Output

A single CSV (`payouts.csv` by default):

```csv
recipient,ngonka,gnk
gonka1...,257001064815774,257001.064815774
gonka1...,255743613433661,255743.613433661
...
```

Sorted by descending amount. The sum of the `ngonka` column equals `T`
exactly.

## Reproducing the Computation

```bash
pip install -r requirements.txt
python3 taxreturn.py {NODE IP} --out payouts.csv
```

The script accepts either a hostname/IP (default port 8000) or a full URL.
A SQLite cache is created in `cache_<NODE>/` so subsequent runs are
incremental — re-running takes seconds rather than minutes.

`START_EPOCH` and `LAST_EPOCH` are intentionally hardcoded so that the
output is reproducible across runs and across nodes, regardless of how
much further the chain has progressed. To extend the range to later
epochs, those constants can be updated and the script rerun; the cache
will pick up only the new epochs.

## Files

- `taxreturn.py` — end-to-end computation script.
- `requirements.txt` — single dependency (`aiohttp`).
- `cache_<NODE_IP>/cache.db` — SQLite cache (block_results, epoch
  metadata, per-participant rewards). Safe to delete; it will be
  rebuilt on the next run.
- `payouts.csv` — output (generated).

## Verification Checklist for Reviewers

- [ ] Module addresses resolved from the live chain (`gov`, `inference`)
      match the addresses your wallet shows.
- [ ] `block_search` total returned by the script matches the count
      visible from any other node.
- [ ] `total_inflow` printed by the script equals the sum of the `ngonka`
      column in the output CSV.
- [ ] `total_inflow + outflows_already_paid_to_miners` is consistent with
      the current gov module balance (the difference accounts for inflows
      from epochs outside [132..247]).
- [ ] Spot-check any individual recipient: their `rewarded_coins` from
      `epoch_performance_summary` for any epoch matches the reward
      reflected in their `vest_reward` events on chain.
