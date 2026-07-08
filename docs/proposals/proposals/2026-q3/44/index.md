---
title: "#44 – Upgrade Proposal: v0.2.12"
description: "Upgrade Proposal: v0.2.12"
template: proposals-proposals-main.html
---

# #44 – Upgrade Proposal: v0.2.12

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-passed">Passed</span>

**Proposal ID:** `44`

**Type:** Software Upgrade

**Submit:** 2026-01-01 00:00 UTC

**Voting:**  → 2026-01-02 00:00 UTC



[View on gonka.gg](https://gonka.gg/network/proposals/44){:target="_blank"}

</div>

Upgrade Proposal: v0.2.12

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
      "name": "v0.2.12",
      "time": "0001-01-01T00:00:00Z",
      "height": "3834200",
      "info": "{\n        \"binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.12/inferenced-amd64.zip?checksum=sha256:df7656503d39f6703767d32d5578d1291e32cb114844d8c1cd0f134d1bf4babd\"\n        },\n        \"api_binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.12/decentralized-api-amd64.zip?checksum=sha256:d0143a95e12e1ada06cfea5e4d3deab13534c3523c967e9a6b87ac9f9bf3247d\"\n        }\n    }",
      "upgraded_client_state": null
    }
  }
]
```

</details>

---