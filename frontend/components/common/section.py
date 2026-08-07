import streamlit as st


def section(title, icon="📄"):
    st.markdown(f"## {icon} {title}")