GRC Proposal #2

Overview

This is the second restitution proposal from the Gonka Restitution Committee (GRC). It is also the largest proposal to date, covering 3 accepted restitution cases across multiple epochs — compared to a single case in the previous proposal.

GRC has recently refreshed its membership: the committee now includes developers from Gonka Labs and Inc4, broadening technical expertise and validation capacity.

New this proposal: before submission, GRC piloted a structured AI interview process — an idea contributed by someone who chose to remain anonymous. The interview covers purpose, cost, stakeholder impact, and risks. This is the first run, conducted for MVP purposes to test the format and prompt before rolling it out more broadly.

Interview block: https://blocks.gonka.gg/blocks/admin/gonka-governance-interview

This proposal's interview: https://blocks.gonka.gg/c/cmpfmwlvh007rsau9qc7sxm3u

Interviewer prompt: https://github.com/votkon/gonka-proposal-interview/blob/main/interviewer-prompt.txt

The full transcript is available at the interview link above. We invite everyone to use this in their own proposals and share feedback on this first iteration.

Cases

Case 1 — Epoch 247: Inactive Status Mid-Epoch (Rejected)

Original definition: Hosts who had POC_SLOT=true in epoch 247 before the upgrade had confirmationWeight=0 in that epoch, leading to lowered or zeroed rewards for epoch 247.

Nine participants served inferences with low miss rates (≤ 3.1%) but received zero rewards in epoch 247 after their status flipped from ACTIVE to INACTIVE during the epoch. A restitution case was filed based on the traffic they served.

After investigation, validators were unable to establish a clear and reproducible causal link between the claimed mechanism and the observed reward outcomes. The victim list selection logic could not be verified against on-chain data, and similar-looking cases not included in the list raised further questions. The case was rejected for insufficient proof of a defined protocol-level issue.

Case 2 — Epochs 249–253: Preserver Weight Double-Scaling Bug

Original definition: MLNodes sampled as preserver nodes in epoch 247 (and potentially the following epoch until their first PoC) had their weight incorrectly scaled to approximately 35% of the full weight.

Status: Accepted | 30,318.50 GNK | Source

Following the v0.2.12 network upgrade, nodes in the Qwen subgroup that were sampled as preserved nodes had their MLNodeInfo.PocWeight stored in pre-scaled units. Post-upgrade code treated these stale values as raw nonces and re-applied the WeightScaleFactor (≈0.36), causing double-scaling. Affected nodes had their consensus weight reduced to approximately 36% of the intended level for every epoch in which they remained "stuck" — until they re-ran a fresh Proof of Compute (PoC) validation.

This resulted in proportionally reduced PoC rewards across multiple epochs. 34 (participant, node) pairs were identified. The fix (PR #1089) introduced episode-scoped preservation and refined reward logic.

Case 3 — Epochs 248, 249 & 250: Epoch Loss Restitution

Original definition: Hosts invalidated with reason consecutive_failures in epoch N cannot participate in further epochs because the status is not reset. Only epoch N+1 should be considered for restitution to avoid abuse. Epochs 250 and beyond are out of scope as the issue became known.

Status: Accepted | 217,612.83 GNK

This case consolidates four related restitution packages covering abnormal reward losses across epochs 248, 249, and 250. All packages use source_overrides.json as the authoritative deduplication layer — amounts already covered by another package are marked external_proposed and excluded, so there is no double-counting across sub-packages or with Case 2.

Epoch 248 — Broad epoch loss (118,204.04 GNK) | Source
Analysis revealed abnormally high loss rates: 63 of 95 participants (66%) received no or reduced rewards, accounting for 41% of the epoch's total reward pool. Multiple failure categories contributed — failed confirmation PoC, consecutive failures, statistical invalidations, and confirmation weight reductions. Given the scale and statistical significance of the loss, full restitution of all unrecovered losses was approved.

Epoch 249 — Consecutive failures restriction (63,391.60 GNK) | Source
Three participants invalidated by the consecutive_failures mechanism remained blocked from reward eligibility in epoch 249 beyond the intended scope of the restriction. Their invalidation status persisted when it should have resolved, causing complete reward exclusion for that epoch.

Epoch 249 — Remaining delta for Case 2 victims (24,597.79 GNK) | Source
Several participants affected by the Case 2 double-scaling bug suffered losses greater than what the 0.35x formula alone covers — where the weight bug compounded with a confirmation failure, resulting in zero reward for the epoch rather than just a reduced one. This package covers the remaining unpaid delta after Case 2 restitution is applied.

Epoch 250 — Broad epoch loss, net of Case 2 and Case 3a (11,419.41 GNK) | Source
34 of 71 participants (48%) experienced losses in epoch 250. Amounts already covered by Case 2 or the consecutive failures package are excluded per-address via source_overrides.

Case 4 — Epoch 254: API Startup Blocking Issue

Original definition: Unexpected API startup behavior caused nodes to be unavailable during epoch 254 CPoC rounds, resulting in zero rewards for affected participants.

Status: Accepted | 58,375.96 GNK | Source

Version v0.2.12-api-post2 was released between CPoC 1 and CPoC 2 (Confirmation Proof of Compute rounds) of epoch 254. This version introduced a blocking devshard migration on API startup, causing servers to be unavailable for up to 20 minutes after a container restart. Participants who applied the update promptly after CPoC 1 — as expected — had their API offline during CPoC 2, resulting in failed confirmations and zero rewards for the epoch despite passing CPoC 1.

The root fix (parallel devshard loading) shipped in v0.2.12-api-post3 only after the epoch had completed. 14 addresses qualified for restitution based on demonstrated CPoC 1 passage and confirmed epoch-end failure.

Summary

Case
Description
Epochs
Status
GNK

1
Inactive status mid-epoch
247
Rejected
—

2
Preserver weight double-scaling
249–253
Accepted
30,318.50

3
Epoch loss restitution (broad + consecutive failures + remaining delta)
248, 249, 250
Accepted
217,612.83

4
API startup blocking issue
254
Accepted
58,375.96

Total
306,307.29 GNK

Bounties

Bounty rates: case investigation — 4,500 GNK | case validation — 2,187.50 GNK | proposal coordination — 4,222.20 GNK

Address
Roles
GNK

gonka14fxt7xlj74h54u5lz8epz0qeuhpka6xjhzsyq3
Case 1 investigator
4,500.00

gonka16j4zv6723mrnycwn0qgw0j48dr9qecyclxg5jh
Case 2 investigator, Case 3 validator, Case 4 validator
8,875.00

gonka100s7x2t0npruu9ta02306qfmaened3vg3a9dn6
Case 3 investigator, Case 1 validator, Case 2 validator, Case 4 validator
11,062.50

gonka197hqnwcl30x4js3egvaujjmfknlxy7rmfw3y6k
Case 4 investigator, Case 1 validator, Case 2 validator, Case 3 validator, proposal coordinator
15,284.70

Aggregated Payout List

The file restitution_aggregated.csv contains the consolidated payout list across all accepted cases: one row per address, amounts summed where the same address appears in multiple cases.

Run aggregate.py to regenerate it from source:

python3 aggregate.py

The script fetches all source CSVs and JSON directly from the case repositories at runtime.
