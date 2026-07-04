"""
Pydantic models for the contact form.

Request and response are separate classes on purpose. It's tempting to
reuse one model for both directions, but that couples "what the client is
allowed to send" to "what we're allowed to send back" — and the moment you
add an internal field (a database id, a spam score, an IP address) to the
request model for bookkeeping, you risk it leaking straight back out in the
response. Two small classes cost nothing and remove that failure mode.

Email is validated for syntax only (via EmailStr) — deliberately not
DNS/MX-checked. A DNS-deliverability check would reject real company or
HR addresses on nothing more than a transient DNS timeout, and it can't
tell a live company domain from a dead one any more reliably than that.
Typo-catching is handled instead as a non-blocking suggestion in the
frontend (see contactForm.js) — "did you mean gmail.com?" rather than a
hard rejection.
"""
from pydantic import BaseModel, EmailStr, Field


class ContactFormRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    message: str = Field(default="", max_length=2000)

    # Honeypot field: a real visitor never sees or fills this in (it's
    # hidden via CSS, not `type="hidden"`, since some bots specifically
    # skip hidden inputs). Simple bots that auto-fill every field in a form
    # populate it. Deliberately NOT validated/rejected here — see
    # contact_service.py for why we accept it silently instead of erroring.
    website: str = ""


class ContactFormResponse(BaseModel):
    success: bool
    message: str
