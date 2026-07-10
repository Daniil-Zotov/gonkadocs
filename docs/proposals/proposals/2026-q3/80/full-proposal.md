# GRC Proposal #3 - Restitution

This proposal closes the confirmed GRC3 restitution package, separating committee-confirmed damage into victim restitution and committee work/bounty payments.

## Executive Summary

GRC Proposal #3 closes the confirmed GRC3 restitution package and separates two different payment classes:

| Payment class | Amount | Chain representation |
|---|---:|---|
| Committee-confirmed damage before overlap deductions | 99773.810455897 GNK | Settlement basis, before already-paid P4 deductions |
| Victim restitution after exact P4 overlap deductions | 70154.024668251 GNK | Settlement basis before chain minimum handling |
| Chain minimum top-up for positive victim outputs below 10 GNK | 30.808440219 GNK | Added so every positive victim output satisfies the chain transfer minimum |
| Victim chain transfer total | 70184.833108470 GNK | One `MsgBatchTransferWithVesting` message |
| Committee review, investigation, validation, and coordination work | 47850.000000000 GNK | Five `MsgCommunityPoolSpend` messages |
| **Total proposal spend** | **118034.833108470 GNK** | `proposal.json` |

The committee/work amount is not an additional victim-damage claim. It is a fixed work and bounty package for case investigation, independent validation, additional review, reconciliation, and proposal coordination.

## Final Victim Settlement

The victim settlement uses exact same-address, same-epoch P4 overlap deductions:

```
final_payout = max(planned_amount - p4_paid_overlap, 0)
```

| Metric | Amount / Count |
|---|---:|
| Committee-confirmed damage before overlap deductions | 99773.810455897 GNK |
| Exact P4 paid overlap | 34944.788622168 GNK |
| Deducted from Proposal #3 payout | 29619.785787646 GNK |
| P4 overpaid amount recorded for audit only | 5325.002834522 GNK |
| Final victim payout | 70154.024668251 GNK |
| Chain minimum top-up for positive outputs below 10 GNK | 30.808440219 GNK |
| Victim chain transfer total | 70184.833108470 GNK |
| Settlement rows | 47 |
| Unique planned recipients | 44 |
| Positive chain recipients after zeroed overlaps | 40 |
| Rows with exact P4 overlap | 7 |

Rows where P4 already paid more than the planned amount are floored at zero. Seven positive victim outputs below the chain transfer minimum of 10 GNK are raised to exactly 10 GNK in the chain payload.

## GRC Case Review

| Case | Decision | Final victim payout |
|---|---:|---:|
| Case 01: High miss rate / devshard issue | Included. Seven rows retained, including the manual-review row. | 35109.923355683 GNK |
| Case 02: Settle-drop / negative balance | Included after independent review. Broader rule questions deferred to next GRC task cycle. | 1075.336150923 GNK |
| Case 03: Failed cPoC / preserved Kimi shortfall | Included for epoch 267; epoch 265 extension zeroed by exact P4 overlap. | 10262.057515369 GNK |
| Case 04: UpgradeProtectionWindow / cPoC misfire | Included with exact P4 overlap deductions applied row by row. | 23706.707646276 GNK |
| Case 05: Kimi restitution aggregate, epochs 265-276 | Rejected as aggregate compensation. Used only as overlap evidence and bounty-eligible investigation work. GRC acknowledges open questions for deeper review. | 0.000000000 GNK |

## Committee Work Package

The role package compensates completed work across investigation, validation, additional checks, attack review, and coordination.

| Metric | Value |
|---|---:|
| Non-zero role lines | 12 |
| Total role/work payout | 47850.000000000 GNK |
| Distinct payout addresses | 5 |

| Case | Investigation / Calculation | Validation / Review | Coordination |
|---|---|---|---|
| Case 01 | @Operator investigated high miss-rate / devshard issue | @mich validated | @Operator coordinated |
| Case 02 | @max investigated settle-drop / negative balance | @den validated | @Operator coordinated |
| Case 03 | @mich investigated failed cPoC / Kimi shortfall | @den validated | @Operator coordinated |
| Case 04 | @max investigated UpgradeProtectionWindow / cPoC misfire | @Operator validated | @Operator coordinated |
| Case 05 | @votkon investigated Kimi restitution aggregate | @max + @mich paid review | @Operator coordinated |

## Chain Payload

The governance payload contains:
- One victim vesting batch with 40 positive recipients (7 raised to 10 GNK minimum)
- Five committee/work `MsgCommunityPoolSpend` messages
- Deposit, metadata, title, and summary from role config

## Verification

The verification script checks:
- CSV totals against settlement.json
- Row-level overlap math with exact 9-decimal ngonka arithmetic
- Case totals for Case 01 through Case 04
- Role/work total and final proposal total
- Generated proposal artifacts match deterministic rebuild output

## Source

Full audit trail, payout breakdown, and chain-ready JSON:
- GitHub: [https://github.com/huxuxuya/GRC-3-result](https://github.com/huxuxuya/GRC-3-result)
- Dashboard: [https://huxuxuya.github.io/GRC-3-result/](https://huxuxuya.github.io/GRC-3-result/)
