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

**Submit:** 2026-05-20 22:12 UTC

**Voting:** 2026-05-20 22:12 UTC → 2026-05-22 22:12 UTC

**Proposer:** [`gonka18lluv53n4h9z34qu20vxcvypgdkhsg6nn2cl2d`](https://gonka.gg/address/gonka18lluv53n4h9z34qu20vxcvypgdkhsg6nn2cl2d){:target="_blank"}

**Metadata:** [https://github.com/gonka-ai/gonka/blob/3f0c34f77c9b8f8c32ca5303ef3ffad23d66d5ea/proposals/governance-artifacts/update-v0.2.13/README.md](https://github.com/gonka-ai/gonka/blob/3f0c34f77c9b8f8c32ca5303ef3ffad23d66d5ea/proposals/governance-artifacts/update-v0.2.13/README.md)

<div class="prop-bounty-line">Bounty Reward из Community Pool: $18,875 USDT · Community Sale · <a href="https://github.com/gonka-ai/gonka/pull/1168" target="_blank">PR #1168</a></div>


[View on gonka.gg](https://gonka.gg/network/proposals/54){:target="_blank"}

</div>

Upgrade Proposal: v0.2.13

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:30.8%"></div>
    <div class="prop-tally-no" style="width:0.0%"></div>
    <div class="prop-tally-veto" style="width:0.0%"></div>
    <div class="prop-tally-abstain" style="width:18.2%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes 228,216 (62.8%)</span>
    <span class="prop-tally-no-text">No 0 (0.0%)</span>
    <span class="prop-tally-veto-text">Veto 0 (0.0%)</span>
    <span class="prop-tally-abstain-text">Abstain 135,071 (37.2%)</span>
    <span class="prop-tally-total-text">Total 363,287 votes</span>
    
  </div>
</div>


## Messages

| # | Type |
| :- | :--- |
| 1 | `/cosmos.upgrade.v1beta1.MsgSoftwareUpgrade` |

<details class="prop-contracts" markdown="1">
<summary markdown="1">Contract Details</summary>

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
