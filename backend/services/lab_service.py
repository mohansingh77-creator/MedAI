import re

from models.lab_db import LAB_TESTS, LAB_RANGES


# ==========================================================
# Extract Numeric Value
# ==========================================================

def extract_lab_value(text, aliases, test_name):

    for alias in aliases:

        pattern = rf"{alias}.*?([0-9]+(?:\.[0-9]+)?)"

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            try:

                value = float(match.group(1))

                # ----------------------------
                # OCR Corrections
                # ----------------------------

                if test_name == "hemoglobin" and value > 30:
                    value = value / 10

                elif test_name == "rbc" and value > 20:
                    value = value / 100

                return value

            except:
                pass

    return None


# ==========================================================
# Determine Status
# ==========================================================

def get_status(value, low, high):

    if value is None:
        return "Not Found"

    if value < low:
        return "Low"

    if value > high:
        return "High"

    return "Normal"


# ==========================================================
# Analyze Lab Report
# ==========================================================

def analyze_lab_report(text):

    findings = {}

    normalized_text = text.replace("\n", " ")

    for test_name, aliases in LAB_TESTS.items():

        value = extract_lab_value(
            normalized_text,
            aliases,
            test_name
        )

        if value is None:
            continue

        low, high = LAB_RANGES[test_name]

        findings[test_name] = {

            "value": value,

            "reference": f"{low}-{high}",

            "status": get_status(
                value,
                low,
                high
            )

        }

    return findings