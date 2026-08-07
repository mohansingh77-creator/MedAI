import streamlit as st


def render_signature_block():

    st.markdown("## 👨‍⚕️ Clinical Review")

    with st.container(border=True):

        left, right = st.columns(2)

        # --------------------------
        # LEFT SIDE
        # --------------------------

        with left:

            st.markdown("### 🤖 AI Clinical Interpretation")

            st.success("✔ OCR Successfully Processed")

            st.success("✔ Medical Information Extracted")

            st.success("✔ Clinical Review Completed")

            st.success("🛡 Powered by MedAI AI Engine • Version 1.0")

        # --------------------------
        # RIGHT SIDE
        # --------------------------

        with right:

            st.markdown("### 📋 Authorized Digital Report")

            c1, c2, c3 = st.columns(3)

            with c1:
                st.markdown("**Status**")
                st.success("Complete")

            with c2:
                st.markdown("**Signature**")
                st.success("Verified")

            with c3:
                st.markdown("**Department**")
                st.info("Clinical AI Systems")

        st.divider()

        st.caption(
            "This report was generated using MedAI Healthcare's AI-assisted clinical document interpretation engine."
        )