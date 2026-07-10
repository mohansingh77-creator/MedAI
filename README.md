# 🏥 MedAI – AI Powered Medical Document Analyzer

![Python](https://img.shields.io/badge/Python-3.14-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![OCR](https://img.shields.io/badge/Tesseract-OCR-orange)
![Gemini AI](https://img.shields.io/badge/Google-Gemini_AI-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📖 Overview

MedAI is an AI-powered healthcare application that extracts text from medical prescriptions and laboratory reports using OCR and analyzes the extracted information using Artificial Intelligence.

The application helps users understand:

- 💊 Medicines prescribed
- 📋 Lab test results
- ❤️ Health Score
- ⚠️ Medical warnings
- 📑 Prescription summary

---

# 🚀 Features

✅ Upload Prescription Images

✅ Upload PDF Medical Reports

✅ OCR using Tesseract

✅ Automatic Document Type Detection

✅ Medicine Detection

✅ Laboratory Report Analysis

✅ AI-powered Medical Summary

✅ Health Score Calculation

✅ PostgreSQL Database Storage

✅ REST API using FastAPI

---

# 🏗️ Project Architecture

```
                User
                  │
                  ▼
          Upload Image/PDF
                  │
                  ▼
             FastAPI Backend
                  │
      ┌───────────┼────────────┐
      │           │            │
      ▼           ▼            ▼
    OCR      AI Analysis    Database
(Tesseract)  (Gemini AI)  (PostgreSQL)
      │           │
      └──────┬────┘
             ▼
      JSON API Response
```

---

# 📂 Project Structure

```
MedAI/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── schemas.py
│   │
│   ├── models/
│   │     ├── report.py
│   │     ├── medicine_db.py
│   │     └── lab_db.py
│   │
│   ├── services/
│   │     ├── ai_service.py
│   │     ├── medicine_service.py
│   │     ├── lab_service.py
│   │     ├── pdf_service.py
│   │     ├── health_score_service.py
│   │     └── document_service.py
│   │
│   └── routes/
│         ├── prescription.py
│         ├── report.py
│         └── user.py
│
├── requirements.txt
├── README.md
└── .env
```

---

# ⚙️ Technology Stack

| Technology | Purpose |
|------------|---------|
| Python | Programming Language |
| FastAPI | Backend API |
| PostgreSQL | Database |
| SQLAlchemy | ORM |
| Tesseract OCR | Text Extraction |
| Google Gemini AI | AI Analysis |
| Pillow | Image Processing |
| Uvicorn | API Server |

---

# 📡 API Endpoints

## Upload Prescription

```
POST /upload-prescription
```

Uploads a prescription image or PDF and returns OCR text, medicine analysis, lab findings, and health score.

---

## Get Reports

```
GET /reports
```

Returns all stored reports.

---

## Get History

```
GET /history
```

Returns uploaded report history.

---

## Health Check

```
GET /health
```

Returns API status.

---

# 📊 Sample Response

```json
{
  "document_type": "Prescription",
  "health_score": 90,
  "analysis": {
    "summary": "Prescription contains medicines.",
    "medicines": [
      {
        "name": "Paracetamol",
        "purpose": "Pain relief"
      }
    ]
  }
}
```

---

# 🛠 Installation

Clone the repository

```bash
git clone https://github.com/mohansingh77-creator/MedAI.git
```

Navigate to the project

```bash
cd MedAI
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the server

```bash
uvicorn app.main:app --reload
```

Open Swagger UI

```
http://127.0.0.1:8000/docs
```

---

# 🔮 Future Enhancements

- User Authentication (JWT)
- Flutter Mobile App
- Medicine Interaction Checker
- Drug Side Effect Prediction
- AI Chat Assistant
- Doctor Recommendation System
- Multi-language OCR
- Cloud Deployment
- Docker Support

---

# 👨‍💻 Developer

**Mohan Singh**

Finance | FP&A | Business Strategy | AI Developer

GitHub:
https://github.com/mohansingh77-creator

---

# ⭐ If you like this project

Please consider giving the repository a ⭐ on GitHub.
