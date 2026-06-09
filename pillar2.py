import pdfplumber
import re

def extract_upo_data(pdf_file):
    """
    Extract key pension data from a UPO PDF.
    Looks for standardised field labels that appear in all Dutch UPOs.
    """
    
    text = ""
    
    # Extract all text from PDF
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    
    # Initialize results
    result = {
        "fund_name": None,
        "accrued_pension_annual": None,
        "projected_pension_annual": None,
        "retirement_age": None,
        "raw_text": text
    }
    
    # Extract fund name - looks for "Pensioenuitvoerder:" label
    fund_match = re.search(r'Pensioenuitvoerder[:\s]+([^\n]+)', text)
    if fund_match:
        result["fund_name"] = fund_match.group(1).strip()
    
    # Extract accrued pension - looks for euro amounts after key phrases
    accrued_match = re.search(r'opgebouwd[^\n]*?€\s*([\d.,]+)', text, re.IGNORECASE)
    if accrued_match:
        amount = accrued_match.group(1).replace('.', '').replace(',', '.')
        result["accrued_pension_annual"] = round(float(amount))
    
    # Extract projected pension
    projected_match = re.search(r'verwachten[^\n]*?€\s*([\d.,]+)', text, re.IGNORECASE)
    if projected_match:
        amount = projected_match.group(1).replace('.', '').replace(',', '.')
        result["projected_pension_annual"] = round(float(amount))
    
    # Extract retirement age
    age_match = re.search(r'(\d{2})\s*jaar\s*en\s*(\d{1,2})\s*maanden', text)
    if age_match:
        years = int(age_match.group(1))
        months = int(age_match.group(2))
        result["retirement_age"] = years + months/12
    
    return result


def manual_pillar2_input():
    """
    Fallback if PDF parsing doesn't work -
    returns empty dict for manual input
    """
    return {
        "fund_name": None,
        "accrued_pension_annual": None,
        "projected_pension_annual": None,
        "retirement_age": None,
        "raw_text": None
    }
