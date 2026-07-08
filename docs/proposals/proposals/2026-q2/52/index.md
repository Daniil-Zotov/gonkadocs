---
title: "#52 – Upgrade Proposal: v0.2.13"
description: "Upgrade Proposal: v0.2.13"
template: proposals-proposals-main.html
---

# #52 – Upgrade Proposal: v0.2.13

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-rejected">Rejected</span>

**Proposal ID:** `52`

**Type:** Software Upgrade

**Submit:** 2026-05-15 07:58 UTC

**Voting:** 2026-05-15 07:58 UTC → 2026-05-17 07:58 UTC

**Proposer:** `gonka18lluv53n4h9z34qu20vxcvypgdkhsg6nn2cl2d`

**Metadata:** [https://github.com/gonka-ai/gonka/blob/aa413e198825ddcc5eac80f4ca2e85a9bc54700e/proposals/governance-artifacts/update-v0.2.13/README.md](https://github.com/gonka-ai/gonka/blob/aa413e198825ddcc5eac80f4ca2e85a9bc54700e/proposals/governance-artifacts/update-v0.2.13/README.md)

**Failed reason:** proposal did not get enough votes to pass

</div>

Upgrade Proposal: v0.2.13

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:34.1%"></div>
    <div class="prop-tally-no" style="width:0.0%"></div>
    <div class="prop-tally-veto" style="width:65.9%"></div>
    <div class="prop-tally-abstain" style="width:0.0%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes 88,420 (34.1%)</span>
    <span class="prop-tally-no-text">No 0 (0.0%)</span>
    <span class="prop-tally-veto-text">Veto 170,799 (65.9%)</span>
    <span class="prop-tally-abstain-text">Abstain 0 (0.0%)</span>
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
      "name": "v0.2.13",
      "time": "0001-01-01T00:00:00Z",
      "height": "4133422",
      "info": "{\n        \"binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.13/inferenced-amd64.zip?checksum=sha256:e5940e5879cb978cc7673bed70a740604ca0c6bcc4f03eccd5353b6a2bee90fe\"\n        },\n        \"api_binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.13/decentralized-api-amd64.zip?checksum=sha256:9aef44e85445db6add0426a380daac42f86345c20151e672b7177d331545c703\"\n        },\n        \"ethereum_bridge_address\": \"0x972a7a92d92796a98801a8818bcf91f1648f2f68\",\n        \"wrapped_token_code_id\": 105\n    }",
      "upgraded_client_state": null
    }
  }
]
```

</details>

---

<div class="prop-footer" markdown="1">

[View on gonka.gg](https://gonka.gg/network/proposals/52){:target="_blank"}

</div>
