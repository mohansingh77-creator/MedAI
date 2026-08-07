import re

# ==========================================================
# OCR Corrections Dictionary
# ==========================================================

OCR_CORRECTIONS = {

    # Patient
    "Mir": "Mr",
    "Mle": "Mr",
    "BOS": "",
    "BieS": "",
    "BMS": "",

    # Common Lab Words
    "Haemoglobin": "Hemoglobin",
    "Phitelet": "Platelet",
    "Phitelet Count": "Platelet Count",

    "W.BC.": "WBC",
    "W.B.C.": "WBC",
    "R.BC.": "RBC",
    "R.B.C.": "RBC",

    "Svphilis": "Syphilis",
    "Nom-Reachive": "Non-Reactive",
}


# ==========================================================
# Normalize OCR Text
# ==========================================================

def clean_ocr_text(text):

    cleaned = text

    # Apply dictionary replacements
    for wrong, correct in OCR_CORRECTIONS.items():

        cleaned = re.sub(
            re.escape(wrong),
            correct,
            cleaned,
            flags=re.IGNORECASE
        )

    # Remove extra spaces
    cleaned = re.sub(r"\s+", " ", cleaned)

    return cleaned.strip()