"""
Data engineering: pipeline status and day-by-day work log for the Data Engineer dashboard.
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

from config.settings import PIPELINE_STATUS_FILE, DATA_ENGINEER_LOG_FILE, DATA_DIR


def get_pipeline_status() -> Dict[str, Any]:
    """Read last pipeline run status (written by jobs/daily_refresh.py)."""
    if not PIPELINE_STATUS_FILE.exists():
        return {
            "last_run_ts": None,
            "last_run_iso": None,
            "status": "never_run",
            "tables_updated": [],
            "message": "Pipeline has not run yet. Run: python jobs/daily_refresh.py",
        }
    try:
        data = json.loads(PIPELINE_STATUS_FILE.read_text())
        return {
            "last_run_ts": data.get("last_run_ts"),
            "last_run_iso": data.get("last_run_iso"),
            "status": data.get("status", "unknown"),
            "tables_updated": data.get("tables_updated", []),
            "message": data.get("message", "OK"),
        }
    except Exception as e:
        return {
            "last_run_ts": None,
            "last_run_iso": None,
            "status": "error",
            "tables_updated": [],
            "message": str(e),
        }


def get_data_engineer_log() -> List[Dict[str, Any]]:
    """Read day-by-day work log (edit data/data_engineer_log.json to update)."""
    if not DATA_ENGINEER_LOG_FILE.exists():
        return _default_log_entries()
    try:
        data = json.loads(DATA_ENGINEER_LOG_FILE.read_text())
        entries = data.get("days", data) if isinstance(data, dict) else data
        if not isinstance(entries, list):
            return _default_log_entries()
        return entries
    except Exception:
        return _default_log_entries()


def _default_log_entries() -> List[Dict[str, Any]]:
    """Default day-by-day entries so the chart works out of the box."""
    return [
        {"day": 1, "date": "2026-02-01", "tasks_done": 5, "tasks": ["Project setup", "Config & paths", "Data loader + synthetic data"], "status": "done", "notes": "Backend skeleton"},
        {"day": 2, "date": "2026-02-02", "tasks_done": 6, "tasks": ["H1B analytics", "Mistake analytics", "Resume analyzer", "Daily refresh pipeline"], "status": "done", "notes": "ETL and services"},
        {"day": 3, "date": "2026-02-03", "tasks_done": 4, "tasks": ["Dash app + USA map", "State detail, mistakes, H1B, candidate pages", "Filters and styling"], "status": "done", "notes": "Dashboards and UI"},
        {"day": 4, "date": "2026-02-04", "tasks_done": 0, "tasks": ["Add your daily tasks here"], "status": "planned", "notes": "Edit data/data_engineer_log.json"},
    ]


def get_day_by_day_for_chart() -> tuple:
    """Return (days list, tasks_done list) for bar chart; (dates, tasks_done) for timeline."""
    log = get_data_engineer_log()
    if not log:
        return ["Day 1"], [0]
    days = [f"Day {e.get('day', i+1)}" for i, e in enumerate(log)]
    tasks_done = [e.get("tasks_done", 0) for e in log]
    return days, tasks_done
