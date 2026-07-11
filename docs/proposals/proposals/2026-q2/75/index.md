---
title: "#75 – Private Inc × Gonka — Network Growth Initiative"
description: "IMPORTANT: Below is a condensed version of the proposal. It highlights only the key points and does not disclose all details of the initiative, implementation mechanics, KPIs, or terms. It is strongly"
template: proposals-proposals-main.html
---

# #75 – Private Inc × Gonka — Network Growth Initiative

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-rejected">Rejected</span>

**Proposal ID:** `75`

**Type:** Execute Contract

**Submit:** 2026-06-13 16:24 UTC

**Voting:** 2026-06-13 16:24 UTC → 2026-06-15 16:24 UTC

**Proposer:** [`gonka1q022xj6uyylzzhdlsh3jtkp5ycrnzwgpwgp4tn`](https://gonka.gg/address/gonka1q022xj6uyylzzhdlsh3jtkp5ycrnzwgpwgp4tn){:target="_blank"}

**Metadata:** [https://vote.gonka.vip/tenders/ed8148eb-535e-4677-9a6b-5316c81c996a](https://vote.gonka.vip/tenders/ed8148eb-535e-4677-9a6b-5316c81c996a)

**Failed reason:** proposal did not get enough votes to pass

<div class="prop-funding-line prop-funding-line-rejected">$300,000 · Community Pool</div>


[View on gonka.gg](https://gonka.gg/network/proposals/75){:target="_blank"}

</div>

IMPORTANT: Below is a condensed version of the proposal. It highlights only the key points and does not disclose all details of the initiative, implementation mechanics, KPIs, or terms. It is strongly recommended to review the full version of the document via the link: <https://vote.gonka.vip/tenders/ed8148eb-535e-4677-9a6b-5316c81c996a>

Private Inc × Gonka — Network Growth Initiative

Private Inc proposes launching a growth program for the Gonka ecosystem aimed at attracting AI developers, AI companies, infrastructure operators, GPU farms, and new computing resources to the network.

Unlike traditional marketing campaigns focused on impressions and reach, this initiative is centered on measurable ecosystem growth: onboarding new participants, connecting infrastructure providers, and increasing available GPU resources.

Who We Are

Private Inc is a performance marketing and media buying company with more than 7 years of experience working with technology, AI, Web3, and DePIN projects.

The team consists of more than 100 specialists, and the monthly advertising budget exceeds $3 million. Our core expertise is building user acquisition and conversion systems rather than conducting PR activities.

Why Gonka

After analyzing the project, we concluded that Gonka’s growth potential significantly exceeds its current market awareness.

Despite having a functioning product, community, and infrastructure, many AI developers, GPU providers, and companies are still unfamiliar with the network’s capabilities. We believe now is the right time to scale the ecosystem through targeted participant acquisition.

Target Market

The primary market is the United States, including regions with a high concentration of AI companies and computing infrastructure.

Target audiences:

• AI Developers
• AI Startups and AI Companies
• GPU Farms and Compute Providers
• Infrastructure Operators and Data Centers
• Web3 & DePIN Communities

How It Works

Audience acquisition is planned through Google Ads, Meta Ads, YouTube Ads, and other channels.

Users will be directed to specialized landing pages, after which they will go through qualification and onboarding. The main objective is not traffic itself, but converting interested participants into active users of the Gonka ecosystem.

Funding Request

The full program is designed around a budget of 600,000 USDT.

Only Phase One is being proposed for consideration — 300,000 USDT over 45 days.

Up to 95% of the budget is planned to be allocated directly to user acquisition, infrastructure operator recruitment, and scaling effective advertising campaigns. Private Inc provides its existing team, advertising infrastructure, and operational resources without requiring additional funding.

Phase One Targets

Key targets for the first phase:

• 325,000–400,000 targeted visits
• 1,000–1,500 qualified AI developers
• 250–350 host leads
• 100–125 new infrastructure operators
• Up to 2,000 additional GPUs connected to the network

The primary focus is on real ecosystem expansion and increased computing capacity.

Transparency & Reporting

Throughout implementation, regular public reporting is planned regarding expenditures, campaign performance, participant acquisition, and KPI achievement. This will allow the community to objectively evaluate the program’s results.

Conclusion

Private Inc is not requesting funding to build a new team or infrastructure — all necessary resources already exist.

The funds are intended to be used primarily for attracting new users, developers, infrastructure operators, and computing resources into the Gonka ecosystem.

Successful completion of the first phase will provide measurable results and help determine the potential for further scaling of the growth program.

IMPORTANT: This is a condensed version of the document and does not include many important details, calculations, implementation terms, or supporting rationale. To fully understand the proposal, please review the complete version of the document via the following link: <https://vote.gonka.vip/tenders/ed8148eb-535e-4677-9a6b-5316c81c996a>

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:0.0%"></div>
    <div class="prop-tally-no" style="width:0.0%"></div>
    <div class="prop-tally-veto" style="width:100.0%"></div>
    <div class="prop-tally-abstain" style="width:0.0%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes 0 (0.0%)</span>
    <span class="prop-tally-no-text">No 0 (0.0%)</span>
    <span class="prop-tally-veto-text">Veto 313,499 (100.0%)</span>
    <span class="prop-tally-abstain-text">Abstain 0 (0.0%)</span>
    <span class="prop-tally-total-text">Total 313,499 votes</span>
    
  </div>
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
        "amount": "300000000000",
        "denom": "ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4",
        "recipient": "gonka1vvhnfezn37yc8aftc0af6rcn97xn53fqjmdzf9"
      }
    },
    "funds": []
  }
]
```

</details>

---

<script>
function _dtInit() {
  document.querySelectorAll('.prop-vote-countdown').forEach(function(el) {
    var deadline = new Date(el.getAttribute('data-deadline'));
    function update() {
      var diff = deadline - new Date();
      if (diff <= 0) { el.textContent = 'Ended'; el.classList.add('ended'); return; }
      var d = Math.floor(diff / 86400000);
      var h = Math.floor((diff % 86400000) / 3600000);
      var m = Math.floor((diff % 3600000) / 60000);
      if (d > 0) el.textContent = d + 'd ' + h + 'h ' + m + 'm';
      else if (h > 0) el.textContent = h + 'h ' + m + 'm';
      else el.textContent = m + 'm';
    }
    update();
    setInterval(update, 60000);
  });
}
_dtInit();
</script>
