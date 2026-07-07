---
title: "2025-Q3 Proposals"
template: proposals-oview.html
---

# 2025-Q3 Proposals

<div class="prop-oview-filter" markdown="1">

<label class="prop-filter-cb">
  <input type="checkbox" id="prop-filter-passed" checked>
  <span class="prop-filter-label">Passed</span>
</label>
<label class="prop-filter-cb">
  <input type="checkbox" id="prop-filter-rejected" checked>
  <span class="prop-filter-label">Rejected</span>
</label>
<label class="prop-filter-cb">
  <input type="checkbox" id="prop-filter-voting" checked>
  <span class="prop-filter-label">Voting</span>
</label>
<label class="prop-filter-cb">
  <input type="checkbox" id="prop-filter-deposit" checked>
  <span class="prop-filter-label">Deposit</span>
</label>
<span class="prop-filter-count"></span>

</div>

<div class="prop-quarter">
<h2>2025-q3</h2>
<p>6 proposals</p>
<div class="prop-card" data-status="prop-passed">
  <div class="prop-card-header">
    <a href="6/" class="prop-card-title">#6 - Upgrade Proposal: v0.2.2</a>
    <span class="prop-badge prop-passed">Passed</span>
  </div>
  <div class="prop-card-meta">
    <span>Submitted 2025-09-24 23:08 UTC</span>
    <span>Voting ends 2025-09-25 02:08</span>
  </div>
  <div class="prop-card-desc">Upgrade Proposal: v0.2.2</div>
</div>

<div class="prop-card" data-status="prop-passed">
  <div class="prop-card-header">
    <a href="5/" class="prop-card-title">#5 - Expedite voting for upgrades</a>
    <span class="prop-badge prop-passed">Passed</span>
  </div>
  <div class="prop-card-meta">
    <span>Submitted 2025-09-23 06:39 UTC</span>
    <span>Voting ends 2025-09-23 18:39</span>
  </div>
  <div class="prop-card-desc">Expedite voting for upgrades</div>
</div>

<div class="prop-card" data-status="prop-rejected">
  <div class="prop-card-header">
    <a href="4/" class="prop-card-title">#4 - Upgrade Proposal: v0.2.2</a>
    <span class="prop-badge prop-rejected">Rejected</span>
  </div>
  <div class="prop-card-meta">
    <span>Submitted 2025-09-22 10:02 UTC</span>
    <span>Voting ends 2025-09-24 10:02</span>
  </div>
  <div class="prop-card-desc">Upgrade Proposal: v0.2.2</div>
</div>

<div class="prop-card" data-status="prop-passed">
  <div class="prop-card-header">
    <a href="3/" class="prop-card-title">#3 - Increase PoC Validation Length</a>
    <span class="prop-badge prop-passed">Passed</span>
  </div>
  <div class="prop-card-meta">
    <span>Submitted 2025-09-20 05:16 UTC</span>
    <span>Voting ends 2025-09-20 17:16</span>
  </div>
  <div class="prop-card-desc">Proposal updates poc_validation_duration from 20 to 100.</div>
</div>

<div class="prop-card" data-status="prop-passed">
  <div class="prop-card-header">
    <a href="2/" class="prop-card-title">#2 - Proposal introducing new Qwen3 models</a>
    <span class="prop-badge prop-passed">Passed</span>
  </div>
  <div class="prop-card-meta">
    <span>Submitted 2025-09-09 21:40 UTC</span>
    <span>Voting ends 2025-09-11 21:40</span>
  </div>
  <div class="prop-card-desc">This proposal introduces new Qwen3 models including Qwen3-32B-FP8 and Qwen3-235B-A22B-Instruct-2507-FP8, along with updating parameters for Qwen2.5-7B-Instruct and QwQ-32B.</div>
</div>

<div class="prop-card" data-status="prop-passed">
  <div class="prop-card-header">
    <a href="1/" class="prop-card-title">#1 - Correct Epoch Length</a>
    <span class="prop-badge prop-passed">Passed</span>
  </div>
  <div class="prop-card-meta">
    <span>Submitted 2025-09-05 21:51 UTC</span>
    <span>Voting ends 2025-09-07 21:51</span>
  </div>
  <div class="prop-card-desc">Proposal updates epoch_length and restrictions length according to real block length in seconds.</div>
</div>

</div>

<p><a href="../"><em>← Back to all proposals</em></a></p>

<script>
function initProposalsPage() {
  var checkboxes = document.querySelectorAll('.prop-oview-filter input[type=checkbox]');
  var cards = document.querySelectorAll('.prop-card');
  var countEl = document.querySelector('.prop-filter-count');
  function apply() {
    var filters = {};
    checkboxes.forEach(function(cb) {
      filters[cb.id.replace('prop-filter-', '')] = cb.checked;
    });
    var visible = 0;
    cards.forEach(function(card) {
      var status = card.getAttribute('data-status');
      var show = false;
      if (status === 'prop-passed' && filters.passed) show = true;
      else if (status === 'prop-rejected' && filters.rejected) show = true;
      else if (status === 'prop-voting' && filters.voting) show = true;
      else if (status === 'prop-deposit' && filters.deposit) show = true;
      else if (status === 'prop-failed' && filters.rejected) show = true;
      card.style.display = show ? '' : 'none';
      if (show) visible++;
    });
    countEl.textContent = visible + ' of ' + cards.length + ' proposals';
  }
  checkboxes.forEach(function(cb) { cb.addEventListener('change', apply); });
  apply();
}
document$.subscribe(initProposalsPage);
</script>
