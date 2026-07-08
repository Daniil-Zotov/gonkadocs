---
title: "#13 – Upgrade Proposal: v0.2.5"
description: "Upgrade Proposal: v0.2.5"
template: proposals-proposals-main.html
---

# #13 – Upgrade Proposal: v0.2.5

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-passed">Passed</span>

**Proposal ID:** `13`

**Type:** Software Upgrade

**Submit:** 2025-11-21 09:13 UTC

**Voting:** 2025-11-21 09:13 UTC → 2025-11-22 09:13 UTC

**Proposer:** [`gonka18lluv53n4h9z34qu20vxcvypgdkhsg6nn2cl2d`](https://gonka.gg/address/gonka18lluv53n4h9z34qu20vxcvypgdkhsg6nn2cl2d){:target="_blank"}

**Metadata:** [https://github.com/gonka-ai/gonka/blob/e25ddb7d462972cce202c8b39448bf3feb8e29a0/proposals/governance-artifacts/update-v0.2.5/README.md](https://github.com/gonka-ai/gonka/blob/e25ddb7d462972cce202c8b39448bf3feb8e29a0/proposals/governance-artifacts/update-v0.2.5/README.md)



[View on gonka.gg](https://gonka.gg/network/proposals/13){:target="_blank"}

</div>

Upgrade Proposal: v0.2.5

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
    <span class="prop-tally-yes-text">Yes 428,459 (100.0%)</span>
    <span class="prop-tally-no-text">No 0 (0.0%)</span>
    <span class="prop-tally-veto-text">Veto 0 (0.0%)</span>
    <span class="prop-tally-abstain-text">Abstain 0 (0.0%)</span>
    <span class="prop-tally-quorum-text">Quorum 25.0%</span>
  </div>
</div>


---

## Messages

| # | Type |
| :- | :--- |
| 1 | `/cosmos.upgrade.v1beta1.MsgSoftwareUpgrade` |

<details class="prop-contracts">
<summary>Contract Details</summary>

```json
[
  {
    "@type": "/cosmos.upgrade.v1beta1.MsgSoftwareUpgrade",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "plan": {
      "name": "v0.2.5",
      "time": "0001-01-01T00:00:00Z",
      "height": "1404000",
      "info": "{\n        \"binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.5/inferenced-amd64.zip?checksum=sha256:fab7be9bcdb4e21f058e6d19cfd698b6862bf6f5a8aeecbf9165907fc7edcc64\"\n        },\n        \"api_binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.5/decentralized-api-amd64.zip?checksum=sha256:6fd12cd92e8226866be76a5e63a57e1b0041c7679db047af75e764e98668cb91\"\n        }\n    }",
      "upgraded_client_state": null
    }
  }
]
```

</details>

---