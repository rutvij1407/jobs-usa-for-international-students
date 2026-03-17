# Google Maps — Procedure to Access the Data

This project can show the USA job-effectiveness data on **Google Maps** (heat map) instead of (or in addition to) the built-in Plotly map. The **same backend data** is used: state-level job count, H1B petitions, and effectiveness score.

---

## 1. Get a Google Maps API Key

1. **Google Cloud account**
   - Go to [Google Cloud Console](https://console.cloud.google.com/).
   - Sign in or create an account.

2. **Create or select a project**
   - Use an existing project or click **Create Project** and give it a name (e.g. `f1-job-dashboard`).

3. **Enable the Maps JavaScript API**
   - In the console: **APIs & Services** → **Library**.
   - Search for **Maps JavaScript API**.
   - Open it and click **Enable**.

4. **Enable the Maps JavaScript API only**
   - For a heat map you only need **Maps JavaScript API** (and the **Visualization** library, which is loaded with `&libraries=visualization` in the script URL).

5. **Billing**
   - Google Maps requires a billing account. Enable billing in **Billing** and link it to your project. There is a free tier; see [Google Maps pricing](https://mapsplatform.google.com/pricing/).

6. **Create an API key**
   - Go to **APIs & Services** → **Credentials**.
   - Click **Create credentials** → **API key**.
   - Copy the key.

7. **Restrict the key (recommended)**
   - Open the key you created.
   - Under **Application restrictions**, choose **HTTP referrers** and add your app’s URLs, e.g.:
     - `http://localhost:8051/*`
     - `http://127.0.0.1:8051/*`
     - Your production domain if you deploy.
   - Under **API restrictions**, restrict to **Maps JavaScript API** (and any others you use).

---

## 2. Give the App Your API Key

1. In the project root, create or edit a `.env` file:
   ```bash
   GOOGLE_MAPS_API_KEY=your_api_key_here
   ```
2. Load `.env` when starting the app (e.g. with `python-dotenv`). The app reads `GOOGLE_MAPS_API_KEY` from the environment (see `config/settings.py`).

   If you start the app with:
   ```bash
   source venv/bin/activate
   python run.py
   ```
   and `run.py` or the app uses `python-dotenv` and loads `.env`, the key will be available. If not, set it in the shell before running:
   ```bash
   export GOOGLE_MAPS_API_KEY=your_api_key_here
   python run.py
   ```

---

## 3. How the App Uses the Data

- **Backend**
  - `backend/services/h1b_analytics.py` has `get_map_data_for_google(job_type, company_type, industry)`.
  - It returns a list of:
    - `state`, `lat`, `lng` (from `config/settings.py` state centroids),
    - `job_count`, `petitions`, `effectiveness_score` (same metrics as the Plotly map).

- **API**
  - The Dash/Flask app exposes:
    - **GET `/api/map-data?job_type=...&company_type=...&industry=...`**
  - Response: JSON array of the objects above. This is what the Google Map page uses.

- **Map page**
  - **GET `/map-view`** (optional query: `?job_type=All&company_type=All&industry=All`) serves an HTML page that:
    1. Loads the Maps JavaScript API with your key and the Visualization library.
    2. Fetches `/api/map-data` with the same query params.
    3. Draws a **HeatmapLayer** with:
       - location = `(lat, lng)` per state,
       - weight = derived from `effectiveness_score`.

So **data access** is: **same backend and same metrics** as the Plotly map; Google Maps is just another view that reads from `/api/map-data`.

---

## 4. Using the Google Map in the App

- From the **USA Map** page in the dashboard, use the **“Google Maps”** link (opens `/map-view` in a new tab).
- Or open in the browser:  
  `http://127.0.0.1:8051/map-view`  
  (or your port).

If `GOOGLE_MAPS_API_KEY` is not set, the map page will show a short message asking you to set it and point to this doc.

---

## 5. Optional: Filter the Google Map

- Default: `/map-view` uses `job_type=All`, `company_type=All`, `industry=All`.
- To pass filters, use query params, e.g.:  
  `http://127.0.0.1:8051/map-view?job_type=Full-time&industry=Technology`  
- The map page requests `/api/map-data` with those same params, so the heat map reflects the same filters as the dropdowns (when you add them to the map-view page or link from the main map with filters).

---

## Summary

| Step | Action |
|------|--------|
| 1 | Create/enable Google Cloud project, enable **Maps JavaScript API**, create and restrict an **API key**. |
| 2 | Set **GOOGLE_MAPS_API_KEY** in `.env` (or env) and run the app so it can read the key. |
| 3 | Data: same as Plotly map, via **`get_map_data_for_google()`** and **GET `/api/map-data`**. |
| 4 | Open **`/map-view`** (or the “Google Maps” link on the USA Map page) to see the heat map. |

This is the full procedure to use Google Maps and how the app accesses the data for it.
