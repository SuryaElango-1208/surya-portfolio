/**
 * Contact form submission.
 *
 * Posts JSON to /api/contact (matching ContactFormRequest in
 * app/models/contact.py) and reflects the result in an aria-live region,
 * so screen reader users get the same feedback sighted users get from the
 * text change — not just a silent DOM update.
 *
 * Email is validated for syntax only, server-side (see contact.py) — no
 * DNS/deliverability check, since that would risk rejecting a perfectly
 * real company or HR address on a false negative. The one improvement
 * offered here is a *non-blocking* "did you mean gmail.com?" suggestion
 * for near-miss typos of well-known providers, which never prevents
 * submission — it's a nudge, not a gate.
 */

// Common providers worth catching a typo against. Deliberately short and
// personal-email-focused — company/HR domains are exactly what we must
// NOT second-guess, so this list stays limited to consumer providers
// where a typo is overwhelmingly more likely than an unusual real domain.
const KNOWN_EMAIL_DOMAINS = [
  'gmail.com',
  'yahoo.com',
  'outlook.com',
  'hotmail.com',
  'icloud.com',
  'live.com',
  'protonmail.com',
  'aol.com',
  'rediffmail.com',
];

function levenshtein(a, b) {
  const dp = Array.from({ length: a.length + 1 }, (_, i) => [i, ...Array(b.length).fill(0)]);
  for (let j = 0; j <= b.length; j += 1) dp[0][j] = j;
  for (let i = 1; i <= a.length; i += 1) {
    for (let j = 1; j <= b.length; j += 1) {
      dp[i][j] =
        a[i - 1] === b[j - 1]
          ? dp[i - 1][j - 1]
          : 1 + Math.min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]);
    }
  }
  return dp[a.length][b.length];
}

/** Returns a suggested domain if `domain` is a close-but-not-exact typo
 * of a known provider, otherwise null. Exact matches return null (nothing
 * to suggest); anything more than 2 edits away is treated as "probably a
 * real, different domain" rather than a typo, so it's left alone. */
function suggestDomain(domain) {
  if (!domain || KNOWN_EMAIL_DOMAINS.includes(domain)) return null;
  let best = null;
  let bestDistance = 3; // anything >= 3 edits away isn't flagged as a typo
  for (const known of KNOWN_EMAIL_DOMAINS) {
    const distance = levenshtein(domain, known);
    if (distance > 0 && distance < bestDistance) {
      best = known;
      bestDistance = distance;
    }
  }
  return best;
}

export function initContactForm() {
  const form = document.getElementById('contact-form');
  if (!form) return;

  const status = document.getElementById('contact-form-status');
  const submitBtn = form.querySelector('.contact-form__submit');
  const submitText = form.querySelector('.contact-form__submit-text');
  const emailInput = document.getElementById('cf-email');
  const emailHint = document.getElementById('cf-email-hint');

  // ---- Non-blocking domain-typo suggestion ----
  if (emailInput && emailHint) {
    emailInput.addEventListener('blur', () => {
      const value = emailInput.value.trim();
      const atIndex = value.lastIndexOf('@');
      if (atIndex === -1) {
        emailHint.textContent = '';
        return;
      }
      const domain = value.slice(atIndex + 1).toLowerCase();
      const suggestion = suggestDomain(domain);
      emailHint.textContent = '';
      if (!suggestion) return;

      const local = value.slice(0, atIndex);
      const correctedAddress = `${local}@${suggestion}`;
      const prefix = document.createTextNode(`Did you mean ${local}@`);
      const link = document.createElement('button');
      link.type = 'button';
      link.className = 'contact-form__hint-action';
      link.textContent = suggestion;
      link.addEventListener('click', () => {
        emailInput.value = correctedAddress;
        emailHint.textContent = '';
        emailInput.focus();
      });
      const suffix = document.createTextNode('?');

      emailHint.append(prefix, link, suffix);
    });

    // Clear the suggestion as soon as they start editing again.
    emailInput.addEventListener('input', () => {
      emailHint.textContent = '';
    });
  }

  form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const payload = {
      name: form.name.value.trim(),
      email: form.email.value.trim(),
      message: form.message.value.trim(),
      website: form.website.value, // honeypot — empty for real visitors
    };

    setLoading(true);
    setStatus('', null);

    try {
      const response = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (response.status === 429) {
        setStatus("That's a few too many messages — try again a bit later.", 'error');
        return;
      }

      if (!response.ok) {
        setStatus(await describeValidationError(response), 'error');
        return;
      }

      const data = await response.json();
      setStatus(data.message, 'success');
      form.reset();
    } catch {
      setStatus("Couldn't reach the server — please try again in a moment.", 'error');
    } finally {
      setLoading(false);
    }
  });

  /** FastAPI/Pydantic 422 bodies look like:
   *   { "detail": [{ "loc": ["body", "email"], "msg": "...", ... }, ...] }
   * We only special-case the email field, since that's the one with a
   * clear, specific, user-facing message; everything else falls back to
   * the original generic copy. */
  async function describeValidationError(response) {
    const fallback = 'Something in the form looks off — please check the fields and try again.';
    if (response.status !== 422) return fallback;

    try {
      const data = await response.json();
      const errors = Array.isArray(data.detail) ? data.detail : [];
      const emailError = errors.find((err) => Array.isArray(err.loc) && err.loc.includes('email'));
      return emailError ? 'Please enter a valid mail id.' : fallback;
    } catch {
      return fallback;
    }
  }

  function setLoading(isLoading) {
    submitBtn.disabled = isLoading;
    submitText.textContent = isLoading ? 'Sending…' : 'Send message';
  }

  function setStatus(message, kind) {
    status.textContent = message;
    if (kind) {
      status.setAttribute('data-status', kind);
    } else {
      status.removeAttribute('data-status');
    }
  }
}
