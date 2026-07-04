"""
Application entrypoint.

This file does composition ONLY — mount static files, wire up routers,
configure logging — and contains zero business logic. That's deliberate:
anyone opening this file for the first time should be able to see the
entire shape of the app in about ten seconds, then go find the layer they
actually need to change.

Run with:  uvicorn app.main:app --reload
"""
import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.core.config import get_settings
from app.routers import contact, pages, resume

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
)

settings = get_settings()

app = FastAPI(title=settings.app_name, debug=settings.debug)

# Everything under app/static/ becomes reachable at /static/... .
# The resume PDF is intentionally NOT in here — see app/routers/resume.py.
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(pages.router)
app.include_router(contact.router)
app.include_router(resume.router)
