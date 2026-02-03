"""
Run the Dash app. From project root: python run.py
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from dashboards.app_dash import app

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)
