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
            if (status) status.textContent = "Thanks — we'll be in touch shortly.";
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
