---
title: "#111 – Bringing AMD and AI ASICs to Gonka: hardware classes for verification"
description: "# Bringing AMD and AI ASICs to Gonka

Gonka's approved hardware list contains six NVIDIA GPU models. Every other accelerator is excluded, including the purpose-built inference ASICs that now form the "
template: proposals-proposals-main.html
---

# #111 – Bringing AMD and AI ASICs to Gonka: hardware classes for verification

<div class="prop-detail-header" markdown="1">

<div class="prop-badge-row"><span class="prop-badge prop-voting">Voting</span><span class="prop-vote-countdown prop-vote-countdown-detail" data-deadline="2026-10-04T00:26:22.750300831Z"></span></div>

**Proposal ID:** `111`

**Type:** Execute Contract

**Submit:** 2026-10-02 00:26 UTC

**Voting:** 2026-10-02 00:26 UTC → 2026-10-04 00:26 UTC

**Proposer:** [`gonka1ycfuz72tutxra27x47ukqye8zmxyuygx8gdh0m`](https://gonka.gg/address/gonka1ycfuz72tutxra27x47ukqye8zmxyuygx8gdh0m){:target="_blank"}

**Metadata:** [https://gonka.vote/proposal/k58ptx](https://gonka.vote/proposal/k58ptx)

<div class="prop-funding-line prop-funding-line-voting">$160,000 · Community Pool</div>


[View on gonka.gg](https://gonka.gg/network/proposals/111){:target="_blank"}

</div>

# Bringing AMD and AI ASICs to Gonka

Gonka's approved hardware list contains six NVIDIA GPU models. Every other accelerator is excluded, including the purpose-built inference ASICs that now form the fastest-growing segment of AI compute.

Wayfaster proposes to change that in 20 weeks. The work delivers hardware classes, the mechanism that lets governance approve any accelerator by vote without further protocol work; AMD support end to end as the first vendor through that mechanism; verification conformance on Tenstorrent and Intel Gaudi 3 silicon; a Furiosa adapter design; Qualcomm and Positron fit assessments; a measured class for NVIDIA's Vera Rubin generation; and written assessments for four further ASIC platforms. This is Track 3, Project 1 of the Gonka roadmap, currently unassigned.

Verification today permits one margin across every model and card, so admitting new hardware means widening that margin for everyone. Per-class margins remove that trade-off. Existing hosts are unaffected on day one: the current fleet maps into NVIDIA classes carrying exactly today's values, and no existing margin is widened.

Total cost is 480,000 USDT, covering four engineers and a project manager for 20 weeks, hardware and vendor programmes, an independent security review, and a month of support after delivery.

This proposal executes the first tranche only: 160,000 USDT to [gonka1ycfuz72tutxra27x47ukqye8zmxyuygx8gdh0m](https://gonka.gg/address/gonka1ycfuz72tutxra27x47ukqye8zmxyuygx8gdh0m). The remaining 320,000 USDT is contingent on delivery and is not authorised by this vote. It requires a separate proposal once the work is complete, less any GNK mined by our nodes during the project. All work is public from week one, a spend report with invoices is published, and hardware bought with grant funds transfers to the network on completion.

Full proposal, with the complete budget, phase plan and sources: <https://gonka.vote/proposal/k58ptx>

Wayfaster, wayfaster.org, hi@wayfaster.org

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:0.0%"></div>
    <div class="prop-tally-no" style="width:0.6%"></div>
    <div class="prop-tally-veto" style="width:0.0%"></div>
    <div class="prop-tally-abstain" style="width:0.7%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes <strong>0.0%</strong> (0)</span>
    <span class="prop-tally-no-text">No <strong>49.3%</strong> (3,471)</span>
    <span class="prop-tally-veto-text">Veto <strong>0.0%</strong> (0)</span>
    <span class="prop-tally-abstain-text">Abstain <strong>50.7%</strong> (3,571)</span>
    <span class="prop-tally-total-text">Total 7,042 votes</span>
    <span class="prop-tally-veto-text">✗ Turnout <strong>1.3%</strong> (7,042 / 537,228) · Quorum <strong>25%</strong> (134,307)</span>
  </div>
</div>



<h2 id="voters">Voters</h2>

<div class="prop-voters-wrap">
<table class="prop-voters">
<thead><tr><th>Voter</th><th>Vote</th></tr></thead>
<tbody>
<tr><td><a href="https://gonka.gg/address/gonka1ym3np7guxart483yfdxnlztuazx22cjt0e4a2p" target="_blank" class="prop-voter-addr">gonka1ym3np7…0e4a2p</a></td><td><span class="prop-voter-option prop-vote-no">No 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka1xvlfshxznnuftsv2lke98rv9eqkjr0v6z8c3uk" target="_blank" class="prop-voter-addr">gonka1xvlfsh…z8c3uk</a></td><td><span class="prop-voter-option prop-vote-abstain">Abstain 100.0%</span></td></tr>
</tbody>
</table>
</div>

---
## Messages

| # | Type |
| :- | :--- |
| 1 | `/cosmwasm.wasm.v1.MsgExecuteContract` |

<details class="prop-contracts" markdown="1">
<summary markdown="1">Contract Details</summary>

```json
[
  {
    "@type": "/cosmwasm.wasm.v1.MsgExecuteContract",
    "sender": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "contract": "gonka18pkq9mwxxlmyq7kr5txhm060wemg2s4u94wvsfd9w2kdc0u99d6spk8pz2",
    "msg": {
      "withdraw_ibc": {
        "denom": "ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4",
        "amount": "160000000000",
        "recipient": "gonka1ycfuz72tutxra27x47ukqye8zmxyuygx8gdh0m"
      }
    },
    "funds": []
  }
]
```

</details>
