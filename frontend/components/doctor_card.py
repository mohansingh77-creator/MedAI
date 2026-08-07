from components.card import render_card


def render_doctor_card(doctor, visit_date):

    render_card(

        "👨‍⚕️ Doctor Information",

        [
            ("Doctor", doctor.get("name","-")),
            ("Hospital", doctor.get("hospital","-")),
            ("Visit Date", visit_date)
        ]

    )