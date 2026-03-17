"""
State detail page: same heat map style for one state; filters apply.
"""
import dash_bootstrap_components as dbc
from dash import dcc, html
from dashboards.components.filters import map_filters_row


def layout(state_abbr: str = None):
    state = (state_abbr or "CA").upper()
    return html.Div(
        className="page-content-wrap",
        children=[
            html.Div(
                [
                    dcc.Link("← Back to USA map", href="/", className="btn btn-outline-primary btn-sm mb-3"),
                    html.H1(f"State: {state}", className="page-title"),
                    html.P(
                        "Metrics and heat map for this state. Use filters to narrow by job type, company, industry.",
                        className="page-subtitle",
                    ),
                ],
                className="mb-4",
            ),
            html.Div(map_filters_row(id_prefix="state"), className="filter-row"),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [dbc.CardBody([html.H6("Job count", className="text-muted"), html.P(id="state-job-count", className="h4 mb-0")])],
                            className="dash-card",
                        ),
                        width=3,
                    ),
                    dbc.Col(
                        dbc.Card(
                            [dbc.CardBody([html.H6("H1B petitions", className="text-muted"), html.P(id="state-h1b", className="h4 mb-0")])],
                            className="dash-card",
                        ),
                        width=3,
                    ),
                    dbc.Col(
                        dbc.Card(
                            [dbc.CardBody([html.H6("Effectiveness score", className="text-muted"), html.P(id="state-score", className="h4 mb-0")])],
                            className="dash-card",
                        ),
                        width=3,
                    ),
                ],
                className="mb-4",
            ),
            html.Div(
                [
                    dcc.Graph(
                        id="state-heatmap",
                        config={"displayModeBar": True, "responsive": True},
                        style={"height": "420px", "width": "100%"},
                    ),
                ],
                className="map-container",
            ),
        ],
    )
