---
title: "#5 – Expedite voting for upgrades"
description: "Proposal #5"
template: proposals-proposals-main.html
---

# #5 – Expedite voting for upgrades

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-passed">Passed</span>

**Proposal ID:** `5`

**Type:** Update Params

**Submit:** 2026-01-01 00:00 UTC

**Voting:**  → 2026-01-02 00:00 UTC



[View on gonka.gg](https://gonka.gg/network/proposals/5){:target="_blank"}

</div>

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
      "max_deposit_period": "10800s",
      "voting_period": "10800s",
      "quorum": "0.334000000000000000",
      "threshold": "0.500000000000000000",
      "veto_threshold": "0.334000000000000000",
      "min_initial_deposit_ratio": "0.000000000000000000",
      "proposal_cancel_ratio": "0.500000000000000000",
      "proposal_cancel_dest": "",
      "expedited_voting_period": "5400s",
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