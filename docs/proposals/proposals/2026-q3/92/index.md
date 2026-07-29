---
title: "#92 – Upgrade Proposal: v0.2.15"
description: "Upgrade Proposal: v0.2.15"
template: proposals-proposals-main.html
---

# #92 – Upgrade Proposal: v0.2.15

<div class="prop-detail-header" markdown="1">

<div class="prop-badge-row"><span class="prop-badge prop-voting">Voting</span><span class="prop-vote-countdown prop-vote-countdown-detail" data-deadline="2026-07-30T07:08:47.579998945Z"></span></div>

**Proposal ID:** `92`

**Type:** Software Upgrade

**Submit:** 2026-07-28 07:08 UTC

**Voting:** 2026-07-28 07:08 UTC → 2026-07-30 07:08 UTC

**Proposer:** [`gonka18lluv53n4h9z34qu20vxcvypgdkhsg6nn2cl2d`](https://gonka.gg/address/gonka18lluv53n4h9z34qu20vxcvypgdkhsg6nn2cl2d){:target="_blank"}

**Metadata:** [https://github.com/gonka-ai/gonka/blob/4d687ed6782bcea3931d2d9135bf322f84e190ab/proposals/governance-artifacts/update-v0.2.15/README.md](https://github.com/gonka-ai/gonka/blob/4d687ed6782bcea3931d2d9135bf322f84e190ab/proposals/governance-artifacts/update-v0.2.15/README.md)



[View on gonka.gg](https://gonka.gg/network/proposals/92){:target="_blank"}

</div>

Upgrade Proposal: v0.2.15

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:1.0%"></div>
    <div class="prop-tally-no" style="width:0.0%"></div>
    <div class="prop-tally-veto" style="width:0.0%"></div>
    <div class="prop-tally-abstain" style="width:0.0%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes 5,398 (100.0%)</span>
    <span class="prop-tally-no-text">No 0 (0.0%)</span>
    <span class="prop-tally-veto-text">Veto 0 (0.0%)</span>
    <span class="prop-tally-abstain-text">Abstain 0 (0.0%)</span>
    <span class="prop-tally-total-text">Total 5,398 votes</span>
    <span class="prop-tally-veto-text">✗ Turnout 5,398 / 539,219 (1.0%) · Quorum 25% (134,804)</span>
  </div>
</div>



<h2 id="voters">Voters</h2>

<div class="prop-voters-wrap">
<table class="prop-voters">
<thead><tr><th>Voter</th><th>Vote</th></tr></thead>
<tbody>
<tr><td><a href="https://gonka.gg/address/gonka1qwfrtz9c7kcrfkrrlne2pkcye74mj6ce33xdkl" target="_blank" class="prop-voter-addr">gonka1qwfrtz…33xdkl</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka1p2lhgng7tcqju7emk989s5fpdr7k2c3ek6h26m" target="_blank" class="prop-voter-addr">gonka1p2lhgn…k6h26m</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka1ym3np7guxart483yfdxnlztuazx22cjt0e4a2p" target="_blank" class="prop-voter-addr">gonka1ym3np7…0e4a2p</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka1d7p03cu2y2yt3vytq9wlfm6tlz0lfhlgv9h82p" target="_blank" class="prop-voter-addr">gonka1d7p03c…v9h82p</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka15p7s7w2hx0y8095lddd4ummm2y0kwpwljk00aq" target="_blank" class="prop-voter-addr">gonka15p7s7w…jk00aq</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka1m58jds005cttwq2vt0p7yk6vy2aqg254cqqppf" target="_blank" class="prop-voter-addr">gonka1m58jds…cqqppf</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
</tbody>
</table>
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
      "name": "v0.2.15",
      "time": "0001-01-01T00:00:00Z",
      "height": "5316315",
      "info": "{\n        \"binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.15/inferenced-amd64.zip?checksum=sha256:91af67df9ef5c576a1695e5e85c8ee344f9f1a69d941bfc28fb339d9fd33617e\"\n        },\n        \"api_binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.15/decentralized-api-amd64.zip?checksum=sha256:c9cf1bfa2c994beca8a528d0ee3ad7197a582144769711600ec9df41faf4c9f7\"\n        },\n        \"approved_versions\": [\n            {\n                \"name\": \"v4\",\n                \"binary\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.15/devshardd.zip\",\n                \"sha256\": \"bdc7ee5d08f0090711c60950c7f3ffdd0c7aef5a5badf6f19c2b075b08264ddf\"\n            }\n        ]\n    }",
      "upgraded_client_state": null
    }
  }
]
```

</details>
