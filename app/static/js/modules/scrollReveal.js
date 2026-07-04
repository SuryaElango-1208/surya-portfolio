/**
 * Scroll reveal: adds .is-visible to .reveal elements as they enter the
 * viewport. The CSS in layout.css already defines the hidden -> visible
 * transition; this module's only job is deciding *when* to flip the class.
 *
 * No-JS fallback: .reveal starts at opacity 0 in CSS, which would leave
 * content invisible if this script fails to load. We guard against that
 * below by immediately revealing everything if IntersectionObserver isn't
 * available, and by unobserving each element once it's shown (a reveal
 * should happen once, not flicker on every scroll back up).
 */
export function initScrollReveal() {
  const targets = document.querySelectorAll('.reveal');

  if (!('IntersectionObserver' in window) || !targets.length) {
    targets.forEach((el) => el.classList.add('is-visible'));
    return;
  }

  const observer = new IntersectionObserver(
    (entries, obs) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          obs.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.15, rootMargin: '0px 0px -60px 0px' }
  );

  targets.forEach((el) => observer.observe(el));
}
