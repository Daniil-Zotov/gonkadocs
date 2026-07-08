---
title: "#26 – Upgrade Proposal: v0.2.9"
description: "Proposal #26"
template: proposals-proposals-main.html
---

# #26 – Upgrade Proposal: v0.2.9

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-passed">Passed</span>

**Proposal ID:** `26`

**Type:** Software Upgrade

**Submit:** 2026-01-01 00:00 UTC

**Voting:**  → 2026-01-02 00:00 UTC



[View on gonka.gg](https://gonka.gg/network/proposals/26){:target="_blank"}

</div>

Proposal #26

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
      "name": "v0.2.9",
      "time": "0001-01-01T00:00:00Z",
      "height": "2451000",
      "info": "{\n        \"binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.9/inferenced-amd64.zip?checksum=sha256:fc628d77aa516896924fbd8f60b8aa6a14161de4582aaef634de62382ea482eb\"\n        },\n        \"api_binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.9/decentralized-api-amd64.zip?checksum=sha256:ac1ad369052a8c3d01af4d463c49cdd16fcbecc365d201232e7a2d08af8501c0\"\n        }\n    }",
      "upgraded_client_state": null
    }
  }
]
```

</details>

---