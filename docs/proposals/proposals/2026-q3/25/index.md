---
title: "#25 – Upgrade Proposal: v0.2.8"
description: "Proposal #25"
template: proposals-proposals-main.html
---

# #25 – Upgrade Proposal: v0.2.8

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-passed">Passed</span>

**Proposal ID:** `25`

**Type:** Software Upgrade

**Submit:** 2026-01-01 00:00 UTC

**Voting:**  → 2026-01-02 00:00 UTC



[View on gonka.gg](https://gonka.gg/network/proposals/25){:target="_blank"}

</div>

Proposal #25

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
      "name": "v0.2.8",
      "time": "0001-01-01T00:00:00Z",
      "height": "2387000",
      "info": "{\n        \"binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.8-post1/inferenced-amd64.zip?checksum=sha256:f0f2e3ee8760e40a78087c98c639a7518bf062138141ed4aec2120f5bc622a67\"\n        },\n        \"api_binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.8-post1/decentralized-api-amd64.zip?checksum=sha256:45f28afba4758e54988f61cc358f0ad683e7832ab121ccd54b684fe4c9381a75\"\n        }\n    }",
      "upgraded_client_state": null
    }
  }
]
```

</details>

---