import re
from models.medicine_db import MEDICINES

# ==========================================================
# Prescription Frequency Dictionary
# ==========================================================

FREQUENCY_MAP = {

    "OD": "Once Daily",
    "BD": "Twice Daily",
    "TDS": "Three Times Daily",
    "QID": "Four Times Daily",

    "HS": "At Bedtime",
    "SOS": "When Required"

}


# ==========================================================
# Food Timing Dictionary
# ==========================================================

TIMING_MAP = {

    "AF": "After Food",
    "BF": "Before Food",

    "AC": "Before Meals",
    "PC": "After Meals"

}

def parse_prescription_line(line: str):

    result = {
        "dosage": "",
        "frequency": "",
        "duration": "",
        "timing": ""
    }

    if not line:
        return result

    line = line.upper()

    for key, value in FREQUENCY_MAP.items():

        if re.search(r"\b" + key + r"\b", line):

            result["frequency"] = value
    
    for key, value in TIMING_MAP.items():

        if re.search(r"\b" + key + r"\b", line):

            result["timing"] = value

    match = re.search(

        r"(\d+)\s*(DAY|DAYS|WEEK|WEEKS|MONTH|MONTHS)",

        line,

        re.IGNORECASE

    )

    if match:

        days = int(match.group(1))

        unit = match.group(2).lower()

        if unit.startswith("day"):

            result["duration"] = (
                "1 Day"
                if days == 1
                else f"{days} Days"
            )

        elif unit.startswith("week"):

            result["duration"] = (
                "1 Week"
                if days == 1
                else f"{days} Weeks"
        )

        elif unit.startswith("month"):

            result["duration"] = (
                "1 Month"
                if days == 1
                else f"{days} Months"
        )

    match = re.search(

    r"(\d)-(\d)-(\d)",

    line

    )

    if match:

        morning = int(match.group(1))
        afternoon = int(match.group(2))
        night = int(match.group(3))

        total = morning + afternoon + night

        if total == 1:
            result["frequency"] = "Once Daily"

        elif total == 2:
            result["frequency"] = "Twice Daily"

        elif total >= 3:
            result["frequency"] = "Three Times Daily"

        result["dosage"] = "1 Tablet"

    # ==========================================================
    # Default Dosage
    # ==========================================================

    if result["frequency"] and not result["dosage"]:

        result["dosage"] = "1 Tablet"
    
    return result

# ==========================================================
# Split OCR into Medicine Blocks
# ==========================================================

def split_medicine_blocks(text):

    print(">>> split_medicine_blocks() CALLED <<<")

    lines = [

        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    blocks = []

    current_block = []

    medicine_names = sorted(
        MEDICINES.keys(),
        key=len,
        reverse=True
    )

    for line in lines:

        is_medicine = False

        for medicine in medicine_names:

            if medicine.upper() in line.upper():

                if current_block:

                    blocks.append(current_block)

                current_block = [line]

                is_medicine = True

                break

        if not is_medicine:

            if current_block:

                current_block.append(line)

    if current_block:

        blocks.append(current_block)

    print("BLOCK COUNT:", len(blocks))
    print(blocks)

    return blocks