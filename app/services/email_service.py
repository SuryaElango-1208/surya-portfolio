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
import socket
from contextlib import contextmanager
from email.message import EmailMessage

from app.core.config import get_settings

logger = logging.getLogger("portfolio.email")


@contextmanager
def _force_ipv4_dns():
    """Some hosts (Render's containers, notably) have no outbound IPv6
    route, but DNS lookups for mail providers like Gmail can still return
    an IPv6 (AAAA) address alongside the IPv4 one. smtplib just connects
    to whatever socket.getaddrinfo() hands back first — if that's the
    IPv6 address, the connection dies immediately with "Network is
    unreachable" before ever trying the IPv4 address that would have
    worked fine. This temporarily restricts DNS resolution to IPv4 only,
    for the duration of the SMTP connection, then restores the normal
    resolver so nothing else in the process is affected."""
    original_getaddrinfo = socket.getaddrinfo

    def ipv4_only_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
        return original_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)

    socket.getaddrinfo = ipv4_only_getaddrinfo
    try:
        yield
    finally:
        socket.getaddrinfo = original_getaddrinfo


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
        with _force_ipv4_dns(), smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=10) as server:
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
