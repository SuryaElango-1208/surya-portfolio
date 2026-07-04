/**
 * Theme toggle: dark by default, light available on request.
 *
 * Deliberately does NOT read `prefers-color-scheme` as the initial state.
 * Dark is the brand identity here, not just a UI default — so unless the
 * visitor has explicitly chosen light before (stored in localStorage), the
 * site opens dark regardless of OS-level preference. The toggle itself is
 * the escape hatch for anyone who wants light instead.
 *
 * localStorage is appropriate here — this is a real, standalone website
 * served by our own FastAPI app and run in the visitor's own browser, not
 * a sandboxed preview environment.
 */
const STORAGE_KEY = 'portfolio-theme';

export function initThemeToggle() {
  const toggle = document.getElementById('theme-toggle');
  const iconMoon = document.getElementById('icon-moon');
  const iconSun = document.getElementById('icon-sun');
  if (!toggle) return;

  const stored = safeGet();
  if (stored === 'light') {
    applyTheme('light');
  }

  toggle.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'light' ? 'dark' : 'light';
    applyTheme(next);
    safeSet(next);
  });

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    toggle.setAttribute('aria-pressed', String(theme === 'light'));
    toggle.setAttribute('aria-label', theme === 'light' ? 'Switch to dark theme' : 'Switch to light theme');
    if (iconMoon && iconSun) {
      iconMoon.style.display = theme === 'light' ? 'none' : 'block';
      iconSun.style.display = theme === 'light' ? 'block' : 'none';
    }
  }
}

function safeGet() {
  try {
    return window.localStorage.getItem(STORAGE_KEY);
  } catch {
    // Private browsing / storage disabled — theme just won't persist.
    return null;
  }
}

function safeSet(value) {
  try {
    window.localStorage.setItem(STORAGE_KEY, value);
  } catch {
    /* no-op */
  }
}
