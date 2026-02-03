"""
H1B data analytics: state-level aggregations, time trends, top employers.
"""
import pandas as pd
import numpy as np
from backend.data_loader import load_h1b_by_state, load_job_postings_daily, load_job_postings_by_state


def get_state_level_metrics(
    job_type: str = "All",
    company_type: str = "All",
    industry: str = "All",
) -> pd.DataFrame:
    """
    Merge H1B and job postings by state for heat map and tables.
    Filters are applied to job_postings; H1B is quarterly so we keep full set.
    """
    h1b = load_h1b_by_state()
    jobs = load_job_postings_by_state()
    merged = jobs.merge(h1b[["state", "petitions"]], on="state", how="left")
    merged["petitions"] = merged["petitions"].fillna(0).astype(int)
    # Composite score for "effectiveness" (job count + H1B weight)
    merged["effectiveness_score"] = merged["job_count"] + merged["petitions"] * 2
    return merged


def get_daily_job_trends(
    start_date: pd.Timestamp = None,
    end_date: pd.Timestamp = None,
) -> pd.DataFrame:
    """Time series of daily job postings for trend chart."""
    df = load_job_postings_daily()
    if start_date is not None:
        df = df[df["date"] >= start_date]
    if end_date is not None:
        df = df[df["date"] <= end_date]
    return df.sort_values("date")


def get_state_detail(state_abbr: str) -> pd.DataFrame:
    """Single-state view for detail page: one row with state metrics."""
    metrics = get_state_level_metrics()
    row = metrics[metrics["state"] == state_abbr]
    if row.empty:
        return pd.DataFrame()
    return row


def get_top_states_by_jobs(n: int = 10) -> pd.DataFrame:
    """Top N states by job count (for tables)."""
    metrics = get_state_level_metrics()
    return metrics.nlargest(n, "job_count")[["state", "job_count", "petitions", "effectiveness_score"]]


def get_top_states_by_h1b(n: int = 10) -> pd.DataFrame:
    """Top N states by H1B petitions."""
    metrics = get_state_level_metrics()
    return metrics.nlargest(n, "petitions")[["state", "petitions", "job_count", "effectiveness_score"]]
