---
title: "#69 – Increase minimum governance deposit to 500 GNK"
description: "Increase the minimum deposit required to submit a governance proposal from the current value to 500 GNK. Also sets expedited minimum deposit to 1000 GNK."
template: proposals-proposals-main.html
---

# #69 – Increase minimum governance deposit to 500 GNK

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-rejected">Failed</span>

**Proposal ID:** `69`

**Type:** Update Params

**Submit:** 2026-06-05 19:21 UTC

**Voting:** 2026-06-05 19:26 UTC → 2026-06-07 19:26 UTC

**Proposer:** [`gonka197hqnwcl30x4js3egvaujjmfknlxy7rmfw3y6k`](https://gonka.gg/address/gonka197hqnwcl30x4js3egvaujjmfknlxy7rmfw3y6k){:target="_blank"}

**Failed reason:** maximum deposit period must not be nil: 0



[View on gonka.gg](https://gonka.gg/network/proposals/69){:target="_blank"}

</div>

Increase the minimum deposit required to submit a governance proposal from the current value to 500 GNK. Also sets expedited minimum deposit to 1000 GNK.

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:26.9%"></div>
    <div class="prop-tally-no" style="width:0.0%"></div>
    <div class="prop-tally-veto" style="width:0.6%"></div>
    <div class="prop-tally-abstain" style="width:0.3%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes 199,799 (96.9%)</span>
    <span class="prop-tally-no-text">No 46 (0.0%)</span>
    <span class="prop-tally-veto-text">Veto 4,202 (2.0%)</span>
    <span class="prop-tally-abstain-text">Abstain 2,210 (1.1%)</span>
    <span class="prop-tally-total-text">Total 206,257 votes</span>
    
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
          "amount": "500000000000"
        }
      ],
      "max_deposit_period": null,
      "voting_period": null,
      "quorum": "",
      "threshold": "",
      "veto_threshold": "",
      "min_initial_deposit_ratio": "",
      "proposal_cancel_ratio": "",
      "proposal_cancel_dest": "",
      "expedited_voting_period": null,
      "expedited_threshold": "",
      "expedited_min_deposit": [
        {
          "denom": "ngonka",
          "amount": "1000000000000"
        }
      ],
      "burn_vote_quorum": false,
      "burn_proposal_deposit_prevote": false,
      "burn_vote_veto": false,
      "min_deposit_ratio": ""
    }
  }
]
```

</details>
