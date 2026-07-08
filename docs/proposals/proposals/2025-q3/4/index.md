---
title: "#4 – Upgrade Proposal: v0.2.2"
description: "Upgrade Proposal: v0.2.2"
template: proposals-proposals-main.html
---

# #4 – Upgrade Proposal: v0.2.2

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-rejected">Rejected</span>

**Proposal ID:** `4`

**Type:** Software Upgrade

**Submit:** 2025-09-22 10:02 UTC

**Voting:** 2025-09-22 10:02 UTC → 2025-09-24 10:02 UTC

**Proposer:** [`gonka18lluv53n4h9z34qu20vxcvypgdkhsg6nn2cl2d`](https://gonka.gg/address/gonka18lluv53n4h9z34qu20vxcvypgdkhsg6nn2cl2d){:target="_blank"}

**Metadata:** [https://github.com/gonka-ai/gonka/blob/f0f3301dadae0a2f30bdc2968bebb21da81026f4/proposals/governance-artifacts/update-v0.2.2/README.md](https://github.com/gonka-ai/gonka/blob/f0f3301dadae0a2f30bdc2968bebb21da81026f4/proposals/governance-artifacts/update-v0.2.2/README.md)

**Failed reason:** proposal did not get enough votes to pass



[View on gonka.gg](https://gonka.gg/network/proposals/4){:target="_blank"}

</div>

Upgrade Proposal: v0.2.2

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:0.1%"></div>
    <div class="prop-tally-no" style="width:0.0%"></div>
    <div class="prop-tally-veto" style="width:99.9%"></div>
    <div class="prop-tally-abstain" style="width:0.0%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes 109 (0.1%)</span>
    <span class="prop-tally-no-text">No 0 (0.0%)</span>
    <span class="prop-tally-veto-text">Veto 109,637 (99.9%)</span>
    <span class="prop-tally-abstain-text">Abstain 0 (0.0%)</span>
    <span class="prop-tally-total-text">Total 109,746 votes</span>
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
      "name": "v0.2.2",
      "time": "0001-01-01T00:00:00Z",
      "height": "512000",
      "info": "{\n        \"binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.2-upgrade/inferenced-amd64.zip?checksum=sha256:ef72ce742f545a6d14d76cf90f72f13cd786b09a7191bf6f1a88e05d865074c0\"\n        },\n        \"api_binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.2-upgrade/decentralized-api-amd64.zip?checksum=sha256:19659fb65acb0d21118024771a292c7b1ba70fc0627364e0911552797009a3c9\"\n        }\n    }",
      "upgraded_client_state": null
    }
  }
]
```

</details>

---