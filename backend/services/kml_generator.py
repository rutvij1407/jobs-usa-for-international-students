"""
Generate KML from H1B/job data for Google Earth. Lightweight alternative to heavy JS maps.
"""
import html
from typing import List, Dict, Any


def generate_h1b_kml(places: List[Dict[str, Any]]) -> str:
    """
    Generate KML document for Google Earth.
    Each item in places should have: name (or state), description (optional), longitude, latitude,
    and optionally title, company, salary for job-style placemarks.
    """
    kml = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.org/kml/2.2">
  <Document>
    <name>H1B Jobs USA</name>
    <description>State-level job and H1B metrics</description>
    <Style id="h1b-marker">
      <IconStyle>
        <color>ff0000ff</color>
        <scale>0.8</scale>
      </IconStyle>
      <LabelStyle>
        <scale>0.8</scale>
      </LabelStyle>
    </Style>
"""
    for place in places:
        name = place.get("name") or place.get("state") or "Location"
        desc = place.get("description") or _description_from_place(place)
        lng = place.get("longitude") or place.get("lng", 0)
        lat = place.get("latitude") or place.get("lat", 0)
        desc_safe = desc.replace("]]>", "]]]]><![CDATA[>").replace("\n", "<br/>")
        kml += f"""
    <Placemark>
      <name>{html.escape(name)}</name>
      <description><![CDATA[{desc_safe}]]></description>
      <styleUrl>#h1b-marker</styleUrl>
      <Point>
        <coordinates>{lng},{lat},0</coordinates>
      </Point>
    </Placemark>
"""
    kml += "  </Document>\n</kml>"
    return kml


def _description_from_place(place: Dict[str, Any]) -> str:
    """Build description from common fields (state-level or job-level)."""
    parts = []
    if place.get("title"):
        parts.append(f"Position: {place['title']}")
    if place.get("company"):
        parts.append(f"Company: {place['company']}")
    if place.get("salary") is not None:
        parts.append(f"Salary: ${place['salary']}")
    if place.get("job_count") is not None:
        parts.append(f"Job count: {place['job_count']:,}")
    if place.get("petitions") is not None:
        parts.append(f"H1B petitions: {place['petitions']:,}")
    if place.get("effectiveness_score") is not None:
        parts.append(f"Effectiveness score: {place['effectiveness_score']:,}")
    return "<br/>".join(parts) if parts else "—"
