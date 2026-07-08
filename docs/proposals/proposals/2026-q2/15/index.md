---
title: "#15 – Upgrade Proposal: v0.2.6"
description: "Proposal #15"
template: proposals-proposals-main.html
---

# #15 – Upgrade Proposal: v0.2.6

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-rejected">Rejected</span>

**Proposal ID:** `15`

**Type:** Software Upgrade

**Submit:** 2026-01-01 00:00 UTC

**Voting:**  → 2026-01-02 00:00 UTC



[View on gonka.gg](https://gonka.gg/network/proposals/15){:target="_blank"}

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
      "name": "v0.2.6",
      "time": "0001-01-01T00:00:00Z",
      "height": "1773000",
      "info": "{\n        \"binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.6/inferenced-amd64.zip?checksum=sha256:cdbcfe214ce7eb2bab993bb344447b84602fb77e32c9a05f48e0671dd469c832\"\n        },\n        \"api_binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.6/decentralized-api-amd64.zip?checksum=sha256:abb5e3ba1db4beb6c1109b5a0cd1fbf226e19c108dc4f30a565582056123c394\"\n        }\n    }",
      "upgraded_client_state": null
    }
  }
]
```

</details>

---