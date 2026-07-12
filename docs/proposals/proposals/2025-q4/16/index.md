---
title: "#16 – Upgrade Proposal: v0.2.6"
description: "Upgrade Proposal: v0.2.6"
template: proposals-proposals-main.html
---

# #16 – Upgrade Proposal: v0.2.6

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-passed">Passed</span>

**Proposal ID:** `16`

**Type:** Software Upgrade

**Submit:** 2025-12-19 17:09 UTC

**Voting:** 2025-12-19 17:09 UTC → 2025-12-20 17:09 UTC

**Proposer:** [`gonka18lluv53n4h9z34qu20vxcvypgdkhsg6nn2cl2d`](https://gonka.gg/address/gonka18lluv53n4h9z34qu20vxcvypgdkhsg6nn2cl2d){:target="_blank"}

**Metadata:** [https://github.com/gonka-ai/gonka/commit/5be305ad380db8854313d2b0369049c8105f681b/proposals/governance-artifacts/update-v0.2.6/README.md](https://github.com/gonka-ai/gonka/commit/5be305ad380db8854313d2b0369049c8105f681b/proposals/governance-artifacts/update-v0.2.6/README.md)



[View on gonka.gg](https://gonka.gg/network/proposals/16){:target="_blank"}

</div>

Upgrade Proposal: v0.2.6

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:100.0%"></div>
    <div class="prop-tally-no" style="width:0.0%"></div>
    <div class="prop-tally-veto" style="width:0.0%"></div>
    <div class="prop-tally-abstain" style="width:0.0%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes 1,985,917 (100.0%)</span>
    <span class="prop-tally-no-text">No 0 (0.0%)</span>
    <span class="prop-tally-veto-text">Veto 0 (0.0%)</span>
    <span class="prop-tally-abstain-text">Abstain 0 (0.0%)</span>
    <span class="prop-tally-total-text">Total 1,985,917 votes</span>
    
  </div>
</div>


---

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
