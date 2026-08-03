---
title: "#19 – Upgrade Proposal: v0.2.7"
description: "Upgrade Proposal: v0.2.7"
template: proposals-proposals-main.html
---

# #19 – Upgrade Proposal: v0.2.7

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-passed">Passed</span>

**Proposal ID:** `19`

**Type:** Software Upgrade

**Submit:** 2026-01-07 04:23 UTC

**Voting:** 2026-01-07 04:23 UTC → 2026-01-08 04:23 UTC

**Proposer:** [`gonka18lluv53n4h9z34qu20vxcvypgdkhsg6nn2cl2d`](https://gonka.gg/address/gonka18lluv53n4h9z34qu20vxcvypgdkhsg6nn2cl2d){:target="_blank"}

**Metadata:** [https://github.com/gonka-ai/gonka/blob/d18165669326fffd6732bc124183a72c076a69ee/proposals/governance-artifacts/update-v0.2.7/README.md](https://github.com/gonka-ai/gonka/blob/d18165669326fffd6732bc124183a72c076a69ee/proposals/governance-artifacts/update-v0.2.7/README.md)



[View on gonka.gg](https://gonka.gg/network/proposals/19){:target="_blank"}

</div>

Upgrade Proposal: v0.2.7

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:523.9%"></div>
    <div class="prop-tally-no" style="width:20.0%"></div>
    <div class="prop-tally-veto" style="width:1.1%"></div>
    <div class="prop-tally-abstain" style="width:0.0%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes <strong>96.1%</strong> (3,886,156)</span>
    <span class="prop-tally-no-text">No <strong>3.7%</strong> (148,604)</span>
    <span class="prop-tally-veto-text">Veto <strong>0.2%</strong> (8,096)</span>
    <span class="prop-tally-abstain-text">Abstain <strong>0.0%</strong> (0)</span>
    <span class="prop-tally-total-text">Total 4,042,856 votes</span>
    
  </div>
</div>


## Messages

| # | Type |
| :- | :--- |
| 1 | `/cosmos.upgrade.v1beta1.MsgSoftwareUpgrade` |

<details class="prop-contracts" markdown="1">
<summary markdown="1">Contract Details</summary>

```json
[
  {
    "@type": "/cosmos.upgrade.v1beta1.MsgSoftwareUpgrade",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "plan": {
      "name": "v0.2.7",
      "time": "0001-01-01T00:00:00Z",
      "height": "2054000",
      "info": "{\n        \"binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.7/inferenced-amd64.zip?checksum=sha256:b7c9034a2a4e1b2fdd525bd45aa32540129c55176fd7a223a1e13a7e177b3246\"\n        },\n        \"api_binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.7/decentralized-api-amd64.zip?checksum=sha256:03555ba60431e72bd01fe1fb1812a211828331f5767ad78316fdd1bcca0e2d52\"\n        }\n    }",
      "upgraded_client_state": null
    }
  }
]
```

</details>
