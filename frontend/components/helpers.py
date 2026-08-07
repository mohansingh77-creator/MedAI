import streamlit as st

def show_field(label, value):
    st.markdown(f"""
    <div class="label">{label}</div>
    <div class="value">{value}</div>
    """, unsafe_allow_html=True)