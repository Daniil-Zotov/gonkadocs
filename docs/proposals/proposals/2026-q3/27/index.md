---
title: "#27 – Upgrade Proposal: v0.2.10"
description: "Proposal #27"
template: proposals-proposals-main.html
---

# #27 – Upgrade Proposal: v0.2.10

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-passed">Passed</span>

**Proposal ID:** `27`

**Type:** Software Upgrade

**Submit:** 2026-01-01 00:00 UTC

**Voting:**  → 2026-01-02 00:00 UTC



[View on gonka.gg](https://gonka.gg/network/proposals/27){:target="_blank"}

</div>

Proposal #27

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