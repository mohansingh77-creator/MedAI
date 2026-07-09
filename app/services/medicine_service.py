from app.models.medicine_db import MEDICINES

def detect_medicines(text):

    found = []

    text_lower = text.lower()

    for medicine, details in MEDICINES.items():

        if medicine in text_lower:

            found.append({
                "name": medicine.title(),
                "purpose": details["purpose"],
                "category": details["category"],
                "side_effects": details["side_effects"]
            })

    return found