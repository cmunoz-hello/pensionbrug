from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER

def create_sample_upo():
    doc = SimpleDocTemplate(
        "sample_upo.pdf",
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Normal'],
        fontSize=16,
        fontName='Helvetica-Bold',
        spaceAfter=6
    )
    heading_style = ParagraphStyle(
        'Heading',
        parent=styles['Normal'],
        fontSize=12,
        fontName='Helvetica-Bold',
        spaceAfter=4,
        spaceBefore=12
    )
    normal_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=4
    )
    small_style = ParagraphStyle(
        'Small',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.grey
    )
    
    story = []
    
    # ── Header ──
    story.append(Paragraph("Uniform Pensioenoverzicht 2025", title_style))
    story.append(Paragraph("Stand op: 31 december 2024", normal_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
    story.append(Spacer(1, 0.3*cm))
    
    # ── Personal data ──
    story.append(Paragraph("Uw persoonlijke gegevens", heading_style))
    
    personal_data = [
        ["Naam:", "C.M. Munoz"],
        ["Geboren op:", "15
