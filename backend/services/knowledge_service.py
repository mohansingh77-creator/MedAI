import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

MEDICINES_FILE = BASE_DIR / "data" / "medicines.json"
DIAGNOSIS_FILE = BASE_DIR / "data" / "diagnosis.json"


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


medicine_db = load_json(MEDICINES_FILE)
diagnosis_db = load_json(DIAGNOSIS_FILE)


def detect_medicines(ocr_text):

    medicines = []

    text = ocr_text.upper()

    for medicine in medicine_db:

        if medicine["name"].upper() in text:

            medicines.append(medicine)

    return medicines


def detect_diagnosis(ocr_text):

    diagnoses = []

    text = ocr_text.upper()

    for diagnosis in diagnosis_db:

        if diagnosis["name"].upper() in text:

            diagnoses.append(diagnosis)

    return diagnoses