import json
from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)


def analyze_prescription(text):

    prompt = f"""
You are an expert medical assistant.

Analyze this medical document.

Explain everything in VERY SIMPLE language so that a patient with no medical background can understand.

IMPORTANT:
Return ONLY valid JSON.
Do NOT wrap the JSON inside markdown.

Return exactly this structure:

{{
  "patient": {{
    "name": "",
    "age": "",
    "gender": ""
  }},

  "doctor": {{
    "name": "",
    "hospital": ""
  }},

  "visit_date": "",

  "diagnosis": {{
    "medical_term": "",
    "simple_explanation": ""
  }},

  "summary": "",

  "medicines": [
    {{
      "name": "",
      "purpose": "",
      "dosage": "",
      "timing": "",
      "duration": "",
      "common_side_effects": []
    }}
  ],

  "recommendations": [],

  "red_flags": [],

  "follow_up": ""
}}

Medical Document:

{text}
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    print("\n===== GEMINI RESPONSE =====")
    print(response.text)
    print("===========================\n")

    response_text = response.text.strip()

    if response_text.startswith("```json"):
        response_text = response_text.replace("```json", "")

    if response_text.endswith("```"):
        response_text = response_text.replace("```", "")

    response_text = response_text.strip()

    print(response_text)
    return json.loads(response_text)