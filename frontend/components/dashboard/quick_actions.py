import streamlit as st


def action_card(icon, title, subtitle):

    with st.container(border=True):

        st.markdown(
            f"""
<div style="text-align:center;padding:18px;">

<div style="font-size:42px;">
{icon}
</div>

<div style="
font-size:20px;
font-weight:700;
margin-top:10px;
color:#1F2937;">
{title}
</div>

<div style="
font-size:14px;
color:#6B7280;
margin-top:6px;">
{subtitle}
</div>

</div>
""",
            unsafe_allow_html=True,
        )


def render_quick_actions():

    st.markdown("## ⚡ Quick Actions")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        action_card(
            "📄",
            "Analyze Prescription",
            "Upload & Analyze"
        )

    with c2:
        action_card(
            "🧪",
            "Analyze Lab Report",
            "Blood Tests"
        )

    with c3:
        action_card(
            "💊",
            "Medicine Library",
            "Search Medicines"
        )

    with c4:
        action_card(
            "📜",
            "Report History",
            "Previous Reports"
        )