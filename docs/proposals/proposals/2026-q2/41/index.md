---
title: "#41 – INC4 | Gonka Node Observability Platform"
description: "Today's explorers and dashboards only show on-chain data, leaving the off-chain state of validators completely opaque. The few operators who do run their own monitoring use different tools, different "
template: proposals-proposals-main.html
---

# #41 – INC4 | Gonka Node Observability Platform

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-rejected">Rejected</span>

**Proposal ID:** `41`

**Type:** Community Pool Spend

**Submit:** 2026-04-16 18:42 UTC

**Voting:** 2026-04-16 18:42 UTC → 2026-04-18 18:42 UTC

**Proposer:** [`gonka12ss9dh7fj3xxmk23s8aje4hrpqq669u20v3ja6`](https://gonka.gg/address/gonka12ss9dh7fj3xxmk23s8aje4hrpqq669u20v3ja6){:target="_blank"}

**Metadata:** [https://github.com/gonka-ai/gonka/discussions/1085](https://github.com/gonka-ai/gonka/discussions/1085)

**Failed reason:** proposal did not get enough votes to pass

<div class="prop-funding-line prop-funding-line-rejected">$96,000 · Community Pool</div>


[View on gonka.gg](https://gonka.gg/network/proposals/41){:target="_blank"}

</div>

Today's explorers and dashboards only show on-chain data, leaving the off-chain state of validators completely opaque. The few operators who do run their own monitoring use different tools, different metrics, and different baselines, leading to different interpretations and making it harder to coordinate when problems arise. The network lacks a single source of truth and a common framework for measuring validator health.

Even today, simply watching how validators operate reveals that many are not reacting to technical problems in time — growing Inference Miss Rates, dropping CPoC Ratios, network sync falling behind. These patterns persist because operators have no way to see the early warning signs or get emergency alerts inside their own infrastructure.

To address this, INC4 — an active Gonka validator operator with hands-on experience in blockchain infrastructure and observability — proposes the creation of the Gonka Node Observability Platform — an open-source, opt-in observability stack that aggregates off-chain metrics from Network nodes and ML nodes into a shared, publicly accessible dashboard. The platform is deployed on independent cloud infrastructure — without using resources of any individual validator or granting anyone privileged access — so that all operators have equal access and visibility into the data.

For the Core Team — a unified view of the entire network, visibility into problematic nodes and time periods, data for informed protocol decisions, SLA reports, and the ability to assess the scope of network-wide issues before and after upgrades. For Individual Validators — real-time alerts, performance comparison against network averages, opt-in log sharing to get help with troubleshooting and metrics interpretation, and no need to build your own monitoring stack.

Detecting and preventing even a single major network-wide incident, or a series of smaller incidents at individual validators, can save the ecosystem far more than the annual cost of this platform. The primary beneficiaries are the validator operators themselves, who bear the direct cost of every missed epoch and every hour of undiagnosed downtime — especially individual hosts without dedicated DevOps staff, for whom building and maintaining a comparable monitoring stack on their own is simply not feasible.

We request 96K in USDT over 12 months, paid in quarterly tranches, to deploy and maintain a production-grade observability platform — custom Gonka exporters, fleet-wide and individual dashboards, opt-in log aggregation, external endpoint health checks, alerting and SLA reporting, hands-on validator onboarding, incident response support, and ongoing operational maintenance. All code, configurations, and dashboards will be open-source and published in public GitHub repositories.

Full proposal and discussion: https://github.com/gonka-ai/gonka/discussions/1085

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:57.1%"></div>
    <div class="prop-tally-no" style="width:42.9%"></div>
    <div class="prop-tally-veto" style="width:0.0%"></div>
    <div class="prop-tally-abstain" style="width:0.0%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes 17,955 (57.1%)</span>
    <span class="prop-tally-no-text">No 13,494 (42.9%)</span>
    <span class="prop-tally-veto-text">Veto 0 (0.0%)</span>
    <span class="prop-tally-abstain-text">Abstain 0 (0.0%)</span>
    <span class="prop-tally-total-text">Total 31,449 votes</span>
  </div>
</div>


---

## Messages

| # | Type |
| :- | :--- |
| 1 | `/cosmos.distribution.v1beta1.MsgCommunityPoolSpend` |

<details class="prop-contracts">
<summary>Contract Details</summary>

```json
[
  {
    "@type": "/cosmos.distribution.v1beta1.MsgCommunityPoolSpend",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "recipient": "gonka1yf2f23sqx8fradjn7laqp0twamlhy4sj6vzwmg946ux4awfqaaes9avx7a",
    "amount": [
      {
        "denom": "ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4",
        "amount": "96000000000"
      }
    ]
  }
]
```

</details>

---