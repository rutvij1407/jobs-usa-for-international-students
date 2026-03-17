"""
Daily data refresh pipeline (ETL): writes processed H1B and job-postings data.
Data engineer responsibilities: run daily (cron/scheduler), monitor via Data Engineer dashboard.
In production, replace synthetic generation with real API/scrape calls.
"""
import json
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta, timezone

# Add project root to path
import sys
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import (
    PROCESSED_DIR,
    PIPELINE_STATUS_FILE,
    H1B_STATE_AGGREGATE,
    JOB_POSTINGS_DAILY,
    JOB_POSTINGS_BY_STATE,
    MISTAKES_AGGREGATE,
    MISTAKES_BY_TYPE,
)
from backend.data_loader import (
    _synthetic_h1b_by_state,
    _synthetic_job_postings_by_state,
    _synthetic_job_postings_daily,
    _synthetic_mistakes,
)


def refresh_h1b_by_state():
    """Fetch/refresh H1B by state. Here we (re)generate synthetic; replace with USCIS fetch."""
    df = _synthetic_h1b_by_state()
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df.to_parquet(H1B_STATE_AGGREGATE, index=False)
    return df


def refresh_job_postings():
    """Refresh daily job postings and by-state aggregates. Replace with job-board API."""
    daily = _synthetic_job_postings_daily()
    by_state = _synthetic_job_postings_by_state()
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    daily.to_parquet(JOB_POSTINGS_DAILY, index=False)
    by_state.to_parquet(JOB_POSTINGS_BY_STATE, index=False)
    return daily, by_state


def refresh_mistakes():
    """Refresh job application mistakes. In production, load from DB or user submissions."""
    df = _synthetic_mistakes()
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df.to_parquet(MISTAKES_AGGREGATE, index=False)
    by_type = df.groupby("mistake_type", as_index=False).agg(count=("id", "count"))
    by_type.to_parquet(MISTAKES_BY_TYPE, index=False)
    return df


def _write_pipeline_status(status: str, tables_updated: list, message: str = "OK"):
    """Write pipeline status for Data Engineer dashboard."""
    now = datetime.now(timezone.utc)
    payload = {
        "last_run_ts": now.timestamp(),
        "last_run_iso": now.isoformat() + "Z",
        "status": status,
        "tables_updated": tables_updated,
        "message": message,
    }
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    PIPELINE_STATUS_FILE.write_text(json.dumps(payload, indent=2))


def run_full_refresh():
    """Run all refresh steps (call from cron/APScheduler daily). Data engineer: run this daily."""
    tables_updated = []
    try:
        refresh_h1b_by_state()
        tables_updated.append("h1b_by_state")
        daily, by_state = refresh_job_postings()
        tables_updated.extend(["job_postings_daily", "job_postings_by_state"])
        refresh_mistakes()
        tables_updated.extend(["job_application_mistakes", "mistakes_by_type"])
        _write_pipeline_status("success", tables_updated)
        print(f"[{datetime.now().isoformat()}] Daily refresh completed. Tables: {tables_updated}")
    except Exception as e:
        _write_pipeline_status("error", [], message=str(e))
        raise


if __name__ == "__main__":
    run_full_refresh()
