import streamlit as st
import requests
import json
from pathlib import Path

from components.common.header import render_header
from components.dashboard.hero import render_hero
from components.dashboard.quick_actions import render_quick_actions
from components.dashboard.recent_activity import render_recent_activity
from components.common.metric_card import metric_card

# ----------------------------------    
# Page Config
# ----------------------------------

st.set_page_config(

    page_title="MedAI Healthcare",

    page_icon="🏥",

    layout="wide",

    initial_sidebar_state="expanded"
)

render_hero(
    title="MedAI v1.0",
    subtitle="AI-Powered Medical Document Interpretation",
    description="Upload prescriptions, laboratory reports and other medical documents to receive AI-assisted clinical interpretation."
)


# ----------------------------------
# Load Global CSS
# ----------------------------------

css_file = Path(__file__).parent / "assets" / "style.css"

with open(css_file) as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )


# ----------------------------------
# Header
# ----------------------------------

# render_header()

st.write("")

# ----------------------------------
# Load Reports
# ----------------------------------

from utils.api import REPORTS_URL

try:
    response = requests.get(REPORTS_URL)
    reports = response.json()

except Exception:
    reports = []

# Dashboard Statistics

total_reports = len(reports)

prescriptions = sum(
    1 for r in reports
    if r.get("document_type") == "Prescription"
)

lab_reports = sum(
    1 for r in reports
    if r.get("document_type") == "Lab Report"
)

scores = []

for r in reports:

    try:
        analysis = r.get("analysis", {})

        if isinstance(analysis, str):
            analysis = json.loads(analysis)

        scores.append(
            analysis.get("health_score", 100)
        )

    except Exception:
        pass

average_score = (
    round(sum(scores) / len(scores), 1)
    if scores else 100
)

# ----------------------------------
# Dashboard
# ----------------------------------

c1, c2, c3, c4 = st.columns(4)

with c1:
    metric_card(
        "📄",
        "Total Reports",
        total_reports,
        "Total uploaded"
    )

with c2:
    metric_card(
        "❤️",
        "Health Score",
        average_score,
        "Average"
    )

with c3:
    metric_card(
        "💊",
        "Prescriptions",
        prescriptions,
        "Detected"
    )

with c4:
    metric_card(
        "🧪",
        "Lab Reports",
        lab_reports,
        "Processed"
    )

st.divider()

render_quick_actions()

st.divider()

render_recent_activity(reports)