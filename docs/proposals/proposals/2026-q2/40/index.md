---
title: "#40 – Governance: extend voting period to 48 hours"
description: "This proposal updates x/gov: the standard voting period becomes 48 hours (was 24), and the expedited voting period becomes 12 hours (was 3). All other governance parameters remain at their current on-"
template: proposals-proposals-main.html
---

# #40 – Governance: extend voting period to 48 hours

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-passed">Passed</span>

**Proposal ID:** `40`

**Type:** Update Params

**Submit:** 2026-04-13 06:11 UTC

**Voting:** 2026-04-13 06:11 UTC → 2026-04-14 06:11 UTC

**Proposer:** `gonka1k6p754pyhxud2399knyccgjpjvdafj2u9xlgyf`

</div>

This proposal updates x/gov: the standard voting period becomes 48 hours (was 24), and the expedited voting period becomes 12 hours (was 3). All other governance parameters remain at their current on-chain values.

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:57.7%"></div>
    <div class="prop-tally-no" style="width:0.0%"></div>
    <div class="prop-tally-veto" style="width:1.8%"></div>
    <div class="prop-tally-abstain" style="width:40.5%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes 377,158 (57.7%)</span>
    <span class="prop-tally-no-text">No 0 (0.0%)</span>
    <span class="prop-tally-veto-text">Veto 12,030 (1.8%)</span>
    <span class="prop-tally-abstain-text">Abstain 264,790 (40.5%)</span>
  </div>
</div>


---

## Messages

| # | Type |
| :- | :--- |
| 1 | `/cosmos.gov.v1.MsgUpdateParams` |

<details class="prop-contracts">
<summary>Contract Details</summary>

```json
[
  {
    "@type": "/cosmos.gov.v1.MsgUpdateParams",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "params": {
      "min_deposit": [
        {
          "denom": "ngonka",
          "amount": "25000000"
        }
      ],
      "max_deposit_period": "86400s",
      "voting_period": "172800s",
      "quorum": "0.334000000000000000",
      "threshold": "0.500000000000000000",
      "veto_threshold": "0.334000000000000000",
      "min_initial_deposit_ratio": "0.000000000000000000",
      "proposal_cancel_ratio": "0.500000000000000000",
      "proposal_cancel_dest": "",
      "expedited_voting_period": "43200s",
      "expedited_threshold": "0.667000000000000000",
      "expedited_min_deposit": [
        {
          "denom": "ngonka",
          "amount": "50000000"
        }
      ],
      "burn_vote_quorum": false,
      "burn_proposal_deposit_prevote": false,
      "burn_vote_veto": true,
      "min_deposit_ratio": "0.010000000000000000"
    }
  }
]
```

</details>

---

<div class="prop-footer" markdown="1">

[View on gonka.gg](https://gonka.gg/network/proposals/40){:target="_blank"}

</div>
