"""
Data Engineer dashboard: pipeline status, day-by-day work chart, daily log table.
Reflects what a data engineer does: ETL, pipelines, monitoring, daily tasks.
"""
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import pandas as pd
from backend.services.pipeline_status import (
    get_pipeline_status,
    get_data_engineer_log,
    get_day_by_day_for_chart,
)


def layout():
    return html.Div(
        className="page-content-wrap",
        children=[
            html.Div(
                [
                    html.H1("Data Engineer", className="page-title"),
                    html.P(
                        "Pipeline status, day-by-day progress, and daily work log. "
                        "Edit data/data_engineer_log.json to add your daily tasks.",
                        className="page-subtitle",
                    ),
                ],
                className="mb-4",
            ),
            # Pipeline status card
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader("Pipeline status", className="fw-bold"),
                                dbc.CardBody(
                                    [
                                        html.Div(id="pipeline-status-body"),
                                        html.Small(
                                            "Run: python jobs/daily_refresh.py (or cron daily)",
                                            className="text-muted",
                                        ),
                                    ]
                                ),
                            ],
                            className="dash-card mb-4",
                        ),
                        width=12,
                    ),
                ],
                className="mb-4",
            ),
            # Day-by-day working chart
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            [
                                html.H5("Day-by-day working chart", className="mb-3"),
                                html.P(
                                    "Tasks completed per day. Update data/data_engineer_log.json to reflect your daily work.",
                                    className="text-muted small mb-2",
                                ),
                                dcc.Graph(id="day-by-day-chart", config={"responsive": True}),
                            ],
                            className="dash-graph-card",
                        ),
                        width=12,
                    ),
                ],
                className="mb-4",
            ),
            # Daily log table
            html.H5("Daily log (edit data/data_engineer_log.json)", className="mb-3"),
            html.Div(id="data-engineer-log-table", className="table-responsive-wrap mb-4"),
            # What a data engineer does
            dbc.Card(
                [
                    dbc.CardHeader("What a data engineer does in this project", className="fw-bold"),
                    dbc.CardBody(
                        [
                            html.Ul(
                                [
                                    html.Li("Run daily pipeline: jobs/daily_refresh.py (ETL: extract, transform, load)."),
                                    html.Li("Monitor pipeline status and data freshness (this page)."),
                                    html.Li("Update day-by-day log (data/data_engineer_log.json) with daily tasks."),
                                    html.Li("Ensure raw → processed data flow; add real H1B/job sources when ready."),
                                    html.Li("Keep dashboards working: USA map, mistakes, H1B market, candidate analysis."),
                                ],
                                className="mb-0",
                            ),
                        ]
                    ),
                ],
                className="dash-card",
            ),
        ],
    )


def register_callbacks(app):
    @app.callback(
        Output("pipeline-status-body", "children"),
        Input("url", "pathname"),
    )
    def update_pipeline_status(pathname):
        if pathname != "/data-engineer":
            return html.Div()
        st = get_pipeline_status()
        last = st.get("last_run_iso") or "—"
        status = st.get("status", "unknown")
        tables = st.get("tables_updated", [])
        msg = st.get("message", "")
        badge = dbc.Badge("Success" if status == "success" else ("Error" if status == "error" else "Never run"), color="success" if status == "success" else ("danger" if status == "error" else "secondary"), className="mb-2")
        return html.Div(
            [
                html.P([html.Strong("Last run: "), last]),
                html.P([html.Strong("Status: "), badge]),
                html.P([html.Strong("Tables updated: "), ", ".join(tables) if tables else "—"]),
                html.P([html.Strong("Message: "), msg], className="small text-muted mb-0"),
            ]
        )

    @app.callback(
        Output("day-by-day-chart", "figure"),
        Input("url", "pathname"),
    )
    def update_day_by_day_chart(pathname):
        if pathname != "/data-engineer":
            return go.Figure()
        days, tasks_done = get_day_by_day_for_chart()
        fig = go.Figure(
            data=[
                go.Bar(
                    x=days,
                    y=tasks_done,
                    name="Tasks done",
                    marker_color="#0d6efd",
                    text=tasks_done,
                    textposition="outside",
                )
            ],
            layout=go.Layout(
                title="Tasks completed per day",
                xaxis_title="Day",
                yaxis_title="Tasks completed",
                height=380,
                margin=dict(t=40, b=60),
                showlegend=False,
            ),
        )
        return fig

    @app.callback(
        Output("data-engineer-log-table", "children"),
        Input("url", "pathname"),
    )
    def update_log_table(pathname):
        if pathname != "/data-engineer":
            return html.Div()
        log = get_data_engineer_log()
        if not log:
            return html.P("No log entries. Add days to data/data_engineer_log.json.", className="text-muted")
        rows = []
        for e in log:
            tasks_str = "; ".join(e.get("tasks", [])) if isinstance(e.get("tasks"), list) else str(e.get("tasks", ""))
            rows.append({
                "Day": e.get("day", "—"),
                "Date": e.get("date", "—"),
                "Tasks done": e.get("tasks_done", 0),
                "Tasks": tasks_str[:80] + ("..." if len(tasks_str) > 80 else ""),
                "Status": e.get("status", "—"),
                "Notes": (e.get("notes") or "")[:60],
            })
        df = pd.DataFrame(rows)
        return dbc.Table.from_dataframe(df, striped=True, bordered=True, size="sm", className="mb-0")

