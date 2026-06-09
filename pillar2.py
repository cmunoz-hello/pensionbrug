import pdfplumber
import re

def extract_upo_data(pdf_file):
    """
    Extract key pension data from a UPO PDF.
    Works with standardised Dutch UPO format (mandated by Pensioenfederatie).
    """
    
    text = ""
    
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    
    result = {
        "fund_name": None,
        "accrued_pension_annual": None,
        "projected_pension_annual": None,
        "retirement_age": None,
        "raw_text": text
    }
    
    # ── Fund name ──
    fund_match = re.search(r'Pensioenuitvoerder:\s*(.+)', text)
    if fund_match:
        result["fund_name"] = fund_match.group(1).strip()
    
    # ── Accrued pension ──
    # Looks for: "zolang u leeft: € 2.847 bruto per jaar"
    # First occurrence = accrued
    accrued_matches = re.findall(r'zolang u leeft:\s*€\s*([\d.,]+)\s*bruto per jaar', text)
    if accrued_matches:
        amount_str = accrued_matches[0].replace('.', '').replace(',', '.')
        try:
            result["accrued_pension_annual"] = round(float(amount_str))
        except:
            pass
    
    # ── Projected pension ──
    # Second occurrence of same pattern = projected
    if len(accrued_matches) >= 2:
        amount_str = accrued_matches[1].replace('.', '').replace(',', '.')
        try:
            result["projected_pension_annual"] = round(float(amount_str))
        except:
            pass
    else:
        # Fallback: look for "verwachten" section specifically
        projected_match = re.search(
            r'blijft opbouwen\?.*?€\s*([\d.,]+)\s*bruto per jaar',
            text,
            re.DOTALL
        )
        if projected_match:
            amount_str = projected_match.group(1).replace('.', '').replace(',', '.')
            try:
                result["projected_pension_annual"] = round(float(amount_str))
            except:
                pass
    
    # ── Retirement age ──
    age_match = re.search(r'Pensioenleeftijd:\s*(\d{2})\s*jaar\s*en\s*(\d{1,2})\s*maanden', text)
    if age_match:
        years = int(age_match.group(1))
        months = int(age_match.group(2))
        result["retirement_age"] = years + months/12
    
    return result


def manual_pillar2_input():
    return {
        "fund_name": None,
        "accrued_pension_annual": None,
        "projected_pension_annual": None,
        "retirement_age": None,
        "raw_text": None
    }
