---
title: "#91 – Temporarily update BLS signing parameters"
description: "Set max_signing_attempts to 1 and signing_deadline_blocks to 60 epoch lengths (923460 blocks) to mitigate a theoretical risk identified in a security report. Historically, retries have never been need"
template: proposals-proposals-main.html
---

# #91 – Temporarily update BLS signing parameters

<div class="prop-detail-header" markdown="1">

<div class="prop-badge-row"><span class="prop-badge prop-voting">Voting</span><span class="prop-vote-countdown prop-vote-countdown-detail" data-deadline="2026-07-24T05:23:56.063230542Z"></span></div>

**Proposal ID:** `91`

**Type:** Update Params

**Submit:** 2026-07-23 17:23 UTC

**Voting:** 2026-07-23 17:23 UTC → 2026-07-24 05:23 UTC

**Expedited:** Yes

**Proposer:** [`gonka1y2a9p56kv044327uycmqdexl7zs82fs5ryv5le`](https://gonka.gg/address/gonka1y2a9p56kv044327uycmqdexl7zs82fs5ryv5le){:target="_blank"}



[View on gonka.gg](https://gonka.gg/network/proposals/91){:target="_blank"}

</div>

Set max_signing_attempts to 1 and signing_deadline_blocks to 60 epoch lengths (923460 blocks) to mitigate a theoretical risk identified in a security report. Historically, retries have never been needed on mainnet, so this temporary change is not expected to affect normal operation.

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:42.7%"></div>
    <div class="prop-tally-no" style="width:0.0%"></div>
    <div class="prop-tally-veto" style="width:0.0%"></div>
    <div class="prop-tally-abstain" style="width:0.0%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes 243,165 (100.0%)</span>
    <span class="prop-tally-no-text">No 0 (0.0%)</span>
    <span class="prop-tally-veto-text">Veto 0 (0.0%)</span>
    <span class="prop-tally-abstain-text">Abstain 0 (0.0%)</span>
    <span class="prop-tally-total-text">Total 243,165 votes</span>
    <span class="prop-tally-yes-text">✓ Turnout 243,165 / 569,511 (42.7%) · Quorum 25% (142,377)</span>
  </div>
</div>



<h2 id="voters">Voters</h2>

<div class="prop-voters-wrap">
<table class="prop-voters">
<thead><tr><th>Voter</th><th>Vote</th></tr></thead>
<tbody>
<tr><td><a href="https://gonka.gg/address/gonka1y2a9p56kv044327uycmqdexl7zs82fs5ryv5le" target="_blank" class="prop-voter-addr">gonka1y2a9p5…ryv5le</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka1gvrrhjmy4w4mayvs2s5l23edj8ertcmtd2v4zr" target="_blank" class="prop-voter-addr">gonka1gvrrhj…d2v4zr</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka1dkl4mah5erqggvhqkpc8j3qs5tyuetgdy552cp" target="_blank" class="prop-voter-addr">gonka1dkl4ma…y552cp</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
<tr><td><a href="https://gonka.gg/address/gonka1kx9mca3xm8u8ypzfuhmxey66u0ufxhs7nm6wc5" target="_blank" class="prop-voter-addr">gonka1kx9mca…nm6wc5</a></td><td><span class="prop-voter-option prop-vote-yes">Yes 100.0%</span></td></tr>
</tbody>
</table>
</div>

---
## Messages

| # | Type |
| :- | :--- |
| 1 | `/inference.bls.MsgUpdateParams` |

<details class="prop-contracts" markdown="1">
<summary markdown="1">Contract Details</summary>

```json
[
  {
    "@type": "/inference.bls.MsgUpdateParams",
    "authority": "gonka10d07y265gmmuvt4z0w9aw880jnsr700j2h5m33",
    "params": {
      "i_total_slots": 100,
      "t_slots_degree_offset": 50,
      "dealing_phase_duration_blocks": "5",
      "verification_phase_duration_blocks": "3",
      "signing_deadline_blocks": "923460",
      "dispute_phase_duration_blocks": "3",
      "completed_fallback_blocks": "0",
      "max_signing_attempts": 1
    }
  }
]
```

</details>
