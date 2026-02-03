"""
Load processed data for dashboards. Falls back to synthetic data if files missing.
"""
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
from config.settings import (
    PROCESSED_DIR,
    H1B_STATE_AGGREGATE,
    JOB_POSTINGS_BY_STATE,
    JOB_POSTINGS_DAILY,
    MISTAKES_AGGREGATE,
    MISTAKES_BY_TYPE,
    USA_STATES,
    JOB_TYPES,
    COMPANY_TYPES,
    INDUSTRIES,
    APPLICATION_SOURCES,
    MISTAKE_TYPES,
)


def _synthetic_h1b_by_state() -> pd.DataFrame:
    """Generate synthetic H1B petition counts by state for analytics."""
    np.random.seed(42)
    # Weight toward CA, TX, NY, WA, NJ
    weights = np.array([3, 0.5, 2, 0.8, 15, 2, 1.5, 0.3, 5, 2, 0.5, 0.5, 4, 1.5, 0.8, 0.6, 0.8, 0.5, 0.3, 1,
                        2.5, 2, 1.5, 0.5, 1.2, 0.3, 0.6, 1, 0.4, 1.5, 0.5, 4, 2, 0.3, 2, 1, 0.8, 1.2, 1.5, 0.3, 0.8,
                        0.2, 1, 8, 1, 0.2, 1, 1.5, 0.5, 1, 0.3, 1])
    n = len(USA_STATES)
    petitions = (np.random.rand(n) * 2000 + weights * 1500).astype(int)
    return pd.DataFrame({
        "state": USA_STATES,
        "petitions": petitions,
        "fy": 2024,
    })


def _synthetic_job_postings_by_state() -> pd.DataFrame:
    """Synthetic daily job postings aggregated by state (for heat map)."""
    np.random.seed(43)
    n = len(USA_STATES)
    # Align with H1B hotspots
    base = np.array([500, 100, 400, 150, 2500, 400, 300, 80, 1200, 600, 120, 150, 900, 350, 200, 180, 220, 100, 80, 250,
                     400, 350, 280, 120, 300, 90, 150, 200, 100, 280, 120, 800, 450, 80, 400, 200, 250, 350, 100, 200,
                     60, 180, 1200, 250, 60, 220, 350, 120, 200, 80, 180])
    noise = np.random.rand(n) * 200
    return pd.DataFrame({
        "state": USA_STATES,
        "job_count": (base + noise).astype(int),
        "date": pd.Timestamp.now().normalize(),
    })


def _synthetic_job_postings_daily() -> pd.DataFrame:
    """Time series of total job postings (last 90 days) for trend charts."""
    np.random.seed(44)
    dates = pd.date_range(end=pd.Timestamp.now(), periods=90, freq="D")
    trend = np.linspace(8000, 12000, 90) + np.random.randn(90) * 500
    return pd.DataFrame({
        "date": dates,
        "total_postings": np.maximum(trend.astype(int), 1000),
    })


def _synthetic_mistakes() -> pd.DataFrame:
    """Synthetic job application mistakes (LinkedIn redirect, wrong page, etc.)."""
    np.random.seed(45)
    n = 500
    return pd.DataFrame({
        "id": range(n),
        "date": pd.date_range(end=pd.Timestamp.now(), periods=n, freq="D")[np.random.randint(0, 90, n)],
        "company": np.random.choice(["Tech Corp", "Health Inc", "Finance Co", "Startup XYZ", "Big Retail"], n),
        "job_title": np.random.choice(["Software Engineer", "Data Analyst", "Product Manager", "UX Designer"], n),
        "source": np.random.choice(["LinkedIn", "Company Site", "Indeed"], n, p=[0.7, 0.2, 0.1]),
        "mistake_type": np.random.choice(MISTAKE_TYPES, n, p=[0.5, 0.2, 0.15, 0.1, 0.05]),
        "intended_url": ["https://company.com/careers"] * n,
        "actual_url": np.where(
            np.random.rand(n) < 0.5,
            "https://www.linkedin.com/easy-apply/...",
            "https://company.com/careers"
        ),
    })


def load_h1b_by_state() -> pd.DataFrame:
    """Load H1B petition counts by state. Uses synthetic if no file."""
    if H1B_STATE_AGGREGATE.exists():
        return pd.read_parquet(H1B_STATE_AGGREGATE)
    return _synthetic_h1b_by_state()


def load_job_postings_by_state() -> pd.DataFrame:
    """Load job postings by state (for heat map)."""
    if JOB_POSTINGS_BY_STATE.exists():
        return pd.read_parquet(JOB_POSTINGS_BY_STATE)
    return _synthetic_job_postings_by_state()


def load_job_postings_daily() -> pd.DataFrame:
    """Load daily job postings time series."""
    if JOB_POSTINGS_DAILY.exists():
        return pd.read_parquet(JOB_POSTINGS_DAILY)
    return _synthetic_job_postings_daily()


def load_mistakes() -> pd.DataFrame:
    """Load job application mistakes log."""
    if MISTAKES_AGGREGATE.exists():
        return pd.read_parquet(MISTAKES_AGGREGATE)
    return _synthetic_mistakes()


def load_mistakes_by_type() -> pd.DataFrame:
    """Aggregated mistake counts by type (for bar/pie charts)."""
    mistakes = load_mistakes()
    return mistakes.groupby("mistake_type", as_index=False).agg(
        count=("id", "count")
    ).sort_values("count", ascending=False)
