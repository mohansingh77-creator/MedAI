import streamlit as st

def render_header():

    st.markdown("""
    <div style="
        background:linear-gradient(90deg,#2563EB,#3B82F6);
        padding:25px;
        border-radius:18px;
        color:white;
        margin-bottom:20px;
    ">

    <h1 style="margin:0;">
    🏥 MedAI
    </h1>

    <p style="
        margin-top:8px;
        font-size:18px;
        opacity:0.95;
    ">
    Your Personal Health Assistant
    </p>

    </div>
    """,
    unsafe_allow_html=True)