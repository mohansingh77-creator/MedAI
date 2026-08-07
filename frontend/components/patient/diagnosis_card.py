import streamlit as st


def render_diagnosis(diagnosis):

    st.markdown("## 🩺 Clinical Findings")

    st.caption(
        "Clinical conditions identified from the uploaded prescription."
    )

    if not diagnosis:
        st.info("No clinical findings detected.")
        return

    for item in diagnosis:

        if isinstance(item, dict):
            name = item.get("name", "Unknown Finding")
        else:
            name = str(item)

        with st.container(border=True):

            col1, col2 = st.columns([4, 1])

            with col1:
                st.markdown(f"### 🩺 {name}")
                st.caption("Extracted from the uploaded prescription")

            with col2:
                st.success("Identified")