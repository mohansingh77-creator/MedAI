import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import json

from utils.api import REPORTS_URL

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 MedAI Analytics Dashboard")

# ==========================================================
# Load Reports
# ==========================================================

try:
    response = requests.get(REPORTS_URL, timeout=10)

    if response.status_code != 200:
        st.error("Unable to load dashboard data.")
        st.stop()

    reports = response.json()

except Exception as e:
    st.error(f"Backend Error: {e}")
    st.stop()

if not reports:
    st.info("No reports found.")
    st.stop()

# ==========================================================
# Prepare Data
# ==========================================================

rows = []

for report in reports:

    # Handle SQLAlchemy model or dict
    if isinstance(report, str):
        try:
            report = json.loads(report)
        except:
            continue

    analysis = {}

    try:
        analysis = json.loads(report.get("analysis", "{}"))
    except:
        pass

    rows.append(
        {
            "Document": report.get("document_type", "Unknown"),
            "Patient": report.get("patient_name", "Unknown Patient"),
            "Health Score": analysis.get("health_score", 0),
        }
    )

df = pd.DataFrame(rows)

# ==========================================================
# Normalize Patient Names
# ==========================================================

df["Patient"] = (
    df["Patient"]
    .fillna("")
    .astype(str)
    .str.strip()
)

df["Patient"] = df["Patient"].replace(
    {
        "": "Unknown Patient",
        "0": "Unknown Patient",
        "Unknown": "Unknown Patient",
        "unknown": "Unknown Patient",
        "None": "Unknown Patient",
        "nan": "Unknown Patient",
    }
)

df["Patient"] = df["Patient"].str.title()

patients = df["Patient"].nunique()

# ==========================================================
# KPIs
# ==========================================================

prescriptions = (
    df["Document"]
    .fillna("")
    .str.lower()
    .str.contains("prescription")
    .sum()
)

lab_reports = (
    df["Document"]
    .fillna("")
    .str.lower()
    .str.contains("lab")
    .sum()
)

avg_score = round(pd.to_numeric(df["Health Score"]).mean())

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("📄 Total Reports", len(df))
c2.metric("👤 Patients", patients)
c3.metric("💊 Prescriptions", prescriptions)
c4.metric("🧪 Lab Reports", lab_reports)
c5.metric("❤️ Avg Health Score", avg_score)

st.divider()

# ==========================================================
# Charts
# ==========================================================

left, right = st.columns(2)

fig = px.pie(
    df,
    names="Document",
    hole=0.45,
    title="📄 Document Distribution"
)

fig.update_traces(
    textposition="inside",
    textinfo="percent+label"
)

with left:
    st.plotly_chart(
        fig,
        use_container_width=True
    )

fig2 = px.histogram(
    df,
    x="Health Score",
    nbins=10,
    title="❤️ Health Score Analytics"
)

fig2.update_layout(
    xaxis_title="Health Score",
    yaxis_title="Number of Reports"
)

with right:
    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# ==========================================================
# Clinical Insights
# ==========================================================

st.divider()

st.subheader("🩺 Clinical Insights")

if avg_score >= 90:
    status = "🟢 Excellent"
elif avg_score >= 75:
    status = "🟡 Good"
else:
    status = "🔴 Needs Attention"

st.info(
    f"""
**MedAI Analysis Summary**

• **Total Reports:** {len(df)}

• **Patients:** {patients}

• **Prescription Reports:** {prescriptions}

• **Lab Reports:** {lab_reports}

• **Average Health Score:** {avg_score}/100

• **Overall Health Status:** {status}
"""
)