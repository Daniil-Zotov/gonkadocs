# Kimi cPoC Validation Failure, Epochs 306–309

| Field | Value |
|---|---|
| **Case** | Kimi operator restitution: cPoC validation failure (e306–e307) + bootstrap carry-over (e309) |
| Epochs affected | 306, 307, 309 |
| Affected participants | 19 unique addresses |
| Estimated compensation | 175,082.07 GONKA |
| **Cause** | The Kimi cPoC validation path failed starting in epoch 306. Validator nodes were unable to vote on submitted Kimi nonces, causing `confirmation_weight` to be severely suppressed for Kimi operators while non-Kimi operators ran normally. The issue persisted through e307 and carried into the e309 bootstrap attempt. |
| **Can it happen again?** | Reduced risk — the validation infrastructure was reviewed and a guardian node is explicitly designated for Kimi bootstrap support from e311 onward (per proposal #79). |
| **Mitigation / fix** | Proposal #78 (June 25, 2026) removed Kimi from the active model lineup. Proposal #79 (June 26, 2026, expedited) restored Kimi with `weight_scale_factor=0.9` and added `zai-org/GLM-5.2-FP8`. Epoch 311 is the first clean epoch. |

---

## Overview

Starting in epoch 306, `moonshotai/Kimi-K2.6` operators experienced a severe
confirmation weight collapse. The Kimi cPoC validation path stopped functioning:
other network participants could not vote on Kimi cPoC submissions, so nonces
accumulated as "no vote" weight rather than approved weight. This drove confirm
ratios down to near zero for Kimi operators while all non-Kimi operators
continued operating normally at 97–125% confirm ratios.

The chain's reward formula uses `confirmation_weight` as the measure of
confirmed work. Operators whose confirmation weight was suppressed received
proportionally less than their earned share of epoch rewards.

E305 (the epoch immediately before) is confirmed clean — Kimi operators had
normal confirm ratios across the board. The failure began in e306.

Governance proposal #78 (passed June 25, 2026) removed Kimi from the active
model lineup while the issue was diagnosed. Proposal #79 (passed June 26,
2026, expedited, 12h voting window) restored Kimi with revised parameters.
The first bootstrap attempt under the restored params was epoch 309, in which
Kimi operators again experienced partial confirmation weight suppression —
the underlying issue had not been fully resolved. Epoch 311 is the first epoch
where Kimi operated cleanly.

---

## Epoch Block Heights

| Epoch | PoC Start | Epoch End | Notes |
|-------|-----------|-----------|-------|
| 305 | 4,705,610 | 4,721,400 | Clean baseline — all Kimi operators healthy |
| 306 | 4,721,001 | 4,736,791 | **First failure epoch** |
| 307 | 4,736,392 | 4,752,182 | **Failure continues — worsens** |
| 308 | 4,751,783 | 4,767,573 | Kimi removed by prop #78 — no compensation |
| 309 | 4,767,174 | 4,782,964 | **Bootstrap attempt — partial failure** |
| 310 | 4,782,565 | 4,798,355 | Zero Kimi commits — no compensation |
| 311 | 4,797,956 | 4,813,746 | Bootstrap succeeds — clean |

Reward formula: `323,000 × e^(−0.000475 × (epoch − 1))` GONKA.

| Epoch | Theoretical Reward |
|-------|--------------------|
| 306 | 279,437.13 GONKA |
| 307 | 279,304.43 GONKA |
| 309 | 279,039.21 GONKA |

---

## Root Cause Evidence

`confirmation_weight` is initialized at epoch start from a fresh ML-node
measurement and can only be lowered by subsequent cPoC min-take events. The
diagnostic signal is whether `conf_w < weight` at epoch end — if so, at least
one cPoC event drove a penalty for that node. Non-Kimi operators are shown for
comparison.

### Epoch 305 — Baseline (clean)

No systematic conf_w suppression concentrated on Kimi operators. **Out of scope.**

### Epoch 306 — First failure

All non-Kimi operators: `conf_w ≥ weight` (no cPoC penalty).
Kimi operators with `conf_w < weight` (penalized by cPoC events):

| Address | weight | conf_w | models |
|---------|--------|--------|--------|
| `gonka1jfv9n2af9y8xgnn6834mnp924vkpucmvchsq8d` | 9,173 | 0 | Kimi only |
| `gonka1yal0ysgzc860zt3y8cds8656tnueusgymftvkw` | 29,693 | 4,724 | Kimi + other |
| `gonka1kx9mca3xm8u8ypzfuhmxey66u0ufxhs7nm6wc5` | 12,012 | 2,194 | Kimi + other |
| `gonka1gvrrhjmy4w4mayvs2s5l23edj8ertcmtd2v4zr` | 24,062 | 4,805 | Kimi + other |
| `gonka1y2a9p56kv044327uycmqdexl7zs82fs5ryv5le` | 3,885 | 1,307 | Kimi + other |
| `gonka168rtjfkszuhcggg4dfyse4yh7xn9zwfglnkns2` | 11,768 | 5,916 | Kimi + other |
| `gonka1gtdrqh9jpkqxdaskxkpwjpy2q284q8qnvg58uj` | 9,202 | 4,814 | Kimi only |
| `gonka125n6kr5gvdup0lndfkps7t6rd6592panhrg3np` | 24,804 | 17,394 | Kimi only |
| `gonka1ym3np7guxart483yfdxnlztuazx22cjt0e4a2p` | 5,841 | 4,818 | Kimi + other |
| `gonka1d694r00czmq75txghwjcuk07lxvc8d4ekgsha0` | 41,468 | 36,235 | Kimi + other |

Five additional pure-Kimi nodes had `conf_w ≥ weight` in e306 — no cPoC
penalty was applied to them in this epoch. All five collapse to `conf_w = 0`
in e307 (see investigation section).

`gonka1qa90...` had `weight = 0` in vw (excluded from the group) — omitted.

Screenshot evidence (CPoC #3, block 4,733,605 — within e306):
`gonka1yal0ysgzc860zt3y8cds8656tnueusgymftvkw` showed weight=29,693,
confirm ratio=20.31%, validation **NOT PASSED**, with 36.2% "No vote" weight —
validators were unable to vote on this node's Kimi cPoC submissions.

Screenshot evidence (CPoC #3, block 4,733,605 — within e306):
`gonka1yal0ysgzc860zt3y8cds8656tnueusgymftvkw` showed weight=29,693,
confirm ratio=20.31%, validation **NOT PASSED**, with 36.2% "No vote" weight —
validators were unable to vote on this node's Kimi cPoC submissions.

### Epoch 307 — Failure worsens

Non-Kimi operators: 97–160% confirm ratios.
Kimi operators — near-total collapse:

| Address | weight | conf_w | ratio | excluded from vw |
|---------|--------|--------|-------|-----------------|
| `gonka1qa90tgczc0k5dvk4l5nvlf5y6phgm6mg22sfjv` | — | — | — | Yes (commits=15,072) |
| `gonka1uhqpup9fev3zahlx6n326lp0krznc6usjtx6lu` | — | — | — | Yes (commits=10,720) |
| `gonka16j7xfk3hvguy5gz95mzg3p5dkuwla7aux03kdw` | 8,369 | 0 | 0.00% | |
| `gonka1aw77zuy536tufqd56zfq6ev3234u5ftty0zkte` | 8,407 | 0 | 0.00% | |
| `gonka1f0u3y2wneer8zhz3ypw4x54h38cpa0qsy8ts3e` | 8,309 | 0 | 0.00% | |
| `gonka1gtdrqh9jpkqxdaskxkpwjpy2q284q8qnvg58uj` | 9,381 | 0 | 0.00% | |
| `gonka1skw86pm4dvfhzslu5a9gsc98ahspalge8rprp4` | 8,249 | 0 | 0.00% | |
| `gonka1ujg4pt8crhxdymnsatalzdj0hhkgfqjmlp9zel` | 8,389 | 0 | 0.00% | |
| `gonka1yal0ysgzc860zt3y8cds8656tnueusgymftvkw` | 28,873 | 983 | 3.40% | |
| `gonka168rtjfkszuhcggg4dfyse4yh7xn9zwfglnkns2` | 11,714 | 1,053 | 8.99% | |
| `gonka1gvrrhjmy4w4mayvs2s5l23edj8ertcmtd2v4zr` | 19,938 | 4,995 | 25.05% | |
| `gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09` | 11,528 | 5,579 | 48.40% | |
| `gonka125n6kr5gvdup0lndfkps7t6rd6592panhrg3np` | 16,287 | 8,908 | 54.69% | |
| `gonka1d694r00czmq75txghwjcuk07lxvc8d4ekgsha0` | 41,105 | 34,864 | 84.82% | |
| `gonka1ym3np7guxart483yfdxnlztuazx22cjt0e4a2p` | 5,311 | 4,572 | 86.09% | |

Three zero-conf operators in e307 with **no Kimi commits** are excluded from
this case: `gonka15p7s7...` (no commits), `gonka1kx9...` (MiniMax+Qwen only),
`gonka1y2a9p5...` (MiniMax only) — their failures are independent of the Kimi
validation issue.

### Epoch 309 — Bootstrap attempt, partial failure

Non-Kimi operators: 97–100% confirm ratios.
Kimi bootstrap operators:

| Address | weight | conf_w | ratio |
|---------|--------|--------|-------|
| `gonka1kx9mca3xm8u8ypzfuhmxey66u0ufxhs7nm6wc5` | 4,921 | 0 | 0.00% |
| `gonka1yal0ysgzc860zt3y8cds8656tnueusgymftvkw` | 14,011 | 0 | 0.00% |
| `gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09` | 9,205 | 3,789 | 41.16% |
| `gonka1ym3np7guxart483yfdxnlztuazx22cjt0e4a2p` | 5,925 | 4,826 | 81.45% |
| `gonka1kvmerzu64094dt9t62ea0cp75larh39ulzldum` | 64,193 | 58,810 | 91.61% |

The same Kimi-specific suppression pattern is present. All 5 operators are
compensated — including `gonka1kvmerzu...` (91.61%) which received 36,802.80
GONKA actual vs 40,171.44 GONKA correct, resulting in 3,368.64 GONKA owed.

---

## cPoC Health Investigation

### Objective

Determine whether on-chain data confirms that the validation failure originated
from the guardian node, identify which other nodes shared the same failure mode,
and verify that no nodes were missed by the compensation scope.

### Findings

**Guardian node is itself a Kimi participant.**
`gonka1kx9mca3xm8u8ypzfuhmxey66u0ufxhs7nm6wc5` ran Kimi alongside MiniMax and
Qwen (27.8% of its commits were Kimi). Its own confirm ratio collapsed in e306
(0.183) and reached 0 in e307 and e309. This is consistent with a circular
failure: the guardian node's Kimi instance degraded, preventing it from
producing valid votes on other nodes' Kimi nonces. The guard being both a
validator and a Kimi participant means its own weight was suppressed at the same
time it lost the ability to validate others. **The guardian is included in the
compensation scope.**

**Five pure-Kimi nodes were not penalized in e306 but collapse to zero in e307.**
`confirmation_weight` is initialized from a fresh ML-node measurement and
lowered only by cPoC min-take. These five nodes ended e306 with `conf_w ≥ weight`
— meaning no cPoC event drove a penalty against their Kimi nonces in e306:

| Address | e306 weight | e306 conf_w | e307 conf_w |
|---------|------------|------------|------------|
| `gonka1skw86pm4dvfhzslu5a9gsc98ahspalge8rprp4` | 8,329 | 9,052 | 0 |
| `gonka16j7xfk3hvguy5gz95mzg3p5dkuwla7aux03kdw` | 8,229 | 8,963 | 0 |
| `gonka1ujg4pt8crhxdymnsatalzdj0hhkgfqjmlp9zel` | 8,150 | 9,054 | 0 |
| `gonka1uhqpup9fev3zahlx6n326lp0krznc6usjtx6lu` | 7,880 | 9,270 | — (excl. from vw) |
| `gonka1f0u3y2wneer8zhz3ypw4x54h38cpa0qsy8ts3e` | 8,407 | 9,008 | 0 |

All five ran Kimi exclusively. The fact that they escaped e306 unpenalized
while other Kimi nodes were heavily suppressed most likely reflects cPoC
sub-round assignment — their nonces landed in a validation window where the
Kimi path had not yet fully degraded. By e307 the degradation was total and
all five show `conf_w = 0`. This progression confirms a single root cause:
the Kimi validation path failed progressively through e306 and reached total
collapse in e307.

These five nodes were **already included in the e307 compensation scope** (as
zero-conf Kimi operators). They have no e306 compensation claim since no cPoC
penalty was applied to them in that epoch.

**Nodes with zero conf_w and no Kimi commits — independent failures.**
Three nodes in e306 had zero confirmation weight but submitted no Kimi commits:

| Address | weight | models | e307 status |
|---------|--------|--------|-------------|
| `gonka17ug06ua2a3hxjuh4punrryl6qzz03sp42u9z9q` | 1,457 | Qwen only | not in vw |
| `gonka1a3pkge3g33v3zdkq7qmycpjwpulms6ejt8z00f` | 119 | MiniMax only | not in vw |
| `gonka1u4zxypjgcr8khlzefwjr0vwdaj2uzruw2cehj3` | 712 | Qwen only | not in vw |

These failures are unrelated to the Kimi validation bug. They are excluded from
compensation, consistent with the treatment of independent zero-conf operators
in previous cases.

**Compensation scope is complete.**
All 10 nodes with Kimi commits and suppressed conf_w in e306 are in the
compensation scope. All affected e307 and e309 Kimi nodes are covered. No
on-chain evidence of Kimi-affected operators outside the current scope.

### Pruning Limitation

Detailed per-vote validation records (`list-inference-validation-details`,
`poc-validations-for-stage`) are pruned by the archive node after 2 epochs
(`inference_pruning_epoch_threshold: 2`). Per-stage conf_w snapshots within
e306 are therefore unavailable. The analysis above is based on final epoch-end
`validation_weights` from cached on-chain data, supplemented by the screenshot
evidence from cPoC #3 (block 4,733,605) showing "No vote" weight suppression in
real time.

---

## Delegation Impact

No delegation penalty compensation is required for any epoch in this case.

In e306 and e307 all affected Kimi operators entered the epoch group
(they appear in `validation_weights`), so their delegators were resolved into
`ModeDelegate` (5% weight transfer to operator) rather than `ModeNone`
(15% penalty). No extra loss was incurred by delegators beyond the normal
transfer — verified by querying delegation state for all 38 vw members at
the e306 snapshot height (poc_start − 500 = block 4,720,501): 24 addresses
held Kimi delegations pointing to operators that entered the epoch, all in
ModeDelegate.

The exception would be the 2 operators excluded from e307 vw entirely
(`gonka1qa90...`, `gonka1uhq...`) — their delegators would have been forced
into ModeNone. However, both operators were **Kimi-only** with no delegators
pointing to them in the snapshot (verified on-chain). No delegation
compensation is owed.

Delegators' own reward losses are already captured through their own
`validation_weights` entries and the standard compensation formula.

---

## Eligibility Criteria

An operator is eligible for compensation if:
1. They submitted Kimi PoC commits in the epoch, **and**
2. They are in `validation_weights` with `weight > 0` (or excluded from vw
   entirely but have on-chain commits — applies to 2 operators in e307), **and**
3. Their confirm ratio was depressed relative to the non-Kimi baseline
   (operationally: `actual_rewards < correct_reward`).

Operators with Kimi commits whose confirm ratio was **not** depressed (≥100%)
will produce zero compensation naturally from the formula and are excluded.

For mixed operators (Kimi + other models): the full `weight` is used as the
correct-reward baseline. This compensates for the total reward loss, whether
it came from their Kimi work or from their other-model work being dragged down
by the Kimi weight component. This is consistent with how the prior case
handled operators running multiple models.

---

## Compensation Methodology

The same formula used across all prior restitution cases:

```
correct_reward = weight / EpochGroupData.total_weight × epoch_reward
compensation   = max(0, correct_reward − actual_rewards_received)
```

For the 2 operators excluded from `validation_weights` in e307
(`gonka1qa90...`, `gonka1uhq...`): weight is reconstructed from on-chain
commit counts × `weight_scale_factor`.

Weight scale factor for `moonshotai/Kimi-K2.6` at e307 poc_start (height 4,736,392): `0.78`
(from chain params — v0.2.13 had set this at block 4,267,300).

---

## Governance Timeline

| Proposal | Title | Status | Vote | Date |
|----------|-------|--------|------|------|
| #78 | Governance 17: update PoC model lineup | Passed | 255,215 yes / 170 no / 7,390 abstain | June 25, 2026 |
| #79 | Add Kimi K2.6 and GLM 5.2 model | Passed | 330,364 yes / 0 no / 0 abstain | June 26, 2026 (expedited) |

**Proposal #78** removed Kimi and Qwen from PoC params, setting MiniMax as
the sole active model. Passed with overwhelming support.

**Proposal #79** restored Kimi with `weight_scale_factor=0.9` and
`penalty_start_epoch=310`, and added `zai-org/GLM-5.2-FP8` with
`weight_scale_factor=2.47` and `penalty_start_epoch=500`. Expedited voting
(12h) was required so the proposal could conclude before epoch 308 ended,
enabling bootstrap into epoch 309. Passed unanimously.

Bootstrap into e309: partial failure (same validation suppression).
Bootstrap into e311: succeeded — epoch 311 is the first clean epoch.

---

## Grand Total

| Epoch | Issue | Affected | Compensation (GONKA) |
|-------|-------|----------|----------------------|
| 306 | cPoC validation failure | 15 | 53,538.64 |
| 307 | cPoC validation failure (worsened) | 15 | 99,879.16 |
| 309 | Bootstrap carry-over | 5 | 21,664.28 |
| **TOTAL** | | **19 unique addresses** | **175,082.07 GONKA** |

Per-address breakdown: [`aggregate_compensation.json`](aggregate_compensation.json) · [`aggregate_compensation.csv`](aggregate_compensation.csv)

---

## Repository Structure

```
gonka-kimi-e306/
├── README.md                          ← this file
├── aggregate_compensation.py          ← aggregates all epochs into per-address totals
├── aggregate_compensation.json        ← per-address totals (machine-readable)
├── aggregate_compensation.csv         ← per-address totals (spreadsheet)
├── e306/
│   ├── calculate_compensation_306.py
│   ├── compensation_306.csv
│   └── compensation_306.json
├── e307/
│   ├── calculate_compensation_307.py
│   ├── compensation_307.csv
│   └── compensation_307.json
└── e309/
    ├── calculate_compensation_309.py
    ├── compensation_309.csv
    └── compensation_309.json
```

---

## Running the Analysis

Requires the `inferenced` binary and archive node access. Configure via `.env`:

```
ARCHIVE_NODE_URL=http://<archive-node>:26657
INFERENCED_BINARY=/path/to/inferenced
```

The `.env` is loaded from `../gonka-segment-report/.env`.

```bash
python3 e306/calculate_compensation_306.py
python3 e307/calculate_compensation_307.py
python3 e309/calculate_compensation_309.py
python3 aggregate_compensation.py
```

---

## Chain Query Reference

```bash
# PoC nonce commits for an epoch
inferenced query inference all-poc-v2-store-commits <poc_start> \
  --node <ARCHIVE_NODE> --height <epoch_end> -o json

# Epoch group data (validation weights, confirmation weights)
inferenced query inference show-epoch-group-data <epoch> \
  --node <ARCHIVE_NODE> --height <epoch_end> -o json

# Per-participant reward summary
inferenced query inference show-epoch-performance-summary-by-participant \
  <epoch> <address> --node <ARCHIVE_NODE> -o json
```

| Epoch | poc_start | epoch_end |
|-------|-----------|-----------|
| 306 | 4,721,001 | 4,736,791 |
| 307 | 4,736,392 | 4,752,182 |
| 309 | 4,767,174 | 4,782,964 |