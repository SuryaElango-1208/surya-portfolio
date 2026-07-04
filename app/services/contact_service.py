"""
Business logic for the contact form: persistence + notification.

Kept separate from app/routers/contact.py so this logic is testable without
spinning up FastAPI at all (call handle_submission() with a plain
ContactFormRequest in a unit test, no HTTP involved), and separate from
email_service.py so "how we store a submission" and "how we notify about
it" can change independently — e.g. swapping SQLite for Postgres someday
touches only this file.

Why SQLite over a flat JSON file: concurrent writes. Two people submitting
the contact form at nearly the same moment could interleave writes to a
JSON file and corrupt it. SQLite handles that correctly for free, is
stdlib (no new dependency), and means the submissions are actually
queryable later ("show me everything from the last week") instead of
requiring a hand-written parser.
"""
import logging
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from app.models.contact import ContactFormRequest
from app.services.email_service import send_contact_notification

logger = logging.getLogger("portfolio.contact")

# Lives in storage/, outside app/, and outside git (see .gitignore) — this
# is runtime data, not source code, and shouldn't be versioned or deployed
# alongside the app itself.
DB_PATH = Path(__file__).resolve().parent.parent.parent / "storage" / "contact_submissions.db"


def _get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    return conn


def handle_submission(payload: ContactFormRequest) -> tuple[bool, str]:
    # Honeypot check lives here, not as a Pydantic validator, deliberately.
    # A validator would reject the request with a 422 — which tells a bot
    # exactly which field tripped the trap. Instead we return the same
    # success message a real visitor gets, and just... don't do anything.
    # No signal, nothing to adapt to.
    if payload.website:
        logger.info("Honeypot field was filled — treating as bot, discarding silently.")
        return True, "Thanks for reaching out — I'll get back to you soon."

    conn = _get_connection()
    try:
        conn.execute(
            "INSERT INTO submissions (name, email, message, created_at) VALUES (?, ?, ?, ?)",
            (payload.name, payload.email, payload.message, datetime.now(timezone.utc).isoformat()),
        )
        conn.commit()
    finally:
        conn.close()

    # Email is best-effort and happens AFTER the write above. The message
    # is durably saved before we even try to send an email, so a down SMTP
    # server never costs a lost message — worst case, I check the database
    # instead of my inbox.
    send_contact_notification(payload.name, payload.email, payload.message)

    return True, "Thanks for reaching out — I'll get back to you soon."
