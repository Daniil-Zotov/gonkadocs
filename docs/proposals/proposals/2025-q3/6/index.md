---
title: "#6 – Upgrade Proposal: v0.2.2"
description: "Upgrade Proposal: v0.2.2"
template: proposals-proposals-main.html
---

# #6 – Upgrade Proposal: v0.2.2

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-passed">Passed</span>

**Proposal ID:** `6`

**Type:** Software Upgrade

**Submit:** 2025-09-24 23:08 UTC

**Voting:** 2025-09-24 23:08 UTC → 2025-09-25 02:08 UTC

**Proposer:** [`gonka18lluv53n4h9z34qu20vxcvypgdkhsg6nn2cl2d`](https://gonka.gg/address/gonka18lluv53n4h9z34qu20vxcvypgdkhsg6nn2cl2d){:target="_blank"}

**Metadata:** [https://github.com/gonka-ai/gonka/blob/422dd37c36ad65bc3be2c84cd18a4d86e7ddec10/proposals/governance-artifacts/update-v0.2.2/README.md](https://github.com/gonka-ai/gonka/blob/422dd37c36ad65bc3be2c84cd18a4d86e7ddec10/proposals/governance-artifacts/update-v0.2.2/README.md)



[View on gonka.gg](https://gonka.gg/network/proposals/6){:target="_blank"}

</div>

Upgrade Proposal: v0.2.2

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
    <span class="prop-tally-yes-text">Yes 130,079 (100.0%)</span>
    <span class="prop-tally-no-text">No 0 (0.0%)</span>
    <span class="prop-tally-veto-text">Veto 0 (0.0%)</span>
    <span class="prop-tally-abstain-text">Abstain 0 (0.0%)</span>
    <span class="prop-tally-total-text">Total 130,079 votes</span>
  </div>
</div>


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