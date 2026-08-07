import fitz
import pytesseract

from PIL import Image

from services.pdf_service import pdf_to_images


# ==========================================================
# Extract Text From PDF
# ==========================================================

def extract_text_from_pdf(pdf_bytes):

    pdf = fitz.open(stream=pdf_bytes, filetype="pdf")

    extracted_text = ""

    for page in pdf:

        extracted_text += page.get_text()

    pdf.close()

    print("\n========== DIRECT PDF TEXT ==========\n")
    print(extracted_text[:3000])
    print("\n=====================================\n")
    
    return extracted_text.strip()


# ==========================================================
# OCR Fallback
# ==========================================================

def extract_text_using_ocr(pdf_bytes):

    images = pdf_to_images(pdf_bytes)

    text = ""

    for image in images:

        text += pytesseract.image_to_string(image)

        text += "\n"

    return text


# ==========================================================
# Hybrid Extraction
# ==========================================================

def extract_document_text(pdf_bytes):

    text = extract_text_from_pdf(pdf_bytes)

    # Use direct PDF text if sufficient content exists
    if len(text.strip()) > 100:

        print("\n✅ Digital PDF detected (Direct Text Extraction)\n")

        return text

    print("\n⚠ Scanned PDF detected (OCR Fallback)\n")

    return extract_text_using_ocr(pdf_bytes)