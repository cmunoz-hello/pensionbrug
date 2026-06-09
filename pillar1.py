def calculate_aow(birth_year, years_in_nl, years_abroad):
    """
    Calculate AOW entitlement.
    - 2% per year of Dutch insurance coverage
    - Reduced by 2% for each year spent abroad without voluntary insurance
    - Full benefit requires 50 years of coverage
    """
    
    # Years insured in NL
    years_insured = years_in_nl - years_abroad
    
    # AOW percentage (max 100%)
    aow_percentage = min(years_insured * 2, 100)
    
    # Full AOW amounts (2025 figures, gross per year)
    FULL_AOW_SINGLE = 19674      # single person
    FULL_AOW_COUPLE = 13435      # per person in couple
    
    # Calculate entitlement
    aow_single = round(FULL_AOW_SINGLE * aow_percentage / 100)
    aow_couple = round(FULL_AOW_COUPLE * aow_percentage / 100)
    
    # Retirement age (currently 67 years and 3 months)
    retirement_age = 67.25
    
    return {
        "years_insured": years_insured,
        "aow_percentage": aow_percentage,
        "aow_annual_single": aow_single,
        "aow_annual_couple": aow_couple,
        "aow_monthly_single": round(aow_single / 12),
        "aow_monthly_couple": round(aow_couple / 12),
        "retirement_age": retirement_age
    }
