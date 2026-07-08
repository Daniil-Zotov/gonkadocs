---
title: "#24 – Upgrade Proposal: v0.2.8"
description: "Proposal #24"
template: proposals-proposals-main.html
---

# #24 – Upgrade Proposal: v0.2.8

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-rejected">Rejected</span>

**Proposal ID:** `24`

**Type:** Software Upgrade

**Submit:** 2026-01-01 00:00 UTC

**Voting:**  → 2026-01-02 00:00 UTC



[View on gonka.gg](https://gonka.gg/network/proposals/24){:target="_blank"}

</div>

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
      "name": "v0.2.8",
      "time": "0001-01-01T00:00:00Z",
      "height": "2386600",
      "info": "{\n        \"binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.8/inferenced-amd64.zip?checksum=sha256:a3e59d5d7a9caa4b729eb7915863770b5465fa12af2a4d41fa7358085c86704f\"\n        },\n        \"api_binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.8/decentralized-api-amd64.zip?checksum=sha256:e3dd428ac9cf3b410e0ae7fc9a2c9fa3efd3b7e97ff748a3fa7d7fb928cb696a\"\n        }\n    }",
      "upgraded_client_state": null
    }
  }
]
```

</details>

---