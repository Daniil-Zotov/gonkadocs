---
title: "#16 – Upgrade Proposal: v0.2.6"
description: "Proposal #16"
template: proposals-proposals-main.html
---

# #16 – Upgrade Proposal: v0.2.6

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-passed">Passed</span>

**Proposal ID:** `16`

**Type:** Software Upgrade

**Submit:** 2026-01-01 00:00 UTC

**Voting:**  → 2026-01-02 00:00 UTC



[View on gonka.gg](https://gonka.gg/network/proposals/16){:target="_blank"}

</div>

Proposal #16

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
      "name": "v0.2.6",
      "time": "0001-01-01T00:00:00Z",
      "height": "1820000",
      "info": "{\n        \"binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.6-post1/inferenced-amd64.zip?checksum=sha256:afa5772b8c7014d3fd9015651aa543ace4196c227ce59ee3f9fed3fcd98f4650\"\n        },\n        \"api_binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.6-post1/decentralized-api-amd64.zip?checksum=sha256:52ac4c55313f77eff7da4f7160396837c8810f9bf84a860c21c0299599968aaa\"\n        }\n    }",
      "upgraded_client_state": null
    }
  }
]
```

</details>

---