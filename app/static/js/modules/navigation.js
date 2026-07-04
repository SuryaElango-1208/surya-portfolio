/**
 * Navigation: sticky "glass" nav on scroll, scroll-spy active link
 * highlighting, and the mobile menu toggle.
 *
 * Scroll-spy uses IntersectionObserver rather than a scroll listener doing
 * getBoundingClientRect() math on every frame — the observer only fires
 * when a section actually crosses the threshold, which is both simpler
 * code and cheaper on the main thread.
 */
export function initNavigation() {
  const nav = document.getElementById('site-nav');
  const burger = document.getElementById('nav-burger');
  const mobileMenu = document.getElementById('mobile-menu');
  const navLinks = document.querySelectorAll('[data-nav-link]');
  const sections = document.querySelectorAll('main section[id]');

  // ---- Sticky glass background after scrolling past the hero ----
  const onScroll = () => {
    nav.classList.toggle('nav--scrolled', window.scrollY > 60);
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // ---- Mobile menu ----
  if (burger && mobileMenu) {
    let scrollYBeforeOpen = 0;

    const setMenuOpen = (isOpen) => {
      burger.setAttribute('aria-expanded', String(isOpen));
      burger.setAttribute('aria-label', isOpen ? 'Close menu' : 'Open menu');
      mobileMenu.hidden = !isOpen;

      // Lock the page behind the menu. Plain `overflow: hidden` on body
      // is well known to NOT reliably stop touch-scrolling on iOS
      // Safari — the page can still rubber-band scroll behind a
      // position:fixed overlay there, which is exactly the kind of
      // "solid" overlay letting content bleed through mid-scroll that
      // shows up in mobile screenshots. Pinning body via its own
      // scroll offset is the standard cross-browser-safe fix.
      if (isOpen) {
        scrollYBeforeOpen = window.scrollY;
        document.body.style.position = 'fixed';
        document.body.style.top = `-${scrollYBeforeOpen}px`;
        document.body.style.width = '100%';
      } else {
        document.body.style.position = '';
        document.body.style.top = '';
        document.body.style.width = '';
        window.scrollTo(0, scrollYBeforeOpen);
      }
    };

    burger.addEventListener('click', () => {
      const isOpen = burger.getAttribute('aria-expanded') === 'true';
      setMenuOpen(!isOpen);
    });

    mobileMenu.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => setMenuOpen(false));
    });
  }

  // ---- Scroll-spy ----
  if ('IntersectionObserver' in window && sections.length) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          const id = entry.target.id;
          navLinks.forEach((link) => {
            const matches = link.getAttribute('href') === `#${id}`;
            link.classList.toggle('is-active', matches);
            if (matches) {
              link.setAttribute('aria-current', 'true');
            } else {
              link.removeAttribute('aria-current');
            }
          });
        });
      },
      { rootMargin: '-45% 0px -50% 0px', threshold: 0 }
    );

    sections.forEach((section) => observer.observe(section));
  }
}
