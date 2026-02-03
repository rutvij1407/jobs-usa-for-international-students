"""
Main Dash app: multi-page routing (USA map, state detail, mistakes, H1B market, candidate analysis).
"""
import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from dashboards.pages import main_map, state_detail, job_mistakes, h1b_market, candidate_analysis

# Bootstrap theme for clean UI
app = dash.Dash(
    __name__,
    use_pages=False,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)

# Navigation links
NAV = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("USA Map", href="/")),
        dbc.NavItem(dbc.NavLink("Job Mistakes", href="/mistakes")),
        dbc.NavItem(dbc.NavLink("H1B Market", href="/h1b")),
        dbc.NavItem(dbc.NavLink("Candidate Analysis", href="/candidate")),
    ],
    brand="F1 Job Dashboard",
    brand_href="/",
    color="primary",
    dark=True,
    className="mb-4",
)

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        dcc.Store(id="current-state", data=None),
        NAV,
        html.Div(id="page-content"),
    ]
)


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
    # Default: USA map
    return main_map.layout(), None


# Register all page callbacks
main_map.register_callbacks(app)
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
