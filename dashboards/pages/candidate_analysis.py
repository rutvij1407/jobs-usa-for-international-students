"""
Candidate analysis dashboard: upload resume, get scores and suggestions.
"""
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State, callback
from pathlib import Path
import base64
import io
from backend.services.resume_analyzer import extract_resume_text, analyze_resume
from config.settings import UPLOADS_DIR


def layout():
    return dbc.Container(
        [
            html.H2("Candidate Analysis", className="mb-3"),
            html.P(
                "Upload your resume (PDF or DOCX). We'll parse it and suggest improvements for F1/ATS.",
                className="text-muted mb-3",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Upload(
                                id="resume-upload",
                                children=dbc.Button("Choose file (PDF/DOCX)", color="primary", className="mb-2"),
                                multiple=False,
                            ),
                            html.Div(id="upload-filename", className="small text-muted mb-2"),
                            html.Label("Optional: paste job description for match score", className="small"),
                            dcc.Textarea(
                                id="job-description",
                                placeholder="Paste job description here...",
                                style={"width": "100%", "height": 100},
                                className="mb-2",
                            ),
                            dbc.Button("Analyze", id="analyze-btn", color="success", className="mb-3"),
                        ],
                        width=4,
                    ),
                    dbc.Col(
                        [
                            html.Div(id="resume-analysis-result"),
                        ],
                        width=8,
                    ),
                ],
                className="mb-4",
            ),
        ],
        fluid=True,
        className="py-4",
    )


def parse_upload(contents):
    """Decode upload and save to temp file; return path."""
    if not contents:
        return None
    try:
        content_type, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)
        suffix = ".pdf" if "pdf" in content_type else ".docx"
        path = UPLOADS_DIR / f"upload{suffix}"
        path.write_bytes(decoded)
        return path
    except Exception:
        return None


def register_callbacks(app):
    @app.callback(
        Output("upload-filename", "children"),
        Input("resume-upload", "contents"),
    )
    def show_filename(contents):
        if not contents:
            return ""
        return "File received. Click Analyze."

    @app.callback(
        Output("resume-analysis-result", "children"),
        Input("analyze-btn", "n_clicks"),
        State("resume-upload", "contents"),
        State("job-description", "value"),
        prevent_initial_call=True,
    )
    def run_analysis(n_clicks, contents, jd):
        if not n_clicks or not contents:
            return html.Div("Upload a resume and click Analyze.")
        path = parse_upload(contents)
        if not path:
            return html.Div("Could not read file. Use PDF or DOCX.")
        text = extract_resume_text(path)
        if not text.strip():
            return html.Div("No text extracted. Check file format.")
        result = analyze_resume(text, jd or "")
        cards = [
            dbc.Card(
                [dbc.CardBody([html.H6("ATS-style score"), html.H4(f"{result['ats_score']}/100")])],
                className="mb-2",
            ),
            dbc.Card(
                [dbc.CardBody([html.H6("F1 / work-auth relevance"), html.H4(f"{result['f1_score']}/100")])],
                className="mb-2",
            ),
            dbc.Card(
                [dbc.CardBody([html.H6("Word count"), html.P(str(result["word_count"]))])],
                className="mb-2",
            ),
        ]
        suggestions = result.get("suggestions", [])
        suggestion_list = html.Ul([html.Li(s) for s in suggestions]) if suggestions else html.P("No specific suggestions.")
        keywords_found = result.get("keywords_found", [])[:15]
        keywords_missing = result.get("keywords_missing", [])[:10]
        return html.Div(
            [
                html.H5("Scores"),
                dbc.Row([dbc.Col(c, width=4) for c in cards]),
                html.H5("Suggestions", className="mt-3"),
                suggestion_list,
                html.H6("Keywords found", className="mt-2"),
                html.P(", ".join(keywords_found) if keywords_found else "—"),
                html.H6("Consider adding (if relevant)"),
                html.P(", ".join(keywords_missing) if keywords_missing else "—"),
            ]
        )
