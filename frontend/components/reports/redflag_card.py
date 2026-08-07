import streamlit as st


def render_red_flags(red_flags):

    with st.container(border=True):

        st.subheader("🚨 Red Flags")

        if not red_flags:
            st.success("No major red flags detected.")
            return

        for flag in red_flags:

            st.error(flag)