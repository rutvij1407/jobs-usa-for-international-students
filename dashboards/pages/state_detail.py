"""
State detail page: same heat map style for one state (zoomed); filters apply.
"""
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
from backend.services.h1b_analytics import get_state_detail, get_state_level_metrics
from dashboards.components.filters import map_filters_row


def layout(state_abbr: str = None):
    state = (state_abbr or "CA").upper()
    return dbc.Container(
        [
            html.H2(f"State Detail: {state}", className="mb-3"),
            html.P(
                "Same heat map style for this state. Use filters to narrow by job type, company, industry.",
                className="text-muted mb-3",
            ),
            map_filters_row(id_prefix="state"),
            dcc.Graph(id="state-heatmap"),
            html.Hr(),
            html.H5("Metrics", className="mt-3"),
            dbc.Row(
                [
                    dbc.Col(dbc.Card([dbc.CardBody([html.H6("Job count", className="text-muted"), html.P(id="state-job-count")])]), width=3),
                    dbc.Col(dbc.Card([dbc.CardBody([html.H6("H1B petitions", className="text-muted"), html.P(id="state-h1b")])]), width=3),
                    dbc.Col(dbc.Card([dbc.CardBody([html.H6("Effectiveness score", className="text-muted"), html.P(id="state-score")])]), width=3),
                ],
                className="mb-4",
            ),
            dcc.Link("← Back to USA map", href="/", className="btn btn-outline-primary"),
        ],
        fluid=True,
        className="py-4",
    )


def register_callbacks(app, state_abbr: str = None):
    """State detail callbacks are registered in app_dash (use current-state Store)."""
    pass
