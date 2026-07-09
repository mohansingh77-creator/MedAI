import json
import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.0-flash")


def analyze_prescription(text):

    prompt = f"""
You are a healthcare document explainer.

Analyze the prescription below.

Return ONLY valid JSON.

Format:

{{
  "summary": "",
  "medicines": [
    {{
      "name": "",
      "purpose": ""
    }}
  ],
  "dos": [],
  "donts": [],
  "warnings": []
}}

Prescription:
{text}
"""

    response = model.generate_content(prompt)

    response_text = response.text.strip()

    # Remove markdown if Gemini wraps JSON in ```json
    response_text = response_text.replace("```json", "")
    response_text = response_text.replace("```", "")

    return json.loads(response_text)