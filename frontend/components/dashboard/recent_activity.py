import streamlit as st
import json


def render_recent_activity(reports):

    st.markdown("## 🕒 Recent Activity")

    if not reports:
        st.info("No reports available.")
        return

    # Show latest 5 reports
    reports = reports[:5]

    for i, report in enumerate(reports):

        # -------------------------
        # Parse Analysis
        # -------------------------

        analysis = {}

        try:

            raw_analysis = report.get("analysis", "{}")

            if isinstance(raw_analysis, str):
                analysis = json.loads(raw_analysis)
            else:
                analysis = raw_analysis

        except Exception:
            analysis = {}

        # -------------------------
        # Nested Analysis
        # -------------------------

        analysis_data = analysis.get("analysis", {})

        # -------------------------
        # Health Score
        # -------------------------

        health_score = analysis.get("health_score", 100)

        # -------------------------
        # Medicine Count
        # -------------------------

        medicines = analysis_data.get("medicines", [])

        medicine_count = len(medicines)

        # -------------------------
        # Other Details
        # -------------------------

        report_date = report.get("created_at", "")[:10]

        report_type = report.get(
            "document_type",
            "Prescription"
        )

        # -------------------------
        # Layout
        # -------------------------

        left, middle, right = st.columns([8,1,2])

        with left:

            with st.container(border=True):

                st.markdown(f"### 📄 {report_type}")

                st.caption(f"📅 {report_date}")

                st.write(f"💊 **{medicine_count} Medicine(s)**")

                st.progress(health_score / 100)

                st.caption(
                    f"Health Score : {health_score}/100"
                )

        with middle:

            st.metric(
                "Health",
                health_score
            )

        with right:

            if health_score >= 80:
                st.success("Excellent")

            elif health_score >= 60:
                st.warning("Average")

            else:
                st.error("Critical")

            st.button(
                "View Report",
                key=f"view_report_{report.get('id', i)}"
            )

        st.write("")