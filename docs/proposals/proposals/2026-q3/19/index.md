---
title: "#19 – Upgrade Proposal: v0.2.7"
description: "Proposal #19"
template: proposals-proposals-main.html
---

# #19 – Upgrade Proposal: v0.2.7

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-passed">Passed</span>

**Proposal ID:** `19`

**Type:** Software Upgrade

**Submit:** 2026-01-01 00:00 UTC

**Voting:**  → 2026-01-02 00:00 UTC



[View on gonka.gg](https://gonka.gg/network/proposals/19){:target="_blank"}

</div>

Proposal #19

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

---