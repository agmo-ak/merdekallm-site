// Mobile nav toggle
document.addEventListener('DOMContentLoaded', function () {
  var toggle = document.querySelector('.nav-toggle');
  var panel = document.querySelector('.mobile-nav');
  if (toggle && panel) {
    toggle.addEventListener('click', function () {
      panel.classList.toggle('open');
      var expanded = panel.classList.contains('open');
      toggle.setAttribute('aria-expanded', String(expanded));
    });
  }

  // Size chart tooltip: same details on hover and keyboard focus. Every value is
  // also in the chart's data table, so the tooltip never gates anything.
  document.querySelectorAll('.size-chart').forEach(function (chart) {
    var wrap = chart.querySelector('.chart-scroll');
    var tip = chart.querySelector('.chart-tip');
    if (!wrap || !tip) return;
    function show(pt) {
      var parts = (pt.getAttribute('data-tip') || '').split('|');
      var value = document.createElement('strong');
      var name = document.createElement('span');
      value.textContent = parts[0] || '';
      name.textContent = parts[1] || '';
      tip.replaceChildren(value, name);
      var dot = pt.querySelector('.chart-dot').getBoundingClientRect();
      var box = wrap.getBoundingClientRect();
      tip.hidden = false;
      // Centred on the dot, but kept inside the viewport (points near the edges on phones).
      var half = tip.offsetWidth / 2, edge = 8;
      var cx = Math.min(Math.max(dot.left + dot.width / 2, half + edge),
                        document.documentElement.clientWidth - half - edge);
      tip.style.left = (cx - box.left + wrap.scrollLeft) + 'px';
      tip.style.top = (dot.top - box.top) + 'px';
    }
    function hide() { tip.hidden = true; }
    chart.querySelectorAll('.chart-pt').forEach(function (pt) {
      pt.addEventListener('pointerenter', function () { show(pt); });
      pt.addEventListener('pointerleave', hide);
      pt.addEventListener('focus', function () { show(pt); });
      pt.addEventListener('blur', hide);
    });
  });

  // Contact form: progressive enhancement over FormSubmit.co's native POST.
  var form = document.querySelector('form[data-contact-form]');
  if (form) {
    form.addEventListener('submit', function (e) {
      var action = form.getAttribute('action') || '';
      e.preventDefault();
      var status = form.querySelector('.form-status');
      var submitBtn = form.querySelector('button[type="submit"]');
      if (submitBtn) submitBtn.disabled = true;
      fetch(action, {
        method: 'POST',
        body: new FormData(form),
        headers: { Accept: 'application/json' }
      })
        .then(function (res) {
          if (res.ok) {
            form.reset();
            if (status) status.textContent = "Thanks. We'll be in touch shortly.";
          } else {
            if (status) status.textContent = 'Something went wrong. Please email merdeka@agmogroup.com directly.';
          }
        })
        .catch(function () {
          if (status) status.textContent = 'Something went wrong. Please email merdeka@agmogroup.com directly.';
        })
        .finally(function () {
          if (submitBtn) submitBtn.disabled = false;
        });
    });
  }
});
