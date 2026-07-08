---
title: "#27 – Upgrade Proposal: v0.2.10"
description: "Upgrade Proposal: v0.2.10"
template: proposals-proposals-main.html
---

# #27 – Upgrade Proposal: v0.2.10

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-passed">Passed</span>

**Proposal ID:** `27`

**Type:** Software Upgrade

**Submit:** 2026-02-17 09:26 UTC

**Voting:** 2026-02-17 09:26 UTC → 2026-02-18 09:26 UTC

**Proposer:** [`gonka18lluv53n4h9z34qu20vxcvypgdkhsg6nn2cl2d`](https://gonka.gg/address/gonka18lluv53n4h9z34qu20vxcvypgdkhsg6nn2cl2d){:target="_blank"}

**Metadata:** [https://github.com/gonka-ai/gonka/blob/faa358dec3091e19cb92267556443775431ecc81/proposals/governance-artifacts/update-v0.2.10/README.md](https://github.com/gonka-ai/gonka/blob/faa358dec3091e19cb92267556443775431ecc81/proposals/governance-artifacts/update-v0.2.10/README.md)



[View on gonka.gg](https://gonka.gg/network/proposals/27){:target="_blank"}

</div>

Upgrade Proposal: v0.2.10

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
    <span class="prop-tally-yes-text">Yes 1,540,653 (100.0%)</span>
    <span class="prop-tally-no-text">No 0 (0.0%)</span>
    <span class="prop-tally-veto-text">Veto 0 (0.0%)</span>
    <span class="prop-tally-abstain-text">Abstain 0 (0.0%)</span>
    <span class="prop-tally-total-text">Total 1,540,653 votes</span>
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
      "name": "v0.2.10",
      "time": "0001-01-01T00:00:00Z",
      "height": "2712600",
      "info": "{\n        \"binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.10/inferenced-amd64.zip?checksum=sha256:b118610cfa1f45f9dfb4eb112a01a91ad886333b73aac49fee20abc0c3f1998a\"\n        },\n        \"api_binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.10/decentralized-api-amd64.zip?checksum=sha256:47d6b64424f34242ba12d04aa367f3a7d3933961b55f9d2434b36399d0faf18f\"\n        }\n    }",
      "upgraded_client_state": null
    }
  }
]
```

</details>

---