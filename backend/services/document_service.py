from services.parser_service import extract_patient_info
from services.medicine_service import detect_medicines
from services.knowledge_service import detect_diagnosis
from services.lab_service import analyze_lab_report
from services.health_score_service import calculate_health_score
from services.schedule_service import generate_today_plan
from services.patient_summary_service import generate_patient_summary
from services.doctor_advice_service import generate_doctor_advice


# ==========================================================
# Detect Document Type
# ==========================================================

def detect_document_type(text):

    text = text.lower()

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

    lab_keywords = [
        "hemoglobin",
        "hb",
        "cholesterol",
        "glucose",
        "hba1c",
        "creatinine",
        "platelet",
        "wbc",
        "rbc",
        "syphilis",
        "esr",
        "cbc",
        "serum",
        "specimen",
        "biochemistry",
    ]

    prescription_score = sum(
        keyword in text
        for keyword in prescription_keywords
    )

    lab_score = sum(
        keyword in text
        for keyword in lab_keywords
    )

    if prescription_score > lab_score:
        return "Prescription"

    elif lab_score > 0:
        return "Lab Report"

    return "Unknown"


# ==========================================================
# Complete Analysis Pipeline
# ==========================================================

def analyze_document(extracted_text):

    # -------------------------------
    # Basic Information
    # -------------------------------

    patient, doctor, visit_date = extract_patient_info(extracted_text)

    medicines = detect_medicines(extracted_text)

    diagnosis = detect_diagnosis(extracted_text)

    lab_findings = analyze_lab_report(extracted_text)

    print("\n========== LAB FINDINGS ==========")
    print(lab_findings)
    print("=================================\n")

    health_score = calculate_health_score(lab_findings)

    today_plan = generate_today_plan(medicines)

    document_type = detect_document_type(extracted_text)


    # -------------------------------
    # Doctor Advice
    # -------------------------------

    doctor_advice = generate_doctor_advice(
        extracted_text,
        diagnosis
    )


    # -------------------------------
    # Red Flags
    # -------------------------------

    red_flags = []

    if "STENOSIS" in extracted_text.upper():
        red_flags.append(
            "Spinal canal narrowing detected."
        )

    if "PIVD" in extracted_text.upper():
        red_flags.append(
            "Slipped Disc (PIVD) detected."
        )


    # -------------------------------
    # Patient Summary
    # -------------------------------

    patient_summary = generate_patient_summary(

        patient=patient,

        diagnosis=diagnosis,

        medicines=medicines,

        follow_up=visit_date,

        red_flags=red_flags

    )


    # -------------------------------
    # Overall Summary
    # -------------------------------

    summary = (
        f"Detected {len(medicines)} medicine(s), "
        f"{len(diagnosis)} diagnosis finding(s), "
        f"and {len(lab_findings)} lab finding(s)."
    )


    # -------------------------------
    # Final Response
    # -------------------------------

    return {

        "patient": patient,

        "doctor": doctor,

        "visit_date": visit_date,

        "document_type": document_type,

        "summary": summary,

        "diagnosis": diagnosis,

        "medicines": medicines,

        "today_plan": today_plan,

        "patient_summary": patient_summary,

        "doctor_advice": doctor_advice,

        "health_score": health_score,

        "lab_findings": lab_findings

    }