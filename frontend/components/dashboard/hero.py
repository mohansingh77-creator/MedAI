import streamlit as st


def render_hero(
    title="MedAI v1.0",
    subtitle="AI-Powered Medical Document Interpretation",
    description="Upload prescriptions, laboratory reports and other medical documents to receive AI-assisted clinical interpretation."
):

    with st.container(border=True):

        left, right = st.columns([5, 1])

        with left:

            st.title(f"🏥 {title}")

            st.markdown(f"### {subtitle}")

            st.caption(description)

            st.markdown(
                """
                <div style="margin-top:12px; color:#475569; font-size:14px;">
                ✅ AI Powered&nbsp;&nbsp;&nbsp;&nbsp;
                ✅ OCR Enabled&nbsp;&nbsp;&nbsp;&nbsp;
                ✅ Clinical Decision Support&nbsp;&nbsp;&nbsp;&nbsp;
                ✅ Professional PDF Reports
                </div>
                """,
                unsafe_allow_html=True,
            )

        with right:

            st.markdown(
                """
                <div style="
                    background:#ECFDF5;
                    border:1px solid #A7F3D0;
                    border-radius:10px;
                    padding:18px;
                    text-align:center;
                    margin-top:8px;
                ">
                    <div style="font-size:22px;">🚀</div>
                    <div style="font-weight:700;font-size:18px;color:#065F46;">
                        MedAI
                    </div>
                    <div style="font-size:14px;color:#047857;">
                        Version 1.0
                    </div>
                    <div style="font-size:12px;color:#6B7280;margin-top:6px;">
                        Production Ready
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )