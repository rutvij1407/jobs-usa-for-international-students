"""
Main Dash app: multi-page routing (USA map, state detail, mistakes, H1B market, candidate analysis).
"""
import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from dashboards.pages import main_map, state_detail, job_mistakes, h1b_market, candidate_analysis, data_engineer
from pathlib import Path
from flask import request, Response
import json

from config.settings import GOOGLE_MAPS_API_KEY
from backend.services.h1b_analytics import get_map_data_for_google
from backend.services.kml_generator import generate_h1b_kml

# Bootstrap theme + custom CSS (in dashboards/assets/custom.css)
app = dash.Dash(
    __name__,
    use_pages=False,
    external_stylesheets=[dbc.themes.BOOTSTRAP, "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"],
    suppress_callback_exceptions=True,
    title="F1 Job Dashboard",
)

# Navigation
NAV = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarBrand("F1 Job Dashboard", href="/", className="fw-bold"),
            dbc.NavbarToggler(id="navbar-toggler"),
            dbc.Collapse(
                        dbc.Nav(
                            [
                                dbc.NavItem(dbc.NavLink("USA Map", href="/", active="exact")),
                                dbc.NavItem(dbc.NavLink("Job Mistakes", href="/mistakes", active="exact")),
                                dbc.NavItem(dbc.NavLink("H1B Market", href="/h1b", active="exact")),
                                dbc.NavItem(dbc.NavLink("Candidate Analysis", href="/candidate", active="exact")),
                                dbc.NavItem(dbc.NavLink("Data Engineer", href="/data-engineer", active="exact")),
                            ],
                    navbar=True,
                    className="ms-auto",
                ),
                id="navbar-collapse",
                navbar=True,
                is_open=True,
            ),
        ],
        fluid=True,
    ),
    color="primary",
    dark=True,
    className="mb-4 shadow-sm",
)

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        dcc.Store(id="current-state", data=None),
        NAV,
        html.Main(html.Div(id="page-content"), className="min-vh-100"),
    ],
    style={"minHeight": "100vh", "background": "#f8f9fa"},
)

# ----- Google Maps API and map view (data access for map) -----
@app.server.route("/api/map-data")
def api_map_data():
    """Return JSON list of {state, lat, lng, job_count, petitions, effectiveness_score} for Google Maps."""
    job_type = request.args.get("job_type", "All")
    company_type = request.args.get("company_type", "All")
    industry = request.args.get("industry", "All")
    data = get_map_data_for_google(job_type=job_type, company_type=company_type, industry=industry)
    return Response(json.dumps(data), mimetype="application/json")


@app.server.route("/api/h1b.kml")
def api_h1b_kml():
    """Generate KML from backend for Google Earth. Same data as map; lightweight."""
    job_type = request.args.get("job_type", "All")
    company_type = request.args.get("company_type", "All")
    industry = request.args.get("industry", "All")
    data = get_map_data_for_google(job_type=job_type, company_type=company_type, industry=industry)
    places = [
        {
            "name": d["state"],
            "state": d["state"],
            "latitude": d["lat"],
            "longitude": d["lng"],
            "lat": d["lat"],
            "lng": d["lng"],
            "job_count": d["job_count"],
            "petitions": d["petitions"],
            "effectiveness_score": d["effectiveness_score"],
        }
        for d in data
    ]
    kml = generate_h1b_kml(places)
    return Response(kml, mimetype="application/vnd.google-earth.kml+xml", headers={"Content-Disposition": "attachment; filename=h1b-jobs-usa.kml"})


@app.server.route("/map-view")
def map_view():
    """Serve Google Maps HTML page; filters passed as query params."""
    template_path = Path(__file__).resolve().parent / "templates" / "google_map.html"
    if not template_path.exists():
        return Response("Map template not found.", status=404)
    html_content = template_path.read_text()
    base_url = request.url_root.rstrip("/")
    job_type = request.args.get("job_type", "All")
    company_type = request.args.get("company_type", "All")
    industry = request.args.get("industry", "All")
    html_content = html_content.replace("{{ API_KEY }}", GOOGLE_MAPS_API_KEY or "")
    html_content = html_content.replace("{{ BASE_URL }}", base_url)
    html_content = html_content.replace("{{ job_type }}", job_type)
    html_content = html_content.replace("{{ company_type }}", company_type)
    html_content = html_content.replace("{{ industry }}", industry)
    return Response(html_content, mimetype="text/html")


@callback(
    [Output("page-content", "children"), Output("current-state", "data")],
    Input("url", "pathname"),
)
def render_page(pathname):
    if pathname is None:
        pathname = "/"
    pathname = pathname or "/"
    # State detail: /state/CA -> state_abbr = CA
    if pathname.startswith("/state/"):
        parts = pathname.strip("/").split("/")
        state_abbr = parts[1] if len(parts) > 1 else "CA"
        return state_detail.layout(state_abbr), state_abbr
    if pathname == "/mistakes":
        return job_mistakes.layout(), None
    if pathname == "/h1b":
        return h1b_market.layout(), None
    if pathname == "/candidate":
        return candidate_analysis.layout(), None
    if pathname == "/data-engineer":
        return data_engineer.layout(), None
    # Default: USA map
    return main_map.layout(), None


# Register all page callbacks
main_map.register_callbacks(app)
data_engineer.register_callbacks(app)
job_mistakes.register_callbacks(app)
h1b_market.register_callbacks(app)
candidate_analysis.register_callbacks(app)


# State detail callbacks: use current-state Store for state_abbr
import plotly.graph_objects as go
from backend.services.h1b_analytics import get_state_level_metrics


def _state_view_response(state_abbr, job_type, company_type, industry):
    """Build state detail figure and metric strings."""
    state = (state_abbr or "CA").upper()
    df_all = get_state_level_metrics(
        job_type=job_type or "All",
        company_type=company_type or "All",
        industry=industry or "All",
    )
    row = df_all[df_all["state"] == state]
    if row.empty:
        fig = go.Figure(layout=go.Layout(title=f"No data for {state}"))
        return fig, "—", "—", "—"
    row = row.iloc[0]
    fig = go.Figure(
        data=go.Choropleth(
            locations=[state],
            z=[row["effectiveness_score"]],
            locationmode="USA-states",
            colorscale="Reds",
            colorbar=dict(title="Effectiveness"),
            hoverinfo="text",
            hovertext=f"<b>{state}</b><br>Jobs: {row['job_count']:,}<br>H1B: {row['petitions']:,}<br>Score: {row['effectiveness_score']:,}",
        ),
        layout=go.Layout(
            title=f"Job effectiveness — {state}",
            geo=dict(scope="usa", center=dict(lat=39, lon=-98), lataxis=dict(range=[24, 50]), lonaxis=dict(range=[-126, -66])),
            margin=dict(l=0, r=0, t=40, b=0),
            height=400,
        ),
    )
    return (
        fig,
        f"{row['job_count']:,}",
        f"{row['petitions']:,}",
        f"{row['effectiveness_score']:,}",
    )


@callback(
    [
        Output("state-heatmap", "figure"),
        Output("state-job-count", "children"),
        Output("state-h1b", "children"),
        Output("state-score", "children"),
    ],
    Input("current-state", "data"),
    Input("state-job-type", "value"),
    Input("state-company-type", "value"),
    Input("state-industry", "value"),
)
def update_state_view(state_abbr, job_type, company_type, industry):
    if not state_abbr:
        return go.Figure(), "—", "—", "—"
    return _state_view_response(state_abbr, job_type, company_type, industry)


# Click on USA map -> navigate to state detail (clientside)
app.clientside_callback(
    """
    function(clickData) {
        if (clickData && clickData.points && clickData.points[0] && clickData.points[0].location) {
            var state = clickData.points[0].location;
            window.location.href = '/state/' + state;
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output("map-click-store", "data"),
    Input("usa-heatmap", "clickData"),
)
