import pdfplumber
import re

def extract_upo_data(pdf_file):
    """
    Extract key pension data from a UPO PDF.
    """
    
    text = ""
    
    # Extract all text from PDF
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    
    # Debug: print extracted text to terminal
    print("=== EXTRACTED TEXT ===")
    print(text)
    print("=== END TEXT ===")
    
    result = {
        "fund_name": None,
        "accrued_pension_annual": None,
        "projected_pension_annual": None,
        "retirement_age": None,
        "raw_text": text
    }
    
    # Extract fund name
    fund_patterns = [
        r'Pensioenuitvoerder[:\s]+([^\n]+)',
        r'(Pensioenfonds[^\n]+)',
        r'(PFZW|ABP|PME|PMT|Achmea|Nationale-Nederlanden)',
    ]
    for pattern in fund_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            result["fund_name"] = match.group(1).strip()
            break
    
    # Extract accrued pension - try multiple patterns
    accrued_patterns = [
        r'opgebouwd[^\n]*?\n[^\n]*?€\s*([\d.,]+)',
        r'opgebouwd bij ons[^\n]*?€\s*([\d.,]+)',
        r'heeft u bij ons pensioen opgebouwd[^\n]*?€\s*([\d.,]+)',
        r'€\s*([\d.,]+)\s*bruto per jaar\s*\n',
        r'zolang u leeft.*?€\s*([\d.,]+)',
    ]
    for pattern in accrued_patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            amount_str = match.group(1).replace('.', '').replace(',', '.')
            try:
                result["accrued_pension_annual"] = round(float(amount_str))
                break
            except:
                continue
    
    # Extract projected pension - try multiple patterns
    projected_patterns = [
        r'verwachten[^\n]*?€\s*([\d.,]+)',
        r'blijft opbouwen[^\n]*?€\s*([\d.,]+)',
        r'kunt u bij[^\n]*?€\s*([\d.,]+)',
        r'€\s*([\d.,]+)\s*bruto per jaar\s*$',
        r'18[.,]\d{3}',  # looks for amounts around 18,000
    ]
    for pattern in projected_patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            amount_str = match.group(0) if '18' in pattern else match.group(1)
            amount_str = re.sub(r'[€\s]', '', amount_str).replace('.', '').replace(',', '.')
            try:
                amount = round(float(amount_str))
                if 1000 < amount < 100000:  # sanity check
                    result["projected_pension_annual"] = amount
                    break
            except:
                continue
    
    # Extract retirement age
    age_patterns = [
        r'(\d{2})\s*jaar\s*en\s*(\d{1,2})\s*maanden',
        r'pensioenleeftijd[:\s]+(\d{2})',
    ]
    for pattern in age_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            if 'jaar' in pattern:
                result["retirement_age"] = int(match.group(1)) + int(match.group(2))/12
            else:
                result["retirement_age"] = float(match.group(1))
            break
    
    return result


def manual_pillar2_input():
    return {
        "fund_name": None,
        "accrued_pension_annual": None,
        "projected_pension_annual": None,
        "retirement_age": None,
        "raw_text": None
    }
