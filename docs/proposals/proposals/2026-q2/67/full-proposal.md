GRC-GONKA-265: Kimi Restitution, Epochs 265–276

Field
Value

Case
GRC-GONKA-265 - Kimi operator restitution: external attack (e265–e266) + ComputeGroupCap underpayment (e267–e276)

Epochs affected
265–276

Affected participants
53 unique addresses

Estimated compensation
946,509.93 GONKA

Cause and evidence
External actor sent malicious requests crashing Kimi vLLM nodes in e265–e266, causing CPoC degradation and mass nonce exclusion; the resulting N-1 weight collapse triggered ComputeGroupCap inversion every epoch through e276. Evidence: weight_fluctuation_analysis.md, per-epoch compensation scripts and JSON in e265/–e276/.

Can it happen again?
ComputeGroupCap: No known repeat path — resolved by v0.2.13 WeightScaleFactor adjustment. External vLLM attack: Reduced risk — the specific crash vectors (stop_token_ids+min_tokens OOM, prompt_logprobs OOM, JSON schema recursion bomb, Jinja injection via chat_template_kwargs) are patched at the devshard gateway (PRs #1170, #1171, #1180, merged May 16–18). A proxy geo-module bug (PR #1183) that made all IP-based rate-limiting ineffective during e265 was also fixed May 18. No known remaining crash path, but gateway coverage of unknown vLLM attack surface cannot be guaranteed.

Mitigation / fix
Nonce exclusion bug: fixed before e267 (version unconfirmed). ComputeGroupCap: v0.2.13 at block 4,267,300 (WeightScaleFactor for Kimi reduced to 0.78). External vLLM attack: devshard gateway patches merged May 16–18 2026 — PR #1170 (stop_token_ids+min_tokens strip, the confirmed e264/e265 attack vector), PR #1171 (prompt_logprobs OOM strip), PR #1180 (CVE-class defenses: schema recursion, Jinja injection, body depth pre-scan), PR #1183 (proxy geo-module bug fix — rate-limiting was non-functional during the attack).

Compensation overlap
Requires investigation — potential address overlap with separate restitution tracks not yet audited.

Current decision
GRC voted to exclude this case from proposal #4 (6 exclude, 2 include, 1 abstain). Calculations are published here for community reference if anyone chooses to bring this forward independently.

Review focus
Highest risk: e266 nonce reconstruction methodology (18 participants, 183,605 GONKA); confirm reconstructed weights match on-chain nonce commits in poc_commits/.

GRC Position

E265–E266 (external attack): The lost rewards in epochs 265 and 266 were a direct
result of a third-party attack on Kimi vLLM nodes. Losses caused by external actors are
outside the scope of the Gonka Restitution Committee. These epochs cannot be included in
a GRC proposal.

E267–E276 (ComputeGroupCap): The cap breach was triggered by the attack-induced N-1
weight collapse in e266, but it was not caused solely by that event. As noted by a
committee reviewer:

"Additionally, the GroupCap issue was not caused solely by recovery from the attack.
It was also influenced by the significant weight imbalance between Kimi and Qwen. In
fact, update 0.2.13 specifically reduced Kimi's weight for this reason. GroupCap was
effectively acting as a balancing mechanism to normalize profitability between the
models."

This context further reduces the case for GRC restitution: the cap was partly correcting
a structural imbalance, not purely an anomalous malfunction.

GRC vote outcome: The committee voted against including this case in the next
proposal.

Vote
Count

Include
2

Exclude
6

Abstain
1

The compensation calculations in this repository were prepared and validated by two
committee reviewers. They are published here so that the community can use these findings
if anyone chooses to bring this proposal forward independently.

Methodology objection (GRC reviewer): One reviewer raised a concern that the
current calculation overstates compensation because it does not recompute the total
network weight. Their argument: the correct question is how much each participant
would have received if GroupCap had never existed — which would require reconstructing
the uncapped weight for every group, summing into a new total network weight, and
compensating only the shortfall against that recalculated denominator. Under that
approach, Kimi participants would receive less than the current calculation produces.

The counter-argument applied here: Qwen rewards have already been paid and cannot
be clawed back, so there is no "same pie" to redistribute. The current approach
applies the same reward formula the chain used for all other participants — using
EpochGroupData.total_weight as denominator — and corrects only the Kimi side.
This is consistent with how prior restitution cases were handled in this repo.

Overview

This repository contains the restitution analysis for epochs 265 through 276 of the
Gonka network. Two distinct bugs caused underpayment to moonshotai/Kimi-K2.6 operators
across these epochs:

Epochs 265–266: external attack — an unknown actor sent malicious requests targeting
Kimi vLLM nodes starting in e265 (attack payload confirmed from production logs: stop_token_ids

min_tokens combination that triggers a vLLM CUDA assert, crashing the engine; 16 crashes
across 12/14 mlnodes observed on 2026-05-14), causing CPoC confirmation weight degradation,
and escalating in e266 to crash most operators and cause mass nonce exclusion; delegation
compensation included for e266 delegators; gateway patches merged May 16–18 (PRs #1170, #1171,
#1180, #1183)

Epochs 267–276: ComputeGroupCap underpayment — the e266 collapse destroyed the
N-1 reference weight used by the cap formula, and when Kimi operators returned in e267
with full accumulated confirmation weight the mismatch caused a severe inversion;
the cap remained triggered every epoch until the v0.2.13 upgrade

The cap breach was resolved by the v0.2.13 upgrade at block 4,267,300 (mid-epoch 276),
which reduced Kimi's WeightScaleFactor to 0.78. Epoch 277 is the first clean epoch.

Epoch Block Heights

Epoch
PoC Start
Epoch End
Notes

265
4,089,970
4,105,360

266
4,105,361
4,120,751

267
4,120,752
4,136,142

268
4,136,143
4,151,533

269
4,151,534
4,166,924

270
4,166,925
4,182,315

271
4,182,316
4,197,706

272
4,197,707
4,213,097

273
4,213,098
4,228,488

274
4,228,489
4,243,879

275
4,249,774
4,259,270

276
4,264,130
4,279,520
true epoch end; v0.2.13 upgrade at 4,267,300

Reward formula: 323,000 × e^(−0.000475 × (epoch − 1)) GONKA.

Eligibility Criteria

Epoch 265 (external attack — CPoC degradation): Participants whose confirmation
weight dropped abnormally mid-epoch at block 4,103,171 due to the attack. Compensation
uses weight / total_epoch_weight × epoch_reward − actual_rewards.

Epoch 266 (external attack — nonce exclusion): The attack escalated, crashing most
Kimi operators and causing mass nonce exclusion. Participants who submitted valid Kimi
nonces but were never registered in the epoch group (or had their Kimi contribution
zeroed) are eligible. Delegation compensation is also included for participants whose
operator was excluded.

Epochs 267–276 (ComputeGroupCap): A participant is eligible only if they
successfully completed the epoch — meaning they both confirmed work
(confirmation_weight on-chain) AND received actual rewards. Participants who failed
the epoch for any reason are excluded: the bug caused underpayment to healthy
participants, not an obligation to pay those who didn't complete the epoch.

Delegation Impact (Epoch 266)

Gonka uses a PoC delegation system where participants without direct MLNodes can
delegate their consensus weight to an operator. When an operator fails to enter the
epoch (due to the nonce bug), the chain resolves all their delegators into ModeNone
instead of ModeDelegate:

Mode
Condition
Weight effect

ModeDelegate
Operator entered epoch
−5% transferred to operator

ModeNone
Operator did not enter
−15% deducted as penalty

The net extra loss for a delegator whose Kimi operator was excluded is 10% of their
original consensus weight.

Full mechanics: e266/DELEGATION.md

Epoch 265 — External Attack (CPoC Degradation)

All Kimi operators entered the epoch group, but CPoC confirmation weights dropped
abnormally at block 4,103,171 as a result of the external attack on Kimi vLLM nodes.
3 participants were affected.

compensation = max(0, weight / total_epoch_weight × epoch_reward − actual_rewards)

Address
weight
cw@healthy
cw@end
drop
Owed (GONKA)

gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6
66,311
66,311
323
99.5%
20,896.53

gonka17pw6099q758qwzewtrqmqpf5c2lrhr97fwqexu
189,884
186,719
172,607
7.6%
5,444.49

gonka1830lqug50lse998x2lakk4pj5ypfumz5pasz0y
13,490
7,031
0
100%
4,251.09

Epoch 265 Total: 30,592.10 GONKA (3 participants)

Output: e265/compensation_265.csv · e265/compensation_265.json

Epoch 266 — External Attack (Nonce Exclusion)

The attack escalated in e266, crashing most Kimi operators' inference nodes and causing
mass exclusion from the epoch. 9 participants submitted Kimi nonces and had their commits
recorded on-chain but were never registered in the epoch group. A further 9 participants entered the epoch but with
their Kimi contribution partially zeroed out. The on-chain total epoch weight was
335,159 — the correctly reconstructed weight from all nonce commits is 1,079,698,
meaning ~69% of the network's true Kimi work was invisible to the reward calculation.

Part 1: Nonce compensation (18 participants)

compensation = max(0, reconstructed_weight / total_reconstructed_weight × epoch_reward − actual_rewards)

Address
Reconstructed weight
Fair share (GONKA)
Actual (GONKA)
Owed (GONKA)

gonka17pw6099q758qwzewtrqmqpf5c2lrhr97fwqexu
214,919.1
56,690.25
14,350.37
42,339.89

gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg
113,567.5
29,956.26
0.00
29,956.26

gonka1wthc28t25pg63hzvl07rl8e8r6km6hesl6jhsz
109,684.6
28,932.04
2,148.14
26,783.90

gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6
72,610.3
19,152.78
239.63
18,913.15

gonka1qa90tgczc0k5dvk4l5nvlf5y6phgm6mg22sfjv
70,111.4
18,493.62
0.00
18,493.62

gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09
64,214.9
16,938.28
5,869.99
11,068.29

gonka1jrgm47v5eg876udmzg6j6glqcsd5x0vk6crpax
32,390.2
8,543.71
0.00
8,543.71

gonka1ujnc662v6g69jm6fgxnr79a2m7ehzeut059239
28,109.2
7,414.49
0.00
7,414.49

(10 more — see compensation_266_nonces.csv)

Part 1 total: 183,605.74 GONKA

Part 2: Delegation compensation (9 participants)

9 participants delegated their Kimi weight to gonka1q5xt54... (excluded operator).
The chain penalised them 15% (ModeNone) instead of transferring 5% (ModeDelegate) —
net extra weight loss of 10% per participant.

compensation = (original_weight × 0.10) / total_epoch_weight × epoch_reward

Address
Extra weight lost
Owed (GONKA)

gonka1tja3g2da45efhe2p83gk3whtussmgmtsdlgprt
2,124.3
1,805.14

gonka1hwvel7n3zuk6wruefuzc356l9myske9stckwnz
1,854.1
1,575.51

gonka12pcu9mcrpa4w4sjd9y3dsksnvu495ss6f9r4ra
1,372.7
1,166.44

gonka1tlvg4kjx7ljd5thgd5fkgh39q6lu8cmxupktgg
207.4
176.25

gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p
134.0
113.86

gonka1cuwejs77gectp3n32wg8q27hlsa4m3hqspf4ww
127.5
108.37

gonka1tmk2tzdneht6smu34pkmqdvu7p34qavvmwtwq2
118.3
100.57

gonka1gyk0aahvr3qeju4zx0nplfreej6cy4jjk8svc5
36.5
30.99

gonka14ef2pxjge75gflqftn7m2wy0xv59gq9uc7qnct
18.4
15.60

Part 2 total: 5,092.73 GONKA

Epoch 266 Grand Total: 188,698.47 GONKA (18 nonce + 9 delegation participants)

Output: e266/compensation_266.json

Epoch 267 — ComputeGroupCap (worst epoch)

All Kimi operators entered the epoch, but the Kimi group's raw weight (899,487)
far exceeded the ComputeGroupCap (0.75 × epoch 266 total weight 335,159 = 251,369).
The e266 total weight was severely depressed by a targeted external attack on Kimi
vLLM nodes, which crashed most operators and collapsed network weight to 335k. This
destroyed the N-1 reference weight used by the cap formula for e267 — when Kimi
operators returned with full accumulated confirmation weight, the mismatch caused the
worst inversion of the entire incident (conf/weight ratio 1.75×).

compensation = max(0, confirmation_weight / EpochGroupData.total_weight × epoch_reward − actual_rewards)

Metric
Value

Kimi participants in epoch
27

Affected participants
25

Total compensation
246,471.82 GONKA

Output: e267/compensation_267.csv · e267/compensation_267.json

Epoch 268 — ComputeGroupCap

Cap baseline rose (using epoch 267's total weight), but Kimi's conf_weight remained
above cap at 85.2% of total network weight. Conf/weight ratio 0.85×.

Metric
Value

Kimi participants in epoch
20

Affected participants
11

Total compensation
42,634.68 GONKA

Output: e268/compensation_268.csv · e268/compensation_268.json

Epoch 269 — ComputeGroupCap

Kimi conf_weight at 87.6% of total network weight. Conf/weight ratio ~1.00×.

Metric
Value

Kimi participants in epoch
30

Affected participants
19

Total compensation
47,504.58 GONKA

Output: e269/compensation_269.csv · e269/compensation_269.json

Epoch 270 — ComputeGroupCap

Kimi conf_weight at 94.9% of total network weight. Conf/weight ratio 1.23×.

Metric
Value

Kimi participants in epoch
23

Affected participants
19

Total compensation
76,870.08 GONKA

Output: e270/compensation_270.csv · e270/compensation_270.json

Epoch 271 — ComputeGroupCap

Kimi conf_weight at 80.5% of total network weight. Conf/weight ratio 0.95×.

Metric
Value

Kimi participants in epoch
23

Affected participants
17

Total compensation
28,422.15 GONKA

Output: e271/compensation_271.csv · e271/compensation_271.json

Epoch 272 — ComputeGroupCap

Kimi conf_weight at 80.0% of total network weight. Conf/weight ratio 0.88×.

Metric
Value

Kimi participants in epoch
23

Affected participants
11

Total compensation
16,988.15 GONKA

Output: e272/compensation_272.csv · e272/compensation_272.json

Epoch 273 — ComputeGroupCap (second inversion)

Kimi node count jumped to 81 nodes (30 participants). Kimi conf_weight reached 107.5%
of total network weight — a second inversion. Conf/weight ratio 1.18×.

Metric
Value

Kimi participants in epoch
30

Affected participants
20

Total compensation
86,243.30 GONKA

Output: e273/compensation_273.csv · e273/compensation_273.json

Epoch 274 — ComputeGroupCap

Kimi conf_weight at 88.5% of total network weight. Conf/weight ratio 0.97×.

Metric
Value

Kimi participants in epoch
24

Affected participants
9

Total compensation
41,818.44 GONKA

Output: e274/compensation_274.csv · e274/compensation_274.json

Epoch 275 — ComputeGroupCap

Kimi conf_weight at 103.6% of total network weight. Conf/weight ratio 1.28×.

Metric
Value

Kimi participants in epoch
24

Affected participants
18

Total compensation
89,984.78 GONKA

Output: e275/compensation_275.csv · e275/compensation_275.json

Epoch 276 — ComputeGroupCap

v0.2.13 activated at block 4,267,300 (mid-epoch), reducing Kimi's WeightScaleFactor
to 0.78. Compensation is calculated against the full epoch end state (block 4,279,520)
using the post-upgrade weights and rewards as recorded by the chain.

Metric
Value

Kimi participants in epoch
23

Affected participants
11

Total compensation
50,281.35 GONKA

Output: e276/compensation_276.csv · e276/compensation_276.json

Grand Total

Epoch
Issue
Affected
Compensation (GONKA)

265
CPoC degradation
3
30,592.10

266
Nonce exclusion + delegation
18 + 9
188,698.47

267
ComputeGroupCap
25
246,471.82

268
ComputeGroupCap
11
42,634.68

269
ComputeGroupCap
19
47,504.58

270
ComputeGroupCap
19
76,870.08

271
ComputeGroupCap
17
28,422.15

272
ComputeGroupCap
11
16,988.15

273
ComputeGroupCap
20
86,243.30

274
ComputeGroupCap
9
41,818.44

275
ComputeGroupCap
18
89,984.78

276
ComputeGroupCap
11
50,281.35

TOTAL

53 unique addresses
946,509.93 GONKA

Per-address breakdown: aggregate_compensation.json · aggregate_compensation.csv

Issue resolved in e277 following v0.2.13 upgrade. No further compensation required.

Repository Structure

.py
│ ├── compensation_.csv
│ ├── compensation_.json
│ ├── epoch_commits.json
│ ├── epoch_group_data.json
│ └── epoch_performance.json">gonka-e26x-issue/
├── README.md ← this file
├── weight_fluctuation_analysis.md ← full root cause analysis, Kimi weight history
├── aggregate_compensation.py ← aggregates all epochs into per-address totals
├── aggregate_compensation.json ← per-address totals (machine-readable)
├── aggregate_compensation.csv ← per-address totals (spreadsheet)
├── poc_commits/ ← raw nonce commits fetched from chain
├── e265/ ← CPoC degradation
│ ├── calculate_compensation_265.py
│ ├── compensation_265.csv
│ └── compensation_265.json
├── e266/ ← nonce exclusion + delegation
│ ├── calculate_compensation_266.py
│ ├── DELEGATION.md
│ ├── compensation_266_nonces.csv
│ ├── compensation_266_delegation.csv
│ ├── compensation_266_combined.csv
│ └── compensation_266.json
├── e267/ … e276/ ← ComputeGroupCap (one directory per epoch)
│ ├── calculate_compensation_.py
│ ├── compensation_.csv
│ ├── compensation_.json
│ ├── epoch_commits.json
│ ├── epoch_group_data.json
│ └── epoch_performance.json

Running the Analysis

Requires the inferenced binary and archive node access. Configure via .env:

:26657
INFERENCED_BINARY=/path/to/inferenced">ARCHIVE_NODE_URL=http://:26657
INFERENCED_BINARY=/path/to/inferenced

The .env is loaded from ../gonka-segment-report/.env.

# Run any epoch's calculator
python3 e267/calculate_compensation_267.py

# Regenerate aggregate per-address totals
python3 aggregate_compensation.py

Chain Query Reference

All queries use --height pinned to the epoch end block to read state before pruning.

 \
 --node --height -o json

# Epoch group data (validation weights, confirmation weights)
inferenced query inference show-epoch-group-data \
 --node --height -o json

# Per-participant reward summary
inferenced query inference show-epoch-performance-summary-by-participant \
 --node -o json

# Delegation snapshot (query at poc_start - 500)
inferenced query inference poc-delegation \
 --node --height -o json"># PoC nonce commits for an epoch
inferenced query inference all-poc-v2-store-commits poc_start> \
 --node ARCHIVE_NODE> --height epoch_end> -o json

# Epoch group data (validation weights, confirmation weights)
inferenced query inference show-epoch-group-data epoch> \
 --node ARCHIVE_NODE> --height epoch_end> -o json

# Per-participant reward summary
inferenced query inference show-epoch-performance-summary-by-participant \
 epoch> address> --node ARCHIVE_NODE> -o json

# Delegation snapshot (query at poc_start - 500)
inferenced query inference poc-delegation address> \
 --node ARCHIVE_NODE> --height poc_start - 500> -o json

Epoch
poc_start
epoch_end

265
4,089,970
4,105,360

266
4,105,361
4,120,751

267
4,120,752
4,136,142

268
4,136,143
4,151,533

269
4,151,534
4,166,924

270
4,166,925
4,182,315

271
4,182,316
4,197,706

272
4,197,707
4,213,097

273
4,213,098
4,228,488

274
4,228,489
4,243,879

275
4,249,774
4,259,270

276
4,264,130
4,279,520
