---
title: "#30 – Test Proposal"
description: "Testing governance voting from the wallet app."
template: proposals-proposals-main.html
---

# #30 – Test Proposal

<div class="prop-detail-header" markdown="1">

<span class="prop-badge prop-rejected">Rejected</span>

**Proposal ID:** `30`

**Type:** —

**Submit:** 2026-03-09 02:33 UTC

**Voting:** 2026-03-09 02:37 UTC → 2026-03-10 02:37 UTC

**Proposer:** [`gonka1awyggfq4e32d4y66ttq3hyud7dyrr0ajf8af0w`](https://gonka.gg/address/gonka1awyggfq4e32d4y66ttq3hyud7dyrr0ajf8af0w){:target="_blank"}

**Metadata:** `Test proposal for governance UI`

**Failed reason:** proposal did not get enough votes to pass



[View on gonka.gg](https://gonka.gg/network/proposals/30){:target="_blank"}

</div>

Testing governance voting from the wallet app.

---

## Final Tally


<div class="prop-tally">
  <div class="prop-tally-bar">
    <div class="prop-tally-yes" style="width:0.0%"></div>
    <div class="prop-tally-no" style="width:100.0%"></div>
    <div class="prop-tally-veto" style="width:0.0%"></div>
    <div class="prop-tally-abstain" style="width:0.0%"></div>
  </div>
  <div class="prop-tally-stats">
    <span class="prop-tally-yes-text">Yes 0 (0.0%)</span>
    <span class="prop-tally-no-text">No 47 (100.0%)</span>
    <span class="prop-tally-veto-text">Veto 0 (0.0%)</span>
    <span class="prop-tally-abstain-text">Abstain 0 (0.0%)</span>
    <span class="prop-tally-total-text">Total 47 votes</span>
    
  </div>
</div>


---

## Messages

| # | Type |
| :- | :--- |

<details class="prop-contracts" markdown="1">
<summary markdown="1">Contract Details</summary>

```json
[]
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
