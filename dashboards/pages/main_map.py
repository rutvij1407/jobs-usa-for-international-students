"""
USA heat map page: most effective regions; hover = state name; click = state detail.
"""
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State, callback
import plotly.graph_objects as go
from backend.services.h1b_analytics import get_state_level_metrics
from dashboards.components.filters import map_filters_row


def layout():
    return dbc.Container(
        [
            html.H2("USA Job Market Heat Map", className="mb-3"),
            html.P(
                "Hover over a state to see its name; click to open the state detail page. "
                "Color shows job effectiveness (job count + H1B activity).",
                className="text-muted mb-3",
            ),
            map_filters_row(id_prefix="map"),
            dcc.Graph(id="usa-heatmap", config={"displayModeBar": True}),
            dcc.Store(id="map-click-store", data=None),
            dcc.Link(id="state-detail-link", href="/state/CA", style={"display": "none"}),
        ],
        fluid=True,
        className="py-4",
    )


def register_callbacks(app):
    @app.callback(
        Output("usa-heatmap", "figure"),
        Input("map-job-type", "value"),
        Input("map-company-type", "value"),
        Input("map-industry", "value"),
    )
    def update_heatmap(job_type, company_type, industry):
        df = get_state_level_metrics(
            job_type=job_type or "All",
            company_type=company_type or "All",
            industry=industry or "All",
        )
        fig = go.Figure(
            data=go.Choropleth(
                locations=df["state"],
                z=df["effectiveness_score"],
                locationmode="USA-states",
                colorscale="Reds",
                colorbar=dict(title="Effectiveness"),
                hoverinfo="text",
                hovertext=[
                    f"<b>{s}</b><br>Jobs: {j:,}<br>H1B petitions: {p:,}<br>Score: {e:,}"
                    for s, j, p, e in zip(
                        df["state"],
                        df["job_count"],
                        df["petitions"],
                        df["effectiveness_score"],
                    )
                ],
            ),
            layout=go.Layout(
                title="Job Effectiveness by State (hover for name, click for detail)",
                geo=dict(
                    scope="usa",
                    showlakes=True,
                    lakecolor="rgb(255,255,255)",
                ),
                margin=dict(l=0, r=0, t=40, b=0),
                height=550,
            ),
        )
        fig.update_traces(
            hoverlabel=dict(bgcolor="white", font_size=14, font_family="sans-serif")
        )
        return fig
