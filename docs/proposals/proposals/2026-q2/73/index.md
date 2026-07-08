---
title: "#73 – Increase minimum governance deposit to 500 GNK and expedited minimum deposit to 1000 GNK"
description: "Increase the minimum deposit required to submit a governance proposal to 500 GNK (500,000,000,000 ngonka) and expedited minimum deposit to 1000 GNK (1,000,000,000,000 ngonka). This resubmits proposal "
template: proposals-proposals-main.html
---

# #73 – Increase minimum governance deposit to 500 GNK and expedited minimum deposit to 1000 GNK

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-passed">Passed</span>

**Proposal ID:** `73`

**Type:** Update Params

**Submit:** 2026-06-10 07:32 UTC

**Voting:** 2026-06-10 07:32 UTC → 2026-06-12 07:32 UTC

**Proposer:** `gonka1337v0tk0ng0dhmz2pk9qv0gsvpe48eafppc6u8`



[View on gonka.gg](https://gonka.gg/network/proposals/73){:target="_blank"}

</div>

Increase the minimum deposit required to submit a governance proposal to 500 GNK (500,000,000,000 ngonka) and expedited minimum deposit to 1000 GNK (1,000,000,000,000 ngonka). This resubmits proposal #69 which passed community vote but failed to execute due to incomplete governance parameter specification.

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:96.3%"></div>
    <div class="prop-tally-no" style="width:0.0%"></div>
    <div class="prop-tally-veto" style="width:0.2%"></div>
    <div class="prop-tally-abstain" style="width:3.5%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes 295,843 (96.3%)</span>
    <span class="prop-tally-no-text">No 40 (0.0%)</span>
    <span class="prop-tally-veto-text">Veto 572 (0.2%)</span>
    <span class="prop-tally-abstain-text">Abstain 10,823 (3.5%)</span>
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
          "amount": "500000000000"
        }
      ],
      "max_deposit_period": "86400s",
      "voting_period": "172800s",
      "quorum": "0.250000000000000000",
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
          "amount": "1000000000000"
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