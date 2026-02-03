"""
Configuration for F1 Job Dashboard backend.
"""
import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
UPLOADS_DIR = PROJECT_ROOT / "uploads"

# Ensure dirs exist
for d in (RAW_DIR, PROCESSED_DIR, UPLOADS_DIR):
    d.mkdir(parents=True, exist_ok=True)

# Data file names (processed outputs used by dashboards)
H1B_STATE_AGGREGATE = PROCESSED_DIR / "h1b_by_state.parquet"
H1B_EMPLOYER_AGGREGATE = PROCESSED_DIR / "h1b_by_employer.parquet"
JOB_POSTINGS_DAILY = PROCESSED_DIR / "job_postings_daily.parquet"
JOB_POSTINGS_BY_STATE = PROCESSED_DIR / "job_postings_by_state.parquet"
MISTAKES_AGGREGATE = PROCESSED_DIR / "job_application_mistakes.parquet"
MISTAKES_BY_TYPE = PROCESSED_DIR / "mistakes_by_type.parquet"

# USA state abbreviations (for choropleth)
USA_STATES = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "DC"
]

# Filter options (used across dashboards)
JOB_TYPES = ["All", "Full-time", "Part-time", "Contract", "Internship"]
COMPANY_TYPES = ["All", "Startup", "Enterprise", "Nonprofit", "Government"]
INDUSTRIES = ["All", "Technology", "Healthcare", "Finance", "Education", "Manufacturing", "Other"]
APPLICATION_SOURCES = ["All", "LinkedIn", "Company Site", "Indeed", "Other"]
MISTAKE_TYPES = ["Wrong page (LinkedIn form)", "Duplicate apply", "Expired posting", "Wrong job title", "Other"]

# Default date range (for synthetic data)
DEFAULT_START_YEAR = 2022
DEFAULT_END_YEAR = 2025
