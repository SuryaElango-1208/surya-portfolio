"""
Structured, resume-derived content.

This module is the single source of truth for every fact the site displays.
It mirrors, at the code level, the same instruction the site itself was
built under: the resume is the one place facts live. Update a bullet point
here, once, and every card, list, and section that renders it updates with
it. No experience bullet, skill, certification, or diagram label is
hardcoded into HTML anywhere in this project.

Every string below is traceable to a specific line in Surya's resume —
reworded or reframed for a portfolio's voice, never invented.
"""

PROFILE = {
    "name": "Surya Elango",
    "title": "Python Developer",
    "tagline": "Automation & Backend Systems",
    "status_badge": "Currently building at Accenture",
    "intro": (
        "I write Python that keeps enterprise systems talking to each other "
        "— SAP, Windows, Linux — so people don't have to do it by hand."
    ),
    "email": "surya.re1208@gmail.com",
    "phone": "+91 6382274185",
    "linkedin_url": "https://linkedin.com/in/surya-elango",
    "linkedin_display": "linkedin.com/in/surya-elango",
    "github_url": "https://github.com/SuryaElango-1208",
    "github_display": "github.com/SuryaElango-1208",
    "resume_download_url": "/api/resume/download",
}

ABOUT = {
    "paragraphs": [
        (
            "My degree is in Electronics and Communication Engineering, not "
            "Computer Science — but the more time I spent around systems, "
            "the more I gravitated toward the code deciding how they "
            "actually behave. That's where I ended up: writing Python that "
            "sits between SAP, Windows, and Linux, and makes them cooperate."
        ),
        (
            "Most of what I build is invisible by design. If a piece of "
            "automation is working, nobody notices it — the manual process "
            "it replaced just quietly stops happening. I like that kind of "
            "work. It rewards being careful: solid error handling, clean "
            "logging, code that fails loudly in a log file instead of "
            "silently in production."
        ),
        (
            "I'm still deliberately curious about the edges of the "
            "toolkit — prompt engineering, agentic AI, whatever changes how "
            "software gets built next — but the core of how I work hasn't "
            "changed: find the manual, repetitive, error-prone part of a "
            "process, and make it something a machine can do reliably "
            "instead."
        ),
    ],
}

EXPERIENCE = [
    {
        "id": "accenture",
        "role": "Packaged App Development Analyst — Python Developer",
        "company": "Accenture",
        "period": "Feb 2024 – Present",
        "period_start": "2024",
        "summary": (
            "Building the Python layer that lets client teams automate SAP "
            "and OS administration instead of doing it by hand — and "
            "giving them a safe way to trigger it themselves."
        ),
        "problem": (
            "SAP and OS administration processes were manual and repetitive, "
            "spread across SAP, Windows, and Linux, and consuming real "
            "staff time on every client engagement."
        ),
        "solution": [
            "Built a Python-based automation tool for SAP and OS system administration processes.",
            "Developed cross-platform automation scripts integrating SAP (PyRFC), Windows (WinRM), and Linux (SSH).",
            "Designed and built a secure FastAPI web application so clients can trigger automation themselves inside restricted environments.",
            "Engineered Python scripts to dynamically invoke ABAP functions and manage SAP process flows via RFC calls and API interactions.",
            "Applied OOP and DSA principles to keep automation components modular and easy to maintain.",
            "Used regex, comprehensions, subprocess, and threading for data extraction, validation, and workflow automation.",
            "Debugged and enhanced existing modules for smooth integration with a .NET-based user interface.",
        ],
        "tech": ["Python", "FastAPI", "SAP PyRFC", "WinRM", "SSH", "ABAP Integration", "OOP", "DSA", "Threading"],
        "impact": [
            "Reduced manual workload equivalent to 10–15 staff per client, across 40+ client projects.",
            "Cut process time by 30% through cross-platform automation.",
            "Improved reliability of SAP workflows and reduced error rates.",
        ],
        "extra": "Acted as primary point of contact for the Python team during lead absences.",
    },
    {
        "id": "urjanet",
        "role": "Data Analyst — Intern",
        "company": "Urjanet",
        "period": "June 2022 – November 2022",
        "period_start": "2022",
        "summary": (
            "Kept automated data pipelines healthy and chased down data "
            "issues before they became customer-facing problems."
        ),
        "problem": (
            "Automated data pipelines needed ongoing maintenance, and "
            "customers were reporting data discrepancies that needed "
            "investigating and resolving."
        ),
        "solution": [
            "Supported the maintenance and optimization of automated data pipelines.",
            "Researched and resolved data issues and customer-reported discrepancies.",
        ],
        "tech": ["Automated Data Pipelines", "Data Quality & Issue Resolution"],
        "impact": [
            "Improved efficiency and reliability of data flow.",
            "Ensured accurate processing and timely resolution of reported issues.",
        ],
        "extra": None,
    },
]

HIGHLIGHTS = [
    {
        "id": "automation-platform",
        "title": "Python Automation Platform",
        "problem": "Manual SAP and OS administration was consuming significant staff time across every client engagement.",
        "solution": "A modular Python automation tool, built on OOP and DSA principles so components stay maintainable as the platform grows.",
        "tech": ["Python", "OOP", "DSA", "Error Handling & Logging"],
        "outcome": "Manual workload cut by the equivalent of 10–15 staff per client, across 40+ client projects.",
    },
    {
        "id": "fastapi-app",
        "title": "FastAPI Enterprise Application",
        "problem": "Clients needed to trigger automation themselves, but their environments were security-restricted.",
        "solution": "A secure FastAPI web application exposing automation as controlled, authenticated endpoints instead of raw system access.",
        "tech": ["FastAPI", "Python", "Secure Web Design"],
        "outcome": "Simplified client access while meeting enterprise security requirements.",
    },
    {
        "id": "sap-integration",
        "title": "SAP Integration",
        "problem": "SAP workflows needed reliable programmatic control from outside SAP's native tooling.",
        "solution": "Python scripts using PyRFC to dynamically invoke ABAP functions and manage SAP process flows via RFC calls and API interactions.",
        "tech": ["SAP PyRFC", "ABAP Integration", "RFC Calls"],
        "outcome": "Improved reliability of SAP workflows.",
    },
    {
        "id": "cross-platform",
        "title": "Cross-Platform Automation",
        "problem": "Automation needed to span SAP, Windows, and Linux in a single coordinated flow, not three separate ones.",
        "solution": "Cross-platform scripts unifying SAP (PyRFC), Windows (WinRM), and Linux (SSH) into one automated execution path.",
        "tech": ["PyRFC", "WinRM", "SSH"],
        "outcome": "Cut end-to-end process time by 30%.",
    },
]

# Powers the interactive Architecture Showcase. Order matters: it's the
# actual request path, top to bottom.
ARCHITECTURE_NODES = [
    {
        "id": "client",
        "layer": "01",
        "label": "Client Interface",
        "short": "Browser-based entry point",
        "purpose": (
            "Where a client user starts an automation run — no direct "
            "access to SAP, Windows, or Linux required."
        ),
        "communicates_via": "HTTPS requests to the FastAPI layer",
        "why": (
            "Client environments were security-restricted, so the entry "
            "point had to be something controlled and web-based rather "
            "than direct system access."
        ),
    },
    {
        "id": "fastapi",
        "layer": "02",
        "label": "FastAPI",
        "short": "Secure web & API layer",
        "purpose": (
            "Authenticates requests, validates input, and exposes "
            "automation as callable, controlled endpoints."
        ),
        "communicates_via": "REST endpoints; invokes the automation engine directly in-process",
        "why": (
            "FastAPI's async support and Pydantic-based request validation "
            "suit a security-conscious internal tool where malformed input "
            "should fail fast, before it reaches SAP or a live server."
        ),
    },
    {
        "id": "engine",
        "layer": "03",
        "label": "Python Automation Engine",
        "short": "Core orchestration layer",
        "purpose": (
            "Houses the modular, OOP-based automation components and "
            "routes each job to the right downstream system."
        ),
        "communicates_via": "PyRFC to SAP, WinRM to Windows, SSH to Linux",
        "why": (
            "A modular design keeps 40+ client projects maintainable from "
            "one codebase, instead of forking logic per client."
        ),
    },
    {
        "id": "sap",
        "layer": "04",
        "label": "SAP",
        "short": "via PyRFC",
        "purpose": "Dynamically invokes ABAP functions and manages SAP process flows.",
        "communicates_via": "RFC (Remote Function Call) protocol, via the PyRFC library",
        "why": "PyRFC is the standard bridge between Python and SAP's native RFC interface.",
    },
    {
        "id": "windows",
        "layer": "04",
        "label": "Windows",
        "short": "via WinRM",
        "purpose": "Remote administration of Windows-based systems as part of OS-level automation.",
        "communicates_via": "WinRM (Windows Remote Management)",
        "why": "WinRM is Microsoft's protocol for secure, scripted remote administration — no manual console access needed.",
    },
    {
        "id": "linux",
        "layer": "04",
        "label": "Linux",
        "short": "via SSH",
        "purpose": "Remote administration of Linux-based systems.",
        "communicates_via": "SSH",
        "why": "SSH is the standard secure channel for scripted Linux administration, mirroring the Windows approach for one unified strategy.",
    },
]

SKILLS = {
    "Programming": ["Python", "Java", "SQL", "Shell Scripting (Linux/Windows)"],
    "Backend": ["FastAPI", "HTML", "CSS", "JavaScript"],
    "Automation": ["WinRM", "SSH", "Automation Framework Design"],
    "Integration": ["SAP PyRFC", "ABAP Integration"],
    "AI & Emerging Tech": ["Prompt Engineering", "Agentic AI", "AI-Assisted Development"],
    "Libraries": ["pandas", "NumPy", "JSON", "regex", "subprocess"],
    "Concepts": ["Object-Oriented Programming", "Data Structures & Algorithms", "Error Handling & Logging"],
    "Tools": ["Git", "GitHub", "Azure DevOps"],
    "Strengths": ["Debugging", "Analytical Thinking", "Problem Solving", "Process Optimization"],
}

CERTIFICATIONS = [
    {"name": "Reinvention with Agentic AI Learning Program", "issuer": "Accenture", "year": "2026"},
    {"name": "SQL (Intermediate)", "issuer": "HackerRank", "year": None},
    {"name": "Oracle Cloud Infrastructure 2024 AI Certified Foundations Associate", "issuer": "Oracle", "year": "2024"},
    {"name": "Data Science using Python", "issuer": "Verzeo", "year": None},
]

ACHIEVEMENT = {
    "title": "ASE Best Cadet Award",
    "issuer": "Accenture",
    "year": "2025",
    "description": (
        "Recognized as a top-performing Associate Software Engineer (ASE) "
        "cadet for technical excellence, ownership, and project "
        "contributions."
    ),
    "why_it_matters": (
        "This wasn't awarded for one project — it's a peer-and-manager "
        "signal, across a full cadet cohort, that the way I work (ownership, "
        "technical depth, follow-through) stood out consistently, not just once."
    ),
}
