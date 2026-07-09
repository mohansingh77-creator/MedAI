def detect_document_type(text):

    text = text.lower()

    # Prescription keywords
    prescription_keywords = [
        "tablet",
        "capsule",
        "take",
        "mg",
        "od",
        "bd",
        "sos",
        "medicine",
        "rx"
    ]

    # Lab report keywords
    lab_keywords = [
        "hemoglobin",
        "hb",
        "cholesterol",
        "glucose",
        "hba1c",
        "creatinine",
        "platelet",
        "wbc",
        "rbc"
    ]

    prescription_score = sum(
        keyword in text for keyword in prescription_keywords
    )

    lab_score = sum(
        keyword in text for keyword in lab_keywords
    )

    if prescription_score > lab_score:
        return "Prescription"

    elif lab_score > 0:
        return "Lab Report"

    else:
        return "Unknown"