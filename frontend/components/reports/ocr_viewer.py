import streamlit as st


def render_ocr(text):

    with st.expander("📝 OCR Extracted Text"):

        if text:

            st.text_area(
                "OCR Extracted Text",
                value=text,
                height=250,
                disabled=True,
                label_visibility="collapsed"
            )

        else:

            st.info("OCR text unavailable.")