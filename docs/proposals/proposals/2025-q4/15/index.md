---
title: "#15 – Upgrade Proposal: v0.2.6"
description: "Upgrade Proposal: v0.2.6"
template: proposals-proposals-main.html
---

# #15 – Upgrade Proposal: v0.2.6

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-rejected">Rejected</span>

**Proposal ID:** `15`

**Type:** Software Upgrade

**Submit:** 2025-12-16 11:12 UTC

**Voting:** 2025-12-16 11:12 UTC → 2025-12-17 11:12 UTC

**Proposer:** [`gonka18lluv53n4h9z34qu20vxcvypgdkhsg6nn2cl2d`](https://gonka.gg/address/gonka18lluv53n4h9z34qu20vxcvypgdkhsg6nn2cl2d){:target="_blank"}

**Metadata:** [https://github.com/gonka-ai/gonka/blob/384b95025f11cff177fa40ec191f724852f54edb/proposals/governance-artifacts/update-v0.2.6/README.md](https://github.com/gonka-ai/gonka/blob/384b95025f11cff177fa40ec191f724852f54edb/proposals/governance-artifacts/update-v0.2.6/README.md)

**Failed reason:** proposal did not get enough votes to pass



[View on gonka.gg](https://gonka.gg/network/proposals/15){:target="_blank"}

</div>

Upgrade Proposal: v0.2.6

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
    <span class="prop-tally-yes-text">Yes 1,034,445 (100.0%)</span>
    <span class="prop-tally-no-text">No 0 (0.0%)</span>
    <span class="prop-tally-veto-text">Veto 0 (0.0%)</span>
    <span class="prop-tally-abstain-text">Abstain 0 (0.0%)</span>
    <span class="prop-tally-total-text">Total 1,034,445 votes</span>
    
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
      "name": "v0.2.6",
      "time": "0001-01-01T00:00:00Z",
      "height": "1773000",
      "info": "{\n        \"binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.6/inferenced-amd64.zip?checksum=sha256:cdbcfe214ce7eb2bab993bb344447b84602fb77e32c9a05f48e0671dd469c832\"\n        },\n        \"api_binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.6/decentralized-api-amd64.zip?checksum=sha256:abb5e3ba1db4beb6c1109b5a0cd1fbf226e19c108dc4f30a565582056123c394\"\n        }\n    }",
      "upgraded_client_state": null
    }
  }
]
```

</details>

---