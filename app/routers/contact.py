"""
POST /api/contact

Note this is a plain `def`, not `async def`. The handler does blocking I/O
— a SQLite write, and potentially a synchronous SMTP call inside the
service layer. FastAPI automatically runs sync route functions in a thread
pool, so this doesn't block the event loop. Mixing blocking calls inside an
`async def` route is a genuinely common mistake: it doesn't just slow down
that one request, it stalls every other request the single-threaded event
loop is trying to handle at the same time.
"""
import time
from collections import defaultdict

from fastapi import APIRouter, HTTPException, Request

from app.core.config import get_settings
from app.models.contact import ContactFormRequest, ContactFormResponse
from app.services.contact_service import handle_submission

router = APIRouter(prefix="/api/contact", tags=["contact"])

# A very small in-memory rate limiter: {ip: [timestamps]}. Good enough for
# a single-process portfolio deployment. It would NOT be good enough behind
# multiple worker processes or instances, since each would keep its own
# separate counts — that's what a shared store like Redis is for in a real
# production deployment.
_submission_log: dict[str, list[float]] = defaultdict(list)


def _is_rate_limited(ip: str, limit_per_hour: int) -> bool:
    now = time.time()
    window_start = now - 3600
    _submission_log[ip] = [t for t in _submission_log[ip] if t > window_start]
    if len(_submission_log[ip]) >= limit_per_hour:
        return True
    _submission_log[ip].append(now)
    return False


@router.post("", response_model=ContactFormResponse)
def submit_contact_form(payload: ContactFormRequest, request: Request):
    settings = get_settings()
    # request.client.host is fine for local dev / a single-instance deploy.
    # Behind a reverse proxy (nginx, a load balancer) this would need to
    # read the X-Forwarded-For header instead, since request.client.host
    # would just be the proxy's own address for every request.
    client_ip = request.client.host if request.client else "unknown"

    if _is_rate_limited(client_ip, settings.contact_rate_limit_per_hour):
        raise HTTPException(status_code=429, detail="Too many submissions — please try again in a bit.")

    success, message = handle_submission(payload)
    return ContactFormResponse(success=success, message=message)
