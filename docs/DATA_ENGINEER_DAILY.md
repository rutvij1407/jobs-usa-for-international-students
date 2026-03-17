# Data Engineer — Daily Work Guide

This project is set up so a **data engineer** can track day-by-day work and keep pipelines and dashboards running smoothly.

---

## What a Data Engineer Does Here

1. **Run the daily pipeline**  
   - Command: `python jobs/daily_refresh.py`  
   - Runs: H1B by state, job postings (daily + by state), job application mistakes.  
   - Writes: `data/processed/*.parquet` and `data/processed/pipeline_status.json`.  
   - Run once per day (e.g. cron or scheduler).

2. **Monitor pipeline status**  
   - Open the **Data Engineer** page in the dashboard (`/data-engineer`).  
   - Check: last run time, status, tables updated.  
   - If status is `error`, fix the pipeline and re-run.

3. **Update the day-by-day work log**  
   - Edit: `data/data_engineer_log.json`.  
   - Add or edit entries for each day: `day`, `date`, `tasks_done`, `tasks`, `status`, `notes`.  
   - The Data Engineer page shows a **day-by-day chart** (tasks completed per day) and a **daily log table** from this file.

4. **Keep dashboards working**  
   - USA Map, Job Mistakes, H1B Market, Candidate Analysis should load and filter correctly.  
   - If something breaks, fix the backend service or data loader and re-run the pipeline if needed.

---

## Day-by-Day Log Format

Edit `data/data_engineer_log.json`. Example entry:

```json
{
  "day": 5,
  "date": "2026-02-05",
  "tasks_done": 3,
  "tasks": ["Task A", "Task B", "Task C"],
  "status": "done",
  "notes": "Optional notes for the day"
}
```

- **day**: Day number (1, 2, 3, …).  
- **date**: Date string (YYYY-MM-DD).  
- **tasks_done**: Number of tasks completed (used in the bar chart).  
- **tasks**: List of task descriptions.  
- **status**: e.g. `"done"`, `"planned"`, `"in_progress"`.  
- **notes**: Optional short note.

Add new objects to the `"days"` array to add new days. The **Data Engineer** dashboard will show the updated chart and table after refresh.

---

## Suggested Daily Tasks (You Can Replace These)

- **Daily:** Run `python jobs/daily_refresh.py`; check Data Engineer page for status.  
- **As needed:** Update `data/data_engineer_log.json` with that day’s work.  
- **As needed:** Fix pipeline or dashboard issues; add real data sources (USCIS, job boards) when ready.  
- **As needed:** Add or adjust filters, charts, or new dashboard pages.

---

## Files a Data Engineer Cares About

| File / folder            | Purpose |
|--------------------------|--------|
| `jobs/daily_refresh.py`  | ETL pipeline; run daily. |
| `data/processed/`        | Output parquet files + `pipeline_status.json`. |
| `data/data_engineer_log.json` | Day-by-day log; edit to update chart and table. |
| `backend/data_loader.py` | Loads processed data (and synthetic fallback). |
| `backend/services/`      | Analytics (H1B, mistakes, resume, pipeline status). |
| `config/settings.py`     | Paths, file names, filter options. |

Everything is set up so you can keep the code working and reflect your daily work in the **Data Engineer** page.
