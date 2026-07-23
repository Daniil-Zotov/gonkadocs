---
title: "#25 – Upgrade Proposal: v0.2.8"
description: "Upgrade Proposal: v0.2.8"
template: proposals-proposals-main.html
---

# #25 – Upgrade Proposal: v0.2.8

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-passed">Passed</span>

**Proposal ID:** `25`

**Type:** Software Upgrade

**Submit:** 2026-01-28 03:02 UTC

**Voting:** 2026-01-28 03:02 UTC → 2026-01-29 03:02 UTC

**Proposer:** [`gonka18lluv53n4h9z34qu20vxcvypgdkhsg6nn2cl2d`](https://gonka.gg/address/gonka18lluv53n4h9z34qu20vxcvypgdkhsg6nn2cl2d){:target="_blank"}

**Metadata:** [https://github.com/gonka-ai/gonka/blob/9241d81b9ed7f33f6864476c2b07c9e833037735/proposals/governance-artifacts/update-v0.2.8/README.md](https://github.com/gonka-ai/gonka/blob/9241d81b9ed7f33f6864476c2b07c9e833037735/proposals/governance-artifacts/update-v0.2.8/README.md)



[View on gonka.gg](https://gonka.gg/network/proposals/25){:target="_blank"}

</div>

Upgrade Proposal: v0.2.8

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:559.9%"></div>
    <div class="prop-tally-no" style="width:0.0%"></div>
    <div class="prop-tally-veto" style="width:0.0%"></div>
    <div class="prop-tally-abstain" style="width:0.0%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes 4,153,562 (100.0%)</span>
    <span class="prop-tally-no-text">No 0 (0.0%)</span>
    <span class="prop-tally-veto-text">Veto 0 (0.0%)</span>
    <span class="prop-tally-abstain-text">Abstain 0 (0.0%)</span>
    <span class="prop-tally-total-text">Total 4,153,562 votes</span>
    
  </div>
</div>


---

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
      "name": "v0.2.8",
      "time": "0001-01-01T00:00:00Z",
      "height": "2387000",
      "info": "{\n        \"binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.8-post1/inferenced-amd64.zip?checksum=sha256:f0f2e3ee8760e40a78087c98c639a7518bf062138141ed4aec2120f5bc622a67\"\n        },\n        \"api_binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.8-post1/decentralized-api-amd64.zip?checksum=sha256:45f28afba4758e54988f61cc358f0ad683e7832ab121ccd54b684fe4c9381a75\"\n        }\n    }",
      "upgraded_client_state": null
    }
  }
]
```

</details>
