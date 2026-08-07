import streamlit as st


def info_card(title, data):

    with st.container(border=True):

        st.markdown(f"### {title}")

        for key, value in data.items():

            st.markdown(
                f"**{key}:** {value if value else '-'}"
            )