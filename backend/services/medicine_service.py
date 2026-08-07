import re

from models.medicine_db import MEDICINES
from services.prescription_parser import split_medicine_blocks
from services.prescription_pattern_parser import (
    parse_prescription_block
)


def detect_medicines(text):

    detected = []

    blocks = split_medicine_blocks(text)

    medicine_names = sorted(
        MEDICINES.keys(),
        key=len,
        reverse=True
    )

    for block in blocks:

        first_line = block[0].upper()

        for medicine in medicine_names:

            if medicine.upper() in first_line:

                parsed = parse_prescription_block(block)

                item = {
                    "name": medicine,

                    "purpose": MEDICINES[medicine]["purpose"],
                    "category": MEDICINES[medicine]["category"],
                    "how_it_works": MEDICINES[medicine]["how_it_works"],
                    "common_side_effects": MEDICINES[medicine]["common_side_effects"],
                    "precautions": MEDICINES[medicine]["precautions"],

                    "dosage": parsed["dosage"],
                    "frequency": parsed["frequency"],
                    "duration": parsed["duration"],
                    "timing": parsed["timing"]
                }

                print("\nADDING MEDICINE")
                print(item)

                detected.append(item)

                break

    print("\n========== FINAL MEDICINES ==========")
    print(detected)
    print("=====================================\n")

    return detected