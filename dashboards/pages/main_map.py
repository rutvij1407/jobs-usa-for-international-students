"""
USA map page: Google Earth iframe (lightweight) + KML from backend. Optional Plotly chart.
"""
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, callback
import plotly.express as px
from backend.services.h1b_analytics import get_state_level_metrics
from dashboards.components.filters import map_filters_row


def layout():
    return html.Div(
        className="page-content-wrap page-content-wrap--animate",
        children=[
            html.Div(
                [
                    html.H1("USA Job Market", className="page-title"),
                    html.P(
                        "Interactive USA map by state. Download KML to open in Google Earth (new tab). Filters apply to map and KML.",
                        className="page-subtitle",
                    ),
                ],
                className="mb-4",
            ),
            html.Div(map_filters_row(id_prefix="map"), className="filter-row"),
            html.Div(
                [
                    html.A(
                        "Open Google Earth in a new tab",
                        href="https://earth.google.com/web/@40,-95,0a,5000000d,35y,0h,0t,0r",
                        target="_blank",
                        rel="noopener noreferrer",
                        className="btn btn-outline-secondary btn-sm mb-2",
                    ),
                    html.Span(" (Google blocks embedding here, so we link out.)", className="text-muted small ms-1"),
                ],
                className="mb-2",
            ),
            html.Div(
                [
                    dcc.Graph(
                        id="usa-heatmap",
                        config={"displayModeBar": True, "responsive": True},
                        style={"height": "520px", "width": "100%"},
                    ),
                ],
                className="map-container",
            ),
            html.Div(
                [
                    html.A(
                        "Download H1B data (KML)",
                        id="kml-download-link",
                        href="/api/h1b.kml?job_type=All&company_type=All&industry=All",
                        target="_blank",
                        className="btn btn-outline-primary btn-sm me-2",
                    ),
                    html.Span(" Open the KML file in Google Earth to see state-level markers.", className="text-muted small"),
                ],
                className="mt-3 mb-4",
            ),
            dcc.Store(id="map-click-store", data=None),
        ],
    )


def register_callbacks(app):
    @app.callback(
        Output("kml-download-link", "href"),
        Input("map-job-type", "value"),
        Input("map-company-type", "value"),
        Input("map-industry", "value"),
    )
    def update_kml_link(job_type, company_type, industry):
        from urllib.parse import urlencode
        params = urlencode({
            "job_type": job_type or "All",
            "company_type": company_type or "All",
            "industry": industry or "All",
        })
        return f"/api/h1b.kml?{params}"

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
        fig = px.choropleth(
            df,
            locations="state",
            locationmode="USA-states",
            color="effectiveness_score",
            scope="usa",
            color_continuous_scale="Reds",
            labels={"effectiveness_score": "Effectiveness", "state": "State"},
            hover_name="state",
            hover_data={"state": False, "job_count": True, "petitions": True, "effectiveness_score": True},
        )
        fig.update_layout(
            title=dict(text="Job effectiveness by state", font=dict(size=16)),
            margin=dict(l=0, r=0, t=40, b=0),
            height=520,
        )
        fig.update_geos(bgcolor="rgba(248,249,250,1)")
        fig.update_traces(hoverlabel=dict(bgcolor="white", font_size=13))
        return fig
