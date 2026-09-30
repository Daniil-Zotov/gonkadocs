---
title: "#109 – Upgrade Proposal: v0.2.16"
description: "Upgrade Proposal: v0.2.16

The v0.2.16 upgrade includes protocol changes and bug fixes across the chain and API node. It also pays 104,150 USDT in bounties from community funds.

Trusted Weight. Befor"
template: proposals-proposals-main.html
---

# #109 – Upgrade Proposal: v0.2.16

<div class="prop-detail-header" markdown="1">

<div class="prop-badge-row"><span class="prop-badge prop-voting">Voting</span><span class="prop-vote-countdown prop-vote-countdown-detail" data-deadline="2026-10-02T02:40:38.717572024Z"></span></div>

**Proposal ID:** `109`

**Type:** Software Upgrade

**Submit:** 2026-09-30 02:40 UTC

**Voting:** 2026-09-30 02:40 UTC → 2026-10-02 02:40 UTC

**Proposer:** [`gonka18lluv53n4h9z34qu20vxcvypgdkhsg6nn2cl2d`](https://gonka.gg/address/gonka18lluv53n4h9z34qu20vxcvypgdkhsg6nn2cl2d){:target="_blank"}

**Metadata:** [https://github.com/gonka-ai/gonka/blob/beb159be59e1b980f63e1caffcb51c89fce7bc23/proposals/governance-artifacts/update-v0.2.16/README.md](https://github.com/gonka-ai/gonka/blob/beb159be59e1b980f63e1caffcb51c89fce7bc23/proposals/governance-artifacts/update-v0.2.16/README.md)



[View on gonka.gg](https://gonka.gg/network/proposals/109){:target="_blank"}

</div>

Upgrade Proposal: v0.2.16

The v0.2.16 upgrade includes protocol changes and bug fixes across the chain and API node. It also pays 104,150 USDT in bounties from community funds.

Trusted Weight. Before v0.2.16, a sudden increase in claimed compute immediately increased a participant's power in governance, BLS, and PoC validation. The upgrade limits that power to compute confirmed in the previous epoch. New or returning participants start with zero voting power but still earn rewards.

Dynamic Coefficients v1. Governance can set a target percentage of network compute and a coefficient range for each model. The protocol adjusts the coefficient inside that range to move compute toward the target. Compute above the target is scored at the minimum coefficient.

Fee. The upgrade groups transaction types and adds per-message gas rules. The epoch and cosmos groups are enabled by default at 1 ngonka per gas. All other groups remain disabled. Before the upgrade, hosts must check that their cold-to-warm feegrant is valid. The cold account must have enough spendable GNK to cover fees.

PoC Challenge. An approved challenger can require an active host to leave inference and run PoC at full capacity. The challenger locks a payment, which goes to the host if it passes or is refunded if it fails. Failure carries the same penalty as failed Confirmation PoC. Only allowlisted devshard escrow creators can open a challenge. If the allowlist is empty, anyone can open one.

Upgrade Plan. Existing hosts are not required to rebuild their api or node containers. Devshard binaries stay on the versions already approved. New hosts joining after the upgrade should use the deploy/join files published with the final v0.2.16 release.

Migration. The handler extends cold-to-warm grants with PoC Challenge and model intent messages. It moves approved devshard versions into a separate store without changing the approved list. It starts dynamic coefficients from current model scales and initializes PoC Challenge with a payment ratio of 0.1, at most 4 active challenges, and a minimum punishable segment of 300 blocks.

Testing. The upgrade from v0.2.15 to v0.2.16 was rehearsed on a testnet using alpha builds. Compatibility testing covered devshard v4.1 and v5 with both v0.2.15 and v0.2.16.

The full technical scope, contributor list, individual contributions, PR references, and bounty breakdown are available here: <https://github.com/gonka-ai/gonka/blob/beb159be59e1b980f63e1caffcb51c89fce7bc23/proposals/governance-artifacts/update-v0.2.16/README.md>

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:3.4%"></div>
    <div class="prop-tally-no" style="width:0.0%"></div>
    <div class="prop-tally-veto" style="width:0.0%"></div>
    <div class="prop-tally-abstain" style="width:2.3%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes <strong>59.1%</strong> (21,518)</span>
    <span class="prop-tally-no-text">No <strong>0.0%</strong> (0)</span>
    <span class="prop-tally-veto-text">Veto <strong>0.0%</strong> (0)</span>
    <span class="prop-tally-abstain-text">Abstain <strong>40.9%</strong> (14,904)</span>
    <span class="prop-tally-total-text">Total 36,422 votes</span>
    <span class="prop-tally-veto-text">✗ Turnout <strong>5.7%</strong> (36,422 / 642,120) · Quorum <strong>25%</strong> (160,530)</span>
  </div>
</div>



<h2 id="voters">Voters</h2>

<div class="prop-voters-wrap">
<table class="prop-voters">
<thead><tr><th>Voter</th><th>Vote</th></tr></thead>
<tbody>
<tr><td><a href="https://gonka.gg/address/gonka1p2lhgng7tcqju7emk989s5fpdr7k2c3ek6h26m" target="_blank" class="prop-voter-addr">gonka1p2lhgn…k6h26m</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka1pd5vx98y59w5v48f6j0gkqyvs5s6z9su7mytch" target="_blank" class="prop-voter-addr">gonka1pd5vx9…7mytch</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka1rqm2u7lxzn7r68y0drcyhag6xnckpsnfmgd53t" target="_blank" class="prop-voter-addr">gonka1rqm2u7…mgd53t</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka168rtjfkszuhcggg4dfyse4yh7xn9zwfglnkns2" target="_blank" class="prop-voter-addr">gonka168rtjf…lnkns2</a></td><td><span class="prop-voter-option prop-vote-abstain">Abstain 100.0%</span></td></tr>
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
      "name": "v0.2.16",
      "time": "0001-01-01T00:00:00Z",
      "height": "6353400",
      "info": "{\n        \"binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.16/inferenced-amd64.zip?checksum=sha256:216cad12ef75da57bcac526b210cd7b9d90e48445912782d78ae82f3547a7105\"\n        },\n        \"api_binaries\": {\n            \"linux/amd64\": \"https://github.com/gonka-ai/gonka/releases/download/release%2Fv0.2.16/decentralized-api-amd64.zip?checksum=sha256:f279866a45fbc8a7c7233310bbd9a1c7b70518da9be2d6c410879f0c36e57725\"\n        }\n    }",
      "upgraded_client_state": null
    }
  }
]
```

</details>
