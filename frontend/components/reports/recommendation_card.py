import streamlit as st


def render_recommendations(recommendations):

    if not recommendations:
        return

    with st.container(border=True):

        st.subheader("👨‍⚕️ Doctor Advice")

        for advice in recommendations:

            st.markdown(
                f"""
                <div style="
                    padding:12px;
                    margin-bottom:10px;
                    border-left:5px solid #2E86DE;
                    background:#F8F9FA;
                    border-radius:8px;
                ">
                    ✔ {advice}
                </div>
                """,
                unsafe_allow_html=True
            )