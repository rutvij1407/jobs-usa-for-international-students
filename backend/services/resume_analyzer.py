"""
Resume analysis: parse PDF/DOCX, extract text, suggest improvements (keywords, ATS).
"""
import re
from pathlib import Path
from typing import Dict, List, Any

try:
    import pdfplumber
except ImportError:
    pdfplumber = None
try:
    from docx import Document as DocxDocument
except ImportError:
    DocxDocument = None

# F1/H1B-friendly and ATS keywords (sample; extend as needed)
F1_KEYWORDS = [
    "authorized to work", "sponsorship", "H1B", "OPT", "CPT", "F1", "work authorization",
    "eligible to work", "US work authorization", "immigration", "visa",
]
COMMON_SKILL_KEYWORDS = [
    "Python", "SQL", "JavaScript", "Java", "R", "machine learning", "data analysis",
    "Excel", "Tableau", "Power BI", "communication", "leadership", "project management",
    "agile", "scrum", "Git", "AWS", "cloud", "REST API", "statistics",
]


def _extract_text_pdf(file_path: Path) -> str:
    """Extract text from PDF using pdfplumber."""
    if not pdfplumber:
        return ""
    text_parts = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text_parts.append(t)
    return "\n".join(text_parts)


def _extract_text_docx(file_path: Path) -> str:
    """Extract text from DOCX."""
    if not DocxDocument:
        return ""
    doc = DocxDocument(file_path)
    return "\n".join(p.text for p in doc.paragraphs)


def extract_resume_text(file_path: Path) -> str:
    """Extract raw text from resume (PDF or DOCX)."""
    path = Path(file_path)
    if not path.exists():
        return ""
    suf = path.suffix.lower()
    if suf == ".pdf":
        return _extract_text_pdf(path)
    if suf in (".docx", ".doc"):
        return _extract_text_docx(path)
    if suf == ".txt":
        return path.read_text(encoding="utf-8", errors="ignore")
    return ""


def analyze_resume(text: str, job_description: str = "") -> Dict[str, Any]:
    """
    Analyze resume text and return scores + suggestions.
    - ats_score: rough keyword match (0-100)
    - f1_score: presence of work-auth/sponsorship keywords
    - suggestions: list of strings
    - keywords_found / keywords_missing
    """
    text_lower = (text or "").lower()
    jd_lower = (job_description or "").lower()
    all_keywords = list(set(COMMON_SKILL_KEYWORDS + F1_KEYWORDS + re.findall(r"\b[a-z]{4,}\b", jd_lower)[:30]))

    keywords_found = [k for k in all_keywords if k.lower() in text_lower]
    keywords_missing = [k for k in COMMON_SKILL_KEYWORDS + F1_KEYWORDS if k.lower() not in text_lower][:20]

    # ATS-style score: share of common + JD keywords found
    relevant = [k for k in all_keywords if k.lower() in (text_lower + " " + jd_lower)]
    ats_score = min(100, int(50 + 50 * len(keywords_found) / max(1, len(set(COMMON_SKILL_KEYWORDS + F1_KEYWORDS)))))

    f1_found = [k for k in F1_KEYWORDS if k.lower() in text_lower]
    f1_score = min(100, int(30 + 70 * len(f1_found) / max(1, len(F1_KEYWORDS))))

    suggestions = []
    if not any(k in text_lower for k in ["work authorization", "authorized", "eligib"]):
        suggestions.append("Add a clear 'Work Authorization' or 'Eligibility to Work' line (e.g., F1 OPT, H1B).")
    if len(text.strip()) < 200:
        suggestions.append("Resume may be too short; add more bullet points for projects and experience.")
    if "objective" not in text_lower and "summary" not in text_lower:
        suggestions.append("Consider adding a short Professional Summary or Objective at the top.")
    for kw in keywords_missing[:5]:
        if kw in COMMON_SKILL_KEYWORDS:
            suggestions.append(f"If relevant, consider mentioning: {kw}.")

    return {
        "ats_score": ats_score,
        "f1_score": f1_score,
        "word_count": len(text.split()),
        "keywords_found": keywords_found[:30],
        "keywords_missing": keywords_missing[:15],
        "f1_keywords_found": f1_found,
        "suggestions": suggestions[:10],
    }
