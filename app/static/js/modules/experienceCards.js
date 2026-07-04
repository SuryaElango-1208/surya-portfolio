/**
 * Experience cards: expand/collapse via aria-expanded + a sibling
 * .is-open class. The actual height animation is pure CSS (the
 * grid-template-rows trick in experience.css) — this module only ever
 * toggles two things: an attribute and a class. No inline style/height
 * measuring, which is what makes the CSS-only animation approach work.
 */
export function initExperienceCards() {
  const toggles = document.querySelectorAll('[data-exp-toggle]');

  toggles.forEach((button) => {
    button.addEventListener('click', () => {
      const expanded = button.getAttribute('aria-expanded') === 'true';
      const wrapper = button.nextElementSibling;

      button.setAttribute('aria-expanded', String(!expanded));
      if (wrapper) {
        wrapper.classList.toggle('is-open', !expanded);
      }
    });
  });
}
