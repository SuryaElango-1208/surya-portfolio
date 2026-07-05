"""
Thin wrapper around Resend's HTTPS email API.

Why an HTTP API instead of raw SMTP? Most hosting platforms — Render
included — either block outbound SMTP ports outright (a common anti-spam
measure) or have inconsistent outbound routing for it, which shows up as
a silent connection timeout that no client-side code can fix. Outbound
HTTPS on port 443, by contrast, is essentially always available — it's
the same port every other web request the platform itself makes uses —
so a REST API call sidesteps that whole class of problem entirely.

Why a dedicated service instead of calling the API straight from the
route? If this ever moves to a different provider (SendGrid, Postmark,
SES), this is the only file that changes. Routers and contact_service.py
don't know or care how email is actually sent — they just call
send_contact_notification().

This module never raises. A broken email config should degrade the
contact form to "still saves your message, just doesn't email me about
it" — not break it entirely. That's why the submission is persisted in
contact_service.py BEFORE this is ever called.

Uses urllib from the standard library rather than adding a requests/httpx
dependency or the resend SDK — a single POST request doesn't need either.
"""
import json
import logging
import urllib.error
import urllib.request

from app.core.config import get_settings

logger = logging.getLogger("portfolio.email")

RESEND_API_URL = "https://api.resend.com/emails"


def send_contact_notification(name: str, email: str, message: str) -> bool:
    """Best-effort send. Returns True if sent, False otherwise — callers
    that don't care can ignore the return value entirely."""
    settings = get_settings()

    if not settings.email_is_configured:
        logger.info("Email not configured (no RESEND_API_KEY) — submission was saved, skipping email.")
        return False

    payload = {
        "from": settings.resend_from_email,
        "to": [settings.contact_receiver_email],
        "reply_to": email,
        "subject": f"Portfolio contact form: {name}",
        "text": f"From: {name} <{email}>\n\n{message}",
    }

    request = urllib.request.Request(
        RESEND_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {settings.resend_api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            # api.resend.com sits behind Cloudflare, which commonly
            # blanket-blocks urllib's default User-Agent string
            # ("Python-urllib/3.x") as a bot signature — that block
            # happens at Cloudflare's edge, before the request ever
            # reaches Resend's own servers, and shows up as HTTP 403
            # with a bare "error code: 1010" body (a Cloudflare error
            # code, not a Resend API error). Any non-default, identifiable
            # User-Agent avoids the blanket rule.
            "User-Agent": "surya-portfolio-contact-form/1.0",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return 200 <= response.status < 300
    except urllib.error.HTTPError as exc:
        # Resend puts the actual reason (bad API key, unverified sender,
        # sandbox recipient restriction, etc.) in the JSON response body,
        # not in the exception's own message. Logging just the exception
        # gives you "HTTP Error 403: Forbidden" and nothing else useful —
        # logging the body gives you the real, specific reason.
        try:
            body = exc.read().decode("utf-8", errors="replace")
        except Exception:
            body = "<could not read response body>"
        logger.error("Resend rejected the email — HTTP %s: %s", exc.code, body)
        return False
    except Exception:
        # Intentionally broad: any other failure (network, timeout,
        # provider outage) should result in "log it and move on," never a
        # 500 for the visitor who was just trying to say hello.
        logger.exception("Failed to send contact notification email via Resend.")
        return False
