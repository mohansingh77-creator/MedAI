import streamlit as st


def render_health_score(score: int):

    # -----------------------------
    # Calculate Status
    # -----------------------------
    if score >= 90:
        status = "🟢 Excellent"
        message = "Overall health appears excellent."

    elif score >= 75:
        status = "🔵 Good"
        message = "Minor observations. Continue healthy habits."

    elif score >= 60:
        status = "🟠 Needs Attention"
        message = "Follow the doctor's advice carefully."

    else:
        status = "🔴 Critical"
        message = "Medical follow-up is strongly recommended."

    # -----------------------------
    # Card
    # -----------------------------
    with st.container(border=True):

        st.subheader("❤️ Health Score")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.metric(
                label="Overall Score",
                value=f"{score}/100"
            )

        with col2:
            st.markdown("###")
            st.success(status)

        st.progress(score / 100)

        st.caption(message)