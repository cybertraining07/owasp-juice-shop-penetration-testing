
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Image,
    KeepTogether
)

BASE = Path("/root/WebApp-Penetration-Testing")

SOURCE = BASE / "reports/OWASP-Juice-Shop-Penetration-Test-Report.txt"
SCREENSHOT = BASE / "evidence/screenshots/FINDING-002-Cross-Account-Basket-Evidence.png"
OUTPUT = BASE / "reports/OWASP-Juice-Shop-Penetration-Test-Report.pdf"

if not SOURCE.exists():
    raise SystemExit(f"Report not found: {SOURCE}")

if not SCREENSHOT.exists():
    raise SystemExit(f"Evidence screenshot not found: {SCREENSHOT}")

styles = getSampleStyleSheet()

cover_title = ParagraphStyle(
    "CoverTitle",
    parent=styles["Title"],
    fontSize=23,
    leading=30,
    alignment=TA_CENTER,
    textColor=colors.HexColor("#17365D"),
    spaceAfter=20
)

cover_subtitle = ParagraphStyle(
    "CoverSubtitle",
    parent=styles["Normal"],
    fontSize=13,
    leading=19,
    alignment=TA_CENTER,
    textColor=colors.HexColor("#444444")
)

heading = ParagraphStyle(
    "SectionHeading",
    parent=styles["Heading2"],
    fontSize=12,
    leading=16,
    textColor=colors.HexColor("#17365D"),
    spaceBefore=12,
    spaceAfter=6,
    keepWithNext=True
)

body = ParagraphStyle(
    "ReportBody",
    parent=styles["BodyText"],
    fontSize=9,
    leading=13,
    spaceAfter=5,
    splitLongWords=True
)

small = ParagraphStyle(
    "SmallText",
    parent=body,
    fontSize=8,
    leading=11
)

story = []

# -------------------------------------------------
# COVER PAGE
# -------------------------------------------------

story.append(Spacer(1, 45 * mm))
story.append(Paragraph(
    "WEB APPLICATION<br/>PENETRATION TEST REPORT",
    cover_title
))
story.append(Spacer(1, 10 * mm))
story.append(Paragraph(
    "OWASP Juice Shop Security Assessment",
    cover_subtitle
))
story.append(Spacer(1, 25 * mm))

cover_details = [
    "<b>Target:</b> http://127.0.0.1:3000",
    "<b>Assessment environment:</b> Authorized local lab",
    "<b>Application:</b> OWASP Juice Shop",
    "<b>Report status:</b> Draft - Remediation retesting pending",
    "<b>Assessment type:</b> Web application penetration testing"
]

for detail in cover_details:
    story.append(Paragraph(detail, body))
    story.append(Spacer(1, 5))

story.append(Spacer(1, 25 * mm))
story.append(Paragraph(
    "CONFIDENTIAL - Prepared for educational and portfolio purposes",
    small
))
story.append(PageBreak())

# -------------------------------------------------
# MAIN REPORT CONTENT
# -------------------------------------------------

lines = SOURCE.read_text(encoding="utf-8").splitlines()

first_nonempty = True

for line in lines:
    value = line.strip()

    if not value:
        story.append(Spacer(1, 4))
        continue

    # Skip the original first title because the new cover replaces it.
    if first_nonempty:
        first_nonempty = False
        continue

    safe_text = escape(value)

    # Detect uppercase section headings.
    if (
        len(value) < 100
        and value.upper() == value
        and any(character.isalpha() for character in value)
    ):
        story.append(Paragraph(safe_text, heading))
    else:
        story.append(Paragraph(safe_text, body))

# -------------------------------------------------
# TECHNICAL EVIDENCE APPENDIX
# -------------------------------------------------

story.append(PageBreak())
story.append(Paragraph(
    "APPENDIX A - TECHNICAL EVIDENCE",
    heading
))
story.append(Spacer(1, 8))

story.append(Paragraph(
    "<b>Finding-002: Cross-Account Basket Access (IDOR/BOLA)</b>",
    body
))
story.append(Paragraph(
    "The following screenshot documents the authenticated "
    "cross-account basket access test performed in the local "
    "OWASP Juice Shop environment. The authorization token "
    "has been redacted.",
    body
))
story.append(Spacer(1, 10))

evidence_image = Image(str(SCREENSHOT))
evidence_image._restrictSize(170 * mm, 235 * mm)

story.append(KeepTogether([
    evidence_image,
    Spacer(1, 8),
    Paragraph(
        "Evidence file: FINDING-002-Cross-Account-Basket-Evidence.png",
        small
    )
]))

# -------------------------------------------------
# PAGE NUMBER
# -------------------------------------------------

def add_page_number(canvas, document):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)

    canvas.drawString(
        20 * mm,
        12 * mm,
        "OWASP Juice Shop - Penetration Test"
    )

    canvas.drawRightString(
        A4[0] - 20 * mm,
        12 * mm,
        f"Page {document.page}"
    )

    canvas.restoreState()

# -------------------------------------------------
# BUILD PDF
# -------------------------------------------------

document = SimpleDocTemplate(
    str(OUTPUT),
    pagesize=A4,
    rightMargin=20 * mm,
    leftMargin=20 * mm,
    topMargin=20 * mm,
    bottomMargin=22 * mm,
    title="OWASP Juice Shop Penetration Test Report",
    author="Security Assessment"
)

document.build(
    story,
    onFirstPage=add_page_number,
    onLaterPages=add_page_number
)

print("\nPDF generated successfully.")
print(f"Report: {OUTPUT}")
print(f"Source report lines: {len(lines)}")
print(f"Screenshot included: {SCREENSHOT.name}")
print(f"PDF size: {OUTPUT.stat().st_size:,} bytes")
