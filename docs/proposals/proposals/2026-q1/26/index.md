---
title: "#26 – Upgrade Proposal: v0.2.9"
description: "Upgrade Proposal: v0.2.9"
template: proposals-proposals-main.html
---

# #26 – Upgrade Proposal: v0.2.9

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-passed">Passed</span>

**Proposal ID:** `26`

**Type:** Software Upgrade

**Submit:** 2026-01-31 22:02 UTC

**Voting:** 2026-01-31 22:02 UTC → 2026-02-01 22:02 UTC

**Proposer:** [`gonka18lluv53n4h9z34qu20vxcvypgdkhsg6nn2cl2d`](https://gonka.gg/address/gonka18lluv53n4h9z34qu20vxcvypgdkhsg6nn2cl2d){:target="_blank"}

**Metadata:** [https://github.com/gonka-ai/gonka/blob/808247ea17c254f0b81cfa67edb579ba249175f0/proposals/governance-artifacts/update-v0.2.9/README.md](https://github.com/gonka-ai/gonka/blob/808247ea17c254f0b81cfa67edb579ba249175f0/proposals/governance-artifacts/update-v0.2.9/README.md)



[View on gonka.gg](https://gonka.gg/network/proposals/26){:target="_blank"}

</div>

Upgrade Proposal: v0.2.9

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
    <span class="prop-tally-yes-text">Yes 2,708,406 (100.0%)</span>
    <span class="prop-tally-no-text">No 0 (0.0%)</span>
    <span class="prop-tally-veto-text">Veto 0 (0.0%)</span>
    <span class="prop-tally-abstain-text">Abstain 0 (0.0%)</span>
    <span class="prop-tally-total-text">Total 2,708,406 votes</span>
  </div>
</div>

<div class="prop-quorum">
  <span class="prop-quorum-label">Turnout</span>
  <span class="prop-quorum-value">2,708,406 / 741,825 (365.1%)</span>
  <span class="prop-quorum-label">Quorum</span>
  <span class="prop-quorum-value">25% (185,456 votes)</span>
  <span class="prop-quorum-status prop-quorum-met">✓ MET</span>
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
      "name": "v0.2.9",
      "time": "0001-01-01T00:00:00Z",
      "height": "2451000",
      "info": "{\n        \"binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.9/inferenced-amd64.zip?checksum=sha256:fc628d77aa516896924fbd8f60b8aa6a14161de4582aaef634de62382ea482eb\"\n        },\n        \"api_binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.9/decentralized-api-amd64.zip?checksum=sha256:ac1ad369052a8c3d01af4d463c49cdd16fcbecc365d201232e7a2d08af8501c0\"\n        }\n    }",
      "upgraded_client_state": null
    }
  }
]
```

</details>

---