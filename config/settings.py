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

# Data engineering: pipeline status + day-by-day work log
PIPELINE_STATUS_FILE = PROCESSED_DIR / "pipeline_status.json"
DATA_ENGINEER_LOG_FILE = DATA_DIR / "data_engineer_log.json"

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

# Google Maps (optional): set GOOGLE_MAPS_API_KEY in .env
GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY", "")

# USA state centroids (lat, lng) for Google Maps heatmap/markers
STATE_CENTROIDS = {
    "AL": (32.3182, -86.9023), "AK": (64.8378, -153.4937), "AZ": (34.0489, -111.0937), "AR": (35.2010, -91.8318),
    "CA": (36.7783, -119.4179), "CO": (39.1130, -105.3111), "CT": (41.6032, -73.0877), "DE": (38.9108, -75.5277),
    "FL": (27.6648, -81.5158), "GA": (32.1574, -82.9071), "HI": (19.8968, -155.5828), "ID": (44.0682, -114.7420),
    "IL": (40.6331, -89.3985), "IN": (40.2672, -86.1349), "IA": (41.8780, -93.0977), "KS": (38.5266, -96.7265),
    "KY": (37.6681, -84.6701), "LA": (31.1695, -91.8678), "ME": (45.2538, -69.4455), "MD": (39.0458, -76.6413),
    "MA": (42.4072, -71.3824), "MI": (43.3266, -84.5361), "MN": (46.7296, -94.6859), "MS": (32.3547, -89.3985),
    "MO": (37.9643, -91.8318), "MT": (46.8797, -110.3626), "NE": (41.4925, -99.9018), "NV": (38.8026, -116.4194),
    "NH": (43.1939, -71.5724), "NJ": (40.0583, -74.4057), "NM": (34.5199, -105.8701), "NY": (43.2994, -74.2179),
    "NC": (35.7596, -79.0193), "ND": (47.5515, -101.0020), "OH": (40.4173, -82.9071), "OK": (35.0078, -97.0929),
    "OR": (43.8041, -120.5542), "PA": (41.2033, -77.1945), "RI": (41.5801, -71.4774), "SC": (33.8361, -81.1637),
    "SD": (43.9695, -99.9018), "TN": (35.5175, -86.5804), "TX": (31.9686, -99.9018), "UT": (39.3210, -111.0937),
    "VT": (44.5588, -72.5778), "VA": (37.4316, -78.6569), "WA": (47.7511, -120.7401), "WV": (38.5976, -80.4549),
    "WI": (43.7844, -88.7879), "WY": (43.0760, -107.2903), "DC": (38.9072, -77.0369),
}
