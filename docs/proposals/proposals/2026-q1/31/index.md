---
title: "#31 – Upgrade Proposal: v0.2.11"
description: "Upgrade Proposal: v0.2.11"
template: proposals-proposals-main.html
---

# #31 – Upgrade Proposal: v0.2.11

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-passed">Passed</span>

**Proposal ID:** `31`

**Type:** Software Upgrade

**Submit:** 2026-03-19 05:59 UTC

**Voting:** 2026-03-19 05:59 UTC → 2026-03-20 05:59 UTC

**Proposer:** [`gonka18lluv53n4h9z34qu20vxcvypgdkhsg6nn2cl2d`](https://gonka.gg/address/gonka18lluv53n4h9z34qu20vxcvypgdkhsg6nn2cl2d){:target="_blank"}

**Metadata:** [https://github.com/gonka-ai/gonka/blob/74f5ff859dd6d83eb8c2576b55c76fa41e669341/proposals/governance-artifacts/update-v0.2.11/README.md](https://github.com/gonka-ai/gonka/blob/74f5ff859dd6d83eb8c2576b55c76fa41e669341/proposals/governance-artifacts/update-v0.2.11/README.md)



[View on gonka.gg](https://gonka.gg/network/proposals/31){:target="_blank"}

</div>

Upgrade Proposal: v0.2.11

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:90.8%"></div>
    <div class="prop-tally-no" style="width:0.0%"></div>
    <div class="prop-tally-veto" style="width:0.0%"></div>
    <div class="prop-tally-abstain" style="width:0.0%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes 673,699 (100.0%)</span>
    <span class="prop-tally-no-text">No 0 (0.0%)</span>
    <span class="prop-tally-veto-text">Veto 0 (0.0%)</span>
    <span class="prop-tally-abstain-text">Abstain 0 (0.0%)</span>
    <span class="prop-tally-total-text">Total 673,699 votes</span>
    
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
      "name": "v0.2.11",
      "time": "0001-01-01T00:00:00Z",
      "height": "3186100",
      "info": "{\n        \"binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.11/inferenced-amd64.zip?checksum=sha256:c77528bd2e31e86355a6eefddb50e0db7f9600ebf2940ca440a61ea36e7ef7ca\"\n        },\n        \"api_binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.11/decentralized-api-amd64.zip?checksum=sha256:e574c3d86189daf325cc7008603ee8e952efb028afda5bcd4a154dcd334192d4\"\n        },\n        \"community_sale_address\": \"gonka18pkq9mwxxlmyq7kr5txhm060wemg2s4u94wvsfd9w2kdc0u99d6spk8pz2\",\n        \"new_code_id\": 84\n    }",
      "upgraded_client_state": null
    }
  }
]
```

</details>
