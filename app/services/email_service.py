"""
Thin wrapper around smtplib.

Why a dedicated service instead of calling smtplib straight from the route?
If this ever moves from raw SMTP to a transactional email API (SendGrid,
Resend, SES), this is the only file that changes. Routers and
contact_service.py don't know or care how email is actually sent — they
just call send_contact_notification().

This module never raises. A broken SMTP config should degrade the contact
form to "still saves your message, just doesn't email me about it" — not
break it entirely. That's why the submission is persisted in
contact_service.py BEFORE this is ever called.
"""
import logging
import smtplib
from email.message import EmailMessage

from app.core.config import get_settings

logger = logging.getLogger("portfolio.email")


def send_contact_notification(name: str, email: str, message: str) -> bool:
    """Best-effort send. Returns True if sent, False otherwise — callers
    that don't care can ignore the return value entirely."""
    settings = get_settings()

    if not settings.email_is_configured:
        logger.info("SMTP not configured — submission was saved, skipping email.")
        return False

    msg = EmailMessage()
    msg["Subject"] = f"Portfolio contact form: {name}"
    msg["From"] = settings.smtp_username
    msg["To"] = settings.contact_receiver_email
    msg["Reply-To"] = email
    msg.set_content(f"From: {name} <{email}>\n\n{message}")

    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=10) as server:
            if settings.smtp_use_tls:
                server.starttls()
            server.login(settings.smtp_username, settings.smtp_password)
            server.send_message(msg)
        return True
    except Exception:
        # Intentionally broad: any SMTP failure (auth, network, timeout)
        # should result in "log it and move on," never a 500 for the
        # visitor who was just trying to say hello.
        logger.exception("Failed to send contact notification email.")
        return False
