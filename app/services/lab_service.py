import re
from app.models.lab_db import LAB_RANGES

def analyze_lab_report(text):

    findings=[]

    lower_text=text.lower()

    for test,data in LAB_RANGES.items():

        pattern=rf"{test}\D+(\d+\.?\d*)"

        match=re.search(pattern,lower_text)

        if match:

            value=float(match.group(1))

            if value<data["low"]:

                findings.append({
                    "test":test.title(),
                    "value":value,
                    "status":"Low",
                    "meaning":data["meaning_low"]
                })

            elif value>data["high"]:

                findings.append({
                    "test":test.title(),
                    "value":value,
                    "status":"High",
                    "meaning":data["meaning_high"]
                })

    return findings