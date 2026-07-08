---
title: "#54 – Upgrade Proposal: v0.2.13"
description: "Upgrade Proposal: v0.2.13"
template: proposals-proposals-main.html
---

# #54 – Upgrade Proposal: v0.2.13

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-passed">Passed</span>

**Proposal ID:** `54`

**Type:** Software Upgrade

**Submit:** 2026-01-01 00:00 UTC

**Voting:**  → 2026-01-02 00:00 UTC



[View on gonka.gg](https://gonka.gg/network/proposals/54){:target="_blank"}

</div>

Upgrade Proposal: v0.2.13

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
      "name": "v0.2.13",
      "time": "0001-01-01T00:00:00Z",
      "height": "4267300",
      "info": "{\n        \"binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.13/inferenced-amd64.zip?checksum=sha256:ea7dea6c4e8d96ed61005bed196768cc9f44e5fb17f0714cb64d1d00a485be0c\"\n        },\n        \"api_binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.13/decentralized-api-amd64.zip?checksum=sha256:cf31fa4d715e721d1e17b7e2b46d628a0b66b6ef603d352d587abe1d57c40925\"\n        },\n        \"ethereum_bridge_address\": \"0x972a7a92d92796a98801a8818bcf91f1648f2f68\",\n        \"wrapped_token_code_id\": 105\n    }",
      "upgraded_client_state": null
    }
  }
]
```

</details>

---