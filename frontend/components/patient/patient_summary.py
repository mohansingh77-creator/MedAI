import streamlit as st


def render_patient_summary(patient, doctor_name, visit_date, health_score=100):

    diagnosis = patient.get(
        "diagnosis",
        "Lumbar Radiculopathy / Sciatica"
    )

    status = "Excellent"

    if health_score < 80:
        status = "Stable"

    if health_score < 60:
        status = "Needs Attention"

    st.markdown("## 👤 Patient Information")

    with st.container(border=True):

        left, right = st.columns([4, 1])

        with left:

            st.markdown(
                f"""
                <div style="font-size:34px;font-weight:700;">
                    {patient.get("name","Unknown Patient")}
                </div>

                <div style="
                    color:#64748B;
                    margin-top:4px;
                    font-size:15px;
                ">
                    Medical Record Summary
                </div>
                """,
                unsafe_allow_html=True
            )

        with right:

            if status == "Excellent":
                st.success(status)
            elif status == "Stable":
                st.warning(status)
            else:
                st.error(status)

        st.divider()

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.markdown("**Age**")
            st.markdown(
                f"<h2>{patient.get('age','-')} Years</h2>",
                unsafe_allow_html=True
            )

        with c2:
            st.markdown("**Gender**")
            st.markdown(
                f"<h2>{patient.get('gender','-')}</h2>",
                unsafe_allow_html=True
            )

        with c3:
            st.markdown("**Visit Date**")
            st.markdown(
                f"<h3>{visit_date or '-'}</h3>",
                unsafe_allow_html=True
            )

        with c4:
            st.markdown("**Health Score**")
            st.markdown(
                f"<h2>{health_score}/100</h2>",
                unsafe_allow_html=True
            )

        st.divider()

        left, right = st.columns([2,2])

        with left:

            st.markdown("### Visit Information")

            st.markdown(
                f"""
                **Consulting Doctor:** {doctor_name or '-'}  

                **Visit Date:** {visit_date or '-'}
                """
            )

        with right:

            st.markdown("### Primary Diagnosis")

            st.info(diagnosis)

            st.markdown(
                f"""
                **Clinical Assessment:** **{status}**
                """
            )