from app.database import Base, engine, get_db
from app.models.report import Report
from app.services.lab_service import analyze_lab_report
from app.services.medicine_service import detect_medicines
from fastapi import FastAPI, UploadFile, File
from PIL import Image
from app.services.health_score_service import calculate_health_score
from app.services.pdf_service import pdf_to_images
from app.services.document_service import detect_document_type
from sqlalchemy.orm import Session
from fastapi import Depends

from app.database import get_db
from app.models.report import Report
import json
import pytesseract
import io

from app.services.ai_service import analyze_prescription

app = FastAPI()
Base.metadata.create_all(bind=engine)

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Temporary history storage
history = []


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/history")
def get_history():
    return history


@app.post("/upload-prescription")
async def upload_prescription(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # Read uploaded file
    file_bytes = await file.read()

    # Handle PDF or Image
    if file.filename.endswith(".pdf"):

        images = pdf_to_images(file_bytes)

        image = images[0]

    else:

        image = Image.open(io.BytesIO(file_bytes))

    # Extract text using OCR
    extracted_text = pytesseract.image_to_string(
        image,
        config="--psm 6"
    )
    document_type = detect_document_type(extracted_text)

    # Detect medicines
    medicines = detect_medicines(extracted_text)
    lab_findings = analyze_lab_report(extracted_text)
    health_score = calculate_health_score(lab_findings)

    # Try AI analysis
    try:
        analysis = analyze_prescription(extracted_text)

    # Fallback if AI fails
    except Exception:

        analysis = {
            "summary": f"Prescription contains {len(medicines)} medicine(s).",
            "medicines": medicines,
            "dos": [
                "Follow doctor's instructions",
                "Take medicines on time"
            ],
            "donts": [
                "Do not skip doses",
                "Do not self-medicate"
            ],
            "warnings": [
                "Consult your doctor if symptoms worsen"
            ]
        }

    # Save history
    history.append({
        "ocr_text": extracted_text,
        "analysis": analysis
    })

    new_report = Report(
    patient_name="Unknown",
    document_type=document_type,
    ocr_text=extracted_text,
    analysis=json.dumps({
        "analysis": analysis,
        "lab_findings": lab_findings,
        "health_score": health_score
    })
)

    db.add(new_report)
    db.commit()
    db.refresh(new_report)

    return {
    "document_type": document_type,
    "health_score": health_score,
    "ocr_text": extracted_text,
    "analysis": analysis,
    "lab_findings": lab_findings
}

@app.get("/reports")
def get_reports(db: Session = Depends(get_db)):
    reports = db.query(Report).all()

    return reports