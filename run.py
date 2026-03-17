"""
Run the Dash app. From project root, use the venv:

  source venv/bin/activate
  pip install -r requirements.txt   # if not done yet
  python run.py

Or:  ./venv/bin/python run.py

Set GOOGLE_MAPS_API_KEY in .env for the Google Maps view (/map-view).
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from dotenv import load_dotenv
    load_dotenv(PROJECT_ROOT / ".env")
except ImportError:
    pass

try:
    from dashboards.app_dash import app
except ModuleNotFoundError as e:
    if "dash" in str(e).lower():
        print("Dash not found. Activate the venv and install dependencies:")
        print("  source venv/bin/activate")
        print("  pip install -r requirements.txt")
        print("  python run.py")
        print("\nOr run with venv Python:  ./venv/bin/python run.py")
        sys.exit(1)
    raise

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8051))
    print(f"Open http://127.0.0.1:{port}")
    app.run(debug=True, host="0.0.0.0", port=port)
