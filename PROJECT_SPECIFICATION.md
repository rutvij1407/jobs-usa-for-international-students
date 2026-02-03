# F1 International Students — Job & Dashboard Backend — Project Specification

**Version:** 1.0  
**Last updated:** February 1, 2026  
**Purpose:** Backend specification for a website serving F1 international students in the USA (job applications, H1B insights, candidate analysis, and interactive USA heat maps).

---

## 1. Project Overview

The project is a **backend and dashboard platform** for F1 international students in the USA. It focuses on:

- **Data analysis** of job and H1B-related data  
- **Visualizations** and **dashboards** (not just static charts)  
- **Interactive USA heat map** (responsive, hover/click, filters)  
- **Job application mistake analysis** (e.g., LinkedIn redirect issues)  
- **Live/near-daily F1–H1B job market data**  
- **Candidate/resume analysis** with improvement suggestions  

Target users: F1 students who are applying to jobs, tracking H1B outcomes, or improving their resumes.

---

## 2. Dashboard Types & Features

### 2.1 Job Application Mistakes Dashboard

**Audience:** Users who have already applied to jobs (e.g., via LinkedIn) and want to improve their process.

**Goals:**

- Surface **common mistakes** when using LinkedIn (or “GPT–LinkedIn”–style flows) for job search and applications.  
- Highlight **redirect/wrong-page issues**: e.g., LinkedIn sending users to its own “Easy Apply” or generic forms instead of the employer’s actual career page or application URL.  
- Help users understand **what went wrong** and **how to avoid** similar mistakes in future applications.

**Suggested features:**

- List or log of applied jobs with **intended vs actual destination URL** (employer site vs LinkedIn form).  
- Categorization of mistakes (wrong page, duplicate apply, expired posting, etc.).  
- Simple visualizations (e.g., bar/pie charts) of mistake types and frequency.  
- Filters by date range, company, job title, or platform (LinkedIn vs others).  
- Export or summary that users can use to refine their strategy.

**Data:** Comes from user-provided or integrated application history (e.g., manual log, browser extension, or API if available). Backend stores and aggregates this for the dashboard.

---

### 2.2 F1 / H1B Job Market Dataset & “Live” Dashboard

**Audience:** F1 students who want to see **who got jobs**, **H1B sponsorship trends**, and **current job market** conditions.

**Requirements:**

- Dataset should feel **“live” or near-daily** so users can answer: “What is the job market today / this week?”  
- Focus on **F1-relevant employment** and **H1B** (employers, roles, locations, approval/denial trends where available).

**Official data (for H1B):**

- **USCIS H-1B Employer Data Hub**  
  - [https://uscis.gov/tools/reports-and-studies/h-1b-employer-data-hub](https://uscis.gov/tools/reports-and-studies/h-1b-employer-data-hub)  
  - Fiscal year data (e.g., FY 2009–2025), queryable by employer, city, state, zip, NAICS.  
  - **Update frequency:** Quarterly (not daily).  
- **Department of Labor H-1B dataset** (data.gov)  
  - Annual updates.  

**To get a “daily” feel:**

- **Aggregate job-board data** (e.g., scraped or API-sourced job postings) and refresh daily.  
- **Combine** daily job-posting counts/trends with **quarterly H1B data** in the same dashboard (e.g., “Jobs this week” + “H1B employers by state last quarter”).  
- Backend: **scheduled job** (cron/worker) that runs at least once per 24 hours to fetch/process and store new data; dashboards read from this stored dataset so they always show the latest run.

**Dashboard features:**

- Time-series of job postings and/or H1B-related metrics.  
- Breakdowns by state, occupation, industry, company size.  
- Filters: date range, job type, company type, location (see Section 5).  
- Optional: link to official USCIS/DOL sources for transparency.

---

### 2.3 Candidate Analysis Dashboard (Resume Improvement)

**Audience:** F1 students who upload their resume and want **actionable suggestions** to improve it.

**Goals:**

- Parse uploaded resume (PDF/DOCX).  
- Extract: education, experience, skills, contact info.  
- Compare against **job descriptions** or **F1/H1B-friendly** criteria (e.g., keywords, common requirements).  
- Provide **concrete suggestions**: missing keywords, weak sections, formatting tips, ATS-friendly improvements.  
- Present results in a **dashboard** (scores, sections, bullet-list suggestions).

**Tech approach:**

- **Python** for backend: resume parsing (e.g., `pyresparser`, `python-docx`, `PyPDF2`), NLP (e.g., `spaCy`, `NLTK`), optional ML for scoring.  
- **Dashboard:** Streamlit, Dash, or FastAPI + frontend; display scores, sections, and suggestion list.  
- Optional: match resume to a **specific job description** (user pastes JD) for relevance scoring.

---

### 2.4 Interactive USA Heat Map (Job Effectiveness by Region)

**Audience:** Users who want to see **where** in the USA jobs (or H1B activity) are concentrated and drill down by location.

**Requirements:**

- **USA-wide heat map** showing “most effective” or “hottest” regions (e.g., by job count, H1B filings, or application success).  
- **Responsive** and **interactive**:  
  - **Hover:** Show state (or region) name; text can **bold** or stand out on hover.  
  - **Click:** Open a **detail page** for that state/region with a **focused heat map** (same style, but for that location only).  
- **Filters** (apply to both main map and detail view):  
  - Date range  
  - Job type / occupation  
  - Company type / industry  
  - Full-time / part-time / contract  
  - Other filters (see Section 5).  
- **Consistency:** The detail-page heat map should use the **same color scale and style** as the main map so comparisons are clear.

**Tech options:**

- **Plotly (Python):** `plotly.graph_objects.Choropleth` or `plotly.express.choropleth` for USA state-level maps; built-in hover; **Dash** for click callbacks and navigation to state detail page.  
- **Alternative:** Google Maps–based heat map (e.g., HeatmapLayer) for lat/long data; more work for state-level aggregation and hover/click logic.  
- **Recommendation:** Start with **Plotly + Dash** for fast, responsive state-level heat maps and filters; add Google Maps later if you need street-level or custom basemaps.

---

## 3. Recommended Programming Languages & Stack

| Layer              | Recommendation | Notes |
|--------------------|----------------|-------|
| **Backend / logic**| **Python 3.10+** | Data processing, APIs, scheduled jobs, resume parsing, NLP. |
| **Visualization**  | **Plotly**     | Choropleth/heat maps, line/bar charts; interactive hover/click. |
| **Dashboard UI**   | **Dash (Plotly)** or **Streamlit** | Dash: more control, callbacks, multi-page (main map → state detail). Streamlit: faster prototype. |
| **Static charts**  | **Matplotlib** | Reports, exports, or simple static figures if needed. |
| **Maps (advanced)**| **Folium** or **Google Maps API** | Folium for quick Leaflet maps; Google Maps if you need custom basemaps or heat layers. |
| **Data & jobs**    | **Pandas**, **NumPy** | Wrangling and aggregations. |
| **Resume / NLP**   | **spaCy**, **NLTK**, **pyresparser** (or similar) | Parsing and suggestion logic. |
| **API / serving**  | **FastAPI** or **Flask** | If you separate REST API from Dash/Streamlit. |
| **Scheduling**     | **APScheduler** or **Celery** + **Redis** | Daily data refresh. |
| **Database**       | **PostgreSQL** or **SQLite** | Store job logs, H1B cache, user application mistakes, resume analysis results. |

**Summary:** **Python** is the main language; **Plotly + Dash** for interactive heat maps and dashboards; **matplotlib** for static charts; **Google Maps** optional for map layer.

---

## 4. Data Sources Summary

| Data type              | Source | Update frequency | Use in project |
|------------------------|--------|-------------------|----------------|
| H1B employer/petition  | USCIS H-1B Employer Data Hub | Quarterly | H1B dashboard, heat map by state/employer. |
| H1B (DOL)             | data.gov H-1B dataset | Annual | Supplementary H1B analytics. |
| “Daily” job market    | Job board APIs or scraped postings | Daily (your pipeline) | “Live” job trend charts and filters. |
| Application mistakes  | User-submitted or extension data | As submitted | Job application mistakes dashboard. |
| Resume content        | User uploads | Per upload | Candidate analysis dashboard. |

---

## 5. Filters to Support (Maps & Dashboards)

Implement these (or a subset) across the **USA heat map**, **state detail map**, and **job/H1B dashboards** so that “most of the time” users can view all applications, but sometimes restrict by criteria.

**Suggested filters:**

1. **Date range** – From / to (application date, posting date, or H1B fiscal year).  
2. **Job type** – Full-time, part-time, contract, internship.  
3. **Company type** – Startup, enterprise, nonprofit, government.  
4. **Industry / sector** – Technology, healthcare, finance, etc. (align with NAICS or your taxonomy).  
5. **Occupation / role** – Software engineer, data analyst, etc.  
6. **State / region** – For non-map views (e.g., tables).  
7. **H1B sponsorship** – Yes / no / unknown (if your data has it).  
8. **Application source** – LinkedIn, company site, other.  
9. **Mistake type** – For the mistakes dashboard only (wrong page, duplicate, expired, etc.).  
10. **Education level** – For candidate/resume views (e.g., BS, MS, PhD).

Default: **all job applications** (or all data); filters narrow down from there.

---

## 6. Dependencies & Libraries (Basic List)

See **`requirements.txt`** in the project root for pinned versions. Summary:

**Visualization & dashboards**

- `plotly` – Interactive choropleth/heat maps and charts.  
- `dash` – Multi-page dashboards, callbacks, URL routing (e.g., main map → state page).  
- `matplotlib` – Static plots and exports.  
- `kaleido` – Export Plotly figures to images if needed.

**Data & backend**

- `pandas`, `numpy` – Data processing.  
- `requests` – Fetching USCIS/DOL or job-board data.  
- `python-dotenv` – Config and API keys.  
- `apscheduler` – Daily refresh job.

**Resume & NLP**

- `spacy` – NLP and entity extraction.  
- `nltk` – Tokenization, keywords.  
- `PyPDF2` or `pdfplumber` – PDF resume parsing.  
- `python-docx` – DOCX resume parsing.  
- Optional: `pyresparser` or similar for higher-level resume parsing.

**API & serving**

- `fastapi` – REST API if you separate backend from Dash.  
- `uvicorn` – ASGI server.

**Maps (optional)**

- `folium` – Leaflet-based maps.  
- `geopandas` – If you use shapefiles for state boundaries.  
- Google Maps: use JavaScript/API on frontend or `gmaps` in Python for prototyping.

**Database (optional)**

- `sqlalchemy` – ORM for PostgreSQL/SQLite.  
- `psycopg2-binary` – PostgreSQL driver.

---

## 7. File Structure (Suggested)

```
jobs-usa-for-international-students/
├── README.md
├── PROJECT_SPECIFICATION.md    # This document
├── SUMMARY_FOR_GIT.md          # Short summary for repo / Word
├── requirements.txt
├── .env.example
├── config/
│   └── settings.py
├── data/
│   ├── raw/                    # Downloaded H1B, job feeds
│   ├── processed/              # Aggregated tables for dashboards
│   └── geo/                    # GeoJSON / shapefiles for USA
├── jobs/
│   └── daily_refresh.py        # Scheduled data pipeline
├── backend/
│   ├── api/                    # FastAPI routes if used
│   ├── models/
│   ├── services/
│   │   ├── h1b_service.py
│   │   ├── resume_analyzer.py
│   │   └── mistake_aggregator.py
│   └── db/
├── dashboards/
│   ├── app_dash.py             # Dash app entry
│   ├── pages/
│   │   ├── main_map.py         # USA heat map
│   │   ├── state_detail.py     # State-level heat map
│   │   ├── job_mistakes.py
│   │   ├── h1b_market.py
│   │   └── candidate_analysis.py
│   └── components/
│       └── filters.py          # Shared filter UI
├── scripts/
│   └── fetch_h1b_data.py
└── tests/
```

---

## 8. What You Have After This Spec

- **Project specification** (this document): dashboards, data sources, tech stack, filters.  
- **Requirements list** in `requirements.txt` for Python.  
- **Summary for Git** in `SUMMARY_FOR_GIT.md` that you can paste into a Word doc or repo README.  

**Next steps:**

1. Set up repo and virtualenv; install `requirements.txt`.  
2. Implement daily data pipeline (job board + H1B cache).  
3. Build Dash app: main USA heat map → state detail page, with shared filters.  
4. Add job application mistakes ingestion and dashboard.  
5. Add resume upload and candidate analysis dashboard.  
6. Connect all dashboards to the same filter set and date range where applicable.

---

*Document prepared for the F1 International Students Job Dashboard backend project. You can open this .md file in Microsoft Word (File → Open) and save as .docx if you need a Word document for submission or Git.*
