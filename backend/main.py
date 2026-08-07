import json
import io

from fastapi import FastAPI, UploadFile, File, Depends
from sqlalchemy.orm import Session
from PIL import Image
import pytesseract

from database import Base, engine, get_db
from models.report import Report

from services.text_extraction_service import extract_document_text
from services.ocr_cleaner import clean_ocr_text
from services.document_service import (
    detect_document_type,
    analyze_document,
)

# ----------------------------------------------------
# FastAPI
# ----------------------------------------------------

app = FastAPI(
    title="MedAI API",
    description="AI-powered Medical Document Interpretation Platform",
    version="1.0"
)

Base.metadata.create_all(bind=engine)

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

history = []


# ----------------------------------------------------
# Home
# ----------------------------------------------------

@app.get("/")
def home():
    return {
        "application": "MedAI API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


# ----------------------------------------------------
# Health
# ----------------------------------------------------

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "application": "MedAI",
        "version": "1.0.0"
    }


# ----------------------------------------------------
# Upload Prescription
# ----------------------------------------------------

@app.post("/api/v1/documents/analyze")
async def upload_prescription(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # ----------------------------------------------------
    # Read Uploaded File
    # ----------------------------------------------------

    file_bytes = await file.read()

    # ----------------------------------------------------
    # Extract Text
    # ----------------------------------------------------

    if file.filename.lower().endswith(".pdf"):

        extracted_text = extract_document_text(file_bytes)

        # Normalize OCR text
        extracted_text = clean_ocr_text(extracted_text)

        print("\n========== CLEANED OCR ==========\n")
        print(extracted_text[:3000])
        print("\n=================================\n")

    else:

        image = Image.open(io.BytesIO(file_bytes))

        extracted_text = pytesseract.image_to_string(
            image,
            config="--psm 6"
        )

    print("\n========== EXTRACTED TEXT ==========\n")
    print(extracted_text[:3000])
    print("\n===================================\n")

    # ----------------------------------------------------
    # Detect Document Type
    # ----------------------------------------------------

    document_type = detect_document_type(extracted_text)

    # ----------------------------------------------------
    # Analyze Document
    # ----------------------------------------------------

    analysis = analyze_document(extracted_text)

    analysis["document_type"] = document_type
    analysis["ocr_text"] = extracted_text

    # Save history
    history.append({
        "ocr_text": extracted_text,
        "analysis": analysis
    })

    # Save database
    report = Report(

        patient_name=analysis["patient"].get(
            "name",
            "Unknown"
        ),

        document_type=document_type,

        ocr_text=extracted_text,

        analysis=json.dumps(analysis)

    )

    db.add(report)
    db.commit()
    db.refresh(report)

    print("\nFINAL RESPONSE")
    print(analysis["medicines"])
    
    return analysis


# ----------------------------------------------------
# Reports
# ----------------------------------------------------

@app.get("/api/v1/reports")
def get_reports(
    db: Session = Depends(get_db)
):
    return db.query(Report).all()

