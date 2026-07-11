---
title: "#66 – test proposal - 测试方案"
description: "test proposal - 测试方案"
template: proposals-proposals-main.html
---

# #66 – test proposal - 测试方案

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-rejected">Rejected</span>

**Proposal ID:** `66`

**Type:** Execute Contract

**Submit:** 2026-06-03 17:45 UTC

**Voting:** 2026-06-03 17:45 UTC → 2026-06-05 17:45 UTC

**Proposer:** [`gonka1hwyjwehgp6e5pgpg0ye4a7unwu5q9xzljpuwr5`](https://gonka.gg/address/gonka1hwyjwehgp6e5pgpg0ye4a7unwu5q9xzljpuwr5){:target="_blank"}

**Failed reason:** proposal did not get enough votes to pass

<div class="prop-funding-line prop-funding-line-rejected">$1,000,000 · Community Pool</div>


[View on gonka.gg](https://gonka.gg/network/proposals/66){:target="_blank"}

</div>

test proposal - 测试方案

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
    <span class="prop-tally-veto-text">Veto 579,377 (100.0%)</span>
    <span class="prop-tally-abstain-text">Abstain 0 (0.0%)</span>
    <span class="prop-tally-total-text">Total 579,377 votes</span>
    
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
        "amount": "1000000000000",
        "denom": "ibc/115F68FBA220A028C6F6ED08EA0C1A9C8C52798B14FB66E6C89D5D8C06A524D4",
        "recipient": "gonka1hwyjwehgp6e5pgpg0ye4a7unwu5q9xzljpuwr5"
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
