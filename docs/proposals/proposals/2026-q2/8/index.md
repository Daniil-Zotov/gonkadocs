---
title: "#8 – Upgrade Proposal: v0.2.4"
description: "Proposal #8"
template: proposals-proposals-main.html
---

# #8 – Upgrade Proposal: v0.2.4

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-passed">Passed</span>

**Proposal ID:** `8`

**Type:** Software Upgrade

**Submit:** 2026-01-01 00:00 UTC

**Voting:**  → 2026-01-02 00:00 UTC



[View on gonka.gg](https://gonka.gg/network/proposals/8){:target="_blank"}

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
      "name": "v0.2.4",
      "time": "0001-01-01T00:00:00Z",
      "height": "937700",
      "info": "{\n        \"binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.4/inferenced-amd64.zip?checksum=sha256:ea00bbc6a40aab85ec0192851a800ac803c8f9513fa4bac8b75545aeacd3bf64\"\n        },\n        \"api_binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.4/decentralized-api-amd64.zip?checksum=sha256:0a26945bc43bd8be11538197cf78d3689fa7d46d0b6eb7ee997d53079feef2b0\"\n        }\n    }",
      "upgraded_client_state": null
    }
  }
]
```

</details>

---