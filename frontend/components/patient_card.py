from components.card import render_card


def render_patient_card(patient):

    render_card(
        "👤 Patient Information",

        [
            ("Name", patient.get("name","Unknown")),
            ("Age", patient.get("age","-")),
            ("Gender", patient.get("gender","-"))
        ]
    )