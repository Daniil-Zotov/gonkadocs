---
title: "#7 – Upgrade Proposal: v0.2.3"
description: "Upgrade Proposal: v0.2.3"
template: proposals-proposals-main.html
---

# #7 – Upgrade Proposal: v0.2.3

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-passed">Passed</span>

**Proposal ID:** `7`

**Type:** Software Upgrade

**Submit:** 2025-10-03 04:53 UTC

**Voting:** 2025-10-03 04:53 UTC → 2025-10-03 07:53 UTC

**Proposer:** [`gonka18lluv53n4h9z34qu20vxcvypgdkhsg6nn2cl2d`](https://gonka.gg/address/gonka18lluv53n4h9z34qu20vxcvypgdkhsg6nn2cl2d){:target="_blank"}

**Metadata:** [https://github.com/gonka-ai/gonka/blob/b8094aaf75bde4041692675dd9e565286b056896/proposals/governance-artifacts/update-v0.2.3/README.md](https://github.com/gonka-ai/gonka/blob/b8094aaf75bde4041692675dd9e565286b056896/proposals/governance-artifacts/update-v0.2.3/README.md)



[View on gonka.gg](https://gonka.gg/network/proposals/7){:target="_blank"}

</div>

Upgrade Proposal: v0.2.3

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
    <span class="prop-tally-yes-text">Yes 132,672 (100.0%)</span>
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
      "name": "v0.2.3",
      "time": "0001-01-01T00:00:00Z",
      "height": "645400",
      "info": "{\n        \"binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.3/inferenced-amd64.zip?checksum=sha256:7620b93420cc79087c04804b8d6bddf51da225877e9d7e872725076aee1e7c61\"\n        },\n        \"api_binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.3/decentralized-api-amd64.zip?checksum=sha256:41544b9a38df77e5cec1807db3e7a0598f13a26c24e4baa68022795dc62c406e\"\n        }\n    }",
      "upgraded_client_state": null
    }
  }
]
```

</details>

---