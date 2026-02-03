"""
Job application mistakes dashboard: LinkedIn redirects, wrong page, etc.
"""
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from backend.services.mistake_analytics import (
    get_mistakes_by_type_df,
    get_mistakes_by_source_df,
    get_mistakes_time_series,
    get_mistakes_filtered,
)
from dashboards.components.filters import mistakes_filters_row


def layout():
    return dbc.Container(
        [
            html.H2("Job Application Mistakes", className="mb-3"),
            html.P(
                "Track mistakes when applying via LinkedIn (e.g., redirect to LinkedIn form instead of employer site). "
                "Use filters to narrow by date, source, and mistake type.",
                className="text-muted mb-3",
            ),
            mistakes_filters_row(id_prefix="mistakes"),
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(id="mistakes-by-type"), width=6),
                    dbc.Col(dcc.Graph(id="mistakes-by-source"), width=6),
                ],
                className="mb-4",
            ),
            dbc.Row([dbc.Col(dcc.Graph(id="mistakes-time-series"), width=12)], className="mb-4"),
            html.H5("Recent mistakes (sample)", className="mt-3"),
            html.Div(id="mistakes-table-wrap"),
        ],
        fluid=True,
        className="py-4",
    )


def register_callbacks(app):
    @app.callback(
        [
            Output("mistakes-by-type", "figure"),
            Output("mistakes-by-source", "figure"),
            Output("mistakes-time-series", "figure"),
            Output("mistakes-table-wrap", "children"),
        ],
        Input("mistakes-date-range", "start_date"),
        Input("mistakes-date-range", "end_date"),
        Input("mistakes-source", "value"),
        Input("mistakes-mistake-type", "value"),
    )
    def update_mistakes(start_date, end_date, source, mistake_type):
        start = pd.to_datetime(start_date) if start_date else None
        end = pd.to_datetime(end_date) if end_date else None
        source = source or "All"
        mistake_type = mistake_type or "All"
        by_type = get_mistakes_by_type_df(start_date=start, end_date=end)
        by_source = get_mistakes_by_source_df(start_date=start, end_date=end)
        ts = get_mistakes_time_series(start_date=start, end_date=end, freq="W")
        raw = get_mistakes_filtered(start_date=start, end_date=end, source=source or "All", mistake_type=mistake_type or "All")

        fig_type = px.bar(
            by_type, x="mistake_type", y="count", title="Mistakes by type",
            labels={"mistake_type": "Type", "count": "Count"},
        )
        fig_type.update_layout(xaxis_tickangle=-45)

        fig_source = px.pie(
            by_source, names="source", values="count", title="Mistakes by application source",
        )

        fig_ts = go.Figure(
            data=[go.Scatter(x=ts["date"], y=ts["count"], mode="lines+markers", name="Mistakes")],
            layout=go.Layout(title="Mistakes over time (weekly)", xaxis_title="Date", yaxis_title="Count", height=350),
        )

        table = dbc.Table.from_dataframe(
            raw.head(15)[["date", "company", "job_title", "source", "mistake_type"]].round(0),
            striped=True,
            bordered=True,
            size="sm",
        )
        return fig_type, fig_source, fig_ts, table
