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
    return html.Div(
        className="page-content-wrap",
        children=[
            html.Div(
                [
                    html.H1("Job Application Mistakes", className="page-title"),
                    html.P(
                        "Track mistakes when applying via LinkedIn (e.g., redirect to LinkedIn form instead of employer site). "
                        "Filter by date, source, and mistake type.",
                        className="page-subtitle",
                    ),
                ],
                className="mb-4",
            ),
            html.Div(mistakes_filters_row(id_prefix="mistakes"), className="filter-row"),
            dbc.Row(
                [
                    dbc.Col(html.Div(dcc.Graph(id="mistakes-by-type", config={"responsive": True}), className="dash-graph-card"), width=6),
                    dbc.Col(html.Div(dcc.Graph(id="mistakes-by-source", config={"responsive": True}), className="dash-graph-card"), width=6),
                ],
                className="mb-4",
            ),
            dbc.Row(
                [dbc.Col(html.Div(dcc.Graph(id="mistakes-time-series", config={"responsive": True}), className="dash-graph-card"), width=12)],
                className="mb-4",
            ),
            html.H5("Recent mistakes (sample)", className="mt-3 mb-2"),
            html.Div(id="mistakes-table-wrap", className="table-responsive-wrap"),
        ],
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
        raw = get_mistakes_filtered(start_date=start, end_date=end, source=source, mistake_type=mistake_type)

        fig_type = px.bar(
            by_type, x="mistake_type", y="count", title="Mistakes by type",
            labels={"mistake_type": "Type", "count": "Count"},
        )
        fig_type.update_layout(xaxis_tickangle=-45, margin=dict(t=40, b=120), height=320)

        fig_source = px.pie(
            by_source, names="source", values="count", title="Mistakes by application source",
        )
        fig_source.update_layout(margin=dict(t=40), height=320)

        fig_ts = go.Figure(
            data=[go.Scatter(x=ts["date"], y=ts["count"], mode="lines+markers", name="Mistakes", line=dict(color="#0d6efd"))],
            layout=go.Layout(
                title="Mistakes over time (weekly)",
                xaxis_title="Date",
                yaxis_title="Count",
                height=320,
                margin=dict(t=40),
            ),
        )

        table = dbc.Table.from_dataframe(
            raw.head(15)[["date", "company", "job_title", "source", "mistake_type"]],
            striped=True,
            bordered=True,
            size="sm",
            className="mb-0",
        )
        return fig_type, fig_source, fig_ts, table
