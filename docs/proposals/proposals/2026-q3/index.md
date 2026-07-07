---
title: "2026-Q3 Proposals"
template: proposals-oview.html
---

# 2026-Q3 Proposals

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
<h2>2026-Q3</h2>
<p>1 proposals</p>
<div class="prop-card" data-status="prop-voting">
  <div class="prop-card-header">
    <a href="80/" class="prop-card-title">#80 – GRC Proposal #3 - Restitution</a>
    <span class="prop-badge prop-voting">Voting</span>
  </div>
  <div class="prop-card-meta">
    <span>Submitted 2026-07-05</span>
    <span>Voting ends 2026-07-07</span>
  </div>
  <div class="prop-card-desc">Restitution payout for confirmed GRC Proposal #3 cases, with Case 05 payments from proposal_id=67 deducted where the same address and epoch were already compensated, and positive victim outputs below …</div>
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
