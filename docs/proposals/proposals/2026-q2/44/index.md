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

**Submit:** 2026-04-28 00:11 UTC

**Voting:** 2026-04-28 00:11 UTC → 2026-04-30 00:11 UTC

**Proposer:** [`gonka18lluv53n4h9z34qu20vxcvypgdkhsg6nn2cl2d`](https://gonka.gg/address/gonka18lluv53n4h9z34qu20vxcvypgdkhsg6nn2cl2d){:target="_blank"}

**Metadata:** [https://github.com/gonka-ai/gonka/blob/76d0eb971233f9544f681a25e860844e3f45641e/proposals/governance-artifacts/update-v0.2.12/README.md](https://github.com/gonka-ai/gonka/blob/76d0eb971233f9544f681a25e860844e3f45641e/proposals/governance-artifacts/update-v0.2.12/README.md)



[View on gonka.gg](https://gonka.gg/network/proposals/44){:target="_blank"}

</div>

Upgrade Proposal: v0.2.12

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:99.6%"></div>
    <div class="prop-tally-no" style="width:0.4%"></div>
    <div class="prop-tally-veto" style="width:0.0%"></div>
    <div class="prop-tally-abstain" style="width:0.0%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes 506,142 (99.6%)</span>
    <span class="prop-tally-no-text">No 2,057 (0.4%)</span>
    <span class="prop-tally-veto-text">Veto 0 (0.0%)</span>
    <span class="prop-tally-abstain-text">Abstain 0 (0.0%)</span>
    <span class="prop-tally-total-text">Total 508,199 votes</span>
    
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
