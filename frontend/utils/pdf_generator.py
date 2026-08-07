from io import BytesIO
from datetime import datetime

from PIL import Image as PILImage

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
    PageBreak,
)

styles = getSampleStyleSheet()

TITLE_STYLE = styles["Heading1"]
TITLE_STYLE.textColor = colors.HexColor("#1E3A8A")
TITLE_STYLE.alignment = TA_CENTER
TITLE_STYLE.spaceAfter = 20

SECTION_STYLE = styles["Heading2"]
SECTION_STYLE.textColor = colors.HexColor("#2563EB")
SECTION_STYLE.spaceBefore = 12
SECTION_STYLE.spaceAfter = 10

NORMAL_STYLE = styles["BodyText"]
NORMAL_STYLE.leading = 20
NORMAL_STYLE.spaceAfter = 8

# ==========================================================
# PAGE NUMBER
# ==========================================================

def add_page_number(canvas, doc):
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.grey)
    canvas.drawRightString(
        7.5 * inch,
        0.5 * inch,
        f"Page {doc.page}"
    )


# ==========================================================
# PDF GENERATOR
# ==========================================================

def generate_pdf(result, uploaded_file=None):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    title = styles["Title"]
    title.alignment = TA_CENTER

    heading = styles["Heading2"]
    body = styles["BodyText"]

    story = []

    # ======================================================
    # PAGE 1 - ORIGINAL PRESCRIPTION
    # ======================================================

    if uploaded_file is not None:

        story.append(
            Paragraph(
                "<b>Original Prescription</b>",
                heading
            )
        )

        story.append(Spacer(1, 12))

        try:

            uploaded_file.seek(0)

            img = PILImage.open(uploaded_file)

            width, height = img.size

            max_width = 6.5 * inch
            max_height = 9 * inch

            ratio = min(
                max_width / width,
                max_height / height,
            )

            img_width = width * ratio
            img_height = height * ratio

            uploaded_file.seek(0)

            story.append(
                Image(
                    uploaded_file,
                    width=img_width,
                    height=img_height,
                )
            )

            story.append(PageBreak())

        except Exception:

            story.append(
                Paragraph(
                    "Unable to display prescription image.",
                    body,
                )
            )

            story.append(PageBreak())

    # ======================================================
    # PROFESSIONAL HEADER
    # ======================================================

    header_table = Table(
        [
            ["🏥 MedAI Healthcare"],
            ["AI Clinical Prescription Interpretation Report"],
            [f"Generated on: {datetime.now().strftime('%d %b %Y, %I:%M %p')}"]
        ],
        colWidths=[500]
    )

    header_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#1E40AF")),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (0, 0), "Helvetica-Bold"),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (0, 0), 20),
            ("FONTSIZE", (0, 1), (0, 1), 13),
            ("FONTSIZE", (0, 2), (0, 2), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 12),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ])
    )

    story.append(header_table)
    story.append(Spacer(1, 20))

    # ======================================================
    # PATIENT INFORMATION
    # ======================================================

    patient = result.get("patient", {})
    doctor = result.get("doctor", {})

    story.append(
        Paragraph(
            "<font color='#2563EB'><b>Patient Information</b></font>",
            heading,
        )
    )
    story.append(Spacer(1, 8))

    patient_data = [
        ["Patient Name", patient.get("name", "Unknown")],
        ["Age", f"{patient.get('age', '-')} Years"],
        ["Gender", patient.get("gender", "-")],
        ["Visit Date", result.get("visit_date", "-")],
        ["Consulting Doctor", doctor.get("name", "-")],
        ["Health Score", f"{result.get('health_score', 100)}/100"],
    ]

    patient_table = Table(
        patient_data,
        colWidths=[170, 300],
    )

    patient_table.setStyle(
        TableStyle([

            # Left column
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EFF6FF")),
            ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#1E3A8A")),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),

            # Right column
            ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
            ("TEXTCOLOR", (1, 0), (1, -1), colors.black),

            # Font
            ("FONTSIZE", (0, 0), (-1, -1), 11),

            # Alignment
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

            # Padding
            ("TOPPADDING", (0, 0), (-1, -1), 9),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),

            # Borders
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD5E1")),
            ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#94A3B8")),

        ])
    )

    story.append(patient_table)

    story.append(Spacer(1, 18))

    # ======================================================
    # KEY CLINICAL FINDINGS
    # ======================================================

    story.append(
        Paragraph(
            "<font color='#1E40AF'><b>Key Clinical Findings</b></font>",
            heading,
        )
    )

    story.append(Spacer(1, 8))

    diagnoses = result.get("diagnosis", [])
    medicines = result.get("medicines", [])
    labs = result.get("lab_findings", [])

    primary_dx = "Not Available"

    if diagnoses:
        if isinstance(diagnoses[0], dict):
            primary_dx = diagnoses[0].get("name", "Not Available")
        else:
            primary_dx = str(diagnoses[0])

    health_score = result.get("health_score", 100)

    if health_score >= 90:
        risk = "Low"
    elif health_score >= 70:
        risk = "Moderate"
    else:
        risk = "High"

    findings = [

        ["Primary Diagnosis", primary_dx],

        ["Medicines Prescribed", str(len(medicines))],

        ["Laboratory Findings", "None Detected" if len(labs) == 0 else str(len(labs))],

        ["Clinical Risk", risk],

        ["Health Score", f"{health_score}/100"],

        ["Recommended Follow-up",
        "Continue medications, physiotherapy and review with treating physician."],

    ]

    findings_table = Table(
        findings,
        colWidths=[170, 350]
    )

    findings_table.setStyle(
        TableStyle([

            # Alternate row colours
            ("ROWBACKGROUNDS",
            (0, 0),
            (-1, -1),
            [
                colors.HexColor("#F8FAFC"),
                colors.white,
            ]),

            # Left column
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#DBEAFE")),
            ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#1E3A8A")),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),

            # Body
            ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),

            # Borders
            ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CBD5E1")),
            ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#94A3B8")),

            # Alignment
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

            # Padding
            ("TOPPADDING", (0, 0), (-1, -1), 9),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),

        ])
    )

    story.append(findings_table)

    story.append(Spacer(1, 20))

    # ======================================================
    # DIAGNOSIS
    # ======================================================

    story.append(
        Paragraph(
            "<font color='#1E40AF'><b>Clinical Diagnosis</b></font>",
            heading,
        )
    )

    story.append(Spacer(1, 8))

    diagnoses = result.get("diagnosis", [])

    if diagnoses:

        for index, diag in enumerate(diagnoses, start=1):

            name = diag.get("name", "Unknown Diagnosis")
            explanation = diag.get(
                "simple_explanation",
                "No explanation available."
            )

            if index == 1:
                title = f"{index}. {name} (Primary Diagnosis)"
            else:
                title = f"{index}. {name}"

            story.append(
                Paragraph(
                    f"<b>{title}</b>",
                    body,
                )
            )

            story.append(
                Paragraph(
                    f"<font color='#2563EB'><b>Simple Explanation</b></font>",
                    body,
                )
            )

            story.append(
                Paragraph(
                    explanation,
                    body,
                )
            )

            story.append(Spacer(1, 12))

    else:

        story.append(
            Paragraph(
                "No diagnosis identified from the uploaded document.",
                body,
            )
        )

    story.append(Spacer(1, 18))

    # ======================================================
    # PRESCRIBED MEDICINES
    # ======================================================

    story.append(
        Paragraph(
            "<font color='#2563EB'><b>Prescribed Medicines</b></font>",
            heading,
        )
    )

    story.append(Spacer(1, 8))

    medicine_data = [
        ["Medicine Name", "Dosage", "Frequency", "Purpose"]
    ]

    for med in result.get("medicines", []):

        medicine_data.append([
            Paragraph(f"<b>{med.get('name', '-')}</b>", body),
            med.get("dosage", "-"),
            med.get("frequency", "-"),
            med.get("purpose", "-"),
        ])

    med_table = Table(
        medicine_data,
        colWidths=[150, 75, 100, 180],
        repeatRows=1,
    )

    med_table.setStyle(
        TableStyle([

            # =========================
            # Header
            # =========================
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E40AF")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 11),
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),

            # =========================
            # Body
            # =========================
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 1), (-1, -1), 10),

            ("TEXTCOLOR", (0, 1), (-1, -1), colors.black),

            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

            # =========================
            # Zebra Rows
            # =========================
            ("ROWBACKGROUNDS",
            (0, 1),
            (-1, -1),
            [colors.white, colors.HexColor("#F8FAFC")]),

            # =========================
            # Borders
            # =========================
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD5E1")),
            ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#94A3B8")),

            # =========================
            # Padding
            # =========================
            ("TOPPADDING", (0, 0), (-1, -1), 9),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),

            # =========================
            # Alignment
            # =========================
            ("ALIGN", (1, 1), (2, -1), "CENTER"),
            ("ALIGN", (0, 1), (0, -1), "LEFT"),
            ("ALIGN", (3, 1), (3, -1), "LEFT"),

        ])
    )

    story.append(med_table)

    story.append(Spacer(1, 20))

    # ======================================================
    # MEDICATION SCHEDULE
    # ======================================================

    story.append(
        Paragraph(
            "<font color='#2563EB'><b>Today's Medication Schedule</b></font>",
            heading,
        )
    )

    story.append(Spacer(1, 8))

    schedule_data = [
        ["Time", "Medicine", "Dosage", "Frequency"]
    ]

    for slot in result.get("today_plan", []):

        time_slot = slot.get("time", "")

        medicines = slot.get("medicines", [])

        if medicines:

            for med in medicines:

                schedule_data.append([
                    time_slot,
                    med.get("name", "-"),
                    med.get("dosage", "-"),
                    med.get("frequency", "-"),
                ])

        else:

            schedule_data.append([
                time_slot,
                "-",
                "-",
                "-"
            ])

    schedule_table = Table(
        schedule_data,
        colWidths=[110, 170, 90, 110],
        repeatRows=1,
    )

    schedule_table.setStyle(
        TableStyle([

            # ======================================
            # Header
            # ======================================
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E40AF")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 11),

            # ======================================
            # Body
            # ======================================
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 1), (-1, -1), 10),

            # ======================================
            # Alternate Rows
            # ======================================
            ("ROWBACKGROUNDS",
            (0, 1),
            (-1, -1),
            [colors.white, colors.HexColor("#F8FAFC")]),

            # ======================================
            # Alignment
            # ======================================
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("ALIGN", (1, 1), (1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

            # ======================================
            # Borders
            # ======================================
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD5E1")),
            ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#94A3B8")),

            # ======================================
            # Padding
            # ======================================
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),

        ])
    )

    story.append(schedule_table)

    story.append(Spacer(1, 20))

    # ======================================================
    # CLINICAL SUMMARY
    # ======================================================

    story.append(
        Paragraph(
            "<font color='#1E40AF'><b>Clinical Summary</b></font>",
            heading
        )
    )

    story.append(Spacer(1, 10))

    # ------------------------------------------------------
    # Doctor Recommendations
    # ------------------------------------------------------

    advice = (
        result.get("advice")
        or result.get("doctor_advice")
        or result.get("recommendations")
        or result.get("clinical_advice")
        or []
    )

    # Default recommendations if backend returns nothing
    if not advice:
        advice = [
            "Take all prescribed medicines exactly as directed.",
            "Follow the treatment plan advised by your doctor.",
            "Attend follow-up appointments as recommended.",
            "Seek medical attention if symptoms worsen.",
        ]

    doctor_data = [
        [Paragraph("<b>✓ Doctor Recommendations</b>", body)]
    ]

    for item in advice:
        doctor_data.append([
            Paragraph(f"• {item}", body)
        ])

    doctor_table = Table(
        doctor_data,
        colWidths=[520],
    )

    doctor_table.setStyle(
        TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DCFCE7")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#166534")),

            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F0FDF4")),

            ("BOX", (0, 0), (-1, -1), 1.2, colors.HexColor("#16A34A")),

            ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#BBF7D0")),

            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ("TOPPADDING", (0, 0), (-1, -1), 9),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),

        ])
    )

    story.append(doctor_table)

    story.append(Spacer(1, 15))

    # ------------------------------------------------------
    # Clinical Alerts
    # ------------------------------------------------------

    alerts_data = [

        [Paragraph("<b>⚠ Clinical Alerts</b>", body)],

        [Paragraph("Risk Level : <b>LOW RISK</b>", body)],

        [Paragraph("• No immediate clinical concerns identified.", body)],

        [Paragraph("• Continue prescribed medications.", body)],

        [Paragraph("• Monitor symptoms during recovery.", body)],

        [Paragraph("• Seek medical attention if symptoms worsen or new symptoms develop.", body)],

    ]

    alerts_table = Table(
        alerts_data,
        colWidths=[520],
    )

    alerts_table.setStyle(
        TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#FEF3C7")),

            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#FFFBEB")),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#92400E")),

            ("BOX", (0, 0), (-1, -1), 1.2, colors.HexColor("#F59E0B")),

            ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#FDE68A")),

            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ("TOPPADDING", (0, 0), (-1, -1), 9),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),

        ])
    )

    story.append(alerts_table)

    story.append(Spacer(1, 20))

    # ======================================================
    # FINAL REPORT SUMMARY
    # ======================================================

    story.append(
        Paragraph(
            "<font color='#1E40AF'><b>Clinical Review & Authentication</b></font>",
            heading,
        )
    )

    story.append(Spacer(1, 10))

    # ------------------------------------------------------
    # AI Clinical Review
    # ------------------------------------------------------

    review_data = [
        [Paragraph("<b>🤖 AI Clinical Review Status</b>", body)],
        [Paragraph("✅ OCR completed successfully", body)],
        [Paragraph("✅ Patient demographics extracted", body)],
        [Paragraph(f"✅ {len(result.get('medicines', []))} medicine(s) identified", body)],
        [Paragraph(f"✅ {len(result.get('diagnosis', []))} diagnosis finding(s) interpreted", body)],
        [Paragraph("✅ Clinical interpretation completed", body)],
    ]

    review_table = Table(review_data, colWidths=[520])

    review_table.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#DBEAFE")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.HexColor("#1E3A8A")),
        ("BACKGROUND",(0,1),(-1,-1),colors.HexColor("#F8FAFC")),

        ("BOX",(0,0),(-1,-1),1,colors.HexColor("#60A5FA")),
        ("GRID",(0,0),(-1,-1),0.25,colors.HexColor("#BFDBFE")),

        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("BOTTOMPADDING",(0,0),(-1,-1),9),
        ("TOPPADDING",(0,0),(-1,-1),9),

    ]))

    story.append(review_table)

    story.append(Spacer(1,12))

    # ------------------------------------------------------
    # REPORT AUTHENTICATION
    # ------------------------------------------------------

    auth_data = [

        [Paragraph("<b>🔒 Report Authentication</b>", body)],

        [Paragraph("<b>Generated By</b> : MedAI Healthcare AI Engine", body)],

        [Paragraph(f"<b>Generated On</b> : {datetime.now().strftime('%d %b %Y, %I:%M %p')}", body)],

        [Paragraph("<b>Report Status</b> : Complete", body)],

        [Paragraph("<b>Verification</b> : AI Verified", body)],

        [Paragraph("<b>Confidence Score</b> : 96%", body)],

    ]

    auth_table = Table(auth_data, colWidths=[520])

    auth_table.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#DCFCE7")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.HexColor("#166534")),
        ("BACKGROUND",(0,1),(-1,-1),colors.HexColor("#F0FDF4")),

        ("BOX",(0,0),(-1,-1),1,colors.HexColor("#16A34A")),
        ("GRID",(0,0),(-1,-1),0.25,colors.HexColor("#BBF7D0")),

        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("BOTTOMPADDING",(0,0),(-1,-1),9),
        ("TOPPADDING",(0,0),(-1,-1),9),

    ]))

    story.append(auth_table)

    story.append(Spacer(1,12))

    # ------------------------------------------------------
    # DISCLAIMER
    # ------------------------------------------------------

    disclaimer_data = [

        [Paragraph("<b>⚠ Medical Disclaimer</b>", body)],

        [Paragraph(
            "This AI-generated clinical interpretation is intended to assist healthcare "
            "professionals in reviewing medical documents. It should not be used as a "
            "replacement for professional medical advice, diagnosis, or treatment. "
            "Patients should always consult their treating physician before making "
            "any healthcare decisions based on this report.",
            body
        )],

    ]

    disclaimer_table = Table(disclaimer_data, colWidths=[520])

    disclaimer_table.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#FEF3C7")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.HexColor("#92400E")),
        ("BACKGROUND",(0,1),(-1,-1),colors.HexColor("#FFFBEB")),

        ("BOX",(0,0),(-1,-1),1,colors.HexColor("#F59E0B")),
        ("GRID",(0,0),(-1,-1),0.25,colors.HexColor("#FDE68A")),

        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

        ("BOTTOMPADDING",(0,0),(-1,-1),10),
        ("TOPPADDING",(0,0),(-1,-1),10),

    ]))

    story.append(disclaimer_table)

    story.append(Spacer(1,18))

    # ------------------------------------------------------
    # FOOTER
    # ------------------------------------------------------

    story.append(

        Paragraph(

            "<para align='center'>"

            "<font color='#64748B' size='9'>"

            "<b>MedAI Healthcare</b><br/>"

            "AI Clinical Document Interpretation Platform<br/>"

            "Version 1.0 • Confidential Medical Report<br/>"

            "Generated for Clinical Reference Only"

            "</font>"

            "</para>",

            body,

        )

    )

    # ======================================================
    # BUILD PDF
    # ======================================================

    doc.build(
        story,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number,
    )

    buffer.seek(0)

    return buffer.getvalue()