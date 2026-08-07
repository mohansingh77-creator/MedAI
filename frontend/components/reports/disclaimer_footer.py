import streamlit as st


def render_disclaimer():

    st.markdown("## ⚠️ Clinical Disclaimer")

    with st.container(border=True):

        st.warning(
            """
            **This report is AI-generated and is intended to assist in interpreting medical documents.**

            It does **not replace** diagnosis, treatment planning, or consultation with a licensed healthcare professional.

            **Always follow the advice of your treating physician.**
            """
        )

        st.divider()

        left, right = st.columns(2)

        with left:
            st.caption("🏥 MedAI Healthcare")
            st.caption("Clinical AI Platform • Version 1.0")

        with right:
            st.caption("🔒 Confidential Medical Document")
            st.caption("Generated for Patient Use")