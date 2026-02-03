# Summary for Git / Word Document

**Project:** F1 International Students — Job & Dashboard Backend  
**Date:** February 1, 2026  

---

## What This Project Is

Backend and dashboard platform for **F1 international students** in the USA. It provides:

1. **Job application mistakes dashboard** — Tracks mistakes when applying via LinkedIn (e.g., redirects to LinkedIn’s own forms instead of the employer’s career page). Helps users see what went wrong and how to improve.
2. **F1/H1B job market dashboard** — Uses official H1B data (USCIS, DOL) plus daily job-posting data to show who got jobs, sponsorship trends, and “live” job market feel. Data pipeline runs daily for near–real-time trends.
3. **Candidate analysis dashboard** — Users upload resumes; backend parses and suggests improvements (keywords, sections, ATS-friendly tips) with a simple dashboard.
4. **Interactive USA heat map** — Shows most effective job regions across the USA. Hover shows state name (bold on hover); click opens a detail page with the same heat map style for that state. Filters (date, job type, company type, etc.) apply to both main map and detail view.

---

## What Was Done (Specification Phase)

- **Project specification document** (`PROJECT_SPECIFICATION.md`):  
  - Defined all four dashboard types (job mistakes, F1/H1B market, candidate analysis, USA heat map).  
  - Described data sources: USCIS H-1B Employer Data Hub (quarterly), DOL H-1B (annual), daily job-board aggregation for “live” feel.  
  - Specified interactive map behavior: hover (state name, bold), click (state detail page), same heat map style and filters on both views.  
  - Listed recommended tech stack: **Python**, **Plotly**, **Dash**, **matplotlib**, optional **Google Maps**; resume/NLP with **spaCy**, **NLTK**, **PyPDF2**, **python-docx**.  
  - Defined a shared **filter set**: date range, job type, company type, industry, occupation, state, H1B sponsorship, application source, mistake type, education level.  
- **Requirements list** (`requirements.txt`):  
  - Plotly, Dash, matplotlib, kaleido; pandas, numpy; requests, python-dotenv; apscheduler; spaCy, NLTK, PyPDF2, pdfplumber, python-docx; FastAPI, uvicorn; folium, geopandas; SQLAlchemy, psycopg2-binary.  
- **Git-ready summary** (this file): Short overview and “what was done” for README or Word.

---

## One-Paragraph Summary (Copy-Paste for Word or README)

This repository contains the backend specification and dependency list for an F1 international students job dashboard. The platform includes four main components: (1) a job application mistakes dashboard that surfaces LinkedIn redirect and wrong-page issues and suggests improvements; (2) an F1/H1B job market dashboard fed by USCIS and DOL data plus a daily job-posting pipeline for near–real-time trends; (3) a candidate analysis dashboard where users upload resumes and receive parsing and improvement suggestions; and (4) an interactive USA heat map (Plotly/Dash) showing job-effective regions with hover-to-state-name, click-to-state-detail, and shared filters (date, job type, company type, etc.). The stack is Python with Plotly, Dash, matplotlib, and optional Google Maps; resume analysis uses spaCy, NLTK, and PDF/DOCX parsing. All deliverables are documented in PROJECT_SPECIFICATION.md, with dependencies in requirements.txt and this summary for Git or Word.

---

*You can copy the above sections into a Word document or use them as the README for your Git repository.*
