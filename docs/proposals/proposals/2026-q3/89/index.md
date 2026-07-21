---
title: "#89 – Upgrade Proposal: v0.2.14"
description: "Upgrade Proposal: v0.2.14"
template: proposals-proposals-main.html
---

# #89 – Upgrade Proposal: v0.2.14

<div class="prop-detail-header" markdown="1">

<div class="prop-badge-row"><span class="prop-badge prop-voting">Voting</span><span class="prop-vote-countdown prop-vote-countdown-detail" data-deadline="2026-07-23T00:02:04.535338507Z"></span></div>

**Proposal ID:** `89`

**Type:** Software Upgrade

**Submit:** 2026-07-21 00:02 UTC

**Voting:** 2026-07-21 00:02 UTC → 2026-07-23 00:02 UTC

**Proposer:** [`gonka18lluv53n4h9z34qu20vxcvypgdkhsg6nn2cl2d`](https://gonka.gg/address/gonka18lluv53n4h9z34qu20vxcvypgdkhsg6nn2cl2d){:target="_blank"}

**Metadata:** [https://github.com/gonka-ai/gonka/blob/upgrade-v0.2.14/proposals/governance-artifacts/update-v0.2.14/README.md](https://github.com/gonka-ai/gonka/blob/upgrade-v0.2.14/proposals/governance-artifacts/update-v0.2.14/README.md)



[View on gonka.gg](https://gonka.gg/network/proposals/89){:target="_blank"}

</div>

Upgrade Proposal: v0.2.14

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
    <span class="prop-tally-yes-text">Yes 3,248 (100.0%)</span>
    <span class="prop-tally-no-text">No 0 (0.0%)</span>
    <span class="prop-tally-veto-text">Veto 0 (0.0%)</span>
    <span class="prop-tally-abstain-text">Abstain 0 (0.0%)</span>
    <span class="prop-tally-total-text">Total 3,248 votes</span>
    <span class="prop-tally-veto-text">✗ Turnout 3,248 / 597,960 (0.5%) · Quorum 25% (149,490)</span>
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
      "name": "v0.2.14",
      "time": "0001-01-01T00:00:00Z",
      "height": "5195700",
      "info": "{\n        \"binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.14/inferenced-amd64.zip?checksum=sha256:ce857ef90deb899c03d78dee01493e544bf8b7ddf8b452e75b3b010b80a8b046\"\n        },\n        \"api_binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.14/decentralized-api-amd64.zip?checksum=sha256:4326a27913a05435e37cd5fa9e3d0cf5271351799f8b01b842e049a733976c87\"\n        }\n    }",
      "upgraded_client_state": null
    }
  }
]
```

</details>
