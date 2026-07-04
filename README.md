# Surya Elango — Portfolio

A single-page portfolio built with **FastAPI + Jinja2** on the backend and
**hand-written HTML/CSS/vanilla JS** on the frontend — no React, no
templates, no page builder. Every fact on the page is sourced from
`app/data/resume_data.py`, which mirrors the resume itself.

## Running it locally

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Then open **http://localhost:8000**.

The contact form works out of the box — submissions are saved to
`storage/contact_submissions.db` (SQLite) even with a completely empty
`.env`. To also get an email when someone submits it, fill in the `SMTP_*`
values in `.env` (a Gmail App Password works fine for `SMTP_HOST=smtp.gmail.com`,
`SMTP_PORT=587`).

## Project structure

```
app/
├── main.py                  composition root — mounts static, includes routers
├── core/config.py           typed settings (pydantic-settings)
├── data/resume_data.py      single source of truth: resume as Python data
├── models/contact.py        Pydantic request/response schemas
├── services/
│   ├── contact_service.py   persistence (SQLite) + honeypot handling
│   └── email_service.py     SMTP wrapper, safe no-op if unconfigured
├── routers/
│   ├── pages.py             GET /            → renders the site
│   ├── contact.py           POST /api/contact
│   └── resume.py            GET /api/resume/download
├── assets/resume/           resume PDF (outside /static — see resume.py)
├── templates/
│   ├── index.html           shell that includes every partial below
│   └── partials/            one file per section (hero, about, experience...)
└── static/
    ├── css/                 tokens → base → layout → components → sections/*
    └── js/                  main.js + one module per concern

storage/                     runtime SQLite db, created on first submission, gitignored
```

## Design system

| Token | Value | Role |
|---|---|---|
| Void | `#08080c` | background |
| Elevated | `#131318` | cards/surfaces |
| Vapor | `#f2f1ed` | primary text |
| Ash | `#8e8e96` | secondary text |
| Signal | `#e0a458` | the one accent |

Type: **Fraunces** (display, used sparingly), **IBM Plex Sans** (body),
**IBM Plex Mono** (tags, dates, the status badge).

The recurring visual idea is a connected-nodes motif — ambient in the Hero
background, literal and interactive in the Architecture Showcase — because
the actual throughline of the work it's describing is making separate
systems (SAP, Windows, Linux) talk to each other.

## Notable implementation decisions

- **Resume as code, not markup.** Every experience bullet, skill, and
  architecture-node description lives in `resume_data.py`. Templates only
  loop over it. Updating content never means touching HTML.
- **Contact form honeypot is checked in the service layer, not as a
  Pydantic validator** — a validator would return a 422 that tells a bot
  exactly which field it tripped. The service silently accepts-and-discards
  instead, returning the same success message a real visitor gets.
- **The resume PDF is served through an API route, not `/static`** — it
  physically lives in `app/assets/`, outside the static mount, so every
  download is forced through `/api/resume/download` and can be logged.
  "Resume downloaded" is a much stronger recruiter-interest signal than a
  page view.
- **The contact route is a plain `def`, not `async def`** — it does
  blocking I/O (SQLite, potentially SMTP). FastAPI runs sync routes in a
  thread pool automatically; mixing blocking calls into an `async def`
  route would stall the whole event loop, not just that request.
- **Rate limiting is a small in-memory dict**, intentionally not backed by
  Redis or similar — correct for a single-process deployment, and called
  out in a comment as the thing that would need to change behind multiple
  workers.
- **No React.** This is a content-forward scrolling page, not a stateful
  app — no client routing, no cross-component state. Vanilla JS keeps the
  payload small and avoids bolting a JS build toolchain onto a Python
  backend for no real capability gain.

## What's still worth adding

- Automated tests for `contact_service.handle_submission()` (it's written
  to be testable without FastAPI running at all — that was the point of
  the service-layer split).
- A `robots.txt` / `sitemap.xml` pass once this has a real deployed URL.
- Swapping the in-memory rate limiter for Redis if this ever runs behind
  more than one worker process.
