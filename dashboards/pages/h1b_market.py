"""
F1/H1B job market dashboard: daily job trends, top states, H1B metrics.
"""
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from backend.services.h1b_analytics import (
    get_daily_job_trends,
    get_top_states_by_jobs,
    get_top_states_by_h1b,
    get_state_level_metrics,
)


def layout():
    return dbc.Container(
        [
            html.H2("F1 / H1B Job Market", className="mb-3"),
            html.P(
                "Daily job posting trends and H1B activity by state. Data refreshes daily; H1B source is quarterly (USCIS).",
                className="text-muted mb-3",
            ),
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(id="h1b-daily-trend"), width=12),
                ],
                className="mb-4",
            ),
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(id="h1b-top-jobs"), width=6),
                    dbc.Col(dcc.Graph(id="h1b-top-h1b"), width=6),
                ],
                className="mb-4",
            ),
            html.H5("State metrics (sample)", className="mt-3"),
            html.Div(id="h1b-state-table-wrap"),
        ],
        fluid=True,
        className="py-4",
    )


def register_callbacks(app):
    @app.callback(
        [
            Output("h1b-daily-trend", "figure"),
            Output("h1b-top-jobs", "figure"),
            Output("h1b-top-h1b", "figure"),
            Output("h1b-state-table-wrap", "children"),
        ],
        Input("h1b-daily-trend", "id"),  # initial load
    )
    def update_h1b_market(_):
        daily = get_daily_job_trends()
        top_jobs = get_top_states_by_jobs(15)
        top_h1b = get_top_states_by_h1b(15)
        metrics = get_state_level_metrics()

        fig_daily = go.Figure(
            data=[go.Scatter(x=daily["date"], y=daily["total_postings"], mode="lines+markers", name="Total postings")],
            layout=go.Layout(
                title="Daily job postings (last 90 days)",
                xaxis_title="Date",
                yaxis_title="Postings",
                height=350,
            ),
        )

        fig_jobs = px.bar(
            top_jobs, x="state", y="job_count", title="Top states by job count",
            labels={"state": "State", "job_count": "Jobs"},
        )
        fig_h1b = px.bar(
            top_h1b, x="state", y="petitions", title="Top states by H1B petitions",
            labels={"state": "State", "petitions": "H1B petitions"},
        )

        table = dbc.Table.from_dataframe(
            metrics.head(15)[["state", "job_count", "petitions", "effectiveness_score"]],
            striped=True,
            bordered=True,
            size="sm",
        )
        return fig_daily, fig_jobs, fig_h1b, table
