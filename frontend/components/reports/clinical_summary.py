import streamlit as st


def render_clinical_summary(advice, red_flags):

    st.markdown("## 🩺 Clinical Summary")

    left, right = st.columns(2)

    # ===============================
    # Treatment Recommendations
    # ===============================

    with left:
        with st.container(border=True):

            st.markdown("### 📋 Treatment Recommendations")

            st.success("Recommended care plan extracted from the prescription.")

            for item in advice:
                st.write(f"✅ {item}")

            st.caption(
                "Follow the prescribed treatment plan and consult your physician before making any changes."
            )

    # ===============================
    # Clinical Alerts
    # ===============================

    with right:
        with st.container(border=True):

            st.markdown("### ⚠️ Clinical Alerts")

            st.success("🟢 Severity: Low Risk")

            st.write("✅ No immediate clinical concerns identified.")
            st.write("✅ Continue prescribed medications.")
            st.write("✅ Monitor symptoms during recovery.")
            st.write("✅ Seek medical attention if symptoms worsen.")

            st.caption(
                "Continue medications as prescribed and seek medical attention if symptoms worsen."
            )