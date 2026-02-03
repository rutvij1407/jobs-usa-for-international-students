"""
Shared filter components for dashboards (job type, company type, date range, etc.).
"""
import dash_bootstrap_components as dbc
from dash import dcc, html
from datetime import datetime, timedelta
from config.settings import (
    JOB_TYPES,
    COMPANY_TYPES,
    INDUSTRIES,
    APPLICATION_SOURCES,
    MISTAKE_TYPES,
)


def date_range_picker(id_prefix: str = "filter"):
    """Date range picker (single date range)."""
    return dbc.Row(
        [
            dbc.Col(
                dcc.DatePickerRange(
                    id=f"{id_prefix}-date-range",
                    start_date=(datetime.now() - timedelta(days=90)).date(),
                    end_date=datetime.now().date(),
                    display_format="YYYY-MM-DD",
                ),
                width="auto",
            ),
        ],
        className="mb-2",
    )


def job_type_dropdown(id_prefix: str = "filter"):
    """Job type: All, Full-time, Part-time, Contract, Internship."""
    return dbc.Col(
        [
            html.Label("Job type", className="small text-muted"),
            dcc.Dropdown(
                id=f"{id_prefix}-job-type",
                options=[{"label": x, "value": x} for x in JOB_TYPES],
                value="All",
                clearable=False,
                className="mb-2",
            ),
        ],
        width=2,
    )


def company_type_dropdown(id_prefix: str = "filter"):
    """Company type filter."""
    return dbc.Col(
        [
            html.Label("Company type", className="small text-muted"),
            dcc.Dropdown(
                id=f"{id_prefix}-company-type",
                options=[{"label": x, "value": x} for x in COMPANY_TYPES],
                value="All",
                clearable=False,
                className="mb-2",
            ),
        ],
        width=2,
    )


def industry_dropdown(id_prefix: str = "filter"):
    """Industry filter."""
    return dbc.Col(
        [
            html.Label("Industry", className="small text-muted"),
            dcc.Dropdown(
                id=f"{id_prefix}-industry",
                options=[{"label": x, "value": x} for x in INDUSTRIES],
                value="All",
                clearable=False,
                className="mb-2",
            ),
        ],
        width=2,
    )


def source_dropdown(id_prefix: str = "filter"):
    """Application source (LinkedIn, Company Site, etc.)."""
    return dbc.Col(
        [
            html.Label("Application source", className="small text-muted"),
            dcc.Dropdown(
                id=f"{id_prefix}-source",
                options=[{"label": x, "value": x} for x in APPLICATION_SOURCES],
                value="All",
                clearable=False,
                className="mb-2",
            ),
        ],
        width=2,
    )


def mistake_type_dropdown(id_prefix: str = "filter"):
    """Mistake type (wrong page, duplicate, etc.)."""
    return dbc.Col(
        [
            html.Label("Mistake type", className="small text-muted"),
            dcc.Dropdown(
                id=f"{id_prefix}-mistake-type",
                options=[{"label": x, "value": x} for x in MISTAKE_TYPES],
                value="All",
                clearable=False,
                className="mb-2",
            ),
        ],
        width=3,
    )


def map_filters_row(id_prefix: str = "map"):
    """Row of filters for USA heat map and state detail."""
    return dbc.Row(
        [
            job_type_dropdown(id_prefix),
            company_type_dropdown(id_prefix),
            industry_dropdown(id_prefix),
        ],
        className="mb-3",
    )


def mistakes_filters_row(id_prefix: str = "mistakes"):
    """Row of filters for job mistakes dashboard."""
    return dbc.Row(
        [
            date_range_picker(id_prefix),
            source_dropdown(id_prefix),
            mistake_type_dropdown(id_prefix),
        ],
        className="mb-3",
    )
