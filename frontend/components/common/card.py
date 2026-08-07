import streamlit as st


def render_card(title, fields):
    """
    Generic reusable card component.

    Parameters
    ----------
    title : str
        Card title (e.g. 👤 Patient Information)

    fields : list
        List of tuples:
        [("Name","Mohan Singh"),
         ("Age","49")]
    """

    html = f"""
    <div class="card">

        <div class="card-title">
            {title}
        </div>
    """

    for label, value in fields:

        html += f"""
        <div class="field-row">

            <div class="label">
                {label}
            </div>

            <div class="value">
                {value}
            </div>

        </div>
        """

    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)