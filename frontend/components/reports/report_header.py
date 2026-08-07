import streamlit as st
from datetime import datetime


def render_report_header(
    patient_name="Unknown Patient",
    document_type="Medical Document"
):

    report_id = f"MED-{datetime.now().strftime('%Y%m%d')}-001"
    generated = datetime.now().strftime("%d %b %Y, %I:%M %p")
    patient_id = f"P-{abs(hash(patient_name)) % 9000 + 1000}"

    with st.container(border=True):

        # -----------------------------
        # Header Row
        # -----------------------------

        left, right = st.columns([5, 1])

        with left:

            st.markdown("# 🏥 MedAI Healthcare")

            st.markdown(
                "**AI Clinical Medical Document Interpretation Report**"
            )

            st.caption(
                "AI-assisted interpretation for prescriptions, laboratory reports and clinical documents."
            )

        with right:

            st.success("✔ Verified")

        st.divider()

        # -----------------------------
        # Information Row
        # -----------------------------

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "Report ID",
                report_id
            )

        with c2:
            st.metric(
                "Generated",
                generated
            )

        with c3:
            st.metric(
                "Patient",
                patient_name
            )

        with c4:
            st.metric(
                "Patient ID",
                patient_id
            )