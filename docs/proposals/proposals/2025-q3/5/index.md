---
title: "#5 – Expedite voting for upgrades"
description: "Expedite voting for upgrades"
template: proposals-proposals-main.html
---

# #5 – Expedite voting for upgrades

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-passed">Passed</span>

**Proposal ID:** `5`

**Type:** Update Params

**Submit:** 2025-09-23 06:39 UTC

**Voting:** 2025-09-23 06:39 UTC → 2025-09-23 18:39 UTC

**Expedited:** Yes

**Proposer:** [`gonka18lluv53n4h9z34qu20vxcvypgdkhsg6nn2cl2d`](https://gonka.gg/address/gonka18lluv53n4h9z34qu20vxcvypgdkhsg6nn2cl2d){:target="_blank"}



[View on gonka.gg](https://gonka.gg/network/proposals/5){:target="_blank"}

</div>

Expedite voting for upgrades

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:100.0%"></div>
    <div class="prop-tally-no" style="width:0.0%"></div>
    <div class="prop-tally-veto" style="width:0.0%"></div>
    <div class="prop-tally-abstain" style="width:0.0%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes 172,265 (100.0%)</span>
    <span class="prop-tally-no-text">No 0 (0.0%)</span>
    <span class="prop-tally-veto-text">Veto 0 (0.0%)</span>
    <span class="prop-tally-abstain-text">Abstain 0 (0.0%)</span>
    <span class="prop-tally-total-text">Total 172,265 votes</span>
    
  </div>
</div>


---

## Messages

| # | Type |
| :- | :--- |
| 1 | `/cosmos.gov.v1.MsgUpdateParams` |

<details class="prop-contracts" markdown="1">
<summary markdown="1">Contract Details</summary>

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
