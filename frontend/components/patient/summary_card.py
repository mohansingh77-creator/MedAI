import streamlit as st


def render_summary(summary, diagnosis):

    st.markdown("## 🩺 Understanding Your Prescription")

    with st.container(border=True):

        st.success(
            "This section explains your prescription in patient-friendly language."
        )

        # =====================================================
        # Build diagnosis text for condition detection
        # =====================================================

        diagnosis_text = ""

        if isinstance(diagnosis, list):

            names = []

            for item in diagnosis:

                if isinstance(item, dict):
                    names.append(item.get("name", ""))

                else:
                    names.append(str(item))

            diagnosis_text = " ".join(names)

        elif isinstance(diagnosis, dict):

            diagnosis_text = diagnosis.get("name", "")

        else:

            diagnosis_text = str(diagnosis)

        diagnosis_text = diagnosis_text.lower()

        # =====================================================
        # Condition-specific content
        # =====================================================

        if (
            "pivd" in diagnosis_text
            or "lumbar" in diagnosis_text
            or "sciatica" in diagnosis_text
            or "stenosis" in diagnosis_text
            or "radiculopathy" in diagnosis_text
        ):

            goals = [
                "Reduce nerve pain.",
                "Reduce inflammation.",
                "Support nerve healing.",
                "Improve movement and daily activities."
            ]

            tips = [
                "Take medicines exactly as prescribed.",
                "Continue physiotherapy if advised.",
                "Avoid heavy lifting.",
                "Avoid prolonged sitting.",
                "Maintain good posture.",
                "Sleep on a firm mattress if recommended."
            ]

            warnings = [
                "Pain becomes severe.",
                "Weakness develops in your legs.",
                "Difficulty walking.",
                "Loss of bladder or bowel control.",
                "Allergic reaction after taking medicines."
            ]

        else:

            goals = [
                "Relieve symptoms.",
                "Treat the underlying condition.",
                "Support recovery."
            ]

            tips = [
                "Take medicines exactly as prescribed.",
                "Complete the full course.",
                "Drink enough water.",
                "Follow your doctor's advice."
            ]

            warnings = [
                "Symptoms become worse.",
                "New symptoms appear.",
                "Severe side effects occur."
            ]

        # =====================================================
        # Simple explanation
        # =====================================================

        st.markdown("### 📖 In Simple Words")

        if isinstance(diagnosis, list) and len(diagnosis) > 0:

            for item in diagnosis:

                if isinstance(item, dict):

                    st.markdown(
                        f"**{item.get('name','Unknown Condition')}**"
                    )

                    st.write(
                        item.get(
                            "simple_explanation",
                            summary
                        )
                    )

                    st.write("")

        else:

            if summary:
                st.write(summary)
            else:
                st.write(
                    "Your prescription has been analysed successfully."
                )

        # =====================================================
        # Treatment Goals
        # =====================================================

        st.divider()

        st.markdown("### 🎯 Treatment Goals")

        for goal in goals:
            st.write(f"✅ {goal}")

        # =====================================================
        # Tips
        # =====================================================

        st.divider()

        st.markdown("### 💡 Important Tips")

        for tip in tips:
            st.write(f"• {tip}")

        # =====================================================
        # Warnings
        # =====================================================

        st.divider()

        st.markdown("### 🚨 Contact Your Doctor If")

        for warning in warnings:
            st.write(f"⚠️ {warning}")