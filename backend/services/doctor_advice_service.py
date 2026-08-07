def generate_doctor_advice(extracted_text, diagnosis):

    advice = []

    text = extracted_text.upper()

    # ------------------------
    # Advice written by doctor
    # ------------------------

    if "PHYSIO" in text:
        advice.append("Attend physiotherapy sessions.")

    if "BELT" in text:
        advice.append("Wear lumbar belt.")

    if "ICE" in text:
        advice.append("Apply ice pack if advised.")

    if "HOT" in text:
        advice.append("Hot fomentation if advised.")

    if "BED REST" in text:
        advice.append("Take adequate bed rest.")

    # ------------------------
    # Diagnosis-based advice
    # ------------------------

    diagnosis_names = [
        d["name"].upper()
        for d in diagnosis
    ]

    if "PIVD" in diagnosis_names:
        advice.append("Avoid heavy lifting.")
        advice.append("Avoid prolonged bending.")
        advice.append("Maintain proper posture.")

    if "CANAL STENOSIS" in diagnosis_names:
        advice.append("Avoid standing for long periods.")
        advice.append("Take short walking breaks.")

    # Remove duplicates
    advice = list(dict.fromkeys(advice))

    return advice