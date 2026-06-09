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
        ["Geboren op:", "15 maart 2000"],
        ["Werkgever:", "Example BV"],
        ["Klantnummer:", "123456789"],
        ["Pensioenuitvoerder:", "Pensioenfonds Zorg en Welzijn (PFZW)"],
        ["Soort pensioenregeling:", "Premieovereenkomst, Flexibele premieregeling (WTP)"],
        ["Datum start pensioenopbouw:", "1 september 2022"],
        ["Pensioenleeftijd:", "67 jaar en 3 maanden"],
    ]
    
    personal_table = Table(personal_data, colWidths=[6*cm, 11*cm])
    personal_table.setStyle(TableStyle([
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(personal_table)
    story.append(Spacer(1, 0.3*cm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey))
    
    # ── Pension data ──
    story.append(Paragraph("Uw pensioengegevens", heading_style))
    
    pension_data = [
        ["Fulltime pensioengevend salaris:", "€ 32.000"],
        ["Percentage dat u werkt:", "100%"],
        ["Premiepercentage 2024:", "14,5%"],
        ["Inkomen waarover u pensioen opbouwt:", "€ 16.184"],
    ]
    
    pension_table = Table(pension_data, colWidths=[6*cm, 11*cm])
    pension_table.setStyle(TableStyle([
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(pension_table)
    story.append(Spacer(1, 0.3*cm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey))
    
    # ── Accrued pension ──
    story.append(Paragraph("Hoeveel pensioen heeft u opgebouwd?", heading_style))
    story.append(Paragraph(
        "Tot 31 december 2024 heeft u bij ons pensioen opgebouwd:",
        normal_style
    ))
    
    accrued_data = [
        ["Vanaf 67 jaar en 3 maanden, zolang u leeft:", "€ 2.847 bruto per jaar"],
    ]
    accrued_table = Table(accrued_data, colWidths=[10*cm, 7*cm])
    accrued_table.setStyle(TableStyle([
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('FONTNAME', (1,0), (1,-1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FDF5EE')),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.HexColor('#FDF5EE')]),
    ]))
    story.append(accrued_table)
    story.append(Spacer(1, 0.3*cm))
    
    # ── Projected pension ──
    story.append(Paragraph("Hoeveel pensioen krijgt u naar verwachting als u blijft opbouwen?", heading_style))
    story.append(Paragraph(
        "Als u tot uw AOW-leeftijd blijft werken, dan kunt u bij PFZW aan pensioen verwachten:",
        normal_style
    ))
    
    projected_data = [
        ["Vanaf 67 jaar en 3 maanden, zolang u leeft:", "€ 18.450 bruto per jaar"],
    ]
    projected_table = Table(projected_data, colWidths=[10*cm, 7*cm])
    projected_table.setStyle(TableStyle([
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('FONTNAME', (1,0), (1,-1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FDF5EE')),
    ]))
    story.append(projected_table)
    story.append(Spacer(1, 0.3*cm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey))
    
    # ── Scenarios ──
    story.append(Paragraph("Wat als het mee- of tegenzit?", heading_style))
    story.append(Paragraph(
        "Hieronder ziet u uw verwachte pensioen in drie scenario's:",
        normal_style
    ))
    
    scenarios_data = [
        ["Scenario", "Verwacht pensioen per jaar"],
        ["Als het tegenzit (pessimistisch):", "€ 14.200"],
        ["Verwacht (mediaan):", "€ 18.450"],
        ["Als het meezit (optimistisch):", "€ 24.800"],
    ]
    scenarios_table = Table(scenarios_data, colWidths=[10*cm, 7*cm])
    scenarios_table.setStyle(TableStyle([
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#3D4A5C')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [
            colors.HexColor('#FDECEA'),
            colors.HexColor('#FDF5EE'),
            colors.HexColor('#EDFAF3')
        ]),
    ]))
    story.append(scenarios_table)
    story.append(Spacer(1, 0.3*cm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey))

    # ── Partner pension ──
    story.append(Paragraph("Wat krijgt uw partner als u overlijdt?", heading_style))
    story.append(Paragraph(
        "Als u overlijdt voor uw AOW-leeftijd, ontvangt uw partner:",
        normal_style
    ))
    story.append(Paragraph("• € 11.070 bruto per jaar (nabestaandenpensioen)", normal_style))
    story.append(Spacer(1, 0.3*cm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey))
    
    # ── Factor A ──
    story.append(Paragraph("Pensioenaangroei (factor A) in 2024", heading_style))
    story.append(Paragraph("€ 312", normal_style))
    story.append(Spacer(1, 0.3*cm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey))

    # ── Footer ──
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(
        "Voor een totaaloverzicht van uw pensioen en AOW, kijk op www.mijnpensioenoverzicht.nl",
        small_style
    ))
    story.append(Paragraph(
        "Vragen? Kijk op www.pfzw.nl of bel (030) 277 55 77",
        small_style
    ))
    
    doc.build(story)
    print("✅ sample_upo.pdf created successfully!")

if __name__ == "__main__":
    create_sample_upo()
