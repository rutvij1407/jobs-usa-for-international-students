"""
Job application mistake analytics: aggregations by type, source, company, time.
"""
import pandas as pd
from backend.data_loader import load_mistakes, load_mistakes_by_type


def get_mistakes_filtered(
    start_date: pd.Timestamp = None,
    end_date: pd.Timestamp = None,
    source: str = "All",
    mistake_type: str = "All",
) -> pd.DataFrame:
    """Filter mistakes by date, application source, and mistake type."""
    df = load_mistakes().copy()
    if start_date is not None:
        df = df[df["date"] >= start_date]
    if end_date is not None:
        df = df[df["date"] <= end_date]
    if source and source != "All":
        df = df[df["source"] == source]
    if mistake_type and mistake_type != "All":
        df = df[df["mistake_type"] == mistake_type]
    return df


def get_mistakes_by_type_df(
    start_date: pd.Timestamp = None,
    end_date: pd.Timestamp = None,
) -> pd.DataFrame:
    """Count of mistakes by type (for bar/pie charts)."""
    df = get_mistakes_filtered(start_date=start_date, end_date=end_date)
    return df.groupby("mistake_type", as_index=False).agg(count=("id", "count")).sort_values(
        "count", ascending=False
    )


def get_mistakes_by_source_df(
    start_date: pd.Timestamp = None,
    end_date: pd.Timestamp = None,
) -> pd.DataFrame:
    """Count by application source (LinkedIn vs others)."""
    df = get_mistakes_filtered(start_date=start_date, end_date=end_date)
    return df.groupby("source", as_index=False).agg(count=("id", "count")).sort_values(
        "count", ascending=False
    )


def get_mistakes_time_series(
    start_date: pd.Timestamp = None,
    end_date: pd.Timestamp = None,
    freq: str = "W",
) -> pd.DataFrame:
    """Mistakes over time (weekly or daily) for trend line."""
    df = get_mistakes_filtered(start_date=start_date, end_date=end_date)
    df = df.set_index("date").resample(freq).agg({"id": "count"}).reset_index()
    df = df.rename(columns={"id": "count"})
    return df
