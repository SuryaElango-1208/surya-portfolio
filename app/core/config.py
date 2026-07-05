"""
Application configuration.

We use pydantic-settings instead of scattering `os.getenv()` calls through
the codebase for three reasons:
  1. Type-checked: a malformed .env fails loudly at startup, not silently
     mid-request three weeks later.
  2. Self-documenting: this class IS the full list of every setting the app
     understands. No hunting through files for what env vars matter.
  3. 12-factor friendly: config lives in the environment, never hardcoded,
     never committed to git.

Common mistake this avoids: reading os.environ directly in random modules
means you can't tell what config an app needs without grepping the whole
codebase. Centralizing it here means `Settings` is the contract.
"""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Surya Elango — Portfolio"
    environment: str = "development"  # "development" | "production"
    debug: bool = True

    # Contact form
    contact_receiver_email: str = "surya.re1208@gmail.com"
    contact_rate_limit_per_hour: int = 5

    # Email notification is optional. Leave this blank and the site still
    # works fully — submissions are safely stored in SQLite either way.
    # See app/services/email_service.py for how the "unconfigured" case
    # is handled without breaking the contact form.
    #
    # Sent via Resend's HTTPS API rather than raw SMTP: most hosting
    # platforms (Render included) either block outbound SMTP ports
    # outright or silently drop that traffic at the network level, which
    # shows up as a connection timeout no client-side code can work
    # around. An HTTPS call on port 443 — the same port every other web
    # request already uses — sidesteps that whole class of problem.
    resend_api_key: str | None = None
    resend_from_email: str = "Portfolio Contact Form <onboarding@resend.dev>"

    @property
    def email_is_configured(self) -> bool:
        return bool(self.resend_api_key)


@lru_cache
def get_settings() -> Settings:
    """
    Cached with lru_cache so the .env file is parsed once per process, not
    once per request. FastAPI's own docs recommend this exact pattern —
    it's why get_settings() is a function and not just a module-level
    `settings = Settings()` (that would also work, but this version is
    trivially overridable in tests via dependency overrides).
    """
    return Settings()
