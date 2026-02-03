# F1 International Students — Job & Dashboard Backend

Backend and dashboard platform for F1 international students in the USA: job application mistakes, F1/H1B job market data, candidate (resume) analysis, and an interactive USA heat map.

---

## Quick Start

```bash
# From project root
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Generate sample data (optional; app uses synthetic data if missing)
python3 jobs/daily_refresh.py

# Run the Dash dashboard
python3 run.py
```

Then open **http://127.0.0.1:8050** in your browser.

**Push to a new GitHub repo:** See [PUSH_INSTRUCTIONS.md](PUSH_INSTRUCTIONS.md) for step-by-step (create repo on GitHub, then `git remote add origin ...` and `git push -u origin main`).

---

## Contents of This Repo

| File | Purpose |
|------|--------|
| **PROJECT_SPECIFICATION.md** | Full project spec: dashboards, data sources, tech stack, filters, file structure. **Open in Word** (File → Open) and **Save As .docx** to get a Word document. |
| **SUMMARY_FOR_GIT.md** | Short summary and “what was done” for README or Word; includes one-paragraph summary you can paste into Git. |
| **requirements.txt** | Python dependencies: Plotly, Dash, matplotlib, pandas, spaCy, NLTK, FastAPI, etc. |
| **README.md** | This file. |

---

## Getting a Word Document

1. Open **PROJECT_SPECIFICATION.md** in **Microsoft Word** (File → Open → choose the file).  
2. Use **File → Save As** and choose **Word Document (.docx)**.  
3. Optionally paste in content from **SUMMARY_FOR_GIT.md** (e.g., “What was done” and “One-Paragraph Summary”) into the same Word doc before saving.

---

## Quick Summary (for Git or Word)

- **Four dashboards:** Job application mistakes (LinkedIn redirects/wrong pages), F1/H1B job market (daily pipeline + USCIS/DOL), candidate analysis (resume upload + suggestions), interactive USA heat map (hover = state name, click = state detail, same style + filters).  
- **Tech:** Python, Plotly, Dash, matplotlib; optional Google Maps; resume parsing with spaCy, NLTK, PyPDF2, python-docx.  
- **Data:** USCIS H-1B Employer Data Hub (quarterly), DOL H-1B (annual), daily job-posting aggregation for “live” feel.  
- **Filters:** Date range, job type, company type, industry, occupation, state, H1B sponsorship, application source, mistake type, education level.

See **PROJECT_SPECIFICATION.md** and **SUMMARY_FOR_GIT.md** for full details.
