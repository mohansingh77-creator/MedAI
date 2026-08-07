def generate_patient_summary(
    patient,
    diagnosis,
    medicines,
    follow_up,
    red_flags
):

    summary = {}

    # ---------------------------------------
    # Patient
    # ---------------------------------------

    summary["patient_name"] = patient.get("name", "")
    summary["age"] = patient.get("age", "")
    summary["gender"] = patient.get("gender", "")

    # ---------------------------------------
    # Diagnosis
    # ---------------------------------------

    if diagnosis:

        conditions = []

        for item in diagnosis:
            conditions.append(item["name"])

        summary["condition"] = (
            "Your report indicates: "
            + ", ".join(conditions)
        )

    else:

        summary["condition"] = "No major diagnosis detected."

    # ---------------------------------------
    # Treatment
    # ---------------------------------------

    if medicines:

        purposes = []

        for med in medicines:

            purpose = med["purpose"]

            if purpose not in purposes:
                purposes.append(purpose)

        summary["treatment"] = (
            "Your medicines are intended for: "
            + ", ".join(purposes)
        )

    else:

        summary["treatment"] = "No medicines detected."

    # ---------------------------------------
    # Red Flags
    # ---------------------------------------

    summary["red_flags"] = red_flags

    # ---------------------------------------
    # Follow-up
    # ---------------------------------------

    summary["follow_up"] = follow_up

    return summary