"""
Daily data refresh pipeline: writes processed H1B and job-postings data.
In production, replace synthetic generation with real API/scrape calls.
"""
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta

# Add project root to path
import sys
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import (
    PROCESSED_DIR,
    USA_STATES,
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


def run_full_refresh():
    """Run all refresh steps (call from cron/APScheduler daily)."""
    refresh_h1b_by_state()
    refresh_job_postings()
    refresh_mistakes()
    print(f"[{datetime.now().isoformat()}] Daily refresh completed.")


if __name__ == "__main__":
    run_full_refresh()
