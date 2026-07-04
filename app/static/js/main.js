/**
 * Entry point. Loaded as a native ES module (type="module" in index.html)
 * — no bundler, no build step. Every browser released in the last several
 * years supports import/export natively, and for a page this size a
 * webpack/vite toolchain would add complexity without adding capability.
 *
 * Each module below owns exactly one concern and exposes a single init
 * function. That's the whole "architecture" for the frontend: small,
 * independent, individually testable pieces, composed here.
 */
import { initNavigation } from './modules/navigation.js';
import { initScrollReveal } from './modules/scrollReveal.js';
import { initThemeToggle } from './modules/themeToggle.js';
import { initExperienceCards } from './modules/experienceCards.js';
import { initArchitectureDiagram } from './modules/architectureDiagram.js';
import { initContactForm } from './modules/contactForm.js';

function init() {
  initThemeToggle();
  initNavigation();
  initScrollReveal();
  initExperienceCards();
  initArchitectureDiagram();
  initContactForm();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
