import streamlit as st

def stat_card(icon, title, value, subtitle=""):

    st.markdown(
        f"""
<div style="
background:#FFFFFF;
border-radius:16px;
padding:20px;
border:1px solid #E5E7EB;
box-shadow:0 3px 8px rgba(0,0,0,.05);
text-align:center;
min-height:140px;
">

<div style="font-size:34px;">
{icon}
</div>

<div style="
color:#6B7280;
font-size:15px;
margin-top:8px;
">
{title}
</div>

<div style="
font-size:34px;
font-weight:700;
color:#2563EB;
margin-top:5px;
">
{value}
</div>

<div style="
color:#9CA3AF;
font-size:13px;
">
{subtitle}
</div>

</div>
""",
        unsafe_allow_html=True,
    )