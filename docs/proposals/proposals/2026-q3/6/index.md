---
title: "#6 – Upgrade Proposal: v0.2.2"
description: "Proposal #6"
template: proposals-proposals-main.html
---

# #6 – Upgrade Proposal: v0.2.2

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-passed">Passed</span>

**Proposal ID:** `6`

**Type:** Software Upgrade

**Submit:** 2026-01-01 00:00 UTC

**Voting:**  → 2026-01-02 00:00 UTC



[View on gonka.gg](https://gonka.gg/network/proposals/6){:target="_blank"}

</div>

Proposal #6

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
      "height": "517935",
      "info": "{\n        \"binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.2-upgrade/inferenced-amd64.zip?checksum=sha256:a0d8117d0bd91bd1ebe537c54668101bd60550642516a8780de301ff46d46b4b\"\n        },\n        \"api_binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.2-upgrade/decentralized-api-amd64.zip?checksum=sha256:c23f28918b28043a90e661575019ae0ad28c6b11d29a544e25bed3ff0f18caa7\"\n        }\n    }",
      "upgraded_client_state": null
    }
  }
]
```

</details>

---