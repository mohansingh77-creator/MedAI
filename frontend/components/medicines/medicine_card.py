import streamlit as st
import pandas as pd


def render_medicines(medicines):

    st.markdown("## 💊 Prescribed Medicines")

    if not medicines:
        st.info("No medicines detected.")
        return

    rows = []

    for med in medicines:

        precautions = med.get("precautions", [])

        if isinstance(precautions, list):
            precautions = ", ".join(precautions[:2])

        rows.append({
            "💊 Medicine": med.get("name", "-"),
            "💉 Dosage": med.get("dosage", "-"),
            "🕒 When to Take": med.get("frequency", "-"),
            "🎯 Purpose": med.get("purpose", "-"),
            "⚠ Precautions": precautions or "-"
        })

    df = pd.DataFrame(rows)

    st.table(df)

    st.caption(
        "Clinical medication summary generated from the uploaded prescription."
    )