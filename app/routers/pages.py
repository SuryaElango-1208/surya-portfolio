"""
GET /

Renders the single-page site. Every list-driven section (experience,
highlights, skills, certifications, the architecture diagram) gets its
content from app/data/resume_data.py — this route's only job is handing
that data to the template. Updating a bullet point, adding a certification,
or fixing a typo should never require touching HTML.
"""
from datetime import datetime

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.data import resume_data

router = APIRouter(tags=["pages"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "profile": resume_data.PROFILE,
            "about": resume_data.ABOUT,
            "experience": resume_data.EXPERIENCE,
            "highlights": resume_data.HIGHLIGHTS,
            "architecture_nodes": resume_data.ARCHITECTURE_NODES,
            "skills": resume_data.SKILLS,
            "certifications": resume_data.CERTIFICATIONS,
            "achievement": resume_data.ACHIEVEMENT,
            "current_year": datetime.now().year,
        },
    )
