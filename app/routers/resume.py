"""
GET /api/resume/download

The PDF lives in app/assets/resume/ — deliberately outside app/static/, so
it isn't reachable directly through the StaticFiles mount. Every download
has to go through this endpoint instead, which means every download can be
logged. For a portfolio, "someone downloaded the resume" is a much stronger
interest signal than a page view, so that's a real feature, not just
extra plumbing.
"""
import logging
from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter(prefix="/api/resume", tags=["resume"])
logger = logging.getLogger("portfolio.resume")

RESUME_PATH = Path(__file__).resolve().parent.parent / "assets" / "resume" / "Surya_Elango_Resume.pdf"


@router.get("/download")
def download_resume():
    logger.info("Resume downloaded.")
    return FileResponse(
        path=RESUME_PATH,
        media_type="application/pdf",
        filename="Surya_Elango_Resume.pdf",
    )
