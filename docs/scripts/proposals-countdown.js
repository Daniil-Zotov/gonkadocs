function initCountdowns() {
  document.querySelectorAll('.prop-vote-countdown').forEach(function(el) {
    var deadline = new Date(el.getAttribute('data-deadline'));
    function update() {
      var diff = deadline - new Date();
      if (diff <= 0) {
        el.textContent = 'Ended';
        el.classList.add('ended');
        return;
      }
      var d = Math.floor(diff / 86400000);
      var h = Math.floor((diff % 86400000) / 3600000);
      var m = Math.floor((diff % 3600000) / 60000);
      if (d > 0) el.textContent = d + 'd ' + h + 'h ' + m + 'm';
      else if (h > 0) el.textContent = h + 'h ' + m + 'm';
      else el.textContent = m + 'm';
    }
    update();
    if (el._countdownTimer) clearInterval(el._countdownTimer);
    el._countdownTimer = setInterval(update, 60000);
  });
}

if (typeof document$ !== 'undefined') {
  document$.subscribe(initCountdowns);
}
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initCountdowns);
} else {
  initCountdowns();
}
