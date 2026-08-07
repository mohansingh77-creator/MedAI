import streamlit as st
import pandas as pd


def render_lab_findings(lab):

    with st.container(border=True):

        st.subheader("🧪 Lab Findings")

        if not lab:

            st.info(
                "No laboratory values were detected in the uploaded document."
            )

            st.caption(
                "This document appears to be a prescription rather than a laboratory report."
            )

            return

        if isinstance(lab, dict):

            df = pd.DataFrame(
                [
                    {
                        "Test": k,
                        "Result": v
                    }
                    for k, v in lab.items()
                ]
            )

        elif isinstance(lab, list):

            df = pd.DataFrame(lab)

        else:

            st.write(lab)
            return

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            height=min(350, (len(df) + 1) * 38)
        )

        st.caption(
            "Laboratory findings extracted from the uploaded medical document."
        )