import re


def clean_text(value):
    """Remove extra spaces and OCR artifacts."""
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def extract_patient_info(text):

    patient = {
        "name": "Unknown",
        "age": "",
        "gender": ""
    }

    doctor = {
        "name": "",
        "hospital": ""
    }

    visit_date = ""

    # ---------------------------------------------------
    # Clean OCR text
    # ---------------------------------------------------

    text = text.replace("\n", " ")

    text = re.sub(r"\s+", " ", text)

    # ---------------------------------------------------
    # Patient Name (OCR tolerant)
    # ---------------------------------------------------

    patient["name"] = "Unknown"

    # Pattern 1 : Patient Name
    match = re.search(
        r"Name\s*[:=\-\[\]0-9]*\s*(?:Mr|Mir|Mrs|Ms|Mle)?\.?\s*([A-Z ]+?)\s+(?:Age|Collection|Reporting|Ref|Client)",
        text,
        re.IGNORECASE
    )

    if match:

        patient["name"] = clean_text(match.group(1)).title()

        # Remove common OCR artifacts
        patient["name"] = re.sub(
            r"\b(Bos|BieS|Bms|Collection|Date)\b",
            "",
            patient["name"],
            flags=re.IGNORECASE
        ).strip()

        print("PATIENT:", patient["name"])

    if not match:

        # Pattern 2 : Name
        match = re.search(
            r"Name[^A-Za-z]*(?:Mr|Mrs|Ms|Mle|Male)?\.?\s*([A-Z][A-Z\s]{3,})",
            text,
            re.IGNORECASE
        )

    if match:

        name = clean_text(match.group(1))

        # Remove OCR artifacts
        name = re.sub(
            r"\b(MR|MRS|MS|MLE|MALE|FEMALE)\b",
            "",
            name,
            flags=re.IGNORECASE
        )

        patient["name"] = name.title().strip()
        print("PATIENT NAME FOUND:", patient["name"])

    # ---------------------------------------------------
    # Age
    # ---------------------------------------------------

    match = re.search(r"\((\d+)\s*[Yy]", text)

    if match:
        patient["age"] = match.group(1)

    # ---------------------------------------------------
    # Gender
    # ---------------------------------------------------

    if re.search(r"\bMale\b", text, re.IGNORECASE):
        patient["gender"] = "Male"

    elif re.search(r"\bFemale\b", text, re.IGNORECASE):
        patient["gender"] = "Female"

    # ---------------------------------------------------
    # Doctor
    #
    # Ignore referral doctors
    # ---------------------------------------------------

    doctor_match = re.search(
        r"Dr\.?\s*Niraj\s+Sharad\s+Kasat",
        text,
        re.IGNORECASE
    )

    if doctor_match:

        doctor["name"] = "Dr. Niraj Sharad Kasat"

    else:

        matches = re.findall(
            r"Dr\.?\s*([A-Za-z ]+)",
            text,
            re.IGNORECASE
        )

        for d in matches:

            if "ARCHANA" in d.upper():
                continue

            doctor["name"] = "Dr. " + clean_text(d).title()
            break

    # ---------------------------------------------------
    # Hospital
    # ---------------------------------------------------

    hospital_patterns = [
        "Joint Replacement And Spine Clinic",
        "Replacement And Spine Clinic",
        "Spine Clinic"
    ]

    for hospital in hospital_patterns:

        if hospital.lower() in text.lower():

            doctor["hospital"] = "Joint Replacement And Spine Clinic"

            break

    # ---------------------------------------------------
    # Visit Date
    # ---------------------------------------------------

    match = re.search(
        r"(\d{1,2}-[A-Za-z]{3}-\d{4})",
        text
    )

    if match:

        visit_date = match.group(1)

    print("=" * 60)
    print("Detected Patient:", patient)
    print("=" * 60)

    return patient, doctor, visit_date