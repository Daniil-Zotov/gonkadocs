---
title: "#4 – Upgrade Proposal: v0.2.2"
description: "Proposal #4"
template: proposals-proposals-main.html
---

# #4 – Upgrade Proposal: v0.2.2

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-rejected">Rejected</span>

**Proposal ID:** `4`

**Type:** Software Upgrade

**Submit:** 2026-01-01 00:00 UTC

**Voting:**  → 2026-01-02 00:00 UTC



[View on gonka.gg](https://gonka.gg/network/proposals/4){:target="_blank"}

</div>

Proposal #4

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