import json
from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)


def extract_medicines_ai(ocr_text):

    prompt = f"""
You are an expert medical assistant.

Extract all medicines from this prescription.

Return ONLY valid JSON.

Format:

[
  {{
    "name":"",
    "purpose":"",
    "dosage":"",
    "timing":"",
    "warnings":""
  }}
]

Prescription:

{ocr_text}
"""

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )

    text = response.text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "").replace("```", "").strip()

    elif text.startswith("```"):
        text = text.replace("```", "").strip()

    print("\n===== GEMINI RESPONSE =====")
    print(text)
    print("===========================\n")
    
    return json.loads(text)