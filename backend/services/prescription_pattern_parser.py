import re


def parse_prescription_block(block):
    
    data = {
        "dosage": "",
        "frequency": "",
        "duration": "",
        "timing": [],
    }

    first_line = block[0]
    text = " ".join(block)
    
    timing_lines = []

    for line in block:

        if line.upper().startswith("TIMING"):

            timing_lines.append(line)

    timing_text = " ".join(timing_lines)

    print("\n========================================")
    print(">>> parse_prescription_block() CALLED <<<")
    print("FIRST LINE:", first_line)

    # Duration
    duration_match = re.search(r"(\d+)\s*Days?", text, re.IGNORECASE)
    if duration_match:
        data["duration"] = f"{duration_match.group(1)} Days"

    # Timing
    timing_patterns = [

    "After Breakfast",

    "After Lunch",

    "After Dinner",

    "Before Breakfast",

    "Before Lunch",

    "Before Dinner",

    "Morning",

    "Night"

    ]

    for t in timing_patterns:

        if t.lower() in timing_text.lower():

            data["timing"].append(t)

    if not data["timing"]:

        fallback = [
            "After Food",
            "Before Food",
            "Morning",
            "Night"
        ]

        for t in fallback:

            if t.lower() in text.lower():

                data["timing"].append(t)
                break

    # Search only after TABLET/TAB/CAPSULE
    parts = re.split(
        r"\b(?:TABLET|TAB|CAPSULE|CAP|SYRUP|INJECTION)\b",
        first_line,
        flags=re.IGNORECASE
    )

    search_text = parts[1] if len(parts) > 1 else first_line

    # OCR cleanup
    search_text = search_text.replace("=", "-")
    search_text = re.sub(r"s(?=\d)", "-", search_text, flags=re.IGNORECASE)
    search_text = re.sub(r"a(?=\d)", "-", search_text, flags=re.IGNORECASE)
    search_text = re.sub(r"-{2,}", "-", search_text)

    print("SEARCH TEXT:", search_text)

    fallback = re.search(
        r"\b(OD|BD|TDS|SOS)\b",
        search_text,
        re.IGNORECASE
    )

    dosage_match = re.search(
        r"(\d)\s*-\s*(\d)\s*-\s*(\d)",
        search_text
    )

    if dosage_match:

        print("DOSAGE MATCH:", dosage_match.groups())

        morning = int(dosage_match.group(1))
        afternoon = int(dosage_match.group(2))
        night = int(dosage_match.group(3))

        total = morning + afternoon + night

        # tablets taken at one time
        per_dose = max(morning, afternoon, night)

        if per_dose == 1:
            data["dosage"] = "1 Tablet"
        elif per_dose > 1:
            data["dosage"] = f"{per_dose} Tablets"

        if total == 1:
            data["frequency"] = "Once Daily"
        elif total == 2:
            data["frequency"] = "Twice Daily"
        elif total == 3:
            data["frequency"] = "Three Times Daily"

    elif fallback:

        code = fallback.group(1).upper()

        if code == "OD":
            data["dosage"] = "1 Tablet"
            data["frequency"] = "Once Daily"

        elif code == "BD":
            data["dosage"] = "1 Tablet"
            data["frequency"] = "Twice Daily"

        elif code == "TDS":
            data["dosage"] = "1 Tablet"
            data["frequency"] = "Three Times Daily"

        elif code == "SOS":
            data["dosage"] = "1 Tablet"
            data["frequency"] = "When Required"

    if "SOS" in text.upper():
        data["frequency"] = "When Required"

        if not data["dosage"]:
            data["dosage"] = "1 Tablet"

    print("PARSED DATA:", data)

    return data