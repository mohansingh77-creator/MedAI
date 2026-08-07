import streamlit as st


def metric_card(
    icon,
    title,
    value,
    subtitle="",
    color="#2563EB"
):

    with st.container(border=True):

        # Icon
        st.markdown(
            f"""
            <div style="text-align:center; font-size:38px; margin-top:8px;">
                {icon}
            </div>
            """,
            unsafe_allow_html=True
        )

        # Title
        st.markdown(
            f"""
            <div style="
                text-align:center;
                color:#64748B;
                font-size:16px;
                font-weight:600;
                margin-top:6px;
            ">
                {title}
            </div>
            """,
            unsafe_allow_html=True
        )

        # Value
        st.markdown(
            f"""
            <div style="
                text-align:center;
                font-size:34px;
                font-weight:700;
                color:{color};
                margin-top:12px;
                margin-bottom:8px;
            ">
                {value}
            </div>
            """,
            unsafe_allow_html=True
        )

        # Subtitle
        st.markdown(
            f"""
            <div style="
                text-align:center;
                color:#94A3B8;
                font-size:13px;
                margin-bottom:8px;
            ">
                {subtitle}
            </div>
            """,
            unsafe_allow_html=True
        )